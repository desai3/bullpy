from datetime import datetime

import pytest

from schedule_period import SchedulePeriod
from schedule import Schedule
from frequency import Frequency
from roll_convention import RollConvention, RollConventionType

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
    assert sch.get_unadjusted_dates() == [JUL_04, JUL_17 ]


if __name__ == '__main__':
    test_term()