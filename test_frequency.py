import pytest
from IPython.core.debugger import set_trace

from frequency import Frequency


def test_not_negative():
    with pytest.raises(ValueError):
        Frequency(days=-1)
    with pytest.raises(ValueError):
        Frequency(months=-1)
    with pytest.raises(ValueError):
        Frequency(years=-1)
    with pytest.raises(ValueError):
        Frequency(years=0, months=-1, days=-1)
    with pytest.raises(ValueError):
        Frequency(years=0, months=-1, days=1)
    with pytest.raises(ValueError):
        Frequency(years=0, months=1, days=-1)


def test_too_big():
    with pytest.raises(ValueError):
        Frequency(months=12001)
    with pytest.raises(ValueError):
        Frequency(years=1001)
    with pytest.raises(ValueError):
        Frequency(years=10000, days=1)


def test_normalized():
    data = [
        [Frequency(days=1), Frequency(days=1)],
        [Frequency(days=7), Frequency(days=7)],
        [Frequency(days=10), Frequency(days=10)],
        [Frequency(months=1), Frequency(months=1)],
        [Frequency(months=2), Frequency(months=2)],
        [Frequency(months=12), Frequency(years=1)],
        [Frequency(months=20), Frequency(years=1, months=8)],
        [Frequency(months=24), Frequency(years=2)],
        [Frequency(years=2), Frequency(years=2)],
        [Frequency(months=30), Frequency(years=2, months=6)],
        [Frequency(months=30, days=1), Frequency(years=2, months=6, days=1)],
    ]

    for f, n in data:
        assert f.normalized() == n


def test_is_month_based():
    data = [
        [Frequency(days=1), False],
        [Frequency(days=2), False],
        [Frequency(days=6), False],
        [Frequency(days=7), False],
        [Frequency(months=1), True],
        [Frequency(months=3), True],
        [Frequency(months=12), True],
        [Frequency(years=1), True],
        [Frequency(years=3), True],
        [Frequency(years=1, months=2, days=3), False],
        [Frequency(), False],
    ]

    for f, b in data:
        assert f.is_month_based() == b


def test_is_annual():
    data = [
        [Frequency(days=1), False],
        [Frequency(days=2), False],
        [Frequency(days=6), False],
        [Frequency(days=7), False],
        [Frequency(months=1), False],
        [Frequency(months=3), False],
        [Frequency(months=12), True],
        [Frequency(years=1), True],
        [Frequency(years=3), False],
        [Frequency(years=1, months=2, days=3), False],
        [Frequency(), False],
    ]

    for f, b in data:
        assert f.is_annual() == b


def test_events_per_year():
    data = [[Frequency(days=1), 364],
            [Frequency(days=7), 52],
            [Frequency(days=2 * 7), 26],
            [Frequency(days=4 * 7), 13],
            [Frequency(days=13 * 7), 4],
            [Frequency(days=26 * 7), 2],
            [Frequency(days=52 * 7), 1],
            [Frequency(months=1), 12],
            [Frequency(months=2), 6],
            [Frequency(months=3), 4],
            [Frequency(months=4), 3],
            [Frequency(months=6), 2],
            [Frequency(months=12), 1],
            [Frequency(), 0]]
    for f, e in data:
        assert f.events_per_year() == e


def test_events_per_year_bad():
    data = [Frequency(days=3),
            Frequency(days=3 * 7),
            Frequency(days=104 * 7),
            Frequency(months=5),
            Frequency(months=24),
            Frequency(years=2, months=2, days=2)
            ]
    for f in data:
        with pytest.raises(ValueError):
            f.events_per_year()


def test_events_per_year_estimate():
    data = [[Frequency(days=1), 364],
            [Frequency(days=7), 52],
            [Frequency(days=2 * 7), 26],
            [Frequency(days=4 * 7), 13],
            [Frequency(days=13 * 7), 4],
            [Frequency(days=26 * 7), 2],
            [Frequency(days=52 * 7), 1],
            [Frequency(months=1), 12],
            [Frequency(months=2), 6],
            [Frequency(months=3), 4],
            [Frequency(months=4), 3],
            [Frequency(months=6), 2],
            [Frequency(months=12), 1],
            [Frequency(), 0]]
    for f, e in data:
        assert abs(f.events_per_year_estimate() - e) < 1e-8


def test_events_per_year_estimate_bad():
    data = [[Frequency(days=3), 364 / 3, 1e-8],
            [Frequency(days=3 * 7), 364 / 21, 1e-8],
            [Frequency(days=104 * 7), 364 / 728, 1e-8],
            [Frequency(months=5), 12 / 5, 1e-8],
            [Frequency(months=22), 12 / 22, 1e-8],
            [Frequency(months=24), 12 / 24, 1e-8],
            [Frequency(years=2), 0.5, 1e-8],
            [Frequency(years=10, months=0, days=1), 0.1, 1e-3],
            [Frequency(years=5, months=0, days=95), 0.19, 1e-3],
            [Frequency(years=5, months=0, days=97), 0.19, 1e-3]]
    for f, a, r in data:
        assert abs(f.events_per_year_estimate() - a) < r


def test_exact_divide():
    data = [[Frequency(days=7), Frequency(days=7), 1],
            [Frequency(days=2 * 7), Frequency(days=7), 2],
            [Frequency(days=3 * 7), Frequency(days=7), 3],
            [Frequency(days=4 * 7), Frequency(days=7), 4],
            [Frequency(days=13 * 7), Frequency(days=7), 13],
            [Frequency(days=26 * 7), Frequency(days=7), 26],
            [Frequency(days=26 * 7), Frequency(days=2 * 7), 13],
            [Frequency(days=52 * 7), Frequency(days=7), 52],
            [Frequency(days=52 * 7), Frequency(days=2 * 7), 26],

            [Frequency(months=1), Frequency(months=1), 1],
            [Frequency(months=2), Frequency(months=1), 2],
            [Frequency(months=3), Frequency(months=1), 3],
            [Frequency(months=4), Frequency(months=1), 4],
            [Frequency(months=6), Frequency(months=1), 6],
            [Frequency(months=6), Frequency(months=2), 3],
            [Frequency(months=12), Frequency(months=1), 12],
            [Frequency(months=12), Frequency(months=2), 6],
            [Frequency(years=1), Frequency(months=6), 2],
            [Frequency(years=1), Frequency(months=3), 4],
            [Frequency(years=2), Frequency(months=6), 4]]

    for f1, f2, a in data:
        assert f1.exact_divide(f2) == a
        if f1 != f2:
            with pytest.raises(ValueError):
                f2.exact_divide(f1)


def test_exact_divide_bad():
    data = [
        # [Frequency(days=5), Frequency(days=2)],
        # [Frequency(months=5), Frequency(months=2)],
        # [Frequency(months=1), Frequency(days=7)],
        # [Frequency(days=7), Frequency(months=1)],
        [Frequency(), Frequency(days=7)],
        [Frequency(months=12), Frequency()],
        # [Frequency(years=1), Frequency(days=7)]
    ]
    for f1, f2 in data:
        with pytest.raises(ValueError):
            f1.exact_divide(f2)


if __name__ == '__main__':
    test_exact_divide_bad()
