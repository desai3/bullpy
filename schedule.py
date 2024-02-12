from typing import List
from datetime import datetime

from dateutil.relativedelta import relativedelta

from schedule_period import SchedulePeriod
from roll_convention import RollConvention, RollConventionType


class Schedule(object):
    def __init__(self, periods: List[SchedulePeriod], freq: relativedelta, roll_conv: RollConvention):
        self.periods = periods
        self.freq = freq
        self.roll_conv = roll_conv

    def size(self) -> int:
        return len(self.perids)

    def is_term(self) -> bool:
        return self.size() == 1 and self.freq is None

    def is_single_period(self) -> bool:
        return self.size() == 1

    def get_period(self, i: int) -> SchedulePeriod:
        return self.periods[i]

    def get_first_period(self) -> SchedulePeriod:
        return self.periods[0]

    def get_last_period(self) -> SchedulePeriod:
        return self.periods[-1]

    def get_start_dt(self) -> datetime:
        return self.get_first_period().get_start_dt()

    def get_end_dt(self) -> datetime:
        return self.get_last_period().get_end_dt()

    def get_unadjusted_start_dt(self) -> datetime:
        return self.get_first_period().get_unadjusted_start_dt()

    def get_unadjusted_end_dt(self) -> datetime:
        return self.get_last_period().get_unadjusted_end_dt()

    def get_initial_stub(self) -> SchedulePeriod | None:
        if self.is_initial_stub():
            return self.get_first_period()
        else:
            return None

    def is_initial_stub(self) -> bool:
        return not self.is_term() and not self.get_first_period().is_regular(self.freq, self.roll_conv)

    def get_final_stub(self) -> SchedulePeriod | None:
        if self.is_final_stub():
            return self.get_last_period()
        else:
            return None

    def is_final_stub(self) -> bool:
        return not self.is_single_period() and not self.get_last_period().is_regular(self.freq, self.roll_conv)

    def get_regular_periods(self) -> List[SchedulePeriod]:
        if self.is_term():
            return self.periods

        start_stub = 1 if self.is_initial_stub() else 0
        end_stub = 1 if self.is_final_stub() else 0
        if start_stub == 0 and end_stub == 0:
            return self.periods
        else:
            return self.periods[start_stub: len(self.periods) - end_stub]

    def get_unadjusted_dates(self) -> List[datetime]:
        dates = [self.get_unadjusted_start_dt()]
        for p in self.periods:
            dates.append(p.get_unadjusted_end_date())
        return dates

    def is_end_of_month_convention(self) -> bool:
        return self.roll_conv == RollConventionType.EOM

    def of_term(self, period: SchedulePeriod):
        return Schedule([period], None, None)

    def merge_to_term(self):
        if self.is_term():
            return self
        first = self.get_first_period()
        last = self.get_last_period()

        sp = SchedulePeriod(first.get_start_dt(), last.get_end_dt(), first.get_unadjusted_start_dt(),
                            last.get_unadjusted_end_dt())
        return Schedule.of_term(sp)
