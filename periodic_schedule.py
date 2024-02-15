import datetime
import calendar

from calendars import HolidayCalendar
from roll_convention import RollConvention
from bdayadj import BDayAdj

class PeriodicSchedule(object):
    def __init__(self, unadjusted_start_dt, unadjusted_end_dt, freq, bday_adj, stub_conv, eom):
        self.unadjusted_start_dt = unadjusted_start_dt
        self.unadjusted_end_dt = unadjusted_end_dt
        self.freq = freq
        self.bday_adj = bday_adj
        self.stub_conv = stub_conv
        self.eom = eom

    def _calculated_unadjusted_date_from_adjusted(self,
                                                  base_dt: datetime,
                                                  roll_conv: RollConvention,
                                                  bday_adj: BDayAdj,
                                                  cal: HolidayCalendar):
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
