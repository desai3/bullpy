import datetime
import calendar


def _next_leap_day(dt: datetime):
    if dt.month == 2 and dt.day == 29:
        return _ensure_leap_day(dt.year + 4)

    if calendar.isleap(dt.year) and dt.month <= 2:
        return datetime.datetime(dt.year, 2, 29)

    return _ensure_leap_day(((dt.year // 4) * 4) + 4)


def _ensure_leap_day(year: int):
    return datetime.datetime(year, 2, 29) if year.isleap(year) else datetime.datetime(year + 4, 2, 29)


def _number_of_leap_days(d1: datetime, d2: datetime):
    res = 0
    cur = _next_leap_day(d1)
    while cur <= d2:
        cur = _next_leap_day(cur)
        res += 1
    return res


def _ordinal_diff(d1: datetime, d2: datetime):
    return d2.toordinal() - d1.toordinal()


class DayCount(object):
    def __init__(self, typ):
        self._type = typ
        self._year_frac = getattr(self, f"_{typ}_year_fraction")
        self._days = getattr(self, f"_{typ}_days")

    def year_fraction(self, d1: datetime, d2: datetime):
        return self._year_frac(d1, d2)

    def days(self, d1: datetime, d2: datetime):
        return self._days(d1, d2)

    def _actual_365_fixed_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _actual_365_fixed_year_fraction(self, d1: datetime, d2: datetime):
        return self._actual_365_fixed_days(d1, d2) / 365.0

    def _actual_364_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _actual_364_year_fraction(self, d1: datetime, d2: datetime):
        return self._actual_364_days(d1, d2) / 364.0

    def _actual_365_25_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _actual_365_25_year_fraction(self, d1: datetime, d2: datetime):
        self._actual_365_25_days(d1, d2) / 365.25

    def _actual_360_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2)

    def _actual_360_year_fraction(self, d1: datetime, d2: datetime):
        return self._actual_360_days(d1, d2) / 360.0

    def _no_leap_365_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2) - _number_of_leap_days(d1, d2)

    def _no_leap_365_year_fraction(self, d1: datetime, d2: datetime):
        return self._no_leap_365_days(d1, d2) / 365.0

    def _no_leap_360_days(self, d1: datetime, d2: datetime):
        return _ordinal_diff(d1, d2) - _number_of_leap_days(d1, d2)

    def _no_leap_360_year_fraction(self, d1: datetime, d2: datetime):
        return self._no_leap_360_days(d1, d2) / 360.0


if __name__ == '__main__':
    d1 = datetime.datetime(2023, 1, 23)
    d2 = datetime.datetime(2023, 12, 20)

    dc = DayCount('actual_365_fixed')
    print(dc.days(d1, d2))
    print(dc.year_fraction(d1, d2))
