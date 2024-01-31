from datetime import datetime
from dateutil.relativedelta import relativedelta

from roll_convention import RollConventionType, RollConvention


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
    data = [[RollConventionType.EOM, datetime(2014, 8, 1), relativedelta(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 8, 30), relativedelta(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 8, 31), relativedelta(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 9, 1), relativedelta(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 9, 30), relativedelta(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 1, 1), relativedelta(months=1), datetime(2014, 2, 28)],
            [RollConventionType.EOM, datetime(2014, 2, 1), relativedelta(months=1), datetime(2014, 3, 31)],
            [RollConventionType.EOM, datetime(2014, 8, 1), relativedelta(months=3), datetime(2014, 11, 30)],
            [RollConventionType.EOM, datetime(2014, 8, 1), relativedelta(days=1), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 8, 30), relativedelta(days=1), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 8, 31), relativedelta(days=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 1, 1), relativedelta(days=1), datetime(2014, 1, 31)],
            [RollConventionType.EOM, datetime(2014, 1, 31), relativedelta(days=1), datetime(2014, 2, 28)],
            [RollConventionType.EOM, datetime(2014, 2, 1), relativedelta(days=1), datetime(2014, 2, 28)],

            [RollConventionType.IMM, datetime(2014, 8, 1), relativedelta(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 8, 31), relativedelta(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 1), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 9, 30), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 8, 1), relativedelta(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 19), relativedelta(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 20), relativedelta(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 8, 31), relativedelta(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 16), relativedelta(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 17), relativedelta(days=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 10, 15)],

            [RollConventionType.IMMAUD, datetime(2014, 8, 1), relativedelta(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 31), relativedelta(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 1), relativedelta(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 30), relativedelta(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 1), relativedelta(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 6), relativedelta(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 7), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 8, 31), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 10), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 11), relativedelta(days=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 10, 9)],

            [RollConventionType.IMMNZD, datetime(2014, 8, 1), relativedelta(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 31), relativedelta(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 1), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 30), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 1), relativedelta(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 12), relativedelta(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 13), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 8, 31), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 9), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 10), relativedelta(days=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 10, 15)],

            [RollConventionType.SFE, datetime(2014, 8, 1), relativedelta(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 8, 31), relativedelta(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 1), relativedelta(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 9, 30), relativedelta(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 8, 1), relativedelta(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 7), relativedelta(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 8, 8), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 8, 31), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 11), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 12), relativedelta(days=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 10, 10)]]
    for rct, d1, f, d2 in data:
        assert RollConvention(rct).next(d1, f) == d2


def test_standard_previous():
    data = [[RollConventionType.EOM, datetime(2014, 10, 1), relativedelta(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 10, 31), relativedelta(months=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 11, 1), relativedelta(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 11, 30), relativedelta(months=1), datetime(2014, 10, 31)],
            [RollConventionType.EOM, datetime(2014, 3, 1), relativedelta(months=1), datetime(2014, 2, 28)],
            [RollConventionType.EOM, datetime(2014, 4, 1), relativedelta(months=1), datetime(2014, 3, 31)],
            [RollConventionType.EOM, datetime(2014, 11, 1), relativedelta(months=3), datetime(2014, 8, 31)],
            [RollConventionType.EOM, datetime(2014, 10, 1), relativedelta(days=1), datetime(2014, 9, 30)],
            [RollConventionType.EOM, datetime(2014, 10, 30), relativedelta(days=1), datetime(2014, 9, 30)],

            [RollConventionType.IMM, datetime(2014, 10, 1), relativedelta(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 10, 31), relativedelta(months=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 11, 1), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 11, 30), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMM, datetime(2014, 8, 1), relativedelta(days=1), datetime(2014, 7, 16)],
            [RollConventionType.IMM, datetime(2014, 8, 20), relativedelta(days=1), datetime(2014, 7, 16)],
            [RollConventionType.IMM, datetime(2014, 8, 21), relativedelta(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 8, 31), relativedelta(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 9, 17), relativedelta(days=1), datetime(2014, 8, 20)],
            [RollConventionType.IMM, datetime(2014, 9, 18), relativedelta(days=1), datetime(2014, 9, 17)],
            [RollConventionType.IMM, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 9, 17)],

            [RollConventionType.IMMAUD, datetime(2014, 10, 1), relativedelta(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 31), relativedelta(months=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 11, 1), relativedelta(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 11, 30), relativedelta(months=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 11), relativedelta(days=1), datetime(2014, 8, 7)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 12), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 1), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 9), relativedelta(days=1), datetime(2014, 9, 11)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 10), relativedelta(days=1), datetime(2014, 10, 9)],
            [RollConventionType.IMMAUD, datetime(2014, 10, 30), relativedelta(days=1), datetime(2014, 10, 9)],

            [RollConventionType.IMMNZD, datetime(2014, 10, 1), relativedelta(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 31), relativedelta(months=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 11, 1), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 11, 30), relativedelta(months=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 10), relativedelta(days=1), datetime(2014, 8, 13)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 11), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 1), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 15), relativedelta(days=1), datetime(2014, 9, 10)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 16), relativedelta(days=1), datetime(2014, 10, 15)],
            [RollConventionType.IMMNZD, datetime(2014, 10, 30), relativedelta(days=1), datetime(2014, 10, 15)],

            [RollConventionType.SFE, datetime(2014, 10, 1), relativedelta(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 31), relativedelta(months=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 11, 1), relativedelta(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 11, 30), relativedelta(months=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 9, 1), relativedelta(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 9, 12), relativedelta(days=1), datetime(2014, 8, 8)],
            [RollConventionType.SFE, datetime(2014, 9, 13), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 9, 30), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 1), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 10), relativedelta(days=1), datetime(2014, 9, 12)],
            [RollConventionType.SFE, datetime(2014, 10, 11), relativedelta(days=1), datetime(2014, 10, 10)],
            [RollConventionType.SFE, datetime(2014, 10, 30), relativedelta(days=1), datetime(2014, 10, 10)]]
    for rct, d1, f, d2 in data:
        assert RollConvention(rct).previous(d1, f) == d2


if __name__ == '__main__':
    test_standard_adjust()
