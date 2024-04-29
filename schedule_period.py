from daycount import DayCount
from schedule import Schedule
from roll_convention import RollConvention
from stub_convention import StubConventionType
from bdayadj import BDayAdj
from periodic_schedule import PeriodicSchedule
from frequency import Frequency

from datetime import datetime


class SchedulePeriod(object):
    def __init__(self, start_dt, end_dt, unadjusted_start_dt=None, unadjusted_end_dt=None):
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.unadjusted_start_dt = unadjusted_start_dt
        self.unadjusted_end_dt = unadjusted_end_dt

    def pre_build(self) -> None:
        if self.unadjusted_start_dt is None:
            self.unadjusted_start_dt = self.start_dt
        if self.unadjusted_end_dt is None:
            self.unadjusted_end_dt = self.end_dt

    def length_in_days(self) -> int:
        return self.start_dt.toordinal() - self.end_dt.to_ordinal()

    def year_fraction(self, dc: DayCount, sched: Schedule):
        return dc.year_fraction(self.start_dt, self.end_dt, sched)

    def is_regular(self, freq: Frequency, roll_conv: RollConvention) -> bool:
        return roll_conv.next(self.unadjusted_start_dt, freq) == self.unadjusted_end_dt and \
            roll_conv.previous(self.unadjusted_end_dt == self.unadjusted_start_dt)

    def contains(self, dt: datetime) -> bool:
        return not dt < self.start_dt and dt < self.end_dt

    def sub_schedule(self,
                     freq: Frequency,
                     roll_conv: RollConvention,
                     stub_conv: StubConventionType,
                     bday_adj: BDayAdj,
                     ) -> PeriodicSchedule:
        return PeriodicSchedule(self.unadjusted_start_dt,
                                self.unadjusted_end_dt,
                                freq,
                                bday_adj,
                                roll_conv,
                                stub_conv)