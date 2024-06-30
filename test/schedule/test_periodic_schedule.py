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
BDA_JPY_MF = BDayAdj(BDayAdjType.MODIFIED_FOLLOWING, HolidayCalendar(HolidayCalendarType.JPTO))
BDA_JPY_P = BDayAdj(BDayAdjType.PRECEDING, HolidayCalendar(HolidayCalendarType.JPTO))
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
        stub_conv=StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_INITIAL)))
    # roll_eom=False)
    assert ps.get_start_date() == JUN_04
    assert ps.get_end_date() == SEP_17
    assert ps.get_frequency() == Frequency(months=1)
    assert ps.get_bday_adj() == BDA
    assert ps.get_start_date_bday_adj() is None
    assert ps.get_end_date_bday_adj() is None
    assert ps.get_stub_convention() == StubConvention(
        StubConventionType.StubConvention(StubConventionType.SHORT_INITIAL))
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
        stub_conv=StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_FINAL)),
        roll_conv=RollConvention(RollConventionType.RollConvention(RollConventionType.EOM)))
    assert ps.get_start_date() == JUN_04
    assert ps.get_end_date() == SEP_17
    assert ps.get_frequency() == Frequency(months=1)
    assert ps.get_bday_adj() == BDA
    assert ps.get_start_date_bday_adj() is None
    assert ps.get_end_date_bday_adj() is None
    assert ps.get_stub_convention() == StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_FINAL))
    assert ps.get_roll_convention() == RollConvention(RollConventionType.RollConvention(RollConventionType.EOM))
    assert ps.get_first_regular_start_date() is None
    assert ps.get_last_regular_end_date() is None
    assert ps.get_override_start_date() is None
    assert ps.calculated_roll_convention() == RollConvention(RollConventionType.DAY_4)
    assert ps.calculated_first_regular_start_date() == JUN_04
    assert ps.calculated_last_regular_end_date() == SEP_17
    assert ps.calculated_start_date() == (JUN_04, BDA)
    assert ps.calculated_end_date() == (SEP_17, BDA)


def test_None():
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=None, unadjusted_end_date=SEP_17,
                         freq=Frequency(months=1), bday_adj=BDA,
                         stub_conv=StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_INITIAL)))
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=JUN_04, unadjusted_end_date=None,
                         freq=Frequency(months=1), bday_adj=BDA,
                         stub_conv=StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_FINAL)))
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
                         freq=None, bday_adj=BDA,
                         stub_conv=StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_FINAL)))
    with pytest.raises(ValueError):
        PeriodicSchedule(unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
                         freq=Frequency(months=1), bday_adj=None,
                         stub_conv=StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_FINAL)))
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
        stub_conv=StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_INITIAL)),
        roll_conv=RollConvention(RollConventionType.DAY_17)
    )
    assert ps.get_start_date() == JUN_04
    assert ps.get_end_date() == SEP_17
    assert ps.get_frequency() == Frequency(months=1)
    assert ps.get_bday_adj() == BDA
    assert ps.get_start_date_bday_adj() is None
    assert ps.get_end_date_bday_adj() is None
    assert ps.get_stub_convention() == StubConvention(
        StubConventionType.StubConvention(StubConventionType.SHORT_INITIAL))
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


def test_invalid_date_order():
    with pytest.raises(ValueError):
        PeriodicSchedule(
            unadjusted_start_date=SEP_17, unadjusted_end_date=SEP_17,
            freq=Frequency(months=1), bday_adj=BDA,
            first_regular_start_date=None, last_regular_end_date=None
        )
    with pytest.raises(ValueError):
        PeriodicSchedule(
            unadjusted_start_date=SEP_17, unadjusted_end_date=JUN_04,
            freq=Frequency(months=1), bday_adj=BDA,
            first_regular_start_date=None, last_regular_end_date=None
        )
    with pytest.raises(ValueError):
        PeriodicSchedule(
            unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
            freq=Frequency(months=1), bday_adj=BDA,
            first_regular_start_date=JUN_03, last_regular_end_date=None
        )
    with pytest.raises(ValueError):
        PeriodicSchedule(
            unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
            freq=Frequency(months=1), bday_adj=BDA,
            first_regular_start_date=None, last_regular_end_date=SEP_18
        )
    PeriodicSchedule(
        unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_05,
        freq=Frequency(months=1), bday_adj=BDA,
        first_regular_start_date=SEP_05, last_regular_end_date=SEP_05
    )
    with pytest.raises(ValueError):
        PeriodicSchedule(
            unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
            freq=Frequency(months=1), bday_adj=BDA,
            first_regular_start_date=SEP_05, last_regular_end_date=SEP_04
        )
    with pytest.raises(ValueError):
        PeriodicSchedule(
            unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
            freq=Frequency(months=1), bday_adj=BDA,
            first_regular_start_date=SEP_05, last_regular_end_date=SEP_04
        )
    with pytest.raises(ValueError):
        PeriodicSchedule(
            unadjusted_start_date=JUN_04, unadjusted_end_date=SEP_17,
            freq=Frequency(months=1), bday_adj=BDA,
            first_regular_start_date=JUL_17, last_regular_end_date=None,
            override_start_date=(AUG_04, BDA_NONE)
        )


def data_gen():
    return [
    # stub None
    [JUN_17, SEP_17, Frequency(months=1), None, None, BDA, None, None, None,
     [JUN_17, JUL_17, AUG_17, SEP_17], [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.RollConvention(RollConventionType.DAY_17))],

    # stub StubConvention(StubConventionType.NONE)
    [JUN_17, SEP_17, Frequency(months=1), STUB_NONE, None, BDA, None, None, None,
     [JUN_17, JUL_17, AUG_17, SEP_17], [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.RollConvention(RollConventionType.DAY_17))],
    [JUN_17, JUL_17, Frequency(months=1), STUB_NONE, None, BDA, None, None, None,
     [JUN_17, JUL_17], [JUN_17, JUL_17], RollConvention(RollConventionType.RollConvention(RollConventionType.DAY_17))],

    # stub StubConvention(StubConventionType.SHORT_INITIAL)
    [JUN_04, SEP_17, Frequency(months=1),
     StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_INITIAL)), None, BDA, None, None, None,
     [JUN_04, JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_04, JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.RollConvention(RollConventionType.DAY_17))],
    [JUN_17, SEP_17, Frequency(months=1),
     StubConvention(StubConventionType.StubConvention(StubConventionType.SHORT_INITIAL)), None, BDA, None, None, None,
     [JUN_17, JUL_17, AUG_17, SEP_17], [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.RollConvention(RollConventionType.DAY_17))],
    [JUN_17, JUL_04, Frequency(months=1), StubConvention(StubConventionType.SHORT_INITIAL), None, BDA, None, None, None,
     [JUN_17, JUL_04], [JUN_17, JUL_04], RollConvention(RollConventionType.DAY_4)],
    [datetime(2011, 6, 28), datetime(2011, 6, 30), Frequency(months=1),
     StubConvention(StubConventionType.SHORT_INITIAL), RollConvention(RollConventionType.EOM), BDA, None, None, None,
     [datetime(2011, 6, 28), datetime(2011, 6, 30)],
     [datetime(2011, 6, 28), datetime(2011, 6, 30)],
     RollConvention(RollConventionType.RollConvention(RollConventionType.EOM))],
    [datetime(2014, 12, 12), datetime(2015, 8, 24), Frequency(months=3),
     StubConvention(StubConventionType.SHORT_INITIAL), None, BDA, None, None, None,
     [datetime(2014, 12, 12), datetime(2015, 2, 24), datetime(2015, 5, 24), datetime(2015, 8, 24)],
     [datetime(2014, 12, 12), datetime(2015, 2, 24), datetime(2015, 5, 25), datetime(2015, 8, 24)], RollConvention(RollConventionType.DAY_24)],
    [datetime(2014, 12, 12), datetime(2015, 8, 24), Frequency(months=3),
     StubConvention(StubConventionType.SHORT_INITIAL), RollConvention(RollConventionType.NONE), BDA, None, None, None,
     [datetime(2014, 12, 12), datetime(2015, 2, 24), datetime(2015, 5, 24), datetime(2015, 8, 24)],
     [datetime(2014, 12, 12), datetime(2015, 2, 24), datetime(2015, 5, 25), datetime(2015, 8, 24)], RollConvention(RollConventionType.DAY_24)],
    [datetime(2014, 11, 24), datetime(2015, 8, 24), Frequency(months=3), None, RollConvention(RollConventionType.NONE), BDA, None, None,
     None,
     [datetime(2014, 11, 24), datetime(2015, 2, 24), datetime(2015, 5, 24), datetime(2015, 8, 24)],
     [datetime(2014, 11, 24), datetime(2015, 2, 24), datetime(2015, 5, 25), datetime(2015, 8, 24)], RollConvention(RollConventionType.DAY_24)],

    # stub StubConvention(StubConventionType.LONG_INITIAL)
    [JUN_04, SEP_17, Frequency(months=1), StubConvention(StubConventionType.LONG_INITIAL), None, BDA, None, None, None,
     [JUN_04, JUL_17, AUG_17, SEP_17],
     [JUN_04, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_17, SEP_17, Frequency(months=1), StubConvention(StubConventionType.LONG_INITIAL), None, BDA, None, None, None,
     [JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_17, JUL_04, Frequency(months=1), StubConvention(StubConventionType.LONG_INITIAL), None, BDA, None, None, None,
     [JUN_17, JUL_04], [JUN_17, JUL_04], RollConvention(RollConventionType.DAY_4)],
    [JUN_17, AUG_04, Frequency(months=1), StubConvention(StubConventionType.LONG_INITIAL), None, BDA, None, None, None,
     [JUN_17, AUG_04], [JUN_17, AUG_04], RollConvention(RollConventionType.DAY_4)],

    # stub StubConvention(StubConventionType.SMART_INITIAL)
    [JUN_04, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SMART_INITIAL), None, BDA, None, None, None,
     [JUN_04, JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_04, JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_10, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SMART_INITIAL), None, BDA, None, None, None,
     [JUN_10, JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_10, JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_11, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SMART_INITIAL), None, BDA, None, None, None,
     [JUN_11, JUL_17, AUG_17, SEP_17],
     [JUN_11, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_17, JUL_04, Frequency(months=1), StubConvention(StubConventionType.SMART_INITIAL), None, BDA, None, None, None,
     [JUN_17, JUL_04], [JUN_17, JUL_04], RollConvention(RollConventionType.DAY_4)],

    # stub StubConvention(StubConventionType.SHORT_FINAL)
    [JUN_04, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SHORT_FINAL), None, BDA, None, None, None,
     [JUN_04, JUL_04, AUG_04, SEP_04, SEP_17], [JUN_04, JUL_04, AUG_04, SEP_04, SEP_17], RollConvention(RollConventionType.DAY_4)],
    [JUN_17, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SHORT_FINAL), None, BDA, None, None, None,
     [JUN_17, JUL_17, AUG_17, SEP_17], [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_17, JUL_04, Frequency(months=1), StubConvention(StubConventionType.SHORT_FINAL), None, BDA, None, None, None,
     [JUN_17, JUL_04], [JUN_17, JUL_04], RollConvention(RollConventionType.DAY_17)],
    [datetime(2011, 6, 28), datetime(2011, 6, 30), Frequency(months=1), StubConvention(StubConventionType.SHORT_FINAL),
     RollConvention(RollConventionType.EOM), BDA, None, None, None,
     [datetime(2011, 6, 28), datetime(2011, 6, 30)],
     [datetime(2011, 6, 28), datetime(2011, 6, 30)], RollConvention(RollConventionType.DAY_28)],
    [datetime(2014, 11, 29), datetime(2015, 9, 2), Frequency(months=3), StubConvention(StubConventionType.SHORT_FINAL), None, BDA, None, None, None,
     [datetime(2014, 11, 29), datetime(2015, 2, 28), datetime(2015, 5, 29), datetime(2015, 8, 29),
          datetime(2015, 9, 2)],
     [datetime(2014, 11, 28), datetime(2015, 2, 27), datetime(2015, 5, 29), datetime(2015, 8, 31),
          datetime(2015, 9, 2)],
     RollConvention(RollConventionType.DAY_29)],
    [datetime(2014, 11, 29), datetime(2015, 9, 2), Frequency(months=3), StubConvention(StubConventionType.SHORT_FINAL), RollConventions.NONE, BDA, None,
     None, None,
     [datetime(2014, 11, 29), datetime(2015, 2, 28), datetime(2015, 5, 29), datetime(2015, 8, 29),
          datetime(2015, 9, 2)],
     [datetime(2014, 11, 28), datetime(2015, 2, 27), datetime(2015, 5, 29), datetime(2015, 8, 31),
          datetime(2015, 9, 2)],
     RollConvention(RollConventionType.DAY_29)],

    # stub StubConvention(StubConventionType.LONG_FINAL)
    [JUN_04, SEP_17, Frequency(months=1), StubConvention(StubConventionType.LONG_FINAL), None, BDA, None, None, None,
     [JUN_04, JUL_04, AUG_04, SEP_17],
     [JUN_04, JUL_04, AUG_04, SEP_17], RollConvention(RollConventionType.DAY_4)],
    [JUN_17, SEP_17, Frequency(months=1), StubConvention(StubConventionType.LONG_FINAL), None, BDA, None, None, None,
     [JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_17, JUL_04, Frequency(months=1), StubConvention(StubConventionType.LONG_FINAL), None, BDA, None, None, None,
     [JUN_17, JUL_04],
     [JUN_17, JUL_04], RollConvention(RollConventionType.DAY_17)],
    [JUN_17, AUG_04, Frequency(months=1), StubConvention(StubConventionType.LONG_FINAL), None, BDA, None, None, None,
     [JUN_17, AUG_04],
     [JUN_17, AUG_04], RollConvention(RollConventionType.DAY_17)],

    # stub StubConvention(StubConventionType.SMART_FINAL)
    [JUN_04, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SMART_FINAL), None, BDA, None, None, None,
     [JUN_04, JUL_04, AUG_04, SEP_04, SEP_17],
     [JUN_04, JUL_04, AUG_04, SEP_04, SEP_17], RollConvention(RollConventionType.DAY_4)],
    [JUN_04, SEP_11, Frequency(months=1), StubConvention(StubConventionType.SMART_FINAL), None, BDA, None, None, None,
     [JUN_04, JUL_04, AUG_04, SEP_04, SEP_11],
     [JUN_04, JUL_04, AUG_04, SEP_04, SEP_11], RollConvention(RollConventionType.DAY_4)],
    [JUN_04, SEP_10, Frequency(months=1), StubConvention(StubConventionType.SMART_FINAL), None, BDA, None, None, None,
     [JUN_04, JUL_04, AUG_04, SEP_10],
     [JUN_04, JUL_04, AUG_04, SEP_10], RollConvention(RollConventionType.DAY_4)],
    [JUN_17, JUL_04, Frequency(months=1), StubConvention(StubConventionType.SMART_FINAL), None, BDA, None, None, None,
     [JUN_17, JUL_04],
     [JUN_17, JUL_04], RollConvention(RollConventionType.DAY_17)],

    # explicit initial stub
    [JUN_04, SEP_17, Frequency(months=1), None, None, BDA, JUN_17, None, None,
     [JUN_04, JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_04, JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_04, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SHORT_INITIAL), None, BDA, JUN_17, None,
     None,
     [JUN_04, JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_04, JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_17, SEP_17, Frequency(months=1), None, None, BDA, JUN_17, None, None,
     [JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_04, SEP_04, Frequency(months=1), StubConvention(StubConventionType.SMART_FINAL), None, BDA, JUN_17, None, None,
     [JUN_04, JUN_17, JUL_17, AUG_17, SEP_04],
     [JUN_04, JUN_17, JUL_17, AUG_18, SEP_04], RollConvention(RollConventionType.DAY_17)],

    # explicit final stub
    [JUN_04, SEP_17, Frequency(months=1), None, None, BDA, None, AUG_04, None,
     [JUN_04, JUL_04, AUG_04, SEP_17],
     [JUN_04, JUL_04, AUG_04, SEP_17], RollConvention(RollConventionType.DAY_4)],
    [JUN_04, SEP_17, Frequency(months=1), StubConvention(StubConventionType.SHORT_FINAL), None, BDA, None, AUG_04, None,
     [JUN_04, JUL_04, AUG_04, SEP_17],
     [JUN_04, JUL_04, AUG_04, SEP_17], RollConvention(RollConventionType.DAY_4)],
    [JUN_17, SEP_17, Frequency(months=1), None, None, BDA, None, AUG_17, None,
     [JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_04, SEP_04, Frequency(months=1), StubConvention(StubConventionType.SMART_INITIAL), None, BDA, None, AUG_17, None,
     [JUN_04, JUN_17, JUL_17, AUG_17, SEP_04],
     [JUN_04, JUN_17, JUL_17, AUG_18, SEP_04], RollConvention(RollConventionType.DAY_17)],

    # explicit double stub
    [JUN_04, SEP_17, Frequency(months=1), None, None, BDA, JUL_11, AUG_11, None,
     [JUN_04, JUL_11, AUG_11, SEP_17],
     [JUN_04, JUL_11, AUG_11, SEP_17], RollConvention(RollConventionType.DAY_11)],
    [JUN_04, OCT_17, Frequency(months=1), STUB_BOTH, None, BDA, JUL_11, SEP_11, None,
     [JUN_04, JUL_11, AUG_11, SEP_11, OCT_17],
     [JUN_04, JUL_11, AUG_11, SEP_11, OCT_17], RollConvention(RollConventionType.DAY_11)],
    [JUN_17, SEP_17, Frequency(months=1), None, None, BDA, JUN_17, SEP_17, None,
     [JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],

    # stub None derive from roll convention
    [JUN_04, SEP_17, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, None, None, None,
     [JUN_04, JUN_17, JUL_17, AUG_17, SEP_17],
     [JUN_04, JUN_17, JUL_17, AUG_18, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_04, SEP_17, Frequency(months=1), None, RollConvention(RollConventionType.DAY_4), BDA, None, None, None,
     [JUN_04, JUL_04, AUG_04, SEP_04, SEP_17],
     [JUN_04, JUL_04, AUG_04, SEP_04, SEP_17], RollConvention(RollConventionType.DAY_4)],

    # near end of month
    # RollConvention(RollConventionType.EOM) flag false, thus roll on 30 th
    [NOV_30_2013, NOV_30, Frequency(months=3), STUB_NONE, None, BDA, None, None, None,
     [NOV_30_2013, FEB_28, MAY_30, AUG_30, NOV_30],
     [NOV_29_2013, FEB_28, MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.DAY_30)],
    # RollConvention(RollConventionType.EOM) flag true and is RollConvention(RollConventionType.EOM), thus roll at RollConvention(RollConventionType.EOM)
    [NOV_30_2013, NOV_30, Frequency(months=3), STUB_NONE, RollConvention(RollConventionType.EOM), BDA, None, None, None,
     [NOV_30_2013, FEB_28, MAY_31, AUG_31, NOV_30],
     [NOV_29_2013, FEB_28, MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag true, and last business day, thus roll at RollConvention(RollConventionType.EOM)(stub convention defined)
    [MAY_30, NOV_30, Frequency(months=3), STUB_NONE, RollConvention(RollConventionType.EOM), BDA, None, None, None,
     [MAY_31, AUG_31, NOV_30],
     [MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag true, and last business day, thus roll at RollConvention(RollConventionType.EOM)
    [MAY_30, NOV_30, Frequency(months=3), None, RollConvention(RollConventionType.EOM), BDA, None, None, None,
     [MAY_31, AUG_31, NOV_30],
     [MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag true, and last business day, thus roll at RollConvention(RollConventionType.EOM)(start adjustment none)
    [MAY_30, NOV_30, Frequency(months=3), None, RollConvention(RollConventionType.EOM), BDA, None, None, BDA_NONE,
     [MAY_31, AUG_31, NOV_30],
     [MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.EOM)],
    # roll datetime set to 30 th, so roll on 30 th
    [MAY_30, NOV_30, Frequency(months=3), None, RollConvention(RollConventionType.DAY_30), BDA, None, None, None,
     [MAY_30, AUG_30, NOV_30],
     [MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.DAY_30)],
    # RollConvention(RollConventionType.EOM) flag true, but not RollConvention(RollConventionType.EOM), thus roll on 30 th
    [JUL_30, OCT_30, Frequency(months=1), None, RollConvention(RollConventionType.EOM), BDA, None, None, None,
     [JUL_30, AUG_30, SEP_30, OCT_30],
     [JUL_30, AUG_29, SEP_30, OCT_30], RollConvention(RollConventionType.DAY_30)],
    # RollConvention(RollConventionType.EOM) flag true and is RollConvention(RollConventionType.EOM), double stub, thus roll at RollConvention(RollConventionType.EOM)
    [datetime(2014, 1, 3), SEP_17, Frequency(months=3), STUB_BOTH, RollConvention(RollConventionType.EOM), BDA, FEB_28,
     AUG_31, None,
     [datetime(2014, 1, 3), FEB_28, MAY_31, AUG_31, SEP_17],
     [datetime(2014, 1, 3), FEB_28, MAY_30, AUG_29, SEP_17], RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag true plus start datetime as last business day of month with start datetime adjust of NONE
    [NOV_29_2013, NOV_30, Frequency(months=3), STUB_NONE, RollConvention(RollConventionType.EOM), BDA, None, None,
     BDA_NONE,
     [NOV_30_2013, FEB_28, MAY_31, AUG_31, NOV_30],
     [NOV_29_2013, FEB_28, MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag true plus start datetime as last business day of month with start datetime adjust of NONE
    [NOV_29_2013, NOV_30, Frequency(months=3), None, RollConvention(RollConventionType.EOM), BDA, None, None, BDA_NONE,
     [NOV_30_2013, FEB_28, MAY_31, AUG_31, NOV_30],
     [NOV_29_2013, FEB_28, MAY_30, AUG_29, NOV_28], RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag false, short initial, implies RollConvention(RollConventionType.EOM) true
    [datetime(2011, 6, 2), datetime(2011, 8, 31), Frequency(months=1), StubConvention(StubConventionType.SHORT_INITIAL),
     None, BDA, None, None, None,
     [datetime(2011, 6, 2), datetime(2011, 6, 30), datetime(2011, 7, 31), datetime(2011, 8, 31)],
     [datetime(2011, 6, 2), datetime(2011, 6, 30), datetime(2011, 7, 29), datetime(2011, 8, 31)],
     RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag false, explicit stub, implies RollConvention(RollConventionType.EOM) true
    [datetime(2011, 6, 2), datetime(2011, 8, 31), Frequency(months=1), None, None, BDA, datetime(2011, 6, 30), None,
     None,
     [datetime(2011, 6, 2), datetime(2011, 6, 30), datetime(2011, 7, 31), datetime(2011, 8, 31)],
     [datetime(2011, 6, 2), datetime(2011, 6, 30), datetime(2011, 7, 29), datetime(2011, 8, 31)],
     RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag false, explicit stub, implies RollConvention(RollConventionType.EOM) true
    [datetime(2011, 7, 31), datetime(2011, 10, 10), Frequency(months=1), None, None, BDA, None, datetime(2011, 9, 30),
     None,
     [datetime(2011, 7, 31), datetime(2011, 8, 31), datetime(2011, 9, 30), datetime(2011, 10, 10)],
     [datetime(2011, 7, 29), datetime(2011, 8, 31), datetime(2011, 9, 30), datetime(2011, 10, 10)],
     RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag false, explicit stub, implies RollConvention(RollConventionType.EOM) true
    [datetime(2011, 2, 2), datetime(2011, 5, 30), Frequency(months=1), None, None, BDA, datetime(2011, 2, 28), None,
     None,
     [datetime(2011, 2, 2), datetime(2011, 2, 28), datetime(2011, 3, 30), datetime(2011, 4, 30),
          datetime(2011, 5, 30)],
     [datetime(2011, 2, 2), datetime(2011, 2, 28), datetime(2011, 3, 30), datetime(2011, 4, 29),
          datetime(2011, 5, 30)],
     RollConvention(RollConventionType.DAY_30)],
    # RollConvention(RollConventionType.EOM) flag true and is RollConvention(RollConventionType.EOM), but end datetime equals start day rather than RollConvention(RollConventionType.EOM)
    [datetime(2018, 2, 28), datetime(2024, 2, 28), Frequency.ofYears(2), STUB_NONE,
     RollConvention(RollConventionType.EOM), BDA, None, None, None,
     [datetime(2018, 2, 28), datetime(2020, 2, 29), datetime(2022, 2, 28), datetime(2024, 2, 28)],
     [datetime(2018, 2, 28), datetime(2020, 2, 28), datetime(2022, 2, 28), datetime(2024, 2, 28)],
     RollConvention(RollConventionType.EOM)],
    # RollConvention(RollConventionType.EOM) flag true and is RollConvention(RollConventionType.EOM), but end datetime equals start day rather than RollConvention(RollConventionType.EOM)
    [datetime(2018, 4, 30), datetime(2018, 10, 30), P2M, STUB_NONE, RollConvention(RollConventionType.EOM), BDA, None,
     None, None,
     [datetime(2018, 4, 30), datetime(2018, 6, 30), datetime(2018, 8, 31), datetime(2018, 10, 30)],
     [datetime(2018, 4, 30), datetime(2018, 6, 29), datetime(2018, 8, 31), datetime(2018, 10, 30)],
     RollConvention(RollConventionType.EOM)],

    # pre - adjusted start datetime, no change needed
    [JUL_17, OCT_17, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, None, None, BDA_NONE,
     [JUL_17, AUG_17, SEP_17, OCT_17],
     [JUL_17, AUG_18, SEP_17, OCT_17], RollConvention(RollConventionType.DAY_17)],
    # pre - adjusted start datetime, change needed
    [AUG_18, OCT_17, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, None, None, BDA_NONE,
     [AUG_17, SEP_17, OCT_17],
     [AUG_18, SEP_17, OCT_17], RollConvention(RollConventionType.DAY_17)],
    # pre - adjusted first regular, change needed
    [JUL_11, OCT_17, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, AUG_18, None, BDA_NONE,
     [JUL_11, AUG_17, SEP_17, OCT_17],
     [JUL_11, AUG_18, SEP_17, OCT_17], RollConvention(RollConventionType.DAY_17)],
    # pre - adjusted last regular, change needed
    [JUL_17, OCT_17, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, None, AUG_18, BDA_NONE,
     [JUL_17, AUG_17, OCT_17],
     [JUL_17, AUG_18, OCT_17], RollConvention(RollConventionType.DAY_17)],
    # pre - adjusted first + last regular, change needed
    [APR_01, OCT_17, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, MAY_19, AUG_18, BDA_NONE,
     [APR_01, MAY_17, JUN_17, JUL_17, AUG_17, OCT_17],
     [APR_01, MAY_19, JUN_17, JUL_17, AUG_18, OCT_17], RollConvention(RollConventionType.DAY_17)],
    # pre - adjusted end datetime, change needed
    [JUL_17, AUG_18, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, None, None, BDA_NONE,
     [JUL_17, AUG_17],
     [JUL_17, AUG_18], RollConvention(RollConventionType.DAY_17)],
    # pre - adjusted end datetime, change needed, with adjustment
    [JUL_17, AUG_18, Frequency(months=1), None, RollConvention(RollConventionType.DAY_17), BDA, None, None, BDA,
         [JUL_17, AUG_17],
         [JUL_17, AUG_18], RollConvention(RollConventionType.DAY_17)],

    # Frequency() period
    [JUN_04, SEP_17, Frequency(), STUB_NONE, None, BDA, None, None, None,
     [JUN_04, SEP_17],
     [JUN_04, SEP_17], ROLL_NONE],
    # Frequency() period defined as a stub and no regular periods
    [JUN_04, SEP_17, Frequency(months=12), StubConvention(StubConventionType.SHORT_INITIAL), None, BDA, SEP_17, None, None,
     [JUN_04, SEP_17],
     [JUN_04, SEP_17], RollConvention(RollConventionType.DAY_17)],
    [JUN_04, SEP_17, Frequency(months=12), StubConvention(StubConventionType.SHORT_INITIAL), None, BDA, None, JUN_04, None,
     [JUN_04, SEP_17],
     [JUN_04, SEP_17], RollConvention(RollConventionType.DAY_4)],
    [datetime(2014, 9, 24), datetime(2016, 11, 24), Frequency.ofYears(2),
     StubConvention(StubConventionType.SHORT_INITIAL), None, BDA, None, None, None,
     [datetime(2014, 9, 24), datetime(2014, 11, 24), datetime(2016, 11, 24)],
     [datetime(2014, 9, 24), datetime(2014, 11, 24), datetime(2016, 11, 24)], RollConvention(RollConventionType.DAY_24)],

    # RollConvention(RollConventionType.IMM)
    [datetime(2014, 9, 17), datetime(2014, 10, 15), Frequency(months=1), STUB_NONE, RollConvention(RollConventionType.IMM), BDA, None, None, None,
     [datetime(2014, 9, 17), datetime(2014, 10, 15)],
     [datetime(2014, 9, 17), datetime(2014, 10, 15)], RollConvention(RollConventionType.IMM)],
    [datetime(2014, 9, 17), datetime(2014, 10, 15), Frequency(), STUB_NONE, RollConvention(RollConventionType.IMM), BDA, None, None, None,
     [datetime(2014, 9, 17), datetime(2014, 10, 15)],
     [datetime(2014, 9, 17), datetime(2014, 10, 15)], RollConvention(RollConventionType.IMM)],
    # RollConvention(RollConventionType.IMM) with stupid short period still works
    [datetime(2014, 9, 17), datetime(2014, 10, 15), Frequency.ofDays(2), STUB_NONE, RollConvention(RollConventionType.IMM), BDA, None, None, None,
     [datetime(2014, 9, 17), datetime(2014, 10, 15)],
     [datetime(2014, 9, 17), datetime(2014, 10, 15)], RollConvention(RollConventionType.IMM)],
    [datetime(2014, 9, 17), datetime(2014, 10, 1), Frequency.ofDays(2), STUB_NONE, RollConvention(RollConventionType.IMM), BDA, None, None, None,
     [datetime(2014, 9, 17), datetime(2014, 10, 1)],
     [datetime(2014, 9, 17), datetime(2014, 10, 1)], RollConvention(RollConventionType.IMM)],

    # RollConvention(RollConventionType.IMM) with adjusted start datetimes and various conventions
    # MF, no stub
    [datetime(2018, 3, 22), datetime(2020, 3, 18), Frequency(months=6), STUB_NONE, RollConvention(RollConventionType.IMM), BDA_JPY_MF, None, None, BDA_NONE,
     [datetime(2018, 3, 21), datetime(2018, 9, 19), datetime(2019, 3, 20), datetime(2019, 9, 18),
          datetime(2020, 3, 18)],
     [datetime(2018, 3, 22), datetime(2018, 9, 19), datetime(2019, 3, 20), datetime(2019, 9, 18),
          datetime(2020, 3, 18)], RollConvention(RollConventionType.IMM)],
    # Preceding, no stub
    [datetime(2018, 3, 20), datetime(2019, 3, 20), Frequency(months=6), STUB_NONE, RollConvention(RollConventionType.IMM), BDA_JPY_P, None, None, BDA_NONE,
     [datetime(2018, 3, 21), datetime(2018, 9, 19), datetime(2019, 3, 20)],
     [datetime(2018, 3, 20), datetime(2018, 9, 19), datetime(2019, 3, 2])), RollConvention(RollConventionType.IMM)],
    # MF, None stub
    [datetime(2018, 3, 22), datetime(2019, 3, 20), Frequency(months=6), None, RollConvention(RollConventionType.IMM), BDA_JPY_MF, None, None, BDA_NONE,
     [datetime(2018, 3, 21), datetime(2018, 9, 19), datetime(2019, 3, 20)],
     [datetime(2018, 3, 22), datetime(2018, 9, 19), datetime(2019, 3, 20)], RollConvention(RollConventionType.IMM)],
    # Explicit long front stub with (adjusted) first regular start datetime
    [datetime(2017, 9, 2), datetime(2018, 9, 19), Frequency(months=6), StubConvention(StubConventionType.LONG_INITIAL), RollConvention(RollConventionType.IMM), BDA_JPY_MF, datetime(2018, 3, 22), None,
     BDA_NONE,
     [datetime(2017, 9, 2), datetime(2018, 3, 21), datetime(2018, 9, 19)],
     [datetime(2017, 9, 2), datetime(2018, 3, 22), datetime(2018, 9, 19)], RollConvention(RollConventionType.IMM)],
    # Implicit short front stub with (adjusted) first regular start datetime
    [datetime(2018, 1, 2), datetime(2018, 9, 19), Frequency(months=6), None, RollConvention(RollConventionType.IMM), BDA_JPY_MF, datetime(2018, 3, 22), None, BDA_NONE,
     [datetime(2018, 1, 2), datetime(2018, 3, 21), datetime(2018, 9, 19)],
     [datetime(2018, 1, 2), datetime(2018, 3, 22), datetime(2018, 9, 19)], RollConvention(RollConventionType.IMM)],
    # Implicit back stub with (adjusted) last regular start datetime
    [datetime(2017, 3, 15), datetime(2018, 5, 19), Frequency(months=6), None, RollConvention(RollConventionType.IMM), BDA_JPY_MF, None, datetime(2018, 3, 22), BDA_NONE,
     [datetime(2017, 3, 15), datetime(2017, 9, 20), datetime(2018, 3, 21), datetime(2018, 5, 19)],
     [datetime(2017, 3, 15), datetime(2017, 9, 20), datetime(2018, 3, 22), datetime(2018, 5, 21)], RollConvention(RollConventionType.IMM)],

    # Day30 rolling with February
    [datetime(2015, 1, 30), datetime(2015, 4, 30), Frequency(months=1), STUB_NONE, RollConvention(RollConventionType.DAY_30), BDA, None, None, None,
         [datetime(2015, 1, 30), datetime(2015, 2, 28), datetime(2015, 3, 30), datetime(2015, 4, 30)],
         [datetime(2015, 1, 30), datetime(2015, 2, 27), datetime(2015, 3, 30), datetime(2015, 4, 30)], RollConvention(RollConventionType.DAY_30)],
    [datetime(2015, 2, 28), datetime(2015, 4, 30), Frequency(months=1), STUB_NONE, RollConvention(RollConventionType.DAY_30), BDA, None, None, None,
     [datetime(2015, 2, 28), datetime(2015, 3, 30), datetime(2015, 4, 30)],
     [datetime(2015, 2, 27), datetime(2015, 3, 30), datetime(2015, 4, 30)], RollConvention(RollConventionType.DAY_30)],
    [datetime(2015, 2, 28), datetime(2015, 4, 30), Frequency(months=1),
     StubConvention(StubConventionType.SHORT_INITIAL), RollConvention(RollConventionType.DAY_30), BDA, None, None, None,
     [datetime(2015, 2, 28), datetime(2015, 3, 30), datetime(2015, 4, 30)],
     [datetime(2015, 2, 27), datetime(2015, 3, 30), datetime(2015, 4, 30)], RollConvention(RollConventionType.DAY_30)],

    # Two stubs no regular
    [datetime(2019, 1, 16), datetime(2020, 10, 22), Frequency(months=12), None, RollConvention(RollConventionType.DAY_22), BDA, datetime(2020, 1, 22),
     datetime(2020, 1, 22), None,
     [datetime(2019, 1, 16), datetime(2020, 1, 22), datetime(2020, 10, 22)],
     [datetime(2019, 1, 16), datetime(2020, 1, 22), datetime(2020, 10, 22)], RollConvention(RollConventionType.DAY_22)],
    [datetime(2019, 1, 16), datetime(2020, 10, 22), Frequency(months=12), STUB_BOTH, RollConvention(RollConventionType.DAY_22), BDA, datetime(2020, 1, 22),
     datetime(2020, 1, 22),
     None,
     [datetime(2019, 1, 16), datetime(2020, 1, 22), datetime(2020, 10, 22)],
     [datetime(2019, 1, 16), datetime(2020, 1, 22), datetime(2020, 10, 22)], RollConvention(RollConventionType.DAY_22)],
]


if __name__ == '__main__':
    test_local_date_eom_false()
