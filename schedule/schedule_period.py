from typing import Callable

from .daycount import DayCount
from .roll_convention import RollConvention
from .stub_convention import StubConventionType
from .bdayadj import BDayAdj
from .periodic_schedule import PeriodicSchedule
from .frequency import Frequency, between

from datetime import datetime


class SchedulePeriod(object):
    def __init__(self,
                 start_dt: datetime,
                 end_dt: datetime,
                 unadjusted_start_dt: datetime | None = None,
                 unadjusted_end_dt: datetime | None = None):
        self.start_dt = start_dt
        self.end_dt = end_dt

        if not isinstance(unadjusted_start_dt, type(unadjusted_end_dt)):
            raise ValueError("unadjusted_start_dt and unadjusted_end_dt should have the same type")
        self.unadjusted_start_dt = unadjusted_start_dt if unadjusted_start_dt is not None else start_dt
        self.unadjusted_end_dt = unadjusted_end_dt if unadjusted_end_dt is not None else end_dt

        if not isinstance(self.start_dt, datetime):
            raise ValueError('start_dt should be of type datetime')
        if not isinstance(self.end_dt, datetime):
            raise ValueError('end_dt should be of type datetime')
        if self.start_dt >= self.end_dt:
            raise ValueError('start_dt should be before end_dt')

        if not isinstance(self.unadjusted_start_dt, datetime):
            raise ValueError('Unadjusted start date should be of type datetime')
        if not isinstance(self.unadjusted_end_dt, datetime):
            raise ValueError('Unadjusted end date should be of type datetime')
        if self.unadjusted_start_dt >= self.unadjusted_end_dt:
            raise ValueError('unadjusted_start_dt should be before unadjusted_end_dt')

    def pre_build(self) -> None:
        if self.unadjusted_start_dt is None:
            self.unadjusted_start_dt = self.start_dt
        if self.unadjusted_end_dt is None:
            self.unadjusted_end_dt = self.end_dt

    def length(self) -> Frequency:
        return between(self.start_dt, self.end_dt)

    def length_in_days(self) -> int:
        return self.end_dt.toordinal() - self.start_dt.toordinal()

    # TODO: figure out how to input datatype of Schedule without breaking circular import
    # TODO: fix year_frac to take sched
    def year_fraction(self, dc: DayCount, sched):
        # return dc.year_fraction(self.start_dt, self.end_dt, sched)
        return dc.year_fraction(self.start_dt, self.end_dt)

    def is_regular(self, freq: Frequency, roll_conv: RollConvention) -> bool:
        if not isinstance(freq, Frequency):
            raise ValueError('freq should be of type Frequency')
        if not isinstance(roll_conv, RollConvention):
            raise ValueError('roll_conv should be of type RollConvention')

        return roll_conv.next(self.unadjusted_start_dt, freq) == self.unadjusted_end_dt and \
            roll_conv.previous(self.unadjusted_end_dt, freq) == self.unadjusted_start_dt

    def contains(self, dt: datetime) -> bool:
        if not isinstance(dt, datetime):
            raise ValueError('dt should be of type datetime')
        return not dt < self.start_dt and dt < self.end_dt

    def sub_schedule(self,
                     freq: Frequency,
                     roll_conv: RollConvention,
                     stub_conv: StubConventionType,
                     bday_adj: BDayAdj,
                     ) -> PeriodicSchedule:

        return PeriodicSchedule(self.unadjusted_start_dt, self.unadjusted_end_dt, freq, bday_adj, roll_conv, stub_conv)

    def get_start_date(self):
        return self.start_dt

    def get_end_date(self):
        return self.end_dt

    def get_unadjusted_start_date(self):
        return self.unadjusted_start_dt

    def get_unadjusted_end_date(self):
        return self.unadjusted_end_dt

    def __eq__(self, o):
        return isinstance(o, type(self)) and \
            o.start_dt == self.start_dt and \
            o.end_dt == self.end_dt and \
            o.unadjusted_start_dt == self.unadjusted_start_dt and \
            o.unadjusted_end_dt == self.unadjusted_end_dt

    def to_adjusted(self, adjuster: Callable[[datetime], datetime], merge_type: int):
        res_start = adjuster(self.start_dt)
        res_end = adjuster(self.end_dt)

        if merge_type == -1 and res_start == res_end:
            res_start = self.start_dt
        elif merge_type == 1 and res_start == res_end:
            res_end = self.end_dt

        if res_start == self.start_dt and res_end == self.end_dt:
            return self
        return SchedulePeriod(res_start, res_end, self.unadjusted_start_dt, self.unadjusted_end_dt)



