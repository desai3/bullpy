from datetime import datetime

import pytest

from ...schedule.roll_convention import RollConvention, RollConventionType
from ...schedule.stub_convention import StubConvention, StubConventionType
from ...schedule.bdayadj import BDayAdj, BDayAdjType
from ...schedule.calendars import HolidayCalendar, HolidayCalendarType, CustomeHolidayCalendar
from ...schedule.periodic_schedule import PeriodicSchedule
from ...schedule.frequency import Frequency, plus_months
from ...schedule.schedule_period import SchedulePeriod

CAL = None
ROLL_NONE = RollConvention(RollConventionType.NONE)
STUB_NONE = StubConvention(StubConventionType.NONE)
STUB_BOTH = StubConvention(StubConventionType.BOTH)
BDA = BDayAdj(BDayAdjType.MODIFIED_FOLLOWING, CustomeHolidayCalendar('SAT_SUN', set()))
# BDA_JPY_MF = BDayAdj(BDayAdjType.MODIFIED_FOLLOWING, HolidayCalendar(HolidayCalendarType.JPTO))
# BDA_JPY_P = BDayAdj(BDayAdjType.PRECEDING, HolidayCalendar(HolidayCalendarType.JPTO))
BDA_NONE = BDayAdj(BDayAdjType.NO_ADJUST)
NOV_29_2013 = datetime(2013, 11, 29)
NOV_30_2013 = datetime(2013, 11, 30)
FEB_28 = datetime(2014, 2, 28)
APR_01 = datetime(2014, 4, 1)
MAY_17 = datetime(2014, 5, 17)
MAY_19 = datetime(2014, 5, 19)
MAY_30 = datetime(2014, 5, 30)
MAY_31 = datetime(2014, 5, 31)
JUN_03 = datetime(2014, 6, 3)
JUN_04 = datetime(2014, 6, 4)
JUN_10 = datetime(2014, 6, 10)
JUN_11 = datetime(2014, 6, 11)
JUN_17 = datetime(2014, 6, 17)
JUL_04 = datetime(2014, 7, 4)
JUL_11 = datetime(2014, 7, 11)
JUL_17 = datetime(2014, 7, 17)
JUL_30 = datetime(2014, 7, 30)
AUG_04 = datetime(2014, 8, 4)
AUG_11 = datetime(2014, 8, 11)
AUG_17 = datetime(2014, 8, 17)
AUG_18 = datetime(2014, 8, 18)
AUG_29 = datetime(2014, 8, 29)
AUG_30 = datetime(2014, 8, 30)
AUG_31 = datetime(2014, 8, 31)
SEP_04 = datetime(2014, 9, 4)
SEP_05 = datetime(2014, 9, 5)
SEP_10 = datetime(2014, 9, 10)
SEP_11 = datetime(2014, 9, 11)
SEP_17 = datetime(2014, 9, 17)
SEP_18 = datetime(2014, 9, 18)
SEP_30 = datetime(2014, 9, 30)
OCT_17 = datetime(2014, 10, 17)
OCT_30 = datetime(2014, 10, 30)
NOV_28 = datetime(2014, 11, 28)
NOV_30 = datetime(2014, 11, 30)


def test_local_date_eom_false():
    ps = PeriodicSchedule(
        unadjusted_start_date=JUN_04,
        unadjusted_end_date=SEP_17,
        freq=Frequency(months=1),
        bday_adj=BDA,
        stub_conv=StubConvention(StubConventionType.SHORT_INITIAL))
        # roll_eom=False)
    assert ps.get_start_date() == JUN_04
    assert ps.get_end_date() == SEP_17
    assert ps.get_frequency() == Frequency(months=1)
    assert ps.get_bday_adj() == BDA
    assert ps.get_start_date_bday_adj() is None
    assert ps.get_end_date_bday_adj() is None
    assert ps.get_stub_convention() == StubConvention(StubConventionType.SHORT_INITIAL)
    assert ps.get_roll_convention() is None
    assert ps.get_first_regular_start_date() is None
    assert ps.get_last_regular_end_date() is None
    assert ps.get_override_start_date() is None
    assert ps.calculated_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert ps.calculated_first_regular_start_date() == JUN_04
    assert ps.calculated_last_regular_end_date() == SEP_17
    assert ps.calculated_start_date() == (JUN_04, BDA)
    assert ps.calculated_end_date() == (SEP_17, BDA)


def test_local_date_eom_true():
    ps = PeriodicSchedule(
        unadjusted_start_date=JUN_04,
        unadjusted_end_date=SEP_17,
        freq=Frequency(months=1),
        bday_adj=BDA,
        stub_conv=StubConvention(StubConventionType.SHORT_FINAL),
        roll_conv=RollConvention(RollConventionType.EOM))
    assert ps.get_start_date() == JUN_04
    assert ps.get_end_date() == SEP_17
    assert ps.get_frequency() == Frequency(months=1)
    assert ps.get_bday_adj() == BDA
    assert ps.get_start_date_bday_adj() is None
    assert ps.get_end_date_bday_adj() is None
    assert ps.get_stub_convention() == StubConvention(StubConventionType.SHORT_FINAL)
    assert ps.get_roll_convention() == RollConvention(RollConventionType.EOM)
    assert ps.get_first_regular_start_date() is None
    assert ps.get_last_regular_end_date() is None
    assert ps.get_override_start_date() is None
    assert ps.calculated_roll_convention() == RollConvention(RollConventionType.DAY_4)
    assert ps.calculated_first_regular_start_date() == JUN_04
    assert ps.calculated_last_regular_end_date() == SEP_17
    assert ps.calculated_start_date() == (JUN_04, BDA)
    assert ps.calculated_end_date() == (SEP_17, BDA)


def test_null():
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=None, unadjusted_end_date=SEP_17,
                         freq=Frequency(months=1), bday_adj=BDA,
                         stub_conv=StubConvention(StubConventionType.SHORT_INITIAL))
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=JUN_04, unadjusted_end_date=None,
                         freq=Frequency(months=1), bday_adj=BDA,
                         stub_conv=StubConvention(StubConventionType.SHORT_FINAL))
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
                         freq=None, bday_adj=BDA,
                         stub_conv=StubConvention(StubConventionType.SHORT_FINAL))
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
                         freq=Frequency(months=1), bday_adj=None,
                         stub_conv=StubConvention(StubConventionType.SHORT_FINAL))
    # with pytest.raises(ValueError):
    #     PeriodicSchedule(unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
    #                      freq=Frequency(months=1), bday_adj=BDA,
    #                      stub_conv=None)


def test_local_date_roll():
    ps = PeriodicSchedule(
        unadjusted_start_date=JUN_04,
        unadjusted_end_date=SEP_17,
        freq=Frequency(months=1),
        bday_adj=BDA,
        stub_conv=StubConvention(StubConventionType.SHORT_INITIAL),
        roll_conv=RollConvention(RollConventionType.DAY_17)
    )
    assert ps.get_start_date() == JUN_04
    assert ps.get_end_date() == SEP_17
    assert ps.get_frequency() == Frequency(months=1)
    assert ps.get_bday_adj() == BDA
    assert ps.get_start_date_bday_adj() is None
    assert ps.get_end_date_bday_adj() is None
    assert ps.get_stub_convention() == StubConvention(StubConventionType.SHORT_INITIAL)
    assert ps.get_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert ps.get_first_regular_start_date() is None
    assert ps.get_last_regular_end_date() is None
    assert ps.get_override_start_date() is None
    assert ps.calculated_roll_convention() == RollConvention(RollConventionType.DAY_17)
    assert ps.calculated_first_regular_start_date() == JUN_04
    assert ps.calculated_last_regular_end_date() == SEP_17
    assert ps.calculated_start_date() == (JUN_04, BDA)
    assert ps.calculated_end_date() == (SEP_17, BDA)




def test_first_payment_date_before_effective_date():
    start_date = datetime(2018, 7, 26)
    end_date = datetime(2019, 6, 20)
    override_start_date = datetime(2018, 3, 20)
    first_regular_start_date = datetime(2018, 6, 20)

    ps = PeriodicSchedule(
        unadjusted_start_date=start_date, unadjusted_end_date=end_date,
        freq=Frequency(months=3), bday_adj=BDA,
        first_regular_start_date=first_regular_start_date,
        override_start_date=(override_start_date, BDA_NONE),
    )

    sched = ps.create_schedule(CAL)
    assert sched.size() == 5

    for i in range(sched.size()):
        expected_start = plus_months(override_start_date, 3 * i)
        expected_end = plus_months(expected_start, 3)
        sp = SchedulePeriod(expected_start, expected_end)
        ap = sched.get_period(i)

        assert sp == ap


if __name__ == '__main__':
    test_local_date_eom_false()
