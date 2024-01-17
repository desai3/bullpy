from typing import Set
import datetime
import calendar
import enum

from dateutil.relativedelta import relativedelta


def easter(year: int) -> datetime:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    # i = c // 4
    # k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.datetime(year, month, day)


def rem_sat_sun(holidays) -> Set:
    return {x for x in holidays if x.weekday() not in (5, 6)}


def bump_sun_to_mon(dt: datetime) -> datetime:
    if dt.weekday() == 6:
        return dt + relativedelta(days=1)
    return dt


def bump_to_mon(dt: datetime) -> datetime:
    if dt.weekday() == 5:
        return dt + relativedelta(days=2)
    elif dt.weekday() == 6:
        return dt + relativedelta(days=1)
    return dt


def bump_to_fri_or_mon(dt: datetime) -> datetime:
    if dt.weekday() == 6:
        return dt + relativedelta(days=1)
    elif dt.weekday() == 5:
        return dt - relativedelta(days=1)
    else:
        return dt


def christmas_bumped_sat_sun(year: int):
    dt = datetime.datetime(year, 12, 25)
    if dt.weekday() == 5 or dt.weekday() == 6:
        return datetime.datetime(year, 12, 27)
    return dt


def boxingday_bumped_sat_sun(year: int):
    dt = datetime.datetime(year, 12, 26)
    if dt.weekday() == 5 or dt.weekday() == 6:
        return datetime.datetime(year, 12, 28)
    return dt


def first_in_month(year: int, month: int, weekday: int) -> datetime:
    dt = datetime.datetime(year, month, 1)
    offset = relativedelta(days=1)
    for i in range(7):
        if dt.weekday() == weekday:
            return dt
        dt += offset


def last_in_month(year: int, month: int, weekday: int) -> datetime:
    dt = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    offset = relativedelta(days=1)
    for i in range(7):
        if dt.weekday() == weekday:
            return dt
        dt -= offset


def day_of_week_in_month(year: int, month: int, weekday: int, week: int) -> datetime:
    dt1 = first_in_month(year, month, weekday) + relativedelta(weeks=week - 1)
    return dt1


def us_common(holidays: Set, year: int, bump_back: bool, columbus_veteran: bool, mlk_start_year: int):
    # New Year
    holidays.add(bump_sun_to_mon(datetime.datetime(year, 1, 1)))

    # MLK: Third Monday of Jan
    if year >= mlk_start_year:
        holidays.add(day_of_week_in_month(year, 1, 0, 3))

    # President's day
    if year < 1971:
        holidays.add(bump_sun_to_mon(datetime.datetime(year, 2, 22)))
    else:
        # Thir Monday of Feb
        holidays.add(day_of_week_in_month(year, 2, 0, 3))

    # Memorial day
    if year < 1971:
        holidays.add(bump_sun_to_mon(datetime.datetime(year, 5, 30)))
    else:
        # Last Monday of May
        holidays.add(last_in_month(year, 5, 0))

    # Labor day, First monday of Sep
    holidays.add(first_in_month(year, 9, 0))

    # Columbus day
    if columbus_veteran:
        if year < 1971:
            holidays.add(bump_sun_to_mon(datetime.datetime(year, 10, 12)))
        else:
            # Second Monday of Oct
            holidays.add(day_of_week_in_month(year, 10, 0, 2))

    # Veterans day
    if columbus_veteran:
        if 1971 <= year < 1978:
            holidays.add(day_of_week_in_month(year, 10, 0, 4))
        else:
            holidays.add(bump_sun_to_mon(datetime.datetime(year, 11, 11)))

    # Thanksgiving 4th Thursday of November
    holidays.add(day_of_week_in_month(year, 11, 3, 4))

    # Independence day and Christmas day
    if bump_back:
        holidays.add(bump_to_fri_or_mon(datetime.datetime(year, 7, 4)))
        holidays.add(bump_to_fri_or_mon(datetime.datetime(year, 12, 25)))
    else:
        holidays.add(bump_sun_to_mon(datetime.datetime(year, 7, 4)))
        holidays.add(bump_sun_to_mon(datetime.datetime(year, 12, 25)))


class HolidayCalendarType(enum.Enum):
    USNY = enum.auto()
    USGS = enum.auto()
    NYFD = enum.auto()
    NYSE = enum.auto()
    GBLO = enum.auto()


class HolidayCalendar(object):

    @staticmethod
    def gen_usny():
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, False, True, 1986)
        holidays = rem_sat_sun(holidays)
        return holidays

    def gen_usgs(self):
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, True, True, 1986)
            holidays.add(easter(y) - relativedelta(days=2))

        # Hurricane sandy
        holidays.add(datetime.datetime(2012, 10, 30))
        # George H W Bush Death
        holidays.add(datetime.datetime(y, 12, 5))

        holidays = rem_sat_sun(holidays)
        return holidays

    def gen_nyfd(self):
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, False, True, 1986)
        holidays = rem_sat_sun(holidays)
        return holidays

    def gen_nyse(self):
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, True, False, 1998)
            holidays.add(easter(y) - relativedelta(days=2))

        # Lincoln day 1896 - 1953
        # Columbus day 1909 - 1953
        # Veterans day 1934 - 1953
        for y in range(1950, 1953 + 1):
            holidays.add(datetime.datetime(y, 2, 12))
            holidays.add(datetime.datetime(y, 10, 12))
            holidays.add(datetime.datetime(y, 11, 11))

        # Election day, Tue after first Monday of November
        for y in range(1950, 1968 + 1):
            holidays.add(first_in_month(y, 11, 0) + relativedelta(days=1))

        holidays.add(datetime.datetime(1972, 11, 7))
        holidays.add(datetime.datetime(1976, 11, 2))
        holidays.add(datetime.datetime(1980, 11, 4))
        # special days
        holidays.add(datetime.datetime(1955, 12, 24))  # Christmas Eve
        holidays.add(datetime.datetime(1956, 12, 24))  # Christmas Eve
        holidays.add(datetime.datetime(1958, 12, 26))  # Day after Christmas
        holidays.add(datetime.datetime(1961, 5, 29))  # Decoration day
        holidays.add(datetime.datetime(1963, 11, 25))  # Death of John F Kennedy
        holidays.add(datetime.datetime(1965, 12, 24))  # Christmas Eve
        holidays.add(datetime.datetime(1968, 2, 12))  # Lincoln birthday
        holidays.add(datetime.datetime(1968, 4, 9))  # Death of Martin Luther King
        holidays.add(datetime.datetime(1968, 6, 12))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 6, 19))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 6, 26))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 7, 3))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 7, 5))  # Day after independence
        holidays.add(datetime.datetime(1968, 7, 10))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 7, 17))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 7, 24))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 7, 31))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 8, 7))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 8, 13))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 8, 21))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 8, 28))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 9, 4))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 9, 11))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 9, 18))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 9, 25))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 10, 2))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 10, 9))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 10, 16))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 10, 23))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 10, 30))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 11, 6))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 11, 13))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 11, 20))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 11, 27))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 12, 4))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 12, 11))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 12, 18))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 12, 25))  # Paperwork crisis
        holidays.add(datetime.datetime(1968, 12, 31))  # Paperwork crisis
        holidays.add(datetime.datetime(1969, 2, 10))  # Snow
        holidays.add(datetime.datetime(1969, 3, 31))  # Death of Dwight Eisenhower
        holidays.add(datetime.datetime(1969, 7, 21))  # Lunar exploration
        holidays.add(datetime.datetime(1972, 12, 28))  # Death of Harry Truman
        holidays.add(datetime.datetime(1973, 1, 25))  # Death of Lyndon Johnson
        holidays.add(datetime.datetime(1977, 7, 14))  # Blackout
        holidays.add(datetime.datetime(1985, 9, 27))  # Hurricane Gloria
        holidays.add(datetime.datetime(1994, 4, 27))  # Death of Richard Nixon
        holidays.add(datetime.datetime(2001, 9, 11))  # 9 / 11 attack
        holidays.add(datetime.datetime(2001, 9, 12))  # 9 / 11 attack
        holidays.add(datetime.datetime(2001, 9, 13))  # 9 / 11 attack
        holidays.add(datetime.datetime(2001, 9, 14))  # 9 / 11 attack
        holidays.add(datetime.datetime(2004, 6, 11))  # Death of Ronald Reagan
        holidays.add(datetime.datetime(2007, 1, 2))  # Death of Gerald Ford
        holidays.add(datetime.datetime(2012, 10, 30))  # Hurricane Sandy
        holidays.add(datetime.datetime(2018, 12, 5))  # Death of George H.W.Bush
        holidays = rem_sat_sun(holidays)
        return holidays

    def gen_gblo(self):
        holidays = set()
        for y in range(1950, 2100):
            # New Year
            if y >= 1974:
                holidays.add(bump_to_mon(datetime.datetime(y, 1, 1)))

            # Easter
            holidays.add(easter(y) - relativedelta(days=2))
            holidays.add(easter(y) + relativedelta(days=2))

            # Early may
            if y == 1995 or y == 2020:
                holidays.add(datetime.datetime(y, 5, 8))
            elif y >= 1978:
                holidays.add(first_in_month(y, 5, 6))

            # Spring
            if y == 2002:
                # Golden Jubilee
                holidays.add(datetime.datetime(2002, 6, 3))
                holidays.add(datetime.datetime(2002, 6, 4))
            elif y == 2012:
                # Diamond Jubilee
                holidays.add(datetime.datetime(2012, 6, 4))
                holidays.add(datetime.datetime(2012, 6, 5))
            elif y == 2022:
                # Platinum Jubilee
                holidays.add(datetime.datetime(2022, 6, 2))
                holidays.add(datetime.datetime(2022, 6, 3))
            elif y == 1967 or y == 1970:
                holidays.add(last_in_month(y, 5, 0))
            elif y < 1971:
                holidays.add(easter(y) + relativedelta(days=50))
            else:
                holidays.add(last_in_month(y, 5, 0))

            # Summer
            if y < 1965:
                holidays.add(first_in_month(y, 8, 0))
            elif y < 1971:
                holidays.add(last_in_month(y, 8, 5) + relativedelta(days=2))
            else:
                holidays.add(last_in_month(y, 8, 0))

            # Queen's funeral
            if y == 2022:
                holidays.add(datetime.datetime(2022, 9, 19))

            # Christmas
            holidays.add(christmas_bumped_sat_sun(y))
            holidays.add(boxingday_bumped_sat_sun(y))

        holidays.add(datetime.datetime(1999, 12, 31))  # millennium
        holidays.add(datetime.datetime(2011, 4, 29))  # royal wedding
        holidays.add(datetime.datetime(2023, 5, 8))  # king's coronation

        rem_sat_sun(holidays)
        return holidays

    def __init__(self, name: HolidayCalendarType):
        self._type = name.name
        self._holidays = getattr(self, f'gen_{self._type.lower()}')()

    def is_holiday(self, dt: datetime) -> bool:
        return dt.weekday() in (5, 6) or dt in self._holidays

    def is_weekday(self, dt: datetime) -> bool:
        return not self.is_holiday(dt)
