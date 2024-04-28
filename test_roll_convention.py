from datetime import datetime
# from dateutil.relativedelta import relativedelta

from roll_convention import RollConventionType, RollConvention
from frequency import Frequency, plus_months

def test_none():
    dt = datetime(2014, 8, 17)
    rc = RollConvention(RollConventionType.NONE)
    assert rc.adjust(dt) == dt
    assert rc.matches(dt)


def test_standard_adjust():
    data = [[RollConventionType.EOM, datetime(2014, 8, 1), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 8, 30), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 9, 1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 9, 30), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 2, 1), datetime(2014, 2, 28)],

            [RollConventionType.DAY_31, datetime(2014, 8, 1), datetime(2014, 8, 31)],
            [RollConventionType.DAY_31, datetime(2014, 8, 30), datetime(2014, 8, 31)],
            [RollConventionType.DAY_31, datetime(2014, 9, 1), datetime(2014, 9, 30)],
            [RollConventionType.DAY_31, datetime(2014, 9, 30), datetime(2014, 9, 30)],
            [RollConventionType.DAY_31, datetime(2014, 2, 1), datetime(2014, 2, 28)],

            [RollConventionType.IMM, datetime(2014, 8, 1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 6), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 19), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 20), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 21), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 31), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 9, 1), datetime(2014, 9, 17)],

            [RollConventionType.IMMCAD, datetime(2014, 8, 1), datetime(2014, 8, 18)],
            [RollConventionType.IMMCAD, datetime(2014, 8, 6), datetime(2014, 8, 18)],
            [RollConventionType.IMMCAD, datetime(2014, 8, 7), datetime(2014, 8, 18)],
            [RollConventionType.IMMCAD, datetime(2014, 8, 8), datetime(2014, 8, 18)],
            [RollConventionType.IMMCAD, datetime(2014, 8, 31), datetime(2014, 8, 18)],
            [RollConventionType.IMMCAD, datetime(2014, 9, 1), datetime(2014, 9, 15)],

            [RollConventionType.IMMAUD, datetime(2014, 8, 1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 6), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 7), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 8), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 31), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 11, 1), datetime(2014, 11, 13)],

            [RollConventionType.IMMNZD, datetime(2014, 8, 1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 6), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 12), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 13), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 14), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 31), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 11, 1), datetime(2014, 11, 12)],

            [RollConventionType.SFE, datetime(2014, 8, 1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 6), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 7), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 8), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 31), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 9, 1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 11, 1), datetime(2014, 11, 14)],

            [RollConventionType.TBILL, datetime(2014, 8, 1), datetime(2014, 8, 4)],
            [RollConventionType.TBILL, datetime(2014, 8, 2), datetime(2014, 8, 4)],
            [RollConventionType.TBILL, datetime(2014, 8, 3), datetime(2014, 8, 4)],
            [RollConventionType.TBILL, datetime(2014, 8, 4), datetime(2014, 8, 4)],
            [RollConventionType.TBILL, datetime(2014, 8, 5), datetime(2014, 8, 11)],
            [RollConventionType.TBILL, datetime(2014, 8, 7), datetime(2014, 8, 11)],
            [RollConventionType.TBILL, datetime(2018, 8, 31), datetime(2018, 9, 4)],  # Tuesday due to holiday
            [RollConventionType.TBILL, datetime(2018, 9, 1), datetime(2018, 9, 4)]]

    for rct, d1, d2 in data:
        assert RollConvention(rct).adjust(d1) == d2


def test_standard_matches():
    data = [[RollConventionType.EOM, datetime(2014, 8, 1), False],
            [RollConventionType.EOM, datetime(2014, 8, 30), False],
            [RollConventionType.EOM, datetime(2014, 8, 31), True],
            [RollConventionType.EOM, datetime(2014, 9, 1), False],
            [RollConventionType.EOM, datetime(2014, 9, 30), True],

            [RollConventionType.DAY_31, datetime(2014, 8, 1), False],
            [RollConventionType.DAY_31, datetime(2014, 8, 30), False],
            [RollConventionType.DAY_31, datetime(2014, 8, 31), True],
            [RollConventionType.DAY_31, datetime(2014, 9, 1), False],
            [RollConventionType.DAY_31, datetime(2014, 9, 30), True],

            [RollConventionType.IMM, datetime(2014, 9, 16), False],
            [RollConventionType.IMM, datetime(2014, 9, 17), True],
            [RollConventionType.IMM, datetime(2014, 9, 18), False],

            [RollConventionType.IMMAUD, datetime(2014, 9, 10), False],
            [RollConventionType.IMMAUD, datetime(2014, 9, 11), True],
            [RollConventionType.IMMAUD, datetime(2014, 9, 12), False],

            [RollConventionType.IMMNZD, datetime(2014, 9, 9), False],
            [RollConventionType.IMMNZD, datetime(2014, 9, 10), True],
            [RollConventionType.IMMNZD, datetime(2014, 9, 11), False],

            [RollConventionType.SFE, datetime(2014, 9, 11), False],
            [RollConventionType.SFE, datetime(2014, 9, 12), True],
            [RollConventionType.SFE, datetime(2014, 9, 13), False]]

    for rct, d1, flag in data:
        assert RollConvention(rct).matches(d1) == flag


def test_standard_next():
    data = [[RollConventionType.EOM, datetime(2014, 8, 1), Frequency(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 8, 30), Frequency(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 8, 31), Frequency(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 9, 1), Frequency(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 9, 30), Frequency(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 1, 1), Frequency(months=1), datetime(2014, 2, 28)],
            [RollConventionType.EOM, datetime(2014, 2, 1), Frequency(months=1), datetime(2014, 3, 31)],
            [RollConventionType.EOM, datetime(2014, 8, 1), Frequency(months=3), datetime(2014, 11, 30)],
            [RollConventionType.EOM, datetime(2014, 8, 1), Frequency(days=1), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 8, 30), Frequency(days=1), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 8, 31), Frequency(days=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 1, 1), Frequency(days=1), datetime(2014, 1, 31)],
            [RollConventionType.EOM, datetime(2014, 1, 31), Frequency(days=1), datetime(2014, 2, 28)],
            [RollConventionType.EOM, datetime(2014, 2, 1), Frequency(days=1), datetime(2014, 2, 28)],

            [RollConventionType.IMM, datetime(2014, 8, 1), Frequency(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 8, 31), Frequency(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 1), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 9, 30), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 8, 1), Frequency(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 19), Frequency(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 20), Frequency(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 8, 31), Frequency(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 16), Frequency(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 17), Frequency(days=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 10, 15)],

            [RollConventionType.IMMAUD, datetime(2014, 8, 1), Frequency(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 31), Frequency(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 1), Frequency(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 30), Frequency(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 1), Frequency(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 6), Frequency(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 7), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 31), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 10), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 11), Frequency(days=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 10, 9)],

            [RollConventionType.IMMNZD, datetime(2014, 8, 1), Frequency(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 31), Frequency(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 1), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 30), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 1), Frequency(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 12), Frequency(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 13), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 31), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 9), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 10), Frequency(days=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 10, 15)],

            [RollConventionType.SFE, datetime(2014, 8, 1), Frequency(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 8, 31), Frequency(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 1), Frequency(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 9, 30), Frequency(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 8, 1), Frequency(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 7), Frequency(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 8), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 8, 31), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 11), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 12), Frequency(days=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 10, 10)]]
    for rct, d1, f, d2 in data:
        assert RollConvention(rct).next(d1, f) == d2


def test_standard_previous():
    data = [[RollConventionType.EOM, datetime(2014, 10, 1), Frequency(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 10, 31), Frequency(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 11, 1), Frequency(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 11, 30), Frequency(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 3, 1), Frequency(months=1), datetime(2014, 2, 28)],
            [RollConventionType.EOM, datetime(2014, 4, 1), Frequency(months=1), datetime(2014, 3, 31)],
            [RollConventionType.EOM, datetime(2014, 11, 1), Frequency(months=3), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 10, 1), Frequency(days=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 10, 30), Frequency(days=1), datetime(2014, 9, 30)],

            [RollConventionType.IMM, datetime(2014, 10, 1), Frequency(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 10, 31), Frequency(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 11, 1), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 11, 30), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 8, 1), Frequency(days=1), datetime(2014, 7, 16)],
            [RollConventionType.IMM, datetime(2014, 8, 20), Frequency(days=1), datetime(2014, 7, 16)],
            [RollConventionType.IMM, datetime(2014, 8, 21), Frequency(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 31), Frequency(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 9, 17), Frequency(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 9, 18), Frequency(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 9, 17)],

            [RollConventionType.IMMAUD, datetime(2014, 10, 1), Frequency(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 31), Frequency(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 11, 1), Frequency(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 11, 30), Frequency(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 11), Frequency(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 12), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 1), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 9), Frequency(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 10), Frequency(days=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 30), Frequency(days=1), datetime(2014, 10, 9)],

            [RollConventionType.IMMNZD, datetime(2014, 10, 1), Frequency(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 31), Frequency(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 11, 1), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 11, 30), Frequency(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 10), Frequency(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 11), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 1), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 15), Frequency(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 16), Frequency(days=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 30), Frequency(days=1), datetime(2014, 10, 15)],

            [RollConventionType.SFE, datetime(2014, 10, 1), Frequency(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 31), Frequency(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 11, 1), Frequency(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 11, 30), Frequency(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 9, 1), Frequency(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 9, 12), Frequency(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 9, 13), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 30), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 1), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 10), Frequency(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 11), Frequency(days=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 10, 30), Frequency(days=1), datetime(2014, 10, 10)]]
    for rct, d1, f, d2 in data:
        assert RollConvention(rct).previous(d1, f) == d2


def test_day_of_month_constant():
    data = [[RollConventionType.DAY_1, datetime(2014, 7, 30), datetime(2014, 7, 1)],
            [RollConventionType.DAY_2, datetime(2014, 7, 30), datetime(2014, 7, 2)],
            [RollConventionType.DAY_3, datetime(2014, 7, 30), datetime(2014, 7, 3)],
            [RollConventionType.DAY_4, datetime(2014, 7, 30), datetime(2014, 7, 4)],
            [RollConventionType.DAY_5, datetime(2014, 7, 30), datetime(2014, 7, 5)],
            [RollConventionType.DAY_6, datetime(2014, 7, 30), datetime(2014, 7, 6)],
            [RollConventionType.DAY_7, datetime(2014, 7, 30), datetime(2014, 7, 7)],
            [RollConventionType.DAY_8, datetime(2014, 7, 30), datetime(2014, 7, 8)],
            [RollConventionType.DAY_9, datetime(2014, 7, 30), datetime(2014, 7, 9)],
            [RollConventionType.DAY_10, datetime(2014, 7, 30), datetime(2014, 7, 10)],
            [RollConventionType.DAY_11, datetime(2014, 7, 30), datetime(2014, 7, 11)],
            [RollConventionType.DAY_12, datetime(2014, 7, 30), datetime(2014, 7, 12)],
            [RollConventionType.DAY_13, datetime(2014, 7, 30), datetime(2014, 7, 13)],
            [RollConventionType.DAY_14, datetime(2014, 7, 30), datetime(2014, 7, 14)],
            [RollConventionType.DAY_15, datetime(2014, 7, 30), datetime(2014, 7, 15)],
            [RollConventionType.DAY_16, datetime(2014, 7, 30), datetime(2014, 7, 16)],
            [RollConventionType.DAY_17, datetime(2014, 7, 30), datetime(2014, 7, 17)],
            [RollConventionType.DAY_18, datetime(2014, 7, 30), datetime(2014, 7, 18)],
            [RollConventionType.DAY_19, datetime(2014, 7, 30), datetime(2014, 7, 19)],
            [RollConventionType.DAY_20, datetime(2014, 7, 30), datetime(2014, 7, 20)],
            [RollConventionType.DAY_21, datetime(2014, 7, 30), datetime(2014, 7, 21)],
            [RollConventionType.DAY_22, datetime(2014, 7, 30), datetime(2014, 7, 22)],
            [RollConventionType.DAY_23, datetime(2014, 7, 30), datetime(2014, 7, 23)],
            [RollConventionType.DAY_24, datetime(2014, 7, 30), datetime(2014, 7, 24)],
            [RollConventionType.DAY_25, datetime(2014, 7, 30), datetime(2014, 7, 25)],
            [RollConventionType.DAY_26, datetime(2014, 7, 30), datetime(2014, 7, 26)],
            [RollConventionType.DAY_27, datetime(2014, 7, 30), datetime(2014, 7, 27)],
            [RollConventionType.DAY_28, datetime(2014, 7, 30), datetime(2014, 7, 28)],
            [RollConventionType.DAY_29, datetime(2014, 7, 30), datetime(2014, 7, 29)],
            [RollConventionType.DAY_30, datetime(2014, 7, 30), datetime(2014, 7, 30)]]
    for rct, d1, d2 in data:
        assert RollConvention(rct).adjust(d1) == d2


def test_day_of_month():
    for i in range(1, 31):
        rc = RollConvention(getattr(RollConventionType, f'DAY_{i}'))
        assert rc.adjust(datetime(2014, 7, 1)) == datetime(2014, 7, i)


def test_day_of_month_adjust_day29():
    assert RollConvention(RollConventionType.DAY_29).adjust(datetime(2014, 2, 2)) == datetime(2014, 2, 28)
    assert RollConvention(RollConventionType.DAY_29).adjust(datetime(2016, 2, 2)) == datetime(2016, 2, 29)


def test_day_of_month_adjust_day30():
    assert RollConvention(RollConventionType.DAY_30).adjust(datetime(2014, 2, 2)) == datetime(2014, 2, 28)
    assert RollConvention(RollConventionType.DAY_30).adjust(datetime(2016, 2, 2)) == datetime(2016, 2, 29)


def test_day_of_month_adjust_day29():
    assert not RollConvention(RollConventionType.DAY_29).matches(datetime(2016, 1, 30))
    assert RollConvention(RollConventionType.DAY_29).matches(datetime(2016, 1, 29))
    assert not RollConvention(RollConventionType.DAY_29).matches(datetime(2016, 1, 30))

    assert not RollConvention(RollConventionType.DAY_29).matches(datetime(2016, 2, 28))
    assert RollConvention(RollConventionType.DAY_29).matches(datetime(2016, 2, 29))

    assert not RollConvention(RollConventionType.DAY_29).matches(datetime(2015, 2, 27))
    assert RollConvention(RollConventionType.DAY_29).matches(datetime(2015, 2, 28))


def test_day_of_month_adjust_day30():
    assert not RollConvention(RollConventionType.DAY_30).matches(datetime(2016, 1, 29))
    assert RollConvention(RollConventionType.DAY_30).matches(datetime(2016, 1, 30))
    assert not RollConvention(RollConventionType.DAY_30).matches(datetime(2016, 1, 31))

    assert not RollConvention(RollConventionType.DAY_30).matches(datetime(2016, 2, 28))
    assert RollConvention(RollConventionType.DAY_30).matches(datetime(2016, 2, 29))

    assert not RollConvention(RollConventionType.DAY_30).matches(datetime(2015, 2, 27))
    assert RollConvention(RollConventionType.DAY_30).matches(datetime(2015, 2, 28))


def test_day_of_month_next_one_month():
    for start in range(1, 6):
        for i in range(1, 31):
            rc = RollConvention(getattr(RollConventionType, f'DAY_{i}'))
            assert rc.next(datetime(2014, 7, start), Frequency(months=1)) == datetime(2014, 8, i)


def test_day_of_month_next_one_day():
    for start in range(1, 6):
        for i in range(1, 31):
            rc = RollConvention(getattr(RollConventionType, f'DAY_{i}'))
            expected = datetime(2014, 7, i)
            if i <= start:
                expected = plus_months(expected, 1)
            assert rc.next(datetime(2014, 7, start), Frequency(days=1)) == expected


def test_day_of_month_previous_one_month():
    for start in range(1, 6):
        for i in range(1, 31):
            rc = RollConvention(getattr(RollConventionType, f'DAY_{i}'))
            assert rc.previous(datetime(2014, 7, start), Frequency(months=1)) == datetime(2014, 6, i)


def test_day_of_month_previous_one_day():
    for start in range(1, 6):
        for i in range(1, 31):
            rc = RollConvention(getattr(RollConventionType, f'DAY_{i}'))
            expected = datetime(2014, 7, i)
            if i >= start:
                expected = plus_months(expected, -1)
            assert rc.previous(datetime(2014, 7, start), Frequency(days=1)) == expected


def test_day_of_week_adjust():
    dt = datetime(2014, 8, 14)

    assert RollConvention(RollConventionType.WEEKDAY_MON).adjust(dt) == datetime(2014, 8, 18)
    assert RollConvention(RollConventionType.WEEKDAY_TUE).adjust(dt) == datetime(2014, 8, 19)
    assert RollConvention(RollConventionType.WEEKDAY_WED).adjust(dt) == datetime(2014, 8, 20)
    assert RollConvention(RollConventionType.WEEKDAY_THU).adjust(dt) == datetime(2014, 8, 14)
    assert RollConvention(RollConventionType.WEEKDAY_FRI).adjust(dt) == datetime(2014, 8, 15)
    assert RollConvention(RollConventionType.WEEKDAY_SAT).adjust(dt) == datetime(2014, 8, 16)
    assert RollConvention(RollConventionType.WEEKDAY_SUN).adjust(dt) == datetime(2014, 8, 17)


def test_day_of_week_matches():
    assert not RollConvention(RollConventionType.WEEKDAY_TUE).matches(datetime(2014, 9, 1))
    assert RollConvention(RollConventionType.WEEKDAY_TUE).matches(datetime(2014, 9, 2))
    assert not RollConvention(RollConventionType.WEEKDAY_TUE).matches(datetime(2014, 9, 3))


def test_day_of_week_next_oneweek():
    dt = datetime(2014, 8, 14)

    assert RollConvention(RollConventionType.WEEKDAY_MON).next(dt, Frequency(days=7)) == datetime(2014, 8, 25)
    assert RollConvention(RollConventionType.WEEKDAY_TUE).next(dt, Frequency(days=7)) == datetime(2014, 8, 26)
    assert RollConvention(RollConventionType.WEEKDAY_WED).next(dt, Frequency(days=7)) == datetime(2014, 8, 27)
    assert RollConvention(RollConventionType.WEEKDAY_THU).next(dt, Frequency(days=7)) == datetime(2014, 8, 21)
    assert RollConvention(RollConventionType.WEEKDAY_FRI).next(dt, Frequency(days=7)) == datetime(2014, 8, 22)
    assert RollConvention(RollConventionType.WEEKDAY_SAT).next(dt, Frequency(days=7)) == datetime(2014, 8, 23)
    assert RollConvention(RollConventionType.WEEKDAY_SUN).next(dt, Frequency(days=7)) == datetime(2014, 8, 24)


def test_day_of_week_next_oneday():
    dt = datetime(2014, 8, 14)

    assert RollConvention(RollConventionType.WEEKDAY_MON).next(dt, Frequency(days=1)) == datetime(2014, 8, 18)
    assert RollConvention(RollConventionType.WEEKDAY_TUE).next(dt, Frequency(days=1)) == datetime(2014, 8, 19)
    assert RollConvention(RollConventionType.WEEKDAY_WED).next(dt, Frequency(days=1)) == datetime(2014, 8, 20)
    assert RollConvention(RollConventionType.WEEKDAY_THU).next(dt, Frequency(days=1)) == datetime(2014, 8, 21)
    assert RollConvention(RollConventionType.WEEKDAY_FRI).next(dt, Frequency(days=1)) == datetime(2014, 8, 15)
    assert RollConvention(RollConventionType.WEEKDAY_SAT).next(dt, Frequency(days=1)) == datetime(2014, 8, 16)
    assert RollConvention(RollConventionType.WEEKDAY_SUN).next(dt, Frequency(days=1)) == datetime(2014, 8, 17)


def test_day_of_week_previous_oneweek():
    dt = datetime(2014, 8, 14)

    assert RollConvention(RollConventionType.WEEKDAY_MON).previous(dt, Frequency(days=7)) == datetime(2014, 8, 4)
    assert RollConvention(RollConventionType.WEEKDAY_TUE).previous(dt, Frequency(days=7)) == datetime(2014, 8, 5)
    assert RollConvention(RollConventionType.WEEKDAY_WED).previous(dt, Frequency(days=7)) == datetime(2014, 8, 6)
    assert RollConvention(RollConventionType.WEEKDAY_THU).previous(dt, Frequency(days=7)) == datetime(2014, 8, 7)
    assert RollConvention(RollConventionType.WEEKDAY_FRI).previous(dt, Frequency(days=7)) == datetime(2014, 8, 1)
    assert RollConvention(RollConventionType.WEEKDAY_SAT).previous(dt, Frequency(days=7)) == datetime(2014, 8, 2)
    assert RollConvention(RollConventionType.WEEKDAY_SUN).previous(dt, Frequency(days=7)) == datetime(2014, 8, 3)


def test_day_of_week_previous_oneday():
    dt = datetime(2014, 8, 14)

    assert RollConvention(RollConventionType.WEEKDAY_MON).previous(dt, Frequency(days=1)) == datetime(2014, 8, 11)
    assert RollConvention(RollConventionType.WEEKDAY_TUE).previous(dt, Frequency(days=1)) == datetime(2014, 8, 12)
    assert RollConvention(RollConventionType.WEEKDAY_WED).previous(dt, Frequency(days=1)) == datetime(2014, 8, 13)
    assert RollConvention(RollConventionType.WEEKDAY_THU).previous(dt, Frequency(days=1)) == datetime(2014, 8, 7)
    assert RollConvention(RollConventionType.WEEKDAY_FRI).previous(dt, Frequency(days=1)) == datetime(2014, 8, 8)
    assert RollConvention(RollConventionType.WEEKDAY_SAT).previous(dt, Frequency(days=1)) == datetime(2014, 8, 9)
    assert RollConvention(RollConventionType.WEEKDAY_SUN).previous(dt, Frequency(days=1)) == datetime(2014, 8, 10)


if __name__ == '__main__':
    test_standard_next()
