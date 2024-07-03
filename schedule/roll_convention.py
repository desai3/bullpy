import enum
import datetime
import calendar

from .calendars import day_of_week_in_month, CombinedHolidayCalendar,HolidayCalendarType, HolidayCalendar
from .frequency import plus_days, plus_months, Frequency


class RollConventionType(enum.Enum):
    NONE = enum.auto()
    EOM = enum.auto()
    IMM = enum.auto()
    IMMCAD = enum.auto()
    IMMAUD = enum.auto()
    IMMNZD = enum.auto()
    SFE = enum.auto()
    TBILL = enum.auto()

    DAY_1 = enum.auto()
    DAY_2 = enum.auto()
    DAY_3 = enum.auto()
    DAY_4 = enum.auto()
    DAY_5 = enum.auto()
    DAY_6 = enum.auto()
    DAY_7 = enum.auto()
    DAY_8 = enum.auto()
    DAY_9 = enum.auto()
    DAY_10 = enum.auto()
    DAY_11 = enum.auto()
    DAY_12 = enum.auto()
    DAY_13 = enum.auto()
    DAY_14 = enum.auto()
    DAY_15 = enum.auto()
    DAY_16 = enum.auto()
    DAY_17 = enum.auto()
    DAY_18 = enum.auto()
    DAY_19 = enum.auto()
    DAY_20 = enum.auto()
    DAY_21 = enum.auto()
    DAY_22 = enum.auto()
    DAY_23 = enum.auto()
    DAY_24 = enum.auto()
    DAY_25 = enum.auto()
    DAY_26 = enum.auto()
    DAY_27 = enum.auto()
    DAY_28 = enum.auto()
    DAY_29 = enum.auto()
    DAY_30 = enum.auto()
    DAY_31 = enum.auto()

    WEEKDAY_MON = enum.auto()
    WEEKDAY_TUE = enum.auto()
    WEEKDAY_WED = enum.auto()
    WEEKDAY_THU = enum.auto()
    WEEKDAY_FRI = enum.auto()
    WEEKDAY_SAT = enum.auto()
    WEEKDAY_SUN = enum.auto()


class RollConvention(object):
    def __init__(self, name: RollConventionType):
        self.name = name

        if self.name in (RollConventionType.IMMCAD, RollConventionType.IMMAUD, RollConventionType.TBILL):
            getattr(self, f'setup_{self.name.name.lower()}')()

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def matches(self, dt: datetime) -> bool:
        # if self.name.name.startswith('DAY_') and self.name != RollConventionType.DAY_31:
        #     day = int(self.name.name.split('_')[-1])
        #     return dt.day == day or \
        #         (dt.month == 2 and day >= calendar.monthrange(dt.year, dt.month)[1] and
        #          dt.day == calendar.monthrange(dt.year, dt.month)[1])
        # elif self.name.name.startswith('WEEKDAY_'):
        #     day = self.name.name.split('_')[-1]
        #     return dt.weekday() == {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}[day]
        return self.adjust(dt) == dt

    def adjust(self, dt: datetime) -> datetime:
        if self.name == RollConventionType.DAY_31:
            return self.adjust_eom(dt)
        elif self.name.name.startswith('DAY_'):
            day = int(self.name.name.split('_')[-1])
            if day >= 29 and dt.month == 2:
                return datetime.datetime(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])
            return datetime.datetime(dt.year, dt.month, day)
        elif self.name.name.startswith('WEEKDAY_'):
            day = self.name.name.split('_')[-1]
            day = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}[day]
            cur = dt
            while cur.weekday() != day:
                # cur += relativedelta(days=1)
                cur = plus_days(cur, 1)
            return cur
        else:
            return getattr(self, f'adjust_{self.name.name.lower()}')(dt)

    def next(self, dt: datetime, delta: Frequency) -> datetime:
        if self.name.name.startswith('WEEKDAY_'):
            # calculated = dt + delta
            calculated = delta.add_to_date(dt)
            dct = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}
            day = dct[self.name.name.split('_')[-1]]
            while calculated.weekday() != day:
                # calculated += relativedelta(days=1)
                calculated = plus_days(calculated, 1)
            return calculated
        else:
            calculated = self.adjust(delta.add_to_date(dt))
            if calculated <= dt:
                calculated = self.adjust(plus_months(dt, 1))
            return calculated

    def previous(self, dt: datetime, delta: Frequency) -> datetime:
        if self.name.name.startswith('WEEKDAY_'):
            # calculated = dt - delta
            calculated = delta.sub_from_date(dt)
            dct = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}
            day = dct[self.name.name.split('_')[-1]]
            while calculated.weekday() != day:
                # calculated -= relativedelta(days=1)
                calculated = plus_days(calculated, -1)
            return calculated
        else:
            calculated = self.adjust(delta.sub_from_date(dt))
            if calculated >= dt:
                # calculated = self.adjust(dt - relativedelta(months=1))
                calculated = self.adjust(plus_months(dt, -1))
            return calculated

    def adjust_none(self, dt: datetime) -> datetime:
        return dt

    def adjust_eom(self, dt: datetime) -> datetime:
        return datetime.datetime(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])

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

    def adjust_immnzd(self, dt: datetime) -> datetime:
        cur = datetime.datetime(dt.year, dt.month, 9)
        while cur.weekday() != 2:
            # cur += relativedelta(days=1)
            cur = plus_days(cur, 1)
        return cur

    def adjust_sfe(self, dt: datetime) -> datetime:
        return day_of_week_in_month(dt.year, dt.month, 4, 2)

    def setup_tbill(self):
        self.usny = HolidayCalendar(HolidayCalendarType.USNY)

    def adjust_tbill(self, dt: datetime) -> datetime:
        cur = dt
        while cur.weekday() != 0:
            # cur += relativedelta(days=1)
            cur = plus_days(cur, 1)
        return self.usny.next_or_same(cur)