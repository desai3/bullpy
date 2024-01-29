import enum
import datetime
import calendar

from dateutil.relativedelta import relativedelta

from .calendars import day_of_week_in_month, CombinedHolidayCalendar,HolidayCalendarType, HolidayCalendar


class RollConventionType(enum.Enum):
    NONE = enum.auto()
    EOM = enum.auto()
    IMM = enum.auto()
    IMMCAD = enum.auto()
    IMMAUD = enum.auto()
    IMMNZD = enum.auto()
    SFE = enum.auto()
    TBILL = enum.auto()


class RolleConvention(object):
    def __init__(self, name: RollConventionType):
        self.name = RollConventionType.name
        getattr(self, f'setup_{self.name}')()

    def adjust(self, dt: datetime) -> datetime:
        return getattr(self, 'adjust_{self.name}')(dt)

    def setup_none(self):
        pass

    def adjust_none(self, dt: datetime) -> datetime:
        return dt

    def setup_none(self):
        pass

    def adjust_eom(self, dt: datetime) -> datetime:
        return datetime.datetime(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])

    def setup_imm(self):
        pass

    def adjust_imm(self, dt: datetime) -> datetime:
        return day_of_week_in_month(dt.year, dt.month, 2, 3)

    def setup_immcad(self):
        self.gblo = HolidayCalendar(HolidayCalendarType.GBLO)
        self.canada = CombinedHolidayCalendar([HolidayCalendarType.CATO, HolidayCalendarType.CAMO])

    def adjust_immcad(self, dt: datetime) -> datetime:
        wed3 = day_of_week_in_month(dt.year, dt.month, 2, 3)
        return self.canada.previous_or_same(self.gblo.shift(wed3, -2))

    def setup_immaud(self):
        self.ausy = HolidayCalendar(HolidayCalendarType.AUSY)

    def adjust_immaud(self, dt: datetime) -> datetime:
        return self.ausy.previous(day_of_week_in_month(dt.year, dt.month, 4, 2))

    def setup_immazd(self):
        pass

    def adjust_immmnzd(self, dt: datetime) -> datetime:
        cur = datetime.datetime(dt.year, dt.month, 9)
        while cur.weekday() != 2:
            cur += relativedelta(days=1)
        return cur

    def setup_sfe(self):
        pass

    def adjust_sfe(self, dt: datetime) -> datetime:
        return day_of_week_in_month(dt.year, dt.month, 4, 2)

    def setup_tbill(self):
        self.usny = HolidayCalendar(HolidayCalendarType.USNY)

    def adjust_tbill(self, dt: datetime) -> datetime:
        cur = dt
        while cur.weekday() != 0:
            cur += relativedelta(days=1)
        return self.usny.next_or_same(cur)