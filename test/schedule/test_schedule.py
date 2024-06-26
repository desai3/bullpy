from datetime import datetime

import pytest

from ...schedule.schedule_period import SchedulePeriod
from ...schedule.schedule import Schedule
from ...schedule.frequency import Frequency, plus_days
from ...schedule.roll_convention import RollConvention, RollConventionType

JUN_15 = datetime(2014, 6, 15);
JUN_16 = datetime(2014, 6, 16);
JUL_03 = datetime(2014, 7, 3);
JUL_04 = datetime(2014, 7, 4);
JUL_16 = datetime(2014, 7, 16);
JUL_17 = datetime(2014, 7, 17);
AUG_16 = datetime(2014, 8, 16);
AUG_17 = datetime(2014, 8, 17);
SEP_17 = datetime(2014, 9, 17);
SEP_30 = datetime(2014, 9, 30);
OCT_15 = datetime(2014, 10, 15);
OCT_17 = datetime(2014, 10, 17);
NOV_17 = datetime(2014, 11, 17);
DEC_17 = datetime(2014, 12, 17);

P1_STUB = SchedulePeriod(JUL_03, JUL_17, JUL_04, JUL_17);
P2_NORMAL = SchedulePeriod(JUL_17, AUG_16, JUL_17, AUG_17);
P3_NORMAL = SchedulePeriod(AUG_16, SEP_17, AUG_17, SEP_17);
P4_STUB = SchedulePeriod(SEP_17, SEP_30);
P4_NORMAL = SchedulePeriod(SEP_17, OCT_17);
P5_NORMAL = SchedulePeriod(OCT_17, NOV_17);
P6_NORMAL = SchedulePeriod(NOV_17, DEC_17);

P1_2 = SchedulePeriod(JUL_03, AUG_16, JUL_04, AUG_17);
P1_3 = SchedulePeriod(JUL_03, SEP_17, JUL_04, SEP_17);
P2_3 = SchedulePeriod(JUL_17, SEP_17);
P3_4 = SchedulePeriod(AUG_16, OCT_17, AUG_17, OCT_17);
P3_4STUB = SchedulePeriod(AUG_16, SEP_30, AUG_17, SEP_30);
P4_5 = SchedulePeriod(SEP_17, NOV_17);
P5_6 = SchedulePeriod(OCT_17, DEC_17);

P2_4 = SchedulePeriod(JUL_17, OCT_17);
P4_6 = SchedulePeriod(SEP_17, DEC_17);


def test_term():
    sch = Schedule([P1_STUB])
    assert sch.size() == 1
    assert sch.is_term()
    assert sch.is_single_period()
    assert sch.get_frequency() == Frequency()
    assert sch.get_roll_convention() == RollConvention(RollConventionType.NONE)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P1_STUB]
    assert sch.get_period(0) == P1_STUB
    assert sch.get_start_date() == P1_STUB.get_start_date()
    assert sch.get_end_date() == P1_STUB.get_end_date()
    assert sch.get_unadjusted_start_date() == P1_STUB.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P1_STUB.get_unadjusted_end_date()
    assert sch.get_first_period() == P1_STUB
    assert sch.get_last_period() == P1_STUB
    assert sch.get_initial_stub() is None
    assert sch.get_final_stub() is None
    assert sch.get_stubs(True) == (None, None)
    assert sch.get_stubs(False) == (None, None)
    assert sch.get_regular_periods() == [P1_STUB]
    with pytest.raises(IndexError):
        sch.get_period(1)
    assert sch.get_unadjusted_dates() == [JUL_04, JUL_17]


def test_size1_stub():
    sch = Schedule([P1_STUB], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 1
    assert not sch.is_term()
    assert sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P1_STUB]
    assert sch.get_period(0) == P1_STUB
    assert sch.get_start_date() == P1_STUB.get_start_date()
    assert sch.get_end_date() == P1_STUB.get_end_date()
    assert sch.get_unadjusted_start_date() == P1_STUB.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P1_STUB.get_unadjusted_end_date()
    assert sch.get_first_period() == P1_STUB
    assert sch.get_last_period() == P1_STUB
    assert sch.get_initial_stub() == P1_STUB
    assert sch.get_final_stub() is None
    assert sch.get_stubs(True) == (None, P1_STUB)
    assert sch.get_stubs(False) == (P1_STUB, None)
    assert sch.get_regular_periods() == []
    with pytest.raises(IndexError):
        sch.get_period(1)
    assert sch.get_unadjusted_dates() == [JUL_04, JUL_17]


def test_size1_nostub():
    sch = Schedule([P2_NORMAL], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 1
    assert not sch.is_term()
    assert sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P2_NORMAL]
    assert sch.get_period(0) == P2_NORMAL
    assert sch.get_start_date() == P2_NORMAL.get_start_date()
    assert sch.get_end_date() == P2_NORMAL.get_end_date()
    assert sch.get_unadjusted_start_date() == P2_NORMAL.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P2_NORMAL.get_unadjusted_end_date()
    assert sch.get_first_period() == P2_NORMAL
    assert sch.get_last_period() == P2_NORMAL
    assert sch.get_initial_stub() is None
    assert sch.get_final_stub() is None
    assert sch.get_stubs(True) == (None, None)
    assert sch.get_stubs(False) == (None, None)
    assert sch.get_regular_periods() == [P2_NORMAL]
    with pytest.raises(IndexError):
        sch.get_period(1)
    assert sch.get_unadjusted_dates() == [JUL_17, AUG_17]


def test_size1_no_stub():
    sch = Schedule([P2_NORMAL], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 1
    assert not sch.is_term()
    assert sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P2_NORMAL]
    assert sch.get_period(0) == P2_NORMAL
    assert sch.get_start_date() == P2_NORMAL.get_start_date()
    assert sch.get_end_date() == P2_NORMAL.get_end_date()
    assert sch.get_unadjusted_start_date() == P2_NORMAL.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P2_NORMAL.get_unadjusted_end_date()
    assert sch.get_first_period() == P2_NORMAL
    assert sch.get_last_period() == P2_NORMAL
    assert sch.get_initial_stub() is None
    assert sch.get_final_stub() is None
    assert sch.get_stubs(True) == (None, None)
    assert sch.get_stubs(False) == (None, None)
    assert sch.get_regular_periods() == [P2_NORMAL]
    with pytest.raises(IndexError):
        sch.get_period(1)
    assert sch.get_unadjusted_dates() == [JUL_17, AUG_17]


def test_size2_init_stub():
    sch = Schedule([P1_STUB, P2_NORMAL], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 2
    assert not sch.is_term()
    assert not sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P1_STUB, P2_NORMAL]
    assert sch.get_period(0) == P1_STUB
    assert sch.get_period(1) == P2_NORMAL
    assert sch.get_start_date() == P1_STUB.get_start_date()
    assert sch.get_end_date() == P2_NORMAL.get_end_date()
    assert sch.get_unadjusted_start_date() == P1_STUB.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P2_NORMAL.get_unadjusted_end_date()
    assert sch.get_first_period() == P1_STUB
    assert sch.get_last_period() == P2_NORMAL
    assert sch.get_initial_stub() == P1_STUB
    assert sch.get_final_stub() is None
    assert sch.get_stubs(True) == (P1_STUB, None)
    assert sch.get_stubs(False) == (P1_STUB, None)
    assert sch.get_regular_periods() == [P2_NORMAL]
    with pytest.raises(IndexError):
        sch.get_period(2)
    assert sch.get_unadjusted_dates() == [JUL_04, JUL_17, AUG_17]


def test_size2_no_stub():
    sch = Schedule([P2_NORMAL, P3_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 2
    assert not sch.is_term()
    assert not sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P2_NORMAL, P3_NORMAL]
    assert sch.get_period(0) == P2_NORMAL
    assert sch.get_period(1) == P3_NORMAL
    assert sch.get_start_date() == P2_NORMAL.get_start_date()
    assert sch.get_end_date() == P3_NORMAL.get_end_date()
    assert sch.get_unadjusted_start_date() == P2_NORMAL.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P3_NORMAL.get_unadjusted_end_date()
    assert sch.get_first_period() == P2_NORMAL
    assert sch.get_last_period() == P3_NORMAL
    assert sch.get_initial_stub() is None
    assert sch.get_final_stub() is None
    assert sch.get_stubs(True) == (None, None)
    assert sch.get_stubs(False) == (None, None)
    assert sch.get_regular_periods() == [P2_NORMAL, P3_NORMAL]
    with pytest.raises(IndexError):
        sch.get_period(2)
    assert sch.get_unadjusted_dates() == [JUL_17, AUG_17, SEP_17]


def test_size2_final_stub():
    sch = Schedule([P3_NORMAL, P4_STUB], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 2
    assert not sch.is_term()
    assert not sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P3_NORMAL, P4_STUB]
    assert sch.get_period(0) == P3_NORMAL
    assert sch.get_period(1) == P4_STUB
    assert sch.get_start_date() == P3_NORMAL.get_start_date()
    assert sch.get_end_date() == P4_STUB.get_end_date()
    assert sch.get_unadjusted_start_date() == P3_NORMAL.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P4_STUB.get_unadjusted_end_date()
    assert sch.get_first_period() == P3_NORMAL
    assert sch.get_last_period() == P4_STUB
    assert sch.get_initial_stub() is None
    assert sch.get_final_stub() == P4_STUB
    assert sch.get_stubs(True) == (None, P4_STUB)
    assert sch.get_stubs(False) == (None, P4_STUB)
    assert sch.get_regular_periods() == [P3_NORMAL]
    with pytest.raises(IndexError):
        sch.get_period(2)
    assert sch.get_unadjusted_dates() == [AUG_17, SEP_17, SEP_30]


def test_of_size3_init_stub():
    sch = Schedule([P1_STUB, P2_NORMAL, P3_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 3
    assert not sch.is_term()
    assert not sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P1_STUB, P2_NORMAL, P3_NORMAL]
    assert sch.get_period(0) == P1_STUB
    assert sch.get_period(1) == P2_NORMAL
    assert sch.get_period(2) == P3_NORMAL
    assert sch.get_start_date() == P1_STUB.get_start_date()
    assert sch.get_end_date() == P3_NORMAL.get_end_date()
    assert sch.get_unadjusted_start_date() == P1_STUB.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P3_NORMAL.get_unadjusted_end_date()
    assert sch.get_first_period() == P1_STUB
    assert sch.get_last_period() == P3_NORMAL
    assert sch.get_initial_stub() == P1_STUB
    assert sch.get_final_stub() is None
    assert sch.get_regular_periods() == [P2_NORMAL, P3_NORMAL]
    with pytest.raises(IndexError):
        sch.get_period(3)
    assert sch.get_unadjusted_dates() == [JUL_04, JUL_17, AUG_17, SEP_17]


def test_size4_both_stubs():
    sch = Schedule([P1_STUB, P2_NORMAL, P3_NORMAL, P4_STUB], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.size() == 4
    assert not sch.is_term()
    assert not sch.is_single_period()
    assert sch.get_frequency() == Frequency(months=1)
    assert sch.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert not sch.is_end_of_month_convention()
    assert sch.get_periods() == [P1_STUB, P2_NORMAL, P3_NORMAL, P4_STUB]
    assert sch.get_period(0) == P1_STUB
    assert sch.get_period(1) == P2_NORMAL
    assert sch.get_period(2) == P3_NORMAL
    assert sch.get_period(3) == P4_STUB
    assert sch.get_start_date() == P1_STUB.get_start_date()
    assert sch.get_end_date() == P4_STUB.get_end_date()
    assert sch.get_unadjusted_start_date() == P1_STUB.get_unadjusted_start_date()
    assert sch.get_unadjusted_end_date() == P4_STUB.get_unadjusted_end_date()
    assert sch.get_first_period() == P1_STUB
    assert sch.get_last_period() == P4_STUB
    assert sch.get_initial_stub() == P1_STUB
    assert sch.get_final_stub() == P4_STUB
    assert sch.get_regular_periods() == [P2_NORMAL, P3_NORMAL]
    with pytest.raises(IndexError):
        sch.get_period(4)
    assert sch.get_unadjusted_dates() == [JUL_04, JUL_17, AUG_17, SEP_17, SEP_30]


def test_is_end_of_month_convention_eom():
    sch = Schedule([P2_NORMAL, P3_NORMAL], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.EOM))
    assert sch.is_end_of_month_convention()


def test_get_period_end_date():
    sch = Schedule([P2_NORMAL, P3_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.get_period_end_date(P2_NORMAL.get_start_date()) == P2_NORMAL.get_end_date()
    assert sch.get_period_end_date(plus_days(P2_NORMAL.get_start_date(), 1)) == P2_NORMAL.get_end_date()
    assert sch.get_period_end_date(P3_NORMAL.get_start_date()) == P3_NORMAL.get_end_date()
    assert sch.get_period_end_date(plus_days(P3_NORMAL.get_start_date(), 1)) == P3_NORMAL.get_end_date()

    with pytest.raises(ValueError):
        sch.get_period_end_date(plus_days(P2_NORMAL.get_start_date(), -1))
    with pytest.raises(ValueError):
        sch.get_period_end_date(plus_days(P5_NORMAL.get_start_date(), -1))


def test_merge_to_term():
    sch = Schedule([P1_STUB, P2_NORMAL, P3_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.merge_to_term() == Schedule([P1_3])
    assert sch.merge_to_term().merge_to_term() == Schedule([P1_3])


def test_merge_to_term_size1_stub():
    sch = Schedule([P1_STUB], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.merge_to_term() == Schedule([P1_STUB])


def test_merge_group2_within2_init_stub():
    sch1 = Schedule([P1_STUB, P2_NORMAL, P3_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P1_STUB, P2_3], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(2, True) == sch2
    assert sch1.merge_regular(2, False) == sch2
    assert sch1.merge(2, P2_NORMAL.get_unadjusted_start_date(), P3_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P2_NORMAL.get_start_date(), P3_NORMAL.get_end_date()) == sch2


def test_merge_group2_within2_no_stub():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_3], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(2, True) == sch2
    assert sch1.merge_regular(2, False) == sch2
    assert sch1.merge(2, P2_NORMAL.get_unadjusted_start_date(), P3_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P2_NORMAL.get_start_date(), P3_NORMAL.get_end_date()) == sch2


def test_merge_group2_within2_final_stub():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_STUB], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_3, P4_STUB], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(2, True) == sch2
    assert sch1.merge_regular(2, False) == sch2
    assert sch1.merge(2, P2_NORMAL.get_unadjusted_start_date(), P3_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P2_NORMAL.get_start_date(), P3_NORMAL.get_end_date()) == sch2


def test_merge_group2_within3_forwards():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_3, P4_NORMAL], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(2, True) == sch2
    assert sch1.merge(2, P2_NORMAL.get_unadjusted_start_date(), P3_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P2_NORMAL.get_start_date(), P3_NORMAL.get_end_date()) == sch2


def test_merge_group2_within3_backwards():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_NORMAL, P3_4], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(2, False) == sch2
    assert sch1.merge(2, P3_NORMAL.get_unadjusted_start_date(), P4_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P3_NORMAL.get_start_date(), P4_NORMAL.get_end_date()) == sch2


def test_merge_group2_within5_forwards():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_3, P4_5, P6_NORMAL], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(2, True) == sch2
    assert sch1.merge(2, P2_NORMAL.get_unadjusted_start_date(), P5_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P2_NORMAL.get_start_date(), P5_NORMAL.get_end_date()) == sch2


def test_merge_group2_within5_backwards():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_NORMAL, P3_4, P5_6], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(2, False) == sch2
    assert sch1.merge(2, P3_NORMAL.get_unadjusted_start_date(), P6_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P3_NORMAL.get_start_date(), P6_NORMAL.get_end_date()) == sch2


def test_merge_group2_within6_include_init_stub():
    sch1 = Schedule([P1_STUB, P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P1_2, P3_4, P5_6], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge(2, P3_NORMAL.get_unadjusted_start_date(), P6_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P3_NORMAL.get_start_date(), P6_NORMAL.get_end_date()) == sch2


def test_merge_group2_within6_include_final_stub():
    sch1 = Schedule([P1_STUB, P2_NORMAL, P3_NORMAL, P4_STUB], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P1_2, P3_4STUB], freq=Frequency(months=2),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge(2, P1_STUB.get_unadjusted_start_date(), P2_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(2, P1_STUB.get_start_date(), P2_NORMAL.get_end_date()) == sch2


def test_merge_group3_within5_forwards():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_4, P5_6], freq=Frequency(months=3),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(3, True) == sch2
    assert sch1.merge(3, P2_NORMAL.get_unadjusted_start_date(), P4_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(3, P2_NORMAL.get_start_date(), P4_NORMAL.get_end_date()) == sch2


def test_merge_group3_within5_backwards():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_3, P4_6], freq=Frequency(months=3),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch1.merge_regular(3, False) == sch2
    assert sch1.merge(3, P4_NORMAL.get_unadjusted_start_date(), P6_NORMAL.get_unadjusted_end_date()) == sch2
    assert sch1.merge(3, P4_NORMAL.get_start_date(), P6_NORMAL.get_end_date()) == sch2


def test_merge_term_no_change():
    sch = Schedule.of_term(P1_STUB)
    assert sch.merge_regular(2, True) == sch
    assert sch.merge_regular(2, False) == sch
    assert sch.merge(2, P1_STUB.get_unadjusted_start_date(), P1_STUB.get_unadjusted_end_date()) == sch
    assert sch.merge(2, P1_STUB.get_start_date(), P1_STUB.get_end_date()) == sch


def test_merge_size1_stub():
    sch = Schedule([P1_STUB], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.merge_regular(2, True) == sch
    assert sch.merge_regular(2, False) == sch
    assert sch.merge(2, P1_STUB.get_unadjusted_start_date(), P1_STUB.get_unadjusted_end_date()) == sch
    assert sch.merge(2, P1_STUB.get_start_date(), P1_STUB.get_end_date()) == sch


def test_merge_group_size_one_no_change():
    sch = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))
    assert sch.merge_regular(1, True) == sch
    assert sch.merge_regular(1, False) == sch
    assert sch.merge(1, P2_NORMAL.get_unadjusted_start_date(), P6_NORMAL.get_unadjusted_end_date()) == sch
    assert sch.merge(1, P2_NORMAL.get_start_date(), P6_NORMAL.get_end_date()) == sch


def test_merge_group_size_invalid():
    sch = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))

    with pytest.raises(ValueError):
        sch.merge_regular(0, True)
    with pytest.raises(ValueError):
        sch.merge_regular(0, False)
    with pytest.raises(ValueError):
        sch.merge_regular(-1, True)
    with pytest.raises(ValueError):
        sch.merge_regular(-1, False)
    with pytest.raises(ValueError):
        sch.merge(0, P2_NORMAL.get_unadjusted_start_date(), P6_NORMAL.get_unadjusted_end_date())
    with pytest.raises(ValueError):
        sch.merge(-1, P2_NORMAL.get_unadjusted_start_date(), P6_NORMAL.get_unadjusted_end_date())


def test_merge_bad_date():
    sch = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))

    with pytest.raises(ValueError):
        sch.merge(2, JUL_03, AUG_17)
    with pytest.raises(ValueError):
        sch.merge(2, JUL_17, SEP_30)


def test_merge_bad_group_size():
    sch = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                   roll_conv=RollConvention(RollConventionType.DAY_17))
    with pytest.raises(ValueError):
        sch.merge(2, P2_NORMAL.get_unadjusted_start_date(), P6_NORMAL.get_unadjusted_end_date())


def test_equals():
    sch1 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([P2_NORMAL, P3_NORMAL], freq=Frequency(months=1),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch3 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=3),
                    roll_conv=RollConvention(RollConventionType.DAY_17))
    sch4 = Schedule([P2_NORMAL, P3_NORMAL, P4_NORMAL, P5_NORMAL, P6_NORMAL], freq=Frequency(months=3),
                    roll_conv=RollConvention(RollConventionType.DAY_1))
    assert sch1 == sch1
    assert sch1 != sch2
    assert sch1 != sch3
    assert sch1 != sch4


def test_to_adjusted():
    sp1 = SchedulePeriod(JUN_15, SEP_17)
    sp2 = SchedulePeriod(SEP_17, SEP_30)
    sp3 = SchedulePeriod(JUN_16, SEP_17, JUN_15, SEP_17)

    sch1 = Schedule([sp1, sp2], freq=Frequency(months=3), roll_conv=RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([sp3, sp2], freq=Frequency(months=3), roll_conv=RollConvention(RollConventionType.DAY_17))

    assert sch1.to_adjusted(lambda x: x) == sch1
    assert sch1.to_adjusted(lambda x: JUN_16 if x == JUN_15 else x) == sch2


def test_to_adjusted_small_first_last():
    sp1 = SchedulePeriod(JUL_03, JUL_04, JUL_03, JUL_04)
    sp2 = SchedulePeriod(JUL_04, AUG_16)
    sp3 = SchedulePeriod(AUG_16, AUG_17, AUG_16, AUG_17)

    sch1 = Schedule([sp1, sp2, sp3], freq=Frequency(months=1), roll_conv=RollConvention(RollConventionType.DAY_4))
    assert sch1.to_adjusted(lambda x: JUL_04 if x == JUL_03 else AUG_16 if x == AUG_17 else x) == sch1


def test_to_unadjusted():
    sp1 = SchedulePeriod(JUL_17, OCT_17, JUL_16, OCT_15)
    sp2 = SchedulePeriod(JUL_16, OCT_15, JUL_16, OCT_15)
    sch1 = Schedule([sp1], Frequency(months=1), RollConvention(RollConventionType.DAY_17))
    sch2 = Schedule([sp2], Frequency(months=1), RollConvention(RollConventionType.DAY_17))
    assert sch1.to_unadjusted() == sch2


if __name__ == '__main__':
    test_merge_group2_within2_init_stub()
