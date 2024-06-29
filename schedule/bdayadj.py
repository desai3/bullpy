import enum
import datetime

from .calendars import HolidayCalendar


class BDayAdjType(enum.Enum):
    NO_ADJUST = enum.auto()
    FOLLOWING = enum.auto()
    MODIFIED_FOLLOWING = enum.auto()
    MODIFIED_FOLLOWING_BI_MONTHLY = enum.auto()
    PRECEDING = enum.auto()
    MODIFIED_PRECEDING = enum.auto()
    NEAREST = enum.auto()


class BDayAdj(object):
    def __init__(self, adj_type: BDayAdjType, cal: HolidayCalendar | None = None):
        self.adj_type = adj_type
        self.cal = cal

    def __eq__(self, other):
        return self.adj_type == other.adj_type and self.cal == other.cal

    def adjust(self, dt: datetime, cal=HolidayCalendar | None) -> datetime:
        return getattr(self, f'adjust_{self.adj_type.name.lower()}')(dt, cal)

    @staticmethod
    def adjust_no_adjust(dt: datetime, cal=HolidayCalendar | None) -> datetime:
        assert isinstance(dt, datetime.datetime)
        return dt

    def adjust_following(self, dt: datetime, cal=HolidayCalendar | None) -> datetime:
        return self.cal.next_or_same(dt)

    def adjust_modified_following(self, dt: datetime, cal=HolidayCalendar | None) -> datetime:
        return self.cal.next_or_same_last_in_month(dt)

    def adjust_modified_following_bi_monthly(self, dt: datetime, cal=HolidayCalendar | None) -> datetime:
        adjusted = self.cal.next_or_same(dt)
        if adjusted.month != dt.month or (adjusted.day > 15 and dt.day <= 15):
            adjusted = self.cal.previous(adjusted)
        return adjusted

    def adjust_preceding(self, dt: datetime, cal=HolidayCalendar | None) -> datetime:
        return self.cal.previous_or_same(dt)

    def adjust_modified_preceding(self, dt: datetime, cal=HolidayCalendar | None) -> datetime:
        adjusted = self.cal.previous_or_same(dt)
        if adjusted.month != dt.month:
            adjusted = self.cal.next(dt)
        return adjusted

    def adjust_nearest(self, dt: datetime, cal=HolidayCalendar | None) -> datetime:
        if self.cal.is_businessday(dt):
            return dt
        if dt.weekday() == 6 or dt.weekday() == 0:
            return self.cal.next(dt)
        else:
            return self.cal.previous(dt)
