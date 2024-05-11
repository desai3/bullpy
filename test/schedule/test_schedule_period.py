import datetime

import pytest

from ...schedule.schedule_period import SchedulePeriod
from ...schedule.schedule import Schedule
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


def test_defaults():
    sp = SchedulePeriod(JUL_05, JUL_18)
    assert sp.get_start_date() == JUL_05
    assert sp.get_end_date() == JUL_18
    assert sp.get_unadjusted_start_date() == JUL_05
    assert sp.get_unadjusted_end_date() == JUL_18


def test_year_fraction():
    sp = SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17)
    sch = Schedule.of_term(sp)
    dc = DayCount(DayCountType.ACT_360)
    assert abs(sp.year_fraction(dc, sch) - dc.year_fraction(JUN_16, JUL_18)) < 1e-8


def test_year_fraction_null():
    sp = SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17)
    sch = Schedule.of_term(sp)
    dc = DayCount(DayCountType.ACT_360)

    with pytest.raises(ValueError):
        sp.year_fraction(None, sch)
    with pytest.raises(ValueError):
        sp.year_fraction(dc, None)
    with pytest.raises(ValueError):
        sp.year_fraction(None, None)


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
    sp1 = SchedulePeriod(JUN_15, SEP_17)
    sp2 = SchedulePeriod(JUN_16, SEP_17, JUN_15, SEP_17)

    assert sp1.to_adjusted(lambda x: x) == sp1
    assert sp1.to_adjusted(lambda x: JUN_16 if x == JUN_15 else x) == sp2

    sp3 = SchedulePeriod(JUN_16, AUG_17)
    sp4 = SchedulePeriod(JUN_16, AUG_18, JUN_16, AUG_17)
    assert sp3.to_adjusted(lambda x: AUG_18 if x == AUG_17 else x) == sp4


def test_to_unadjusted():
    sp1 = SchedulePeriod(JUN_15, SEP_17)
    assert sp1.to_unadjusted() == sp1

    sp2 = SchedulePeriod(JUN_16, SEP_17, JUN_15, SEP_17)
    sp3 = SchedulePeriod(JUN_15, SEP_17)
    assert sp2.to_unadjusted() == sp3

    sp4 = SchedulePeriod(JUN_16, JUL_18, JUN_16, JUL_17)
    sp5 = SchedulePeriod(JUN_16, JUL_17)
    assert sp4.to_unadjusted() == sp5


def test_compare():
    sp1 = SchedulePeriod(JUL_05, JUL_18)
    sp2 = SchedulePeriod(JUL_04, JUL_18)
    sp3 = SchedulePeriod(JUL_05, JUL_17)

    assert sp1.compare(sp1) == 0
    assert sp1.compare(sp2) == 1
    assert sp1.compare(sp3) == 1

    assert sp2.compare(sp1) == -1
    assert sp2.compare(sp2) == 0
    assert sp2.compare(sp3) == -1

    assert sp3.compare(sp1) == -1
    assert sp3.compare(sp2) == 1
    assert sp3.compare(sp3) == 0


def test_equal():
    sp11 = SchedulePeriod(JUL_05, JUL_18, JUL_04, JUL_17)
    sp12 = SchedulePeriod(JUL_05, JUL_18, JUL_04, JUL_17)

    sp2 = SchedulePeriod(JUL_04, JUL_18, JUL_04, JUL_17)
    sp3 = SchedulePeriod(JUL_05, JUL_17, JUL_04, JUL_17)
    sp4 = SchedulePeriod(JUL_05, JUL_18, JUL_05, JUL_17)
    sp5 = SchedulePeriod(JUL_05, JUL_18, JUL_04, JUL_18)

    assert sp11 == sp11
    assert sp11 == sp12
    assert sp11 != sp2
    assert sp11 != sp3
    assert sp11 != sp4
    assert sp11 != sp5


if __name__ == '__main__':
    test_is_regular()