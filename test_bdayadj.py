from datetime import datetime

from bdayadj import BDayAdj, BDayAdjType
from calendars import CustomeHolidayCalendar


def test_bdayadjust():
    data = [[BDayAdjType.NO_ADJUST, datetime(2014, 7, 11), datetime(2014, 7, 11)],
            [BDayAdjType.NO_ADJUST, datetime(2014, 7, 12), datetime(2014, 7, 12)],
            [BDayAdjType.NO_ADJUST, datetime(2014, 7, 13), datetime(2014, 7, 13)],
            [BDayAdjType.NO_ADJUST, datetime(2014, 7, 14), datetime(2014, 7, 14)],

            [BDayAdjType.FOLLOWING, datetime(2014, 7, 11), datetime(2014, 7, 11)],
            [BDayAdjType.FOLLOWING, datetime(2014, 7, 12), datetime(2014, 7, 14)],
            [BDayAdjType.FOLLOWING, datetime(2014, 7, 13), datetime(2014, 7, 14)],
            [BDayAdjType.FOLLOWING, datetime(2014, 7, 14), datetime(2014, 7, 14)],

            [BDayAdjType.FOLLOWING, datetime(2014, 8, 29), datetime(2014, 8, 29)],
            [BDayAdjType.FOLLOWING, datetime(2014, 8, 30), datetime(2014, 9, 1)],
            [BDayAdjType.FOLLOWING, datetime(2014, 8, 31), datetime(2014, 9, 1)],
            [BDayAdjType.FOLLOWING, datetime(2014, 9, 1), datetime(2014, 9, 1)],

            [BDayAdjType.FOLLOWING, datetime(2014, 10, 31), datetime(2014, 10, 31)],
            [BDayAdjType.FOLLOWING, datetime(2014, 11, 1), datetime(2014, 11, 3)],
            [BDayAdjType.FOLLOWING, datetime(2014, 11, 2), datetime(2014, 11, 3)],
            [BDayAdjType.FOLLOWING, datetime(2014, 11, 3), datetime(2014, 11, 3)],

            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 7, 11), datetime(2014, 7, 11)],
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 7, 12), datetime(2014, 7, 14)],
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 7, 13), datetime(2014, 7, 14)],
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 7, 14), datetime(2014, 7, 14)],

            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 8, 29), datetime(2014, 8, 29)],
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 8, 30), datetime(2014, 8, 29)],  # modified
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 8, 31), datetime(2014, 8, 29)],  # modified
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 9, 1), datetime(2014, 9, 1)],

            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 10, 31), datetime(2014, 10, 31)],
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 11, 1), datetime(2014, 11, 3)],
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 11, 2), datetime(2014, 11, 3)],
            [BDayAdjType.MODIFIED_FOLLOWING, datetime(2014, 11, 3), datetime(2014, 11, 3)],

            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 7, 11), datetime(2014, 7, 11)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 7, 12), datetime(2014, 7, 14)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 7, 13), datetime(2014, 7, 14)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 7, 14), datetime(2014, 7, 14)],

            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 8, 29), datetime(2014, 8, 29)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 8, 30), datetime(2014, 8, 29)],  # modified
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 8, 31), datetime(2014, 8, 29)],  # modified
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 9, 1), datetime(2014, 9, 1)],

            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 10, 31), datetime(2014, 10, 31)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 11, 1), datetime(2014, 11, 3)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 11, 2), datetime(2014, 11, 3)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 11, 3), datetime(2014, 11, 3)],

            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 11, 14), datetime(2014, 11, 14)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 11, 15), datetime(2014, 11, 14)],  # modified
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 11, 16), datetime(2014, 11, 17)],
            [BDayAdjType.MODIFIED_FOLLOWING_BI_MONTHLY, datetime(2014, 11, 17), datetime(2014, 11, 17)],

            [BDayAdjType.PRECEDING, datetime(2014, 7, 11), datetime(2014, 7, 11)],
            [BDayAdjType.PRECEDING, datetime(2014, 7, 12), datetime(2014, 7, 11)],
            [BDayAdjType.PRECEDING, datetime(2014, 7, 13), datetime(2014, 7, 11)],
            [BDayAdjType.PRECEDING, datetime(2014, 7, 14), datetime(2014, 7, 14)],

            [BDayAdjType.PRECEDING, datetime(2014, 8, 29), datetime(2014, 8, 29)],
            [BDayAdjType.PRECEDING, datetime(2014, 8, 30), datetime(2014, 8, 29)],
            [BDayAdjType.PRECEDING, datetime(2014, 8, 31), datetime(2014, 8, 29)],
            [BDayAdjType.PRECEDING, datetime(2014, 9, 1), datetime(2014, 9, 1)],

            [BDayAdjType.PRECEDING, datetime(2014, 10, 31), datetime(2014, 10, 31)],
            [BDayAdjType.PRECEDING, datetime(2014, 11, 1), datetime(2014, 10, 31)],
            [BDayAdjType.PRECEDING, datetime(2014, 11, 2), datetime(2014, 10, 31)],
            [BDayAdjType.PRECEDING, datetime(2014, 11, 3), datetime(2014, 11, 3)],

            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 7, 11), datetime(2014, 7, 11)],
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 7, 12), datetime(2014, 7, 11)],
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 7, 13), datetime(2014, 7, 11)],
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 7, 14), datetime(2014, 7, 14)],

            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 8, 29), datetime(2014, 8, 29)],
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 8, 30), datetime(2014, 8, 29)],
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 8, 31), datetime(2014, 8, 29)],
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 9, 1), datetime(2014, 9, 1)],

            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 10, 31), datetime(2014, 10, 31)],
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 11, 1), datetime(2014, 11, 3)],  # modified
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 11, 2), datetime(2014, 11, 3)],  # modified
            [BDayAdjType.MODIFIED_PRECEDING, datetime(2014, 11, 3), datetime(2014, 11, 3)],

            [BDayAdjType.NEAREST, datetime(2014, 7, 11), datetime(2014, 7, 11)],
            [BDayAdjType.NEAREST, datetime(2014, 7, 12), datetime(2014, 7, 11)],
            [BDayAdjType.NEAREST, datetime(2014, 7, 13), datetime(2014, 7, 14)],
            [BDayAdjType.NEAREST, datetime(2014, 7, 14), datetime(2014, 7, 14)]]

    for typ, dt, expected in data:
        assert BDayAdj(typ).adjust(dt, CustomeHolidayCalendar('SAT_SUN', set())) == expected


if __name__ == '__main__':
    test_bdayadjust()
