import datetime

import pytest

from ...schedule.schedule_period import SchedulePeriod
from ...schedule.daycount import DayCount, DayCountType
from ...schedule.frequency import between, Frequency
from ...schedule.roll_convention import RollConvention, RollConventionType

JUN_15 = datetime.datetime(2014, 6, 15)
JUN_16 = datetime.datetime(2014, 6, 16)
JUN_17 = datetime.datetime(2014, 6, 17)
JUN_18 = datetime.datetime(2014, 6, 18)
JUL_04 = datetime.datetime(2014, 7, 4)
JUL_05 = datetime.datetime(2014, 7, 5)
JUL_17 = datetime.datetime(2014, 7, 17)
JUL_18 = datetime.datetime(2014, 7, 18)
AUG_17 = datetime.datetime(2014, 8, 17)
AUG_18 = datetime.datetime(2014, 8, 18)
SEP_17 = datetime.datetime(2014, 9, 17)


def test_null():
    with pytest.raises(ValueError):
        SchedulePeriod(None, JUL_18, JUL_04, JUL_17)
    with pytest.raises(ValueError):
        SchedulePeriod(JUL_05, None, JUL_04, JUL_17)
    with pytest.raises(ValueError):
        SchedulePeriod(JUL_05, JUL_18, None, JUL_17)
    with pytest.raises(ValueError):
        SchedulePeriod(JUL_05, JUL_18, JUL_04, None)
    with pytest.raises(ValueError):
        SchedulePeriod(None, None, None, None)


def test_of_all():
    sp = SchedulePeriod(JUL_05, JUL_18, JUL_04, JUL_17)
    assert sp.get_start_date() == JUL_05
    assert sp.get_end_date() == JUL_18
    assert sp.get_unadjusted_start_date() == JUL_04
    assert sp.get_unadjusted_end_date() == JUL_17


def test_no_unadjsted():
    sp = SchedulePeriod(JUL_05, JUL_18)
    assert sp.get_start_date() == JUL_05
    assert sp.get_end_date() == JUL_18
    assert sp.get_unadjusted_start_date() == JUL_05
    assert sp.get_unadjusted_end_date() == JUL_18


def test_year_fraction():
    sp = SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17)
    dc = DayCount(DayCountType.ACT_360)
    assert abs(sp.year_fraction(dc, None) - dc.year_fraction(JUN_16, JUL_18)) < 1e-8


def test_length():
    assert SchedulePeriod(JUN_16, JUN_18, JUN_16, JUN_18).length() == between(JUN_16, JUN_18)
    assert SchedulePeriod(JUN_16, JUN_18, JUN_16, JUN_17).length() == between(JUN_16, JUN_18)


def test_length_in_days():
    assert SchedulePeriod(JUN_16, JUN_18, JUN_16, JUN_18).length_in_days() == 2
    assert SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17).length_in_days() == 32


def test_is_regular():
    assert SchedulePeriod(JUN_18, JUL_18).is_regular(Frequency(months=1), RollConvention(RollConventionType.DAY_18))
    assert not SchedulePeriod(JUN_18, JUL_05).is_regular(Frequency(months=1), RollConvention(RollConventionType.DAY_18))
    assert not SchedulePeriod(JUL_05, JUL_18).is_regular(Frequency(months=1), RollConvention(RollConventionType.DAY_18))
    assert not SchedulePeriod(JUN_18, JUL_05).is_regular(Frequency(months=2), RollConvention(RollConventionType.DAY_18))


def test_is_regular_null():
    sp = SchedulePeriod(JUN_16, JUL_18)
    with pytest.raises(ValueError):
        sp.is_regular(None, RollConvention(RollConventionType.DAY_18))
    with pytest.raises(ValueError):
        sp.is_regular(Frequency(months=1), None)
    with pytest.raises(ValueError):
        sp.is_regular(None, None)


def test_contains():
    assert not SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17).contains(JUN_15)
    assert SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17).contains(JUN_16)
    assert SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17).contains(JUL_05)
    assert SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17).contains(JUL_17)
    assert not SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17).contains(JUL_18)


def test_contains_null():
    with pytest.raises(ValueError):
        SchedulePeriod(JUN_16, JUL_18).contains(None)


def test_to_adjusted():
    sp = SchedulePeriod(JUN_15, SEP_17)


if __name__ == '__main__':
    test_is_regular()