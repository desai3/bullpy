import enum
import datetime

from frequency import plus_days

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
        self._to_implicit = getattr(self, f"_{self._type.lower()}_to_implicit")
        self._is_stub_long = getattr(self, f"_{self._type.lower()}_is_stub_long")

    def _none_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if explicit_initial_stub or explicit_final_stub:
            raise ValueError("Dates specify an explicit stub, but stub convention is NONE")
        return StubConvention(StubConventionType.NONE)

    def _none_initial_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return False

    def _short_initial_to_implicit(self, explicit_initial_stub: bool , explicit_final_stub: bool):
        if explicit_final_stub:
            raise ValueError('Dates specifiy an explicit final stub, but stub convention is SHORT_INITIAL')

        if explicit_initial_stub:
            return StubConvention(StubConventionType.NONE)
        else:
            return StubConvention(StubConventionType.SHORT_INITIAL)

    def _short_initial_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return False

    def _long_initial_to_implicit(self, explicit_initial_stub: bool , explicit_final_stub: bool):
        if explicit_final_stub:
            raise ValueError('Dates specifiy an explicit final stub, but stub convention is LONG_INITIAL')

        if explicit_initial_stub:
            return StubConvention(StubConventionType.NONE)
        else:
            return StubConvention(StubConventionType.LONG_INITIAL)

    def _long_initial_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return True

    def _smart_initial_to_implicit(self, explicit_initial_stub: bool , explicit_final_stub: bool):
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
        return False

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

    def _both_final_to_implicit(self, explicit_initial_stub: bool, explicit_final_stub: bool):
        if not (explicit_initial_stub and explicit_final_stub):
            raise ValueError("Stub convention is BOTH but explicit dates not specified")
        return StubConvention(StubConventionType.NONE)

    def _both_final_is_stub_long(self, dt1: datetime, dt2: datetime) -> bool:
        return False
