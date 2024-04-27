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


if __name__ == '__main__':
    test_normalized()