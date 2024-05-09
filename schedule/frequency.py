import calendar
import datetime


def get_proleptic_month(dt: datetime):
    return 12 * dt.year + dt.month - 1


def plus_months(dt: datetime, months_to_add: int) -> datetime:
    if not months_to_add:
        return dt
    months_count = get_proleptic_month(dt)
    calc_month = months_count + months_to_add
    year = calc_month // 12
    month = calc_month % 12 + 1
    day = dt.day

    if month == 2:
        day = min(day, 29 if calendar.isleap(year) else 28)
    elif month in (4, 6, 9, 11):
        day = min(day, 30)
    return datetime.datetime(year, month, day)


def plus_years(dt: datetime, years_to_add: int) -> datetime:
    year = dt.year + years_to_add
    month = dt.month
    day = dt.day

    if month == 2:
        day = min(day, 29 if calendar.isleap(year) else 28)
    elif month in (4, 6, 9, 11):
        day = min(day, 30)
    return datetime.datetime(year, month, day)


def plus_days(dt: datetime, days_to_add: int) -> datetime:
    if not days_to_add:
        return dt

    dom = dt.day + days_to_add
    if 0 < dom <= 59:
        month_len = calendar.monthrange(dt.year, dt.month)[1]
        month = dt.month
        year = dt.year
        if dom <= month_len:
            return datetime.datetime(year, month, dom)
        elif month < 12:
            return datetime.datetime(year, month + 1, dom - month_len)
        else:
            return datetime.datetime(year + 1, 1, dom - month_len)
    mj_day = datetime.date.fromordinal(dt.toordinal() + days_to_add)
    return datetime.datetime(mj_day.year, mj_day.month, mj_day.day)



class Frequency(object):
    max_years = 1_000
    max_months = 12 * max_years

    def __init__(self, years=0, months=0, days=0):
        self._years = years
        self._months = months
        self._days = days

        if self._years > Frequency.max_years:
            raise ValueError(f"Years should not exceed {Frequency.max_years}")
        if self._months > Frequency.max_months:
            raise ValueError(f"Months should not exceed {Frequency.max_months}")
        if self._years < 0:
            raise ValueError("Years must be non-negative")
        if self._months < 0:
            raise ValueError("Months must be non-negative")
        if self._days < 0:
            raise ValueError("Days must be non-negative")

        tot_months = self.to_total_months()
        if tot_months > Frequency.max_months or self.is_term():
            self._events_per_year = 0
            self._events_per_year_estimate = 0.0
        else:
            months = tot_months
            days = self._days
            if months > 0 and days == 0:
                self._events_per_year = 12 // months if 12 % months == 0 else -1
                self._events_per_year_estimate = 12 / months
            elif days > 0 and months == 0:
                self._events_per_year = 364 // days if 364 % days == 0 else -1
                self._events_per_year_estimate = 364 / days
            else:
                self._events_per_year = -1
                estimated_secs = months * (31556952 // 12) + days * 86400
                self._events_per_year_estimate = 31556952 / estimated_secs

    def __eq__(self, other):
        return self.get_years() == other.get_years() and \
            self.get_months() == other.get_months() and \
            self.get_days() == other.get_days()

    def is_month_based(self) -> bool:
        return self.to_total_months() > 0 and self.get_days() == 0 and not self.is_term()

    def exact_divide(self, other):
        if self.is_term():
            raise ValueError("Frequency is of type TERM")
        if other.is_term():
            raise ValueError("Other frequency is of type TERM")

        if self.is_month_based() and other.is_month_based():
            payment_months = self.to_total_months()
            accrual_months = other.to_total_months()

            if payment_months % accrual_months == 0:
                return payment_months // accrual_months
        elif self.to_total_months() == 0 and other.to_total_months() == 0:
            payment_days = self.get_days()
            accrual_days = other.get_days()
            if payment_days % accrual_days == 0:
                return payment_days // accrual_days
        raise ValueError(f"Frequency {self} is not a multiple of {other}")

    def normalized(self):
        tot_months = self.to_total_months()
        years, months = divmod(tot_months, 12)
        if years == self._years and months == self._months:
            return self
        return Frequency(years, months, self._days)

    def get_months(self) -> int:
        return self._months

    def to_total_months(self) -> int:
        return 12 * self._years + self._months

    def get_days(self) -> int:
        return self._days

    def get_years(self) -> int:
        return self._years

    def is_annual(self):
        return self.to_total_months() == 12 and self.get_days() == 0

    def events_per_year(self):
        if self._events_per_year == -1:
            raise ValueError("Unable to calculate events per year")
        return self._events_per_year

    def events_per_year_estimate(self):
        return self._events_per_year_estimate

    def is_term(self):
        return self._years == 0 and self._months == 0 and self._days == 0

    def add_to_date(self, dt: datetime) -> datetime:
        return plus_days(plus_months(dt, self.to_total_months()), self.get_days())

    def sub_from_date(self, dt: datetime) -> datetime:
        return plus_days(plus_months(dt, -self.to_total_months()), -self.get_days())

    def is_week_based(self):
        return self.to_total_months() == 0 and self.get_days() % 7 == 0 and not self.is_term()

    def __repr__(self):
        return f"Frequency(years={self._years}, months={self._months}, days={self._days})"


def between(start: datetime, end: datetime) -> Frequency:
    tot_months = get_proleptic_month(end) - get_proleptic_month(start)
    days = end.day - start.day

    if tot_months > 0 and days < 0:
        tot_months -= 1
        calc_date = plus_months(start, tot_months)
        days = end.toordinal() - calc_date.toordinal()
    elif tot_months < 0 and days > 0:
        tot_months += 1
        days -= calendar.monthrange(end.year, end.month)[1]
    years, months = divmod(tot_months, 12)
    return Frequency(years=years, months=months, days=days)
