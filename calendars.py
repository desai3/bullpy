from typing import Set
import datetime
import calendar
import enum

from dateutil.relativedelta import relativedelta


def rem_sat_sun(holidays) -> Set:
    return {x for x in holidays if x.weekday() not in (5, 6)}


def bump_sun_to_mon(dt: datetime) -> datetime:
    if dt.weekday() == 6:
        return dt + relativedelta(days=1)
    return dt


def bump_to_fri_or_mon(dt: datetime) -> datetime:
    if dt.weekday() == 6:
        return dt + relativedelta(days=1)
    elif dt.weekday() == 5:
        return dt - relativedelta(days=1)
    else:
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


class HolidayCalendar(object):

    @staticmethod
    def gen_usny():
        holidays = set()
        for y in range(1950, 2100):
            us_common(holidays, y, False, True, 1986)
        holidays = rem_sat_sun(holidays)
        return holidays

    def __init__(self, name: HolidayCalendarType):
        self._type = name.name
        self._holidays = getattr(self, f'gen_{self._type.lower()}')()

    def is_holiday(self, dt: datetime) -> bool:
        return dt.weekday() in (5, 6) or dt in self._holidays

    def is_weekday(self, dt: datetime) -> bool:
        return not self.is_holiday(dt)