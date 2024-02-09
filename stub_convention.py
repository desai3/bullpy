import enum


class StubConventionType(enum.Enum):
    NONE = enum.auto()

    SHORT_INITIAL = enum.auto()
    LONG_INITIAL = enum.auto()
    SMART_INITIAL = enum.auto()

    SHORT_FINAL = enum.auto()
    LONG_FINAL = enum.auto()
    SMART_FINAL = enum.auto()

    BOTH = enum.auto()
