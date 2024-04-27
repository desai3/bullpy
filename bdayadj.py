import enum
import datetime

from calendars import HolidayCalendar


class BDayAdjType(enum.Enum):
    NO_ADJUST = enum.auto()
    FOLLOWING = enum.auto()
    MODIFIED_FOLLOWING = enum.auto()
    MODIFIED_FOLLOWING_BI_MONTHLY = enum.auto()
    PRECEDING = enum.auto()
    MODIFIED_PRECEDING = enum.auto()
    NEAREST = enum.auto()


class BDayAdj(object):
    def __init__(self, adj_type: BDayAdjType):
        self.adj_type = adj_type

    def adjust(self, dt: datetime, calendar: HolidayCalendar) -> datetime:
        return getattr(self, f'adjust_{self.adj_type.name.lower()}')(dt, calendar)

    @staticmethod
    def adjust_no_adjust(dt: datetime, calendar: HolidayCalendar) -> datetime:
        assert isinstance(dt, datetime.datetime)
        return dt

    @staticmethod
    def adjust_following(dt: datetime, calendar: HolidayCalendar) -> datetime:
        return calendar.next_or_same(dt)

    @staticmethod
    def adjust_modified_following(dt: datetime, calendar: HolidayCalendar) -> datetime:
        return calendar.next_or_same_last_in_month(dt)

    @staticmethod
    def adjust_modified_following_bi_monthly(dt: datetime, calendar: HolidayCalendar) -> datetime:
        adjusted = calendar.next_or_same(dt)
        if adjusted.month != dt.month or (adjusted.day > 15 and dt.day <= 15):
            adjusted = calendar.previous(adjusted)
        return adjusted

    @staticmethod
    def adjust_preceding(dt: datetime, calendar: HolidayCalendar) -> datetime:
        return calendar.previous_or_same(dt)

    @staticmethod
    def adjust_modified_preceding(dt: datetime, calendar: HolidayCalendar) -> datetime:
        adjusted = calendar.previous_or_same(dt)
        if adjusted.month != dt.month:
            adjusted = calendar.next(dt)
        return adjusted

    @staticmethod
    def adjust_nearest(dt: datetime, calendar: HolidayCalendar) -> datetime:
        if calendar.is_businessday(dt):
            return dt
        if dt.weekday() == 6 or dt.weekday() == 0:
            return calendar.next(dt)
        else:
            return calendar.previous(dt)
