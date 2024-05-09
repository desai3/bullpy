import calendar
import enum
import datetime

from .frequency import plus_days, Frequency, get_proleptic_month
from .roll_convention import RollConvention, RollConventionType


class StubConventionType(enum.Enum):
    NONE = enum.auto()

    SHORT_INITIAL = enum.auto()
    LONG_INITIAL = enum.auto()
    SMART_INITIAL = enum.auto()

    SHORT_FINAL = enum.auto()
    LONG_FINAL = enum.auto()
    SMART_FINAL = enum.auto()

    BOTH = enum.auto()


class StubConvention(object):
    def __init__(self, stub_conv_type: StubConventionType):
        self._type = stub_conv_type.name
        self.to_implicit = getattr(self, f"_{self._type.lower()}_to_implicit")
        self.is_stub_long = getattr(self, f"_{self._type.lower()}_is_stub_long")

    def _none_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if explicit_initial_stub or explicit_final_stub:
            raise ValueError("Dates specify an explicit stub, but stub convention is NONE")
        return StubConvention(StubConventionType.NONE)

    def _none_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return False

    def _short_initial_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if explicit_final_stub:
            raise ValueError('Dates specifiy an explicit final stub, but stub convention is SHORT_INITIAL')

        if explicit_initial_stub:
            return StubConvention(StubConventionType.NONE)
        else:
            return StubConvention(StubConventionType.SHORT_INITIAL)

    def _short_initial_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return False

    def _long_initial_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if explicit_final_stub:
            raise ValueError('Dates specifiy an explicit final stub, but stub convention is LONG_INITIAL')

        if explicit_initial_stub:
            return StubConvention(StubConventionType.NONE)
        else:
            return StubConvention(StubConventionType.LONG_INITIAL)

    def _long_initial_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return True

    def _smart_initial_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if explicit_final_stub:
            if explicit_initial_stub:
                return StubConvention(StubConventionType.BOTH)
            else:
                return StubConvention(StubConventionType.SMART_INITIAL)
        else:
            if explicit_initial_stub:
                return StubConvention(StubConventionType.NONE)
            else:
                return StubConvention(StubConventionType.SMART_INITIAL)

    def _smart_initial_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return plus_days(dt1, 7) > dt2

    def _short_final_to_implicit(self, explicity_initial_stub: bool, explicit_final_stub: bool):
        if explicity_initial_stub:
            raise ValueError("Dates specify an explicit initial stub, but stub convention is SHORT_FINAL")
        if explicit_final_stub:
            return StubConvention(StubConventionType.NONE)
        else:
            return StubConvention(StubConventionType.SHORT_FINAL)

    def _short_final_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return False

    def _long_final_to_implicit(self, explicity_initial_stub: bool, explicit_final_stub: bool):
        if explicity_initial_stub:
            raise ValueError("Dates specify an explicit initial stub, but stub convention is LONG_FINAL")
        if explicit_final_stub:
            return StubConvention(StubConventionType.NONE)
        else:
            return StubConvention(StubConventionType.LONG_FINAL)

    def _long_final_is_stub_long(self, dt1: datetime, dt2: datetime):
        return True

    def _smart_final_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if explicit_initial_stub:
            if explicit_final_stub:
                return StubConvention(StubConventionType.BOTH)
            else:
                return StubConvention(StubConventionType.SMART_FINAL)
        else:
            if explicit_final_stub:
                return StubConvention(StubConventionType.NONE)
            else:
                return StubConvention(StubConventionType.SMART_FINAL)

    def _smart_final_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return plus_days(dt1, 7) > dt2

    def _both_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if not (explicit_initial_stub and explicit_final_stub):
            raise ValueError("Stub convention is BOTH but explicit dates not specified")
        return StubConvention(StubConventionType.NONE)

    def _both_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return False

    def is_smart(self):
        return self._type == StubConventionType.SMART_INITIAL.name or self._type == StubConventionType.SMART_FINAL.name

    def is_short(self):
        return self._type == StubConventionType.SHORT_INITIAL.name or self._type == StubConventionType.SHORT_FINAL.name

    def is_long(self):
        return self._type == StubConventionType.LONG_INITIAL.name or self._type == StubConventionType.LONG_FINAL.name

    def is_final(self):
        return self._type == StubConventionType.SHORT_FINAL.name or \
            self._type == StubConventionType.LONG_FINAL.name or \
            self._type == StubConventionType.SMART_FINAL.name

    def is_calculate_forwards(self):
        return self._type == StubConventionType.SHORT_FINAL.name or \
            self._type == StubConventionType.LONG_FINAL.name or \
            self._type == StubConventionType.SMART_FINAL.name or \
            self._type == StubConventionType.NONE.name

    def is_calculate_backwards(self):
        return self._type == StubConventionType.SHORT_INITIAL.name or \
            self._type == StubConventionType.LONG_INITIAL.name or \
            self._type == StubConventionType.SMART_INITIAL.name

    @staticmethod
    def implied_roll_convention(dt1: datetime, dt2: datetime, freq: Frequency, eom: bool) -> RollConvention:
        if freq.is_month_based():
            if eom and dt1.day == calendar.monthrange(dt1.year, dt1.month)[1]:
                return RollConvention(RollConventionType.EOM)
            return RollConvention(getattr(RollConventionType, f'DAY_{dt1.day}'))
        elif freq.is_week_based():
            day = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'}[dt1.weekday()]
            return RollConvention(getattr(RollConventionType, f'WEEKDAY_{day}'))
        else:
            return RollConvention(RollConventionType.NONE)

    def to_roll_convention(self, start: datetime, end: datetime, freq: Frequency, eom: bool) -> RollConvention:
        assert start is not None, 'Start date cannot be None'
        assert end is not None, 'End date cannot be None'
        assert freq is not None, 'Frequency cannot be None'
        if self._type == RollConventionType.NONE.name and freq.is_month_based():
            if (start.day != end.day and
                    (get_proleptic_month(start) != get_proleptic_month(end)) and
                    (start.day == calendar.monthrange(start.year, start.month)[1] or
                     end.day == calendar.monthrange(end.year, end.month)[1])):
                if eom:
                    return RollConvention(RollConventionType.EOM)
                else:
                    return RollConvention(getattr(RollConventionType, f"DAY_{max(start.day, end.day)}"))
        if self.is_calculate_backwards():
            return self.implied_roll_convention(end, start, freq, eom)
        else:
            return self.implied_roll_convention(start, end, freq, eom)

    def __eq__(self, o):
        return isinstance(o, type(self)) and o._type == self._type
