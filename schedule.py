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

    def merge(self, group_size: int, first_reg_start_dt: datetime, last_reg_end_dt: datetime):
        if self.is_single_period() or group_size == 1:
            return self
        start_reg_i = -1
        end_reg_i = -1

        for i in range(self.size()):
            period = self.periods[i]
            if period.get_unadjusted_start_dt() == first_reg_start_dt or period.get_start_dt() == last_reg_end_dt:
                start_reg_i = i
            if period.get_unadjusted_end_dt() == last_reg_end_dt or period.get_end_dt() == last_reg_end_dt:
                end_reg_i = i + 1

        if start_reg_i < 0:
            raise ValueError(f"Unable to merge schedule, first_reg_start_dt {first_reg_start_dt} " +
                             f"does not match any date in the underlying schedule {self.get_unadjusted_dates()}")
        if end_reg_i < 0:
            raise ValueError(f"Unable to merge schedule, last_reg_end_dt {last_reg_end_dt} " +
                             f"does not match any date in the underlying schedule {self.get_unadjusted_dates()}")

        num_reg = end_reg_i - start_reg_i
        if num_reg % group_size != 0:
            raise ValueError(f"Unable to merge schedule, first_reg_start_dt {first_reg_start_dt} " +
                             f"and last_reg_end_dt {last_reg_end_dt} cannot be used to create regular " +
                             "periods of frequency")

        new_sched = []
        if start_reg_i > 0:
            new_sched += self.create_schedule_period(self.periods[0: start_reg_i])
        for i in range(start_reg_i, end_reg_i, group_size):
            new_sched += self.create_schedule_period(self.period[i: i + group_size])
        if end_reg_i < len(self.periods):
            new_sched += self.create_schedule_period(self.periods[end_reg_i, len(self.periods)])

        return Schedule(new_sched, self.freq * group_size if self.freq is not None else self.freq, self.roll_conv)

    def merge_regular(self, group_size: int, roll_forward: bool):
        if self.is_single_period() or group_size == 1:
            return self

        new_sched = []

        init_stub = self.get_initial_stub()
        if init_stub is not None:
            new_sched.append(init_stub)

        reg_periods = self.get_regular_periods()
        reg_size = len(reg_periods)
        remainder = reg_size % group_size
        start_i = (0 if roll_forward or remainder == 0 else -(group_size - remainder))
        for i in range(start_i, reg_size, group_size):
            frm = max(i, 0)
            to = min(i + group_size, reg_size)
            new_sched.append(self.create_schedule_period(reg_periods[frm: to]))

        final_stub = self.get_final_stub()
        if final_stub is not None:
            new_sched.append(final_stub)
        return Schedule(new_sched, self.freq * group_size if self.freq is not None else self.freq, self.roll_conv)

    @staticmethod
    def create_schedule_period(accruals: List[SchedulePeriod]) -> SchedulePeriod:
        first = accruals[0]
        if len(accruals) == 1:
            return first
        last = accruals[-1]
        return SchedulePeriod(first.get_start_dt(), last.get_end_dt(),
                              first.get_unadjusted_start_dt(), last.get_unadjusted_end_dt())


