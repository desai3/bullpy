from datetime import datetime

import pytest
from IPython.core.debugger import set_trace

from stub_convention import StubConvention, StubConventionType
from roll_convention import RollConvention, RollConventionType
from frequency import Frequency


def test_None():
    for sct in StubConventionType:
        sc = StubConvention(sct)

        with pytest.raises(AssertionError):
            sc.to_roll_convention(None, datetime(2014, 7, 1), Frequency(months=3), True)
        with pytest.raises(AssertionError):
            sc.to_roll_convention(datetime(2014, 7, 1), None, Frequency(months=3), True)
        with pytest.raises(AssertionError):
            sc.to_roll_convention(datetime(2014, 7, 1), datetime(2014, 10, 1), None, True)


def test_to_roll_convention():
    data = [[StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), False,
             RollConventionType.DAY_14],
            [StubConventionType.NONE, datetime(2014, 1, 14), datetime(2014, 8, 16), Frequency(months=1), True,
             RollConventionType.DAY_14],

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
             RollConventionType.DAY_14]
            ]

    for sct, start, end, freq, eom, rct in data:
        res = StubConvention(sct).to_roll_convention(start, end, freq, eom)
        ans = RollConvention(rct)
        assert res == ans


def test_to_implicit():
    data = [[StubConventionType.NONE, False, False, StubConventionType.NONE],
            [StubConventionType.NONE, True, False, None],
            [StubConventionType.NONE, False, True, None],
            [StubConventionType.NONE, True, True, None],

            [StubConventionType.SHORT_INITIAL, False, False, StubConventionType.SHORT_INITIAL],
            [StubConventionType.SHORT_INITIAL, True, False, StubConventionType.NONE],
            [StubConventionType.SHORT_INITIAL, False, True, None],
            [StubConventionType.SHORT_INITIAL, True, True, None],

            [StubConventionType.LONG_INITIAL, False, False, StubConventionType.LONG_INITIAL],
            [StubConventionType.LONG_INITIAL, True, False, StubConventionType.NONE],
            [StubConventionType.LONG_INITIAL, False, True, None],
            [StubConventionType.LONG_INITIAL, True, True, None],

            [StubConventionType.SMART_INITIAL, False, False, StubConventionType.SMART_INITIAL],
            [StubConventionType.SMART_INITIAL, True, False, StubConventionType.NONE],
            [StubConventionType.SMART_INITIAL, False, True, StubConventionType.SMART_INITIAL],
            [StubConventionType.SMART_INITIAL, True, True, StubConventionType.BOTH],

            [StubConventionType.SHORT_FINAL, False, False, StubConventionType.SHORT_FINAL],
            [StubConventionType.SHORT_FINAL, True, False, None],
            [StubConventionType.SHORT_FINAL, False, True, StubConventionType.NONE],
            [StubConventionType.SHORT_FINAL, True, True, None],

            [StubConventionType.LONG_FINAL, False, False, StubConventionType.LONG_FINAL],
            [StubConventionType.LONG_FINAL, True, False, None],
            [StubConventionType.LONG_FINAL, False, True, StubConventionType.NONE],
            [StubConventionType.LONG_FINAL, True, True, None],

            [StubConventionType.SMART_FINAL, False, False, StubConventionType.SMART_FINAL],
            [StubConventionType.SMART_FINAL, True, False, StubConventionType.SMART_FINAL],
            [StubConventionType.SMART_FINAL, False, True, StubConventionType.NONE],
            [StubConventionType.SMART_FINAL, True, True, StubConventionType.BOTH],

            [StubConventionType.BOTH, False, False, None],
            [StubConventionType.BOTH, True, False, None],
            [StubConventionType.BOTH, False, True, None],
            [StubConventionType.BOTH, True, True, StubConventionType.NONE]]

    for sct1, istub, fstub, sct2 in data:
        if sct2 is None:
            with pytest.raises(ValueError):
                StubConvention(sct1).to_implicit(istub, fstub)
        else:
            assert StubConvention(sct1).to_implicit(istub, fstub) == StubConvention(sct2)


def test_is_stub_long():
    data = [[StubConventionType.NONE, datetime(2018, 6, 1), datetime(2018, 6, 8), False],
            [StubConventionType.SHORT_INITIAL, datetime(2018, 6, 1), datetime(2018, 6, 8), False],
            [StubConventionType.LONG_INITIAL, datetime(2018, 6, 1), datetime(2018, 6, 8), True],
            [StubConventionType.SHORT_FINAL, datetime(2018, 6, 1), datetime(2018, 6, 8), False],
            [StubConventionType.LONG_FINAL, datetime(2018, 6, 1), datetime(2018, 6, 8), True],
            [StubConventionType.BOTH, datetime(2018, 6, 1), datetime(2018, 6, 8), False],

            [StubConventionType.SMART_INITIAL, datetime(2018, 6, 1), datetime(2018, 6, 2), True],
            [StubConventionType.SMART_INITIAL, datetime(2018, 6, 1), datetime(2018, 6, 7), True],
            [StubConventionType.SMART_INITIAL, datetime(2018, 6, 1), datetime(2018, 6, 8), False],
            [StubConventionType.SMART_INITIAL, datetime(2018, 6, 1), datetime(2018, 6, 9), False],

            [StubConventionType.SMART_FINAL, datetime(2018, 6, 1), datetime(2018, 6, 2), True],
            [StubConventionType.SMART_FINAL, datetime(2018, 6, 1), datetime(2018, 6, 7), True],
            [StubConventionType.SMART_FINAL, datetime(2018, 6, 1), datetime(2018, 6, 8), False],
            [StubConventionType.SMART_FINAL, datetime(2018, 6, 1), datetime(2018, 6, 9), False]]

    for sct, d1, d2, ans in data:
        assert StubConvention(sct).is_stub_long(d1, d2) == ans


def test_none():
    assert StubConvention(StubConventionType.NONE).is_calculate_forwards()
    assert not StubConvention(StubConventionType.NONE).is_calculate_backwards()
    assert not StubConvention(StubConventionType.NONE).is_final()
    assert not StubConvention(StubConventionType.NONE).is_long()
    assert not StubConvention(StubConventionType.NONE).is_short()
    assert not StubConvention(StubConventionType.NONE).is_smart()


def test_short_initial():
    assert not StubConvention(StubConventionType.SHORT_INITIAL).is_calculate_forwards()
    assert StubConvention(StubConventionType.SHORT_INITIAL).is_calculate_backwards()
    assert not StubConvention(StubConventionType.SHORT_INITIAL).is_final()
    assert not StubConvention(StubConventionType.SHORT_INITIAL).is_long()
    assert StubConvention(StubConventionType.SHORT_INITIAL).is_short()
    assert not StubConvention(StubConventionType.SHORT_INITIAL).is_smart()


def test_long_initial():
    assert not StubConvention(StubConventionType.LONG_INITIAL).is_calculate_forwards()
    assert StubConvention(StubConventionType.LONG_INITIAL).is_calculate_backwards()
    assert not StubConvention(StubConventionType.LONG_INITIAL).is_final()
    assert StubConvention(StubConventionType.LONG_INITIAL).is_long()
    assert not StubConvention(StubConventionType.LONG_INITIAL).is_short()
    assert not StubConvention(StubConventionType.LONG_INITIAL).is_smart()


def test_smart_initial():
    assert not StubConvention(StubConventionType.SMART_INITIAL).is_calculate_forwards()
    assert StubConvention(StubConventionType.SMART_INITIAL).is_calculate_backwards()
    assert not StubConvention(StubConventionType.SMART_INITIAL).is_final()
    assert not StubConvention(StubConventionType.SMART_INITIAL).is_long()
    assert not StubConvention(StubConventionType.SMART_INITIAL).is_short()
    assert StubConvention(StubConventionType.SMART_INITIAL).is_smart()


def test_short_final():
    assert StubConvention(StubConventionType.SHORT_FINAL).is_calculate_forwards()
    assert not StubConvention(StubConventionType.SHORT_FINAL).is_calculate_backwards()
    assert StubConvention(StubConventionType.SHORT_FINAL).is_final()
    assert not StubConvention(StubConventionType.SHORT_FINAL).is_long()
    assert StubConvention(StubConventionType.SHORT_FINAL).is_short()
    assert not StubConvention(StubConventionType.SHORT_FINAL).is_smart()


def test_long_final():
    assert StubConvention(StubConventionType.LONG_FINAL).is_calculate_forwards()
    assert not StubConvention(StubConventionType.LONG_FINAL).is_calculate_backwards()
    assert StubConvention(StubConventionType.LONG_FINAL).is_final()
    assert StubConvention(StubConventionType.LONG_FINAL).is_long()
    assert not StubConvention(StubConventionType.LONG_FINAL).is_short()
    assert not StubConvention(StubConventionType.LONG_FINAL).is_smart()


def test_smart_final():
    assert StubConvention(StubConventionType.SMART_FINAL).is_calculate_forwards()
    assert not StubConvention(StubConventionType.SMART_FINAL).is_calculate_backwards()
    assert StubConvention(StubConventionType.SMART_FINAL).is_final()
    assert not StubConvention(StubConventionType.SMART_FINAL).is_long()
    assert not StubConvention(StubConventionType.SMART_FINAL).is_short()
    assert StubConvention(StubConventionType.SMART_FINAL).is_smart()


def test_both():
    assert not StubConvention(StubConventionType.BOTH).is_calculate_forwards()
    assert not StubConvention(StubConventionType.BOTH).is_calculate_backwards()
    assert not StubConvention(StubConventionType.BOTH).is_final()
    assert not StubConvention(StubConventionType.BOTH).is_long()
    assert not StubConvention(StubConventionType.BOTH).is_short()
    assert not StubConvention(StubConventionType.BOTH).is_smart()


if __name__ == '__main__':
    pass
