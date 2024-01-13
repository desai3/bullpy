import datetime
import calendar

from dateutil.relativedelta import relativedelta

from calendars import HolidayCalendar, HolidayCalendarType


def data_usny():
    data = {2008: [(1, 1), (1, 21), (2, 18), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
            2009: [(1, 1), (1, 19), (2, 16), (5, 25), (7, 4), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)],
            2010: [(1, 1), (1, 18), (2, 15), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25), (12, 25)],
            2011: [(1, 1), (1, 17), (2, 21), (5, 30), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24), (12, 26)],
            2012: [(1, 2), (1, 16), (2, 20), (5, 28), (7, 4), (9, 3), (10, 8), (11, 12), (11, 22), (12, 25)],
            2013: [(1, 1), (1, 21), (2, 18), (5, 27), (7, 4), (9, 2), (10, 14), (11, 11), (11, 28), (12, 25)],
            2014: [(1, 1), (1, 20), (2, 17), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
            2015: [(1, 1), (1, 19), (2, 16), (5, 25), (7, 4), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)]}

    holidays = set()
    for y in data:
        for md in data[y]:
            holidays.add(datetime.datetime(y, md[0], md[1]))
    return holidays


def test_usny():
    data = data_usny()
    cal = HolidayCalendar(HolidayCalendarType.USNY)

    min_date = min(data)
    max_date = max(data)

    dt = datetime.datetime(min_date.year, min_date.month, 1)
    max_date = datetime.datetime(max_date.year, max_date.month, calendar.monthrange(max_date.year, max_date.month)[1])

    offset = relativedelta(days=1)
    while dt <= max_date:
        assert cal.is_holiday(dt) != cal.is_weekday(dt)
        if cal.is_holiday(dt):
            assert dt in data or dt.weekday() in (5, 6)
        else:
            assert dt not in data

        dt += offset


if __name__ == '__main__':
    test_usny()