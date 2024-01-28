import datetime

from dateutil.relativedelta import relativedelta

from calendars import HolidayCalendar, HolidayCalendarType, CustomeHolidayCalendar


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

        self.gblo = {
            # Whitsun, Last Mon Aug - http://hansard.millbanksystems.com/commons/1964/mar/04/staggered-holidays
            1965: [(4, 16), (4, 19), (6, 7), (8, 30), (12, 27), (12, 28)],
            # Whitsun May - http://hansard.millbanksystems.com/commons/1964/mar/04/staggered-holidays
            # 29th Aug - http://hansard.millbanksystems.com/written_answers/1965/nov/25/august-bank-holiday
            1966: [(4, 8), (4, 11), (5, 30), (8, 29), (12, 26), (12, 27)],
            # 29th May, 28th Aug - http://hansard.millbanksystems.com/written_answers/1965/jun/03/bank-holidays-1967-and-1968
            1967: [(3, 24), (3, 27), (5, 29), (8, 28), (12, 25), (12, 26)],
            # 3rd Jun, 2nd Sep - http://hansard.millbanksystems.com/written_answers/1965/jun/03/bank-holidays-1967-and-1968
            1968: [(4, 12), (4, 15), (6, 3), (9, 2), (12, 25), (12, 26)],
            # 26th May, 1st Sep - http://hansard.millbanksystems.com/written_answers/1967/mar/21/bank-holidays-1969-dates
            1969: [(4, 4), (4, 7), (5, 26), (9, 1), (12, 25), (12, 26)],
            # 25th May, 31st Aug - http://hansard.millbanksystems.com/written_answers/1967/jul/28/bank-holidays
            1970: [(3, 27), (3, 30), (5, 25), (8, 31), (12, 25), (12, 28)],
            # applying rules
            1971: [(4, 9), (4, 12), (5, 31), (8, 30), (12, 27), (12, 28)],
            2009: [(1, 1), (4, 10), (4, 13), (5, 4), (5, 25), (8, 31), (12, 25), (12, 28)],
            2010: [(1, 1), (4, 2), (4, 5), (5, 3), (5, 31), (8, 30), (12, 27), (12, 28)],
            # https://www.gov.uk/bank-holidays
            2012: [(1, 2), (4, 6), (4, 9), (5, 7), (6, 4), (6, 5), (8, 27), (12, 25), (12, 26)],
            2013: [(1, 1), (3, 29), (4, 1), (5, 6), (5, 27), (8, 26), (12, 25), (12, 26)],
            2014: [(1, 1), (4, 18), (4, 21), (5, 5), (5, 26), (8, 25), (12, 25), (12, 26)],
            2015: [(1, 1), (4, 3), (4, 6), (5, 4), (5, 25), (8, 31), (12, 25), (12, 28)],
            2016: [(1, 1), (3, 25), (3, 28), (5, 2), (5, 30), (8, 29), (12, 26), (12, 27)],
            2020: [(1, 1), (4, 10), (4, 13), (5, 8), (5, 25), (8, 31), (12, 25), (12, 28)],
            2022: [(1, 3), (4, 15), (4, 18), (5, 2), (6, 2), (6, 3), (8, 29), (9, 19), (12, 26), (12, 27)],
            2023: [(1, 2), (4, 7), (4, 10), (5, 1), (5, 8), (5, 29), (8, 28), (12, 25), (12, 26)]}

        self.euta = {  # 1997 - 1998(testing phase), Jan 1, christmas day
            1997: [(1, 1), (12, 25)],
            1998: [(1, 1), (12, 25)],
            # in 1999, Jan 1, christmas day, Dec 26, Dec 31
            1999: [(1, 1), (12, 25), (12, 31)],
            # in 2000, Jan 1, good friday, easter monday, May 1, christmas day, Dec 26
            2000: [(1, 1), (4, 21), (4, 24), (5, 1), (12, 25), (12, 26)],
            # in 2001, Jan 1, good friday, easter monday, May 1, christmas day, Dec 26, Dec 31
            2001: [(1, 1), (4, 13), (4, 16), (5, 1), (12, 25), (12, 26), (12, 31)],
            # from 2002, Jan 1, good friday, easter monday, May 1, christmas day, Dec 26
            2002: [(1, 1), (3, 29), (4, 1), (5, 1), (12, 25), (12, 26)],
            2003: [(1, 1), (4, 18), (4, 21), (5, 1), (12, 25), (12, 26)],
            # http: // www.ecb.europa.eu / home / html / holidays.en.html
            2014: [(1, 1), (4, 18), (4, 21), (5, 1), (12, 25), (12, 26)],
            2015: [(1, 1), (4, 3), (4, 6), (5, 1), (12, 25), (12, 26)]}

        self.ausy = {
            2012: [(1, 1), (1, 2), (1, 26), (4, 6), (4, 7), (4, 8), (4, 9), (4, 25), (6, 11), (8, 6), (10, 1), (12, 25),
                   (12, 26)],
            2013: [(1, 1), (1, 26), (1, 28), (3, 29), (3, 30), (3, 31), (4, 1), (4, 25), (6, 10), (8, 5), (10, 7),
                   (12, 25), (12, 26)],
            2014: [(1, 1), (1, 26), (1, 27), (4, 18), (4, 19), (4, 20), (4, 21), (4, 25), (6, 9), (8, 4), (10, 6),
                   (12, 25), (12, 26)],
            2015: [(1, 1), (1, 26), (4, 3), (4, 4), (4, 5), (4, 6), (4, 25), (6, 8), (8, 3), (10, 5), (12, 25),
                   (12, 26), (12, 27), (12, 28)],
            2016: [(1, 1), (1, 26), (3, 25), (3, 26), (3, 27), (3, 28), (4, 25), (6, 13), (8, 1), (10, 3), (12, 25),
                   (12, 26), (12, 27)],
            2017: [(1, 1), (1, 2), (1, 26), (4, 14), (4, 15), (4, 16), (4, 17), (4, 25), (6, 12), (8, 7), (10, 2),
                   (12, 25), (12, 26)],
            2022: [(1, 3), (1, 26), (4, 15), (4, 18), (4, 25), (6, 13), (8, 1), (9, 22), (10, 3), (12, 26), (12, 27)]}

        self.camo = {2017: [(1, 2), (4, 14), (5, 22), (6, 26), (7, 3), (9, 4), (10, 9), (12, 25)],
                     2018: [(1, 1), (3, 30), (5, 21), (6, 25), (7, 2), (9, 3), (10, 8), (12, 25)],
                     2022: [(1, 3), (4, 15), (5, 23), (6, 24), (7, 1), (9, 5), (10, 10), (12, 26)]}

        self.cato = {
            2009: [(1, 1), (2, 16), (4, 10), (5, 18), (7, 1), (8, 3), (9, 7), (10, 12), (11, 11), (12, 25), (12, 28)],
            2010: [(1, 1), (2, 15), (4, 2), (5, 24), (7, 1), (8, 2), (9, 6), (10, 11), (11, 11), (12, 27), (12, 28)],
            2011: [(1, 3), (2, 21), (4, 22), (5, 23), (7, 1), (8, 1), (9, 5), (10, 10), (11, 11), (12, 26), (12, 27)],
            2012: [(1, 2), (2, 20), (4, 6), (5, 21), (7, 2), (8, 6), (9, 3), (10, 8), (11, 12), (12, 25), (12, 26)],
            2013: [(1, 1), (2, 18), (3, 29), (5, 20), (7, 1), (8, 5), (9, 2), (10, 14), (11, 11), (12, 25), (12, 26)],
            2014: [(1, 1), (2, 17), (4, 18), (5, 19), (7, 1), (8, 4), (9, 1), (10, 13), (11, 11), (12, 25), (12, 26)],
            2015: [(1, 1), (2, 16), (4, 3), (5, 18), (7, 1), (8, 3), (9, 7), (10, 12), (11, 11), (12, 25), (12, 28)],
            2016: [(1, 1), (2, 15), (3, 25), (5, 23), (7, 1), (8, 1), (9, 5), (10, 10), (11, 11), (12, 26), (12, 27)]}

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

        assert cal.is_holiday(dt) != cal.is_businessday(dt)
        if cal.is_holiday(dt):
            assert dt in hl or dt.weekday() in (5, 6)
        else:
            assert dt not in hl

        dt += offset


def test_default_calendars():
    cal_types = [HolidayCalendarType.USNY, HolidayCalendarType.USGS, HolidayCalendarType.NYFD, HolidayCalendarType.NYSE,
                 HolidayCalendarType.GBLO, HolidayCalendarType.EUTA, HolidayCalendarType.AUSY]
    for ct in cal_types:
        test_cal(ct)


def test_next():
    data = [[datetime.datetime(2014, 7, 10), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 11), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 12), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 13), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 14), datetime.datetime(2014, 7, 15)],
            [datetime.datetime(2014, 7, 15), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 17), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 19), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 20), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 21), datetime.datetime(2014, 7, 22)]]

    dts = set([datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 31)])
    custom_cal = CustomeHolidayCalendar('test', dts)

    for d1, d2 in data:
        assert custom_cal.next(d1) == d2


def test_next_or_same():
    data = [[datetime.datetime(2014, 7, 10), datetime.datetime(2014, 7, 10)],
            [datetime.datetime(2014, 7, 11), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 12), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 13), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 14), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 15), datetime.datetime(2014, 7, 15)],
            [datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 17), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 19), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 20), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 21), datetime.datetime(2014, 7, 21)]]

    dts = set([datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 31)])
    custom_cal = CustomeHolidayCalendar('test', dts)

    for d1, d2 in data:
        assert custom_cal.next_or_same(d1) == d2


def test_previous():
    data = [[datetime.datetime(2014, 7, 11), datetime.datetime(2014, 7, 10)],
            [datetime.datetime(2014, 7, 12), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 13), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 14), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 15), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 15)],
            [datetime.datetime(2014, 7, 17), datetime.datetime(2014, 7, 15)],
            [datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 19), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 20), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 21), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 22), datetime.datetime(2014, 7, 21)]]

    dts = set([datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 31)])
    custom_cal = CustomeHolidayCalendar('test', dts)

    for d1, d2 in data:
        assert custom_cal.previous(d1) == d2


def test_previous_or_same():
    data = [[datetime.datetime(2014, 7, 11), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 12), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 13), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 14), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 15), datetime.datetime(2014, 7, 15)],
            [datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 15)],
            [datetime.datetime(2014, 7, 17), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 19), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 20), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 21), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 22), datetime.datetime(2014, 7, 22)]]

    dts = set([datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 31)])
    custom_cal = CustomeHolidayCalendar('test', dts)

    for d1, d2 in data:
        assert custom_cal.previous_or_same(d1) == d2


def test_next_or_same_last_in_month():
    data = [[datetime.datetime(2014, 7, 10), datetime.datetime(2014, 7, 10)],
            [datetime.datetime(2014, 7, 11), datetime.datetime(2014, 7, 11)],
            [datetime.datetime(2014, 7, 12), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 13), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 14), datetime.datetime(2014, 7, 14)],
            [datetime.datetime(2014, 7, 15), datetime.datetime(2014, 7, 15)],
            [datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 17), datetime.datetime(2014, 7, 17)],
            [datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 19), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 20), datetime.datetime(2014, 7, 21)],
            [datetime.datetime(2014, 7, 21), datetime.datetime(2014, 7, 21)],

            [datetime.datetime(2014, 7, 31), datetime.datetime(2014, 7, 30)]]

    dts = set([datetime.datetime(2014, 7, 16), datetime.datetime(2014, 7, 18), datetime.datetime(2014, 7, 31)])
    custom_cal = CustomeHolidayCalendar('test', dts)

    for d1, d2 in data:
        assert custom_cal.next_or_same_last_in_month(d1) == d2


if __name__ == '__main__':
    test_default_calendars()
