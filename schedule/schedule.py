from typing import List, Tuple, Callable
from datetime import datetime

from IPython.core.debugger import set_trace

from .schedule_period import SchedulePeriod
from .roll_convention import RollConvention, RollConventionType
from .frequency import Frequency


class Schedule(object):
    def __init__(self, periods: List[SchedulePeriod],
                 freq: Frequency | None = None,
                 roll_conv: RollConvention | None = None):
        self.periods = periods
        self.freq = freq if freq is not None else Frequency()
        self.roll_conv = roll_conv if roll_conv is not None else RollConvention(RollConventionType.NONE)

    def size(self) -> int:
        return len(self.periods)

    def is_term(self) -> bool:
        return self.size() == 1 and self.freq.is_term()

    def is_single_period(self) -> bool:
        return self.size() == 1

    def get_period(self, i: int) -> SchedulePeriod:
        return self.periods[i]

    def get_first_period(self) -> SchedulePeriod:
        return self.periods[0]

    def get_last_period(self) -> SchedulePeriod:
        return self.periods[-1]

    def get_start_date(self) -> datetime:
        return self.get_first_period().get_start_date()

    def get_end_date(self) -> datetime:
        return self.get_last_period().get_end_date()

    def get_unadjusted_start_date(self) -> datetime:
        return self.get_first_period().get_unadjusted_start_date()

    def get_unadjusted_end_date(self) -> datetime:
        return self.get_last_period().get_unadjusted_end_date()

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
        dates = [self.get_unadjusted_start_date()]
        for p in self.periods:
            dates.append(p.get_unadjusted_end_date())
        return dates

    def is_end_of_month_convention(self) -> bool:
        return self.roll_conv == RollConvention(RollConventionType.EOM)

    @staticmethod
    def of_term(period: SchedulePeriod):
        return Schedule([period])

    def merge_to_term(self):
        if self.is_term():
            return self
        first = self.get_first_period()
        last = self.get_last_period()

        sp = SchedulePeriod(first.get_start_date(), last.get_end_date(), first.get_unadjusted_start_date(),
                            last.get_unadjusted_end_date())
        return self.of_term(sp)

    def merge(self, group_size: int, first_reg_start_dt: datetime, last_reg_end_dt: datetime):
        if group_size <= 0:
            raise ValueError("group_size should be a positive integer")

        if self.is_single_period() or group_size == 1:
            return self
        start_reg_i = -1
        end_reg_i = -1

        for i in range(self.size()):
            period = self.periods[i]
            if period.get_unadjusted_start_date() == first_reg_start_dt or \
                    period.get_start_date() == first_reg_start_dt:
                start_reg_i = i
            if period.get_unadjusted_end_date() == last_reg_end_dt or period.get_end_date() == last_reg_end_dt:
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
            new_sched += [self.create_schedule_period(self.periods[0: start_reg_i])]
        for i in range(start_reg_i, end_reg_i, group_size):
            new_sched += [self.create_schedule_period(self.periods[i: i + group_size])]
        if end_reg_i < len(self.periods):
            new_sched += [self.create_schedule_period(self.periods[end_reg_i: len(self.periods)])]

        return Schedule(new_sched, self.freq.multiply(group_size) if self.freq is not None else self.freq,
                        self.roll_conv)

    def merge_regular(self, group_size: int, roll_forward: bool):
        if group_size <= 0:
            raise ValueError("group_size should be a positive integer")

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
        return Schedule(new_sched, self.freq.multiply(group_size) if self.freq is not None else self.freq,
                        self.roll_conv)

    @staticmethod
    def create_schedule_period(accruals: List[SchedulePeriod]) -> SchedulePeriod:
        first = accruals[0]
        if len(accruals) == 1:
            return first
        last = accruals[-1]
        return SchedulePeriod(first.get_start_date(), last.get_end_date(),
                              first.get_unadjusted_start_date(), last.get_unadjusted_end_date())

    def get_frequency(self) -> Frequency:
        return self.freq

    def get_roll_convention(self) -> RollConvention:
        return self.roll_conv

    def get_periods(self) -> List[SchedulePeriod]:
        return self.periods

    def get_period(self, i: int) -> SchedulePeriod:
        return self.periods[i]

    def get_stubs(self, prefer_final: bool) -> Tuple[SchedulePeriod | None]:
        init = self.get_initial_stub()
        if prefer_final and self.size() == 1 and init is not None:
            return None, init
        return init, self.get_final_stub()

    def get_period_end_date(self, dt: datetime):
        for sp in self.periods:
            if sp.contains(dt):
                return sp.get_end_date()
        raise ValueError("Date is not contained in any periods")

    def to_adjusted(self, adjuster: Callable[[datetime], datetime]):
        adjusted = False
        new_periods = []
        size = self.size()
        for i, sp in enumerate(self.periods):
            merge_type = -1 if i == 0 else (1 if i == size -1 else 0)
            adj_sp = sp.to_adjusted(adjuster, merge_type)
            new_periods.append(adj_sp)
            adjusted = adjusted or (adj_sp != sp)
        return Schedule(new_periods, self.freq, self.roll_conv) if adjusted else self

    def to_unadjusted(self):
        return Schedule([x.to_unadjusted() for x in self.periods], self.freq, self.roll_conv)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        elif self.freq != other.freq:
            return False
        elif self.roll_conv != other.roll_conv:
            return False
        elif self.periods != other.periods:
            return False
        else:
            return True
