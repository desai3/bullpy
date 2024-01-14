import datetime

from dateutil.relativedelta import relativedelta

from calendars import HolidayCalendar, HolidayCalendarType


class CalData(object):
    def __init__(self, cal_type: HolidayCalendarType):
        self._type = cal_type

        self.usny = {2008: [(1, 1), (1, 21), (2, 18), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
                     2009: [(1, 1), (1, 19), (2, 16), (5, 25), (7, 4), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)],
                     2010: [(1, 1), (1, 18), (2, 15), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25), (12, 25)],
                     2011: [(1, 1), (1, 17), (2, 21), (5, 30), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24), (12, 26)],
                     2012: [(1, 2), (1, 16), (2, 20), (5, 28), (7, 4), (9, 3), (10, 8), (11, 12), (11, 22), (12, 25)],
                     2013: [(1, 1), (1, 21), (2, 18), (5, 27), (7, 4), (9, 2), (10, 14), (11, 11), (11, 28), (12, 25)],
                     2014: [(1, 1), (1, 20), (2, 17), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
                     2015: [(1, 1), (1, 19), (2, 16), (5, 25), (7, 4), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)],
                     2021: [(1, 1), (1, 18), (2, 15), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25), (12, 25)],
                     2022: [(1, 1), (1, 17), (2, 21), (5, 30), (6, 20), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24),
                            (12, 26)]}

        self.usgs = {
            1996: [(1, 1), (1, 15), (2, 19), (4, 5), (5, 27), (7, 4), (9, 2), (10, 14), (11, 11), (11, 28), (12, 25)],
            1997: [(1, 1), (1, 20), (2, 17), (3, 28), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
            1998: [(1, 1), (1, 19), (2, 16), (4, 10), (5, 25), (7, 3), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)],
            1999: [(1, 1), (1, 18), (2, 15), (4, 2), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25), (12, 24)],
            2000: [(1, 17), (2, 21), (4, 21), (5, 29), (7, 4), (9, 4), (10, 9), (11, 23), (12, 25)],
            2001: [(1, 1), (1, 15), (2, 19), (4, 13), (5, 28), (7, 4), (9, 3), (10, 8), (11, 12), (11, 22), (12, 25)],
            2002: [(1, 1), (1, 21), (2, 18), (3, 29), (5, 27), (7, 4), (9, 2), (10, 14), (11, 11), (11, 28), (12, 25)],
            2003: [(1, 1), (1, 20), (2, 17), (4, 18), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
            2004: [(1, 1), (1, 19), (2, 16), (4, 9), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25), (12, 24)],
            2005: [(1, 17), (2, 21), (3, 25), (5, 30), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24), (12, 26)],
            2006: [(1, 2), (1, 16), (2, 20), (4, 14), (5, 29), (7, 4), (9, 4), (10, 9), (11, 23), (12, 25)],
            2007: [(1, 1), (1, 15), (2, 19), (4, 6), (5, 28), (7, 4), (9, 3), (10, 8), (11, 12), (11, 22), (12, 25)],
            2008: [(1, 1), (1, 21), (2, 18), (3, 21), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
            2009: [(1, 1), (1, 19), (2, 16), (4, 10), (5, 25), (7, 3), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)],
            2010: [(1, 1), (1, 18), (2, 15), (4, 2), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25), (12, 24)],
            2011: [(1, 17), (2, 21), (4, 22), (5, 30), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24), (12, 26)],
            2012: [(1, 2), (1, 16), (2, 20), (4, 6), (5, 28), (7, 4), (9, 3), (10, 8), (10, 30), (11, 12), (11, 22),
                   (12, 25)],
            2013: [(1, 1), (1, 21), (2, 18), (3, 29), (5, 27), (7, 4), (9, 2), (10, 14), (11, 11), (11, 28), (12, 25)],
            2014: [(1, 1), (1, 20), (2, 17), (4, 18), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
            2015: [(1, 1), (1, 19), (2, 16), (4, 3), (5, 25), (7, 3), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)]}

        self.nyfd = {2003: [(1, 1), (1, 20), (2, 17), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
                     2004: [(1, 1), (1, 19), (2, 16), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25)],
                     2005: [(1, 17), (2, 21), (5, 30), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24), (12, 26)],
                     2006: [(1, 2), (1, 16), (2, 20), (5, 29), (7, 4), (9, 4), (10, 9), (11, 23), (12, 25)],
                     2007: [(1, 1), (1, 15), (2, 19), (5, 28), (7, 4), (9, 3), (10, 8), (11, 12), (11, 22), (12, 25)],
                     2008: [(1, 1), (1, 21), (2, 18), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
                     2009: [(1, 1), (1, 19), (2, 16), (5, 25), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)],
                     2010: [(1, 1), (1, 18), (2, 15), (5, 31), (7, 5), (9, 6), (10, 11), (11, 11), (11, 25)],
                     2011: [(1, 17), (2, 21), (5, 30), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24), (12, 26)],
                     2012: [(1, 2), (1, 16), (2, 20), (5, 28), (7, 4), (9, 3), (10, 8), (11, 12), (11, 22), (12, 25)],
                     2013: [(1, 1), (1, 21), (2, 18), (5, 27), (7, 4), (9, 2), (10, 14), (11, 11), (11, 28), (12, 25)],
                     2014: [(1, 1), (1, 20), (2, 17), (5, 26), (7, 4), (9, 1), (10, 13), (11, 11), (11, 27), (12, 25)],
                     2015: [(1, 1), (1, 19), (2, 16), (5, 25), (9, 7), (10, 12), (11, 11), (11, 26), (12, 25)],
                     2016: [(1, 1), (1, 18), (2, 15), (5, 30), (7, 4), (9, 5), (10, 10), (11, 11), (11, 24), (12, 26)],
                     2017: [(1, 2), (1, 16), (2, 20), (5, 29), (7, 4), (9, 4), (10, 9), (11, 23), (12, 25)],
                     2018: [(1, 1), (1, 15), (2, 19), (5, 28), (7, 4), (9, 3), (10, 8), (11, 12), (11, 22), (12, 25)]}

        self.nyse = {2008: [(1, 1), (1, 21), (2, 18), (3, 21), (5, 26), (7, 4), (9, 1), (11, 27), (12, 25)],
                     2009: [(1, 1), (1, 19), (2, 16), (4, 10), (5, 25), (7, 3), (9, 7), (11, 26), (12, 25)],
                     2010: [(1, 1), (1, 18), (2, 15), (4, 2), (5, 31), (7, 5), (9, 6), (11, 25), (12, 24)],
                     2011: [(1, 1), (1, 17), (2, 21), (4, 22), (5, 30), (7, 4), (9, 5), (11, 24), (12, 26)],
                     2012: [(1, 2), (1, 16), (2, 20), (4, 6), (5, 28), (7, 4), (9, 3), (10, 30), (11, 22), (12, 25)],
                     2013: [(1, 1), (1, 21), (2, 18), (3, 29), (5, 27), (7, 4), (9, 2), (11, 28), (12, 25)],
                     2014: [(1, 1), (1, 20), (2, 17), (4, 18), (5, 26), (7, 4), (9, 1), (11, 27), (12, 25)],
                     2015: [(1, 1), (1, 19), (2, 16), (4, 3), (5, 25), (7, 3), (9, 7), (11, 26), (12, 25)]}

    def data(self):
        hl = getattr(self, self._type.name.lower())
        return hl


def test_cal(ct):
    data = CalData(ct).data()
    cal = HolidayCalendar(ct)

    offset = relativedelta(days=1)
    for yr in data:
        hl = {datetime.datetime(yr, x[0], x[1]) for x in data[yr]}
        dt = datetime.datetime(yr, 1, 1)

        assert cal.is_holiday(dt) != cal.is_weekday(dt)
        if cal.is_holiday(dt):
            assert dt in hl or dt.weekday() in (5, 6)
        else:
            assert dt not in hl

        dt += offset


def test_default_calendars():
    cal_types = [HolidayCalendarType.USNY, HolidayCalendarType.USGS, HolidayCalendarType.NYFD, HolidayCalendarType.NYSE]
    for ct in cal_types:
        test_cal(ct)


if __name__ == '__main__':
    test_default_calendars()
