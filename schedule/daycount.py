import datetime
from dateutil.relativedelta import relativedelta
import calendar
import enum


def _next_leap_day(dt: datetime):
    if dt.month == 2 and dt.day == 29:
        return _ensure_leap_day(dt.year + 4)

    if calendar.isleap(dt.year) and dt.month <= 2:
        return datetime.datetime(dt.year, 2, 29)

    return _ensure_leap_day(((dt.year // 4) * 4) + 4)


def _next_or_same_leap_day(dt: datetime):
    if dt.month == 2 and dt.day == 29:
        return dt

    if calendar.isleap(dt.year) and dt.month <= 2:
        return datetime.datetime(dt.year, 2, 29)

    return _ensure_leap_day(((dt.year // 4) * 4) + 4)


def _ensure_leap_day(year: int):
    return datetime.datetime(year, 2, 29) if calendar.isleap(year) else datetime.datetime(year + 4, 2, 29)


def _number_of_leap_days(d1: datetime, d2: datetime):
    res = 0
    cur = _next_leap_day(d1)
    while cur <= d2:
        cur = _next_leap_day(cur)
        res += 1
    return res


def _ordinal_diff(d1: datetime, d2: datetime):
    return d2.toordinal() - d1.toordinal()


def _thirty_360_diff(y1, m1, d1, y2, m2, d2):
    return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)


def _length_of_year(dt: datetime):
    return 366 if calendar.isleap(dt.year) else 365


def _doy(dt: datetime):
    if calendar.isleap(dt.year):
        lookup = [0, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    else:
        lookup = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    return lookup[dt.month] + dt.day


def _last_day_of_feb(dt: datetime):
    return dt.month == 2 and dt.day == calendar.monthrange(dt.year, dt.month)[1]


class DayCountType(enum.Enum):
    ONE_ONE = enum.auto()
    ACT_ACT_ISDA = enum.auto()
    ACT_ACT_AFB = enum.auto()
    ACT_ACT_YEAR = enum.auto()
    ACT_365_ACTUAL = enum.auto()
    ACT_360 = enum.auto()
    ACT_364 = enum.auto()
    ACT_365F = enum.auto()
    ACT_365_25 = enum.auto()
    NL_360 = enum.auto()
    NL_365 = enum.auto()
    THIRTY_360_ISDA = enum.auto()
    THIRTY_U_360_EOM = enum.auto()
    THIRTY_360_PSA = enum.auto()
    THIRTY_E_360 = enum.auto()
    THIRTY_EPLUS_360 = enum.auto()
    THIRTY_E_365 = enum.auto()


class DayCount(object):
    def __init__(self, typ: DayCountType):
        self._type = typ.name
        self._year_frac = getattr(self, f"_{self._type.lower()}_year_fraction")
        self._days = getattr(self, f"_{self._type.lower()}_days")

    def year_fraction(self, d1: datetime, d2: datetime):
        return self._year_frac(d1, d2)

    def days(self, d1: datetime, d2: datetime):
        return self._days(d1, d2)

    def _one_one_days(self, d1: datetime, d2: datetime):
        return 1

    def _one_one_year_fraction(self, d1: datetime, d2: datetime):
        return 1.0

    def _act_act_isda_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_act_isda_year_fraction(self, d1: datetime, d2: datetime):
        yr1 = d1.year
        yr2 = d2.year
        first_year_len = _length_of_year(d1)

        if yr1 == yr2:
            return (_doy(d2) - _doy(d1)) / first_year_len

        first_rem_year = first_year_len - _doy(d1) + 1
        second_rem_year = _doy(d2) - 1
        second_year_len = _length_of_year(d2)

        return (first_rem_year / first_year_len) + (second_rem_year / second_year_len) + (yr2 - yr1 - 1)

    def _act_act_afb_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_act_afb_year_fraction(self, d1: datetime, d2: datetime):
        end = d2
        start = d2 - relativedelta(years=1)

        years = 0
        while start >= d1:
            years += 1
            end = start
            start = d2 - relativedelta(years=years + 1)

        actual_days = _ordinal_diff(d1, end)
        next_leap = _next_or_same_leap_day(d1)
        return years + (actual_days / (366.0 if next_leap < end else 365.0))

    def _act_act_year_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_act_year_year_fraction(self, d1: datetime, d2: datetime):
        start_dt = d1
        years_added = 0
        while d2 > start_dt + relativedelta(years=1):
            years_added += 1
            start_dt = d1 + relativedelta(years=years_added)
        actual_days = _ordinal_diff(start_dt, d2)
        actual_days_year = _ordinal_diff(start_dt, start_dt + relativedelta(years=1))
        return years_added + (actual_days / actual_days_year)

    def _act_360_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_360_year_fraction(self, d1: datetime, d2: datetime):
        return self._act_360_days(d1, d2) / 360.0

    def _act_364_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_364_year_fraction(self, d1: datetime, d2: datetime):
        return self._act_364_days(d1, d2) / 364.0

    def _act_365f_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_365f_year_fraction(self, d1: datetime, d2: datetime):
        return self._act_365f_days(d1, d2) / 365.0

    def _act_365_actual_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_365_actual_year_fraction(self, d1: datetime, d2: datetime):
        diff = self._act_365_actual_days(d1, d2)
        next_leap = _next_leap_day(d1)
        return diff / (365.0 if next_leap > d2 else 366.0)

    def _act_365_25_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _act_365_25_year_fraction(self, d1: datetime, d2: datetime):
        return self._act_365_25_days(d1, d2) / 365.25

    def _nl_360_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2) - _number_of_leap_days(d1, d2)

    def _nl_360_year_fraction(self, d1: datetime, d2: datetime):
        return self._nl_360_days(d1, d2) / 360.0

    def _nl_365_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2) - _number_of_leap_days(d1, d2)

    def _nl_365_year_fraction(self, d1: datetime, d2: datetime):
        return self._nl_365_days(d1, d2) / 365.0

    def _thirty_360_isda_days(self, d1: datetime, d2: datetime):
        dt1 = d1.day
        dt2 = d2.day

        if dt1 == 31:
            dt1 = 30
        if dt2 == 31 and dt1 == 30:
            dt2 = 30
        return _thirty_360_diff(d1.year, d1.month, dt1, d2.year, d2.month, dt2)

    def _thirty_360_isda_year_fraction(self, d1: datetime, d2: datetime):
        return self._thirty_360_isda_days(d1, d2) / 360.0

    def _thirty_u_360_eom_days(self, d1: datetime, d2: datetime):
        dt1 = d1.day
        dt2 = d2.day

        if _last_day_of_feb(d1):
            if _last_day_of_feb(d2):
                dt2 = 30
            dt1 = 30

        if dt1 == 31:
            dt1 = 30
        if dt2 == 31 and dt1 == 30:
            dt2 = 30
        return _thirty_360_diff(d1.year, d1.month, dt1, d2.year, d2.month, dt2)

    def _thirty_u_360_eom_year_fraction(self, d1: datetime, d2: datetime):
        self._thirty_u_360_eom_days(d1, d2) / 360.0

    def _thirty_360_psa_days(self, d1: datetime, d2: datetime):
        dt1 = d1.day
        dt2 = d2.day

        if dt1 == calendar.monthrange(d1.year, d1.month)[1]:
            dt1 = 30
        if dt2 == 31 and dt1 == 30:
            dt2 = 30
        return _thirty_360_diff(d1.year, d1.month, dt1, d2.year, d2.month, dt2)

    def _thirty_360_psa_year_fraction(self, d1: datetime, d2: datetime):
        return self._thirty_360_psa_days(d1, d2) / 360.0

    def _thirty_e_360_days(self, d1: datetime, d2: datetime):
        dt1 = d1.day
        dt2 = d2.day

        if dt1 == 31:
            dt1 = 30
        if dt2 == 31:
            dt2 = 30
        return _thirty_360_diff(d1.year, d1.month, dt1, d2.year, d2.month, dt2)

    def _thirty_e_360_year_fraction(self, d1: datetime, d2: datetime):
        return self._thirty_e_360_days(d1, d2) / 360.0

    def _thirty_eplus_360_days(self, d1: datetime, d2: datetime):
        dt1 = d1.day
        dt2 = d2.day
        mn1 = d1.month
        mn2 = d2.month

        if dt1 == 31:
            dt1 = 30
        if dt2 == 31:
            dt2 = 1
            mn2 += 1
        return _thirty_360_diff(d1.year, mn1, dt1, d2.year, mn2, dt2)

    def _thirty_eplus_360_year_fraction(self, d1: datetime, d2: datetime):
        return self._thirty_eplus_360_days(d1, d2) / 360.0

    def _thirty_e_365_days(self, d1: datetime, d2: datetime):
        dt1 = d1.day
        dt2 = d2.day

        if dt1 == calendar.monthrange(d1.year, d1.month)[1]:
            dt1 = 30
        if dt2 == calendar.monthrange(d2.year, d2.month)[1]:
            dt2 = 30
        return _thirty_360_diff(d1.year, d1.month, dt1, d2.year, d2.month, dt2)

    def _thirty_e_365_year_fraction(self, d1: datetime, d2: datetime):
        return self._thirty_e_365_days(d1, d2) / 365.0


if __name__ == '__main__':
    d1 = datetime.datetime(2023, 1, 23)
    d2 = datetime.datetime(2023, 12, 20)

    dct = DayCountType.THIRTY_E_360
    dc = DayCount(dct)
    print(dc.days(d1, d2))
    print(dc.year_fraction(d1, d2))
