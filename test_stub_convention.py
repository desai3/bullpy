from datetime import datetime

import pytest
from IPython.core.debugger import set_trace

from stub_convention import StubConvention, StubConventionType
from roll_convention import RollConvention, RollConventionType
from frequency import Frequency


def test_null():
    for sct in StubConventionType:
        sc = StubConvention(sct)

        with pytest.raises(AssertionError):
            sc.to_roll_convention(None, datetime(2014, 7, 1), Frequency(months=3), True)
        with pytest.raises(AssertionError):
            sc.to_roll_convention(datetime(2014, 7, 1), None, Frequency(months=3), True)
        with pytest.raises(AssertionError):
            sc.to_roll_convention(datetime(2014, 7, 1), datetime(2014, 10, 1), None, True)


def test_to_roll_convention():
    data = [# [StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
            #  RollConventionType.DAY_14],
            # [StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
            #  RollConventionType.DAY_14],

            [StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), False,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), True,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), False,
             RollConventionType.NONE],
            [StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), True,
             RollConventionType.NONE],
            [StubConventionType.NONE, datetime(2014, 1, 31), datetime(2014, 4, 30), Frequency(months=1), True,
             RollConventionType.EOM],
            [StubConventionType.NONE, datetime(2014, 4, 30), datetime(2014, 8, 31), Frequency(months=1), True,
             RollConventionType.EOM],
            [StubConventionType.NONE, datetime(2014, 4, 30), datetime(2014, 2, 28), Frequency(months=1), True,
             RollConventionType.EOM],
            [StubConventionType.NONE, datetime(2016, 2, 29), datetime(2019, 2, 28), Frequency(months=6), True,
             RollConventionType.EOM],
            [StubConventionType.NONE, datetime(2015, 2, 28), datetime(2016, 2, 29), Frequency(months=6), True,
             RollConventionType.EOM],
            [StubConventionType.NONE, datetime(2015, 4, 30), datetime(2016, 2, 29), Frequency(months=1), True,
             RollConventionType.EOM],
            [StubConventionType.NONE, datetime(2016, 3, 31), datetime(2017, 3, 27), Frequency(months=6), True,
             RollConventionType.EOM],
            [StubConventionType.NONE, datetime(2016, 3, 16), datetime(2016, 3, 31), Frequency(months=6), True,
             RollConventionType.DAY_16],
            [StubConventionType.NONE, datetime(2016, 3, 16), datetime(2017, 3, 31), Frequency(months=6), True,
             RollConventionType.EOM],

            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_16],
            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_16],
            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 6, 30), Frequency(months=1), False,
             RollConventionType.DAY_30],
            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 6, 30), Frequency(months=1), True,
             RollConventionType.EOM],

            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7),
             True, RollConventionType.WEEKDAY_SAT],
            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7),
             True, RollConventionType.WEEKDAY_SAT],
            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), False,
             RollConventionType.NONE],
            [StubConventionType.SHORT_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), True,
             RollConventionType.NONE],

            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_16],
            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_16],
            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 6, 30), Frequency(months=1), False,
             RollConventionType.DAY_30],
            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 6, 30), Frequency(months=1), True,
             RollConventionType.EOM],

            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7),
             False, RollConventionType.WEEKDAY_SAT],
            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), True,
             RollConventionType.WEEKDAY_SAT],
            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), False,
             RollConventionType.NONE],
            [StubConventionType.LONG_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), True,
             RollConventionType.NONE],

            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_16],
            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_16],
            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 6, 30), Frequency(months=1), False,
             RollConventionType.DAY_30],
            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 6, 30), Frequency(months=1), True,
             RollConventionType.EOM],

            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7),
             False, RollConventionType.WEEKDAY_SAT],
            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7),
             True, RollConventionType.WEEKDAY_SAT],
            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), False,
             RollConventionType.NONE],
            [StubConventionType.SMART_INITIAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), True,
             RollConventionType.NONE],

            [StubConventionType.SHORT_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_14],
            [StubConventionType.SHORT_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_14],
            [StubConventionType.SHORT_FINAL, datetime(2014, 6, 30), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_30],
            [StubConventionType.SHORT_FINAL, datetime(2014, 6, 30), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.EOM],

            [StubConventionType.SHORT_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), False,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.SHORT_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), True,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.SHORT_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), False,
             RollConventionType.NONE],
            [StubConventionType.SHORT_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), True,
             RollConventionType.NONE],

            [StubConventionType.LONG_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_14],
            [StubConventionType.LONG_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_14],
            [StubConventionType.LONG_FINAL, datetime(2014, 6, 30), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_30],
            [StubConventionType.LONG_FINAL, datetime(2014, 6, 30), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.EOM],

            [StubConventionType.LONG_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), False,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.LONG_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), True,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.LONG_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), False,
             RollConventionType.NONE],
            [StubConventionType.LONG_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), True,
             RollConventionType.NONE],

            [StubConventionType.SMART_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_14],
            [StubConventionType.SMART_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_14],
            [StubConventionType.SMART_FINAL, datetime(2014, 6, 30), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_30],
            [StubConventionType.SMART_FINAL, datetime(2014, 6, 30), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.EOM],

            [StubConventionType.SMART_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), False,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.SMART_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(days=2 * 7), True,
             RollConventionType.WEEKDAY_TUE],
            [StubConventionType.SMART_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), False,
             RollConventionType.NONE],
            [StubConventionType.SMART_FINAL, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(), True,
             RollConventionType.NONE],

            [StubConventionType.BOTH, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_14],
            [StubConventionType.BOTH, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_14]]

    count = 0
    for sct, start, end, freq, eom, rct in data:
        print(count)
        count += 1
        res = StubConvention(sct).to_roll_convention(start, end, freq, eom)
        ans = RollConvention(rct)
        assert res == ans


if __name__ == '__main__':
    test_to_roll_convention()
