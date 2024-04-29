import datetime
import calendar

from calendars import HolidayCalendar
from roll_convention import RollConvention, RollConventionType
from bdayadj import BDayAdj, BDayAdjType
from stub_convention import StubConventionType


def first_not_null(a, b):
    if a is not None:
        return a
    if b is not None:
        return b
    raise ValueError('One of the values have to be not null')


class PeriodicSchedule(object):
    # TODO: put data types in
    def __init__(self,
                 unadjusted_start_dt: datetime,
                 unadjusted_end_dt: datetime,
                 freq,
                 bday_adj: BDayAdj,
                 stub_conv,
                 eom: bool):
        self.unadjusted_start_dt = unadjusted_start_dt
        self.unadjusted_end_dt = unadjusted_end_dt
        self.freq = freq
        self.bday_adj = bday_adj
        self.stub_conv = stub_conv
        self.eom = eom
        self.roll_conv = RollConvention(RollConventionType.EOM) if self.eom else None

    def _estimate_number_periods(self,
                                 start: datetime,
                                 end: datetime,
                                 freq,
                                 ):
        term_in_years_estimate = end.year - start.year + 2
        return max(freq._events_per_year_estimate, 1) * term_in_years_estimate

    def _calculated_unadjusted_date_from_adjusted(self,
                                                  base_dt: datetime,
                                                  roll_conv: RollConvention,
                                                  bday_adj: BDayAdj,
                                                  cal: HolidayCalendar|None=None) -> datetime:
        roll_dom = roll_conv.get_day_of_month()
        if roll_dom > 0 and base_dt.day() != roll_dom:
            length_of_month = calendar.monthrange(base_dt.year(), base_dt.month())[1]
            act_dom = min(roll_dom, length_of_month)
            if base_dt.month() != act_dom:
                roll_implied_dt = datetime.datetime(base_dt.year(), base_dt.month(), act_dom)
                adj_dt = bday_adj.adjust(roll_implied_dt, cal)
                if adj_dt == base_dt:
                    return roll_implied_dt
        elif roll_dom == 0:
            roll_implied_dt = roll_conv.adjust(base_dt)
            if roll_implied_dt != base_dt:
                adj_dt = bday_adj.adjust(roll_implied_dt, cal)
                if adj_dt == base_dt:
                    return roll_implied_dt
        return base_dt

    def _calculate_unadjusted_start_dt(self, cal: HolidayCalendar | None = None) -> datetime:
        if cal is not None and self.roll_conv is not None and (
                self.start_dt_bday_adj == BDayAdj(BDayAdjType.NONE) or
                self.roll_conv == RollConvention(RollConventionType.EOM)
        ):
            return self._calculated_unadjusted_date_from_adjusted(self.start_dt, self.roll_conv, self.bday_adj, cal)
        return self.start_dt

    def _calculate_unadjusted_end_dt(self, cal: HolidayCalendar | None = None) -> datetime:
        if cal is not None and self.roll_conv is not None:
            return self._calculated_unadjusted_date_from_adjusted(self.end_dt,
                                                                  self.roll_conv,
                                                                  self._calculate_end_dt_bday_adj(),
                                                                  cal)
        return self.end_dt

    def _calculate_end_dt_bday_adj(self) -> BDayAdj:
        return first_not_null(self.end_dt_bday_adj, self.bday_adj)

    def _calculated_first_regular_start_dt(self, unadj_start: datetime, cal: HolidayCalendar | None = None) -> datetime:
        if self.first_reg_start_dt is None:
            return unadj_start
        if cal is not None and self.roll_conv is not None:
            return self._calculated_unadjusted_date_from_adjusted(
                self.first_reg_start_dt, self.roll_conv, self.bday_adj, cal
            )
        return self.first_reg_start_dt

    def _calculated_last_regular_start_dt(self):
        return first_not_null(self.last_reg_start_dt, self.end_dt)

    def _calculated_roll_conv(self,
                              calculated_first_reg_start_dt: datetime,
                              calculated_last_reg_end_dt: datetime) :
        stub_conv = first_not_null(self.stub_conv, Stub)