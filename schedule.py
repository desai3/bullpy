from typing import List
from datetime import datetime

from dateutil.relativedelta import relativedelta

from schedule_period import SchedulePeriod
from roll_convention import RollConvention


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

    
