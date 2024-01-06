import datetime


class DayCount(object):
    def __init__(self, typ):
        self._type = typ
        self._year_frac = getattr(self, f"_{typ}_year_fraction")
        self._days = getattr(self, f"_{typ}_days")

    def year_fraction(self, d1: datetime, d2: datetime):
        return self._year_frac(d1, d2)

    def days(self, d1: datetime, d2: datetime):
        return self._days(d1, d2)

    @staticmethod
    def _day_count(d1: datetime, d2: datetime):
        return d2.toordinal() - d1.toordinal()

    def _actual_365_fixed_days(self, d1: datetime, d2: datetime):
        return self._day_count(d1, d2)

    def _actual_365_fixed_year_fraction(self, d1: datetime, d2: datetime):
        return self._actual_365_fixed_days(d1, d2) / 365.0

    def _actual_364_days(self, d1: datetime, d2: datetime):
        return self._day_count(d1, d2)

    def _actual_364_year_fraction(self, d1: datetime, d2: datetime):
        return self._actual_364_days(d1, d2) / 364.0

    def _actual_365_25_days(self, d1: datetime, d2: datetime):
        return self._day_count(d1, d2)

    def _actual_365_25_year_fraction(self, d1: datetime, d2: datetime):
        self._actual_365_25_days(d1, d2) / 365.25


if __name__ == '__main__':
    d1 = datetime.datetime(2023, 1, 23)
    d2 = datetime.datetime(2023, 12, 20)

    dc = DayCount('actual_365_fixed')
    print(dc.days(d1, d2))
    print(dc.year_fraction(d1, d2))