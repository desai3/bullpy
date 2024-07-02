from typing import Set, List
import datetime
import calendar
import enum

from .frequency import plus_days


def citizens_day(holidays: Set[datetime], d1: datetime, d2: datetime):
    if d1 in holidays and d2 in holidays:
        if d1.weekday() in (0, 1, 2):
            holidays.add(plus_days(d1, 1))


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


def add_sat_sun(holidays: Set[datetime], start: datetime, end: datetime) -> Set:
    dt = start
    while dt.weekday() not in (5, 6):
        dt = plus_days(dt, 1)

    offset = -1 if dt.weekday() == 6 else 1
    while True:
        if start <= dt <= end:
            holidays.add(dt)
        elif dt > end:
            break

        dt1 = plus_days(dt, offset)
        if start <= dt1 <= end:
            holidays.add(dt1)
        elif dt > end:
            break
        dt = plus_days(dt, 7)


def bump_sun_to_mon(dt: datetime) -> datetime:
    if dt.weekday() == 6:
        return plus_days(dt, 1)
    return dt


def bump_to_mon(dt: datetime) -> datetime:
    if dt.weekday() == 5:
        return plus_days(dt, 2)
    elif dt.weekday() == 6:
        return plus_days(dt, 1)
    return dt


def bump_to_fri_or_mon(dt: datetime) -> datetime:
    if dt.weekday() == 6:
        return plus_days(dt, 1)
    elif dt.weekday() == 5:
        return plus_days(dt, -1)
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
    for i in range(7):
        if dt.weekday() == weekday:
            return dt
        dt = plus_days(dt, 1)


def last_in_month(year: int, month: int, weekday: int) -> datetime:
    dt = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    for i in range(7):
        if dt.weekday() == weekday:
            return dt
        dt = plus_days(dt, -1)


def day_of_week_in_month(year: int, month: int, weekday: int, week: int) -> datetime:
    # dt1 = first_in_month(year, month, weekday) + relativedelta(weeks=week - 1)
    dt1 = plus_days(first_in_month(year, month, weekday), 7 * (week - 1))
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
    EUTA = enum.auto()
    CATO = enum.auto()
    CAMO = enum.auto()
    AUSY = enum.auto()
    JPTO = enum.auto()
    SAT_SUN = enum.auto()


class HolidayCalendar(object):

    @staticmethod
    def gen_sat_sun():
        holidays = set()
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_usny():
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, False, True, 1986)
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_usgs():
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, True, True, 1986)
            holidays.add(plus_days(easter(y), 2))

        # Hurricane sandy
        holidays.add(datetime.datetime(2012, 10, 30))
        # George H W Bush Death
        holidays.add(datetime.datetime(y, 12, 5))

        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_nyfd():
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, False, True, 1986)
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_nyse():
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, True, False, 1998)
            holidays.add(plus_days(easter(y), -2))

        # Lincoln day 1896 - 1953
        # Columbus day 1909 - 1953
        # Veterans day 1934 - 1953
        for y in range(1950, 1953 + 1):
            holidays.add(datetime.datetime(y, 2, 12))
            holidays.add(datetime.datetime(y, 10, 12))
            holidays.add(datetime.datetime(y, 11, 11))

        # Election day, Tue after first Monday of November
        for y in range(1950, 1968 + 1):
            holidays.add(plus_days(first_in_month(y, 11, 0), 1))

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
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_jpto():
        holidays = set()
        for y in range(1950, 2100):
            # New year
            holidays.add(datetime.datetime(y, 1, 1))
            holidays.add(datetime.datetime(y, 1, 2))
            holidays.add(datetime.datetime(y, 1, 3))
            # Coming of age
            if y >= 2000:
                holidays.add(day_of_week_in_month(y, 1, 0, 2))
            else:
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 1, 15)))

            # National foundation
            if y >= 1967:
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 2, 11)))

            # vernal equinox (from 1948), 20th or 21st (predictions/facts  2000 to 2030
            if y in {2000, 2001, 2004, 2005, 2008, 2009, 2012, 2013, 2016, 2017, 2020, 2021,
                     2024, 2025, 2026, 2028, 2029, 2030}:
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 3, 20)))
            else:
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 3, 21)))

            # Showa (from 2007 onwards), greenery (from 1989 to 2006), emperor (before 1989)
            holidays.add(bump_sun_to_mon(datetime.datetime(y, 4, 29)))
            # constitution (from 1948)
            if y >= 1985:
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 5, 3)))
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 5, 4)))
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 5, 5)))
                if y >= 2007 and datetime.datetime(y, 5, 3).weekday() == 6 or datetime.datetime(y, 5, 3).weekday() == 6:
                    holidays.add(datetime.datetime(y, 5, 6))
                else:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 5, 3)))
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 5, 5)))
                # Marine
                if y == 2021:
                    # Moved because of the Olympics
                    holidays.add(datetime.datetime(y, 7, 22))
                elif y == 2020:
                    # Moved because of the Olympics (day prior to opening ceremony)
                    holidays.add(datetime.datetime(y, 7, 23))
                elif y >= 2003:
                    holidays.add(day_of_week_in_month(y, 7, 0, 3))
                elif y >= 1996:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 7, 20)))

                # Mountain
                if y == 2021:
                    # Moved because of the Olympics
                    holidays.add(datetime.datetime(y, 8, 9))
                elif y == 2020:
                    # Moved because of the Olympics (day after closing ceremony)
                    holidays.add(datetime.datetime(y, 8, 10))
                elif y >= 2016:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 8, 11)))

                # Aged
                if y >= 2003:
                    holidays.add(day_of_week_in_month(y, 9, 0, 3))
                elif y >= 1966:
                    holidays.add(datetime.datetime(y, 9, 15))

                # Autumn equinox (from 1948), 22nd or 23rd (predictions/facts 2000 to 2030)
                if y in {2012, 2016, 2020, 2024, 2028}:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 9, 22)))
                else:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 9, 23)))
                citizens_day(holidays, datetime.datetime(y, 9, 20), datetime.datetime(y, 9, 22))
                citizens_day(holidays, datetime.datetime(y, 9, 21), datetime.datetime(y, 9, 23))

                # Health-sports
                if y == 2021:
                    # Moved because of the Olympics
                    holidays.add(datetime.datetime(y, 7, 23))
                elif y == 2020:
                    # Moved because of the Olympics (day after closing ceremony)
                    holidays.add(datetime.datetime(y, 7, 24))
                elif y >= 2000:
                    holidays.add(day_of_week_in_month(y, 10, 0, 2))
                elif y >= 1966:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 10, 10)))

                # Culture (from 1948)
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 11, 3)))
                # Labor (from 1948)
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 11, 23)))
                # Emperor (current emperor birthday)
                if 1990 <= y < 2019:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 12, 23)))
                elif y >= 2020:
                    holidays.add(bump_sun_to_mon(datetime.datetime(y, 2, 23)))
                # New years eve - bank of Japan, but not national holiday
                holidays.add(bump_sun_to_mon(datetime.datetime(y, 12, 31)))

            holidays.add(datetime.datetime(1959, 4, 10))  # Marriage Akihito
            holidays.add(datetime.datetime(1989, 2, 24))  # Funeral Showa
            holidays.add(datetime.datetime(1990, 11, 12))  # Enthrone Akihito
            holidays.add(datetime.datetime(1993, 6, 9))  # Marriage Naruhito
            holidays.add(datetime.datetime(2019, 4, 30))  # Abdication
            holidays.add(datetime.datetime(2019, 5, 1))  # Accession
            holidays.add(datetime.datetime(2019, 5, 2))  # Accession
            holidays.add(datetime.datetime(2019, 10, 22))  # Enthronement

        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays


    @staticmethod
    def gen_gblo():
        holidays = set()
        for y in range(1950, 2100):
            # New Year
            if y >= 1974:
                holidays.add(bump_to_mon(datetime.datetime(y, 1, 1)))

            # Easter
            holidays.add(plus_days(easter(y), -2))
            holidays.add(plus_days(easter(y), 2))

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
                holidays.add(plus_days(easter(y), 50))
            else:
                holidays.add(last_in_month(y, 5, 0))

            # Summer
            if y < 1965:
                holidays.add(first_in_month(y, 8, 0))
            elif y < 1971:
                holidays.add(plus_days(last_in_month(y, 8, 5), 2))
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

        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_euta():
        holidays = set()
        for y in range(1997, 2100):
            if y >= 2000:
                holidays.add(datetime.datetime(y, 1, 1))
                holidays.add(plus_days(easter(y), -2))
                holidays.add(plus_days(easter(y), 1))
                holidays.add(datetime.datetime(y, 5, 1))
                holidays.add(datetime.datetime(y, 12, 25))
                holidays.add(datetime.datetime(y, 12, 26))
            else:  # 1997 to 1999
                holidays.add(datetime.datetime(y, 1, 1))
                holidays.add(datetime.datetime(y, 12, 25))
            if y == 1999 or y == 2001:
                holidays.add(datetime.datetime(y, 12, 31))
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_cato():
        holidays = set()
        for y in range(1950, 2100):
            # New Year (Public)
            holidays.add(bump_to_mon(datetime.datetime(y, 1, 1)))
            if y >= 2008:
                holidays.add(day_of_week_in_month(y, 2, 0, 3))
            # good friday(public)
            holidays.add(plus_days(easter(y), -2))
            # victoria(public)
            cur = datetime.datetime(y, 5, 25)
            while cur.weekday() != 0:
                cur = plus_days(cur, 1)
            holidays.add(cur)
            # canada(public)
            holidays.add(bump_to_mon(datetime.datetime(y, 7, 1)))
            # civic
            holidays.add(day_of_week_in_month(y, 8, 0, 1))
            # labour(public)
            holidays.add(day_of_week_in_month(y, 9, 0, 1))
            # thanksgiving(public)
            holidays.add(day_of_week_in_month(y, 10, 0, 2))
            # remembrance
            holidays.add(bump_to_mon(datetime.datetime(y, 11, 11)))
            # christmas(public)
            holidays.add(christmas_bumped_sat_sun(y))
            # boxing(public)
            holidays.add(boxingday_bumped_sat_sun(y))
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_camo():
        holidays = set()
        for y in range(1950, 2100):
            # new year
            holidays.add(bump_to_mon(datetime.datetime(y, 1, 1)))
            # good friday(public)
            holidays.add(plus_days(easter(y), -2))
            # patriots
            cur = datetime.datetime(y, 5, 25)
            while cur.weekday() != 0:
                cur = plus_days(cur, -1)
            holidays.add(cur)
            # fete nationale quebec
            holidays.add(bump_to_mon(datetime.datetime(y, 6, 24)))
            # canada
            holidays.add(bump_to_mon(datetime.datetime(y, 7, 1)))
            # labour
            holidays.add(day_of_week_in_month(y, 9, 0, 1))
            # thanksgiving
            holidays.add(day_of_week_in_month(y, 10, 0, 2))
            # christmas
            holidays.add(christmas_bumped_sat_sun(y))
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    @staticmethod
    def gen_ausy():
        holidays = set()
        for y in range(1950, 2100):
            # new year
            holidays.add(bump_to_mon(datetime.datetime(y, 1, 1)))
            # australia day
            holidays.add(bump_to_mon(datetime.datetime(y, 1, 26)));
            # good friday
            holidays.add(plus_days(easter(y), -2))
            # easter monday
            holidays.add(plus_days(easter(y), 1))
            # anzac day
            holidays.add(datetime.datetime(y, 4, 25));
            # queen 's birthday
            holidays.add(day_of_week_in_month(y, 6, 0, 2))
            # bank holiday
            holidays.add(day_of_week_in_month(y, 8, 0, 1))
            # labour day
            holidays.add(day_of_week_in_month(y, 10, 0, 1))
            # christmas
            holidays.add(christmas_bumped_sat_sun(y))
            # boxing
            holidays.add(boxingday_bumped_sat_sun(y))
        add_sat_sun(holidays, datetime.datetime(1950, 1, 1), plus_days(datetime.datetime(2100, 12, 31), -1))
        return holidays

    def __init__(self, name: HolidayCalendarType):
        self._type = name.name
        self._holidays = getattr(self, f'gen_{self._type.lower()}')()

    def is_holiday(self, dt: datetime) -> bool:
        return dt in self._holidays

    def is_businessday(self, dt: datetime) -> bool:
        return not self.is_holiday(dt)

    def next(self, dt: datetime) -> datetime:
        nxt = plus_days(dt, 1)
        return self.next(nxt) if self.is_holiday(nxt) else nxt

    def previous(self, dt: datetime) -> datetime:
        prev = plus_days(dt, -1)
        return self.previous(prev) if self.is_holiday(prev) else prev

    def previous_or_same(self, dt: datetime) -> datetime:
        return self.previous(dt) if self.is_holiday(dt) else dt

    def next_or_same(self, dt: datetime) -> datetime:
        return self.next(dt) if self.is_holiday(dt) else dt

    def next_or_same_last_in_month(self, dt: datetime) -> datetime:
        nxt_or_same = self.next_or_same(dt)
        return self.previous(dt) if nxt_or_same.month != dt.month else nxt_or_same

    def shift(self, dt: datetime, amount: int) -> datetime:
        adjusted = dt
        if amount > 0:
            for _ in range(amount):
                adjusted = self.next(adjusted)
        elif amount < 0:
            for _ in range(-amount):
                adjusted = self.previous(adjusted)
        return adjusted

    def __eq__(self, other):
        return isinstance(other, type(self)) and self._type == other._type


class CustomeHolidayCalendar(HolidayCalendar):
    def __init__(self, name: str, holidays: Set):
        self._type = name
        self._holidays = holidays

    def __eq__(self, other):
        return isinstance(other, type(self)) and self._holidays == other._holidays


class CombinedHolidayCalendar(HolidayCalendar):
    def __init__(self, calendar_names=List[HolidayCalendarType]):
        self._type = "_".join([x.name for x in calendar_names])
        self._holidays = set()
        for cn in calendar_names:
            self._holidays |= HolidayCalendar(cn)._holidays
