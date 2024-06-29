from datetime import datetime
import calendar
from typing import List, Tuple
from collections import deque

from .calendars import HolidayCalendar
from .roll_convention import RollConvention, RollConventionType
from .bdayadj import BDayAdj, BDayAdjType
from .stub_convention import StubConvention, StubConventionType
from .frequency import Frequency
from .schedule_period import SchedulePeriod
from .schedule import Schedule


def first_not_null(a, b):
    if a is not None:
        return a
    if b is not None:
        return b
    raise ValueError('One of the values have to be not null')


class PeriodicSchedule(object):
    # TODO: put data types in
    def __init__(self,
                 unadjusted_start_date: datetime,
                 unadjusted_end_date: datetime,
                 freq: Frequency,
                 bday_adj: BDayAdj,
                 stub_conv: StubConvention | None = None,
                 roll_eom: bool = False,
                 start_date: datetime | None = None,
                 end_date: datetime | None = None,
                 start_date_bday_adj: BDayAdj | None = None,
                 end_date_bday_adj: BDayAdj | None = None,
                 first_regular_start_date: datetime | None = None,
                 last_regular_end_date: datetime | None = None,
                 override_start_date: Tuple[datetime, BDayAdj] | None = None):

        if not isinstance(unadjusted_start_date, datetime):
            raise ValueError("unadjusted_start_date should be of type datetime")
        if not isinstance(unadjusted_end_date, datetime):
            raise ValueError("unadjusted_end_date should be of type datetime")
        if not isinstance(freq, Frequency):
            raise ValueError("freq should be of type Frequency")
        if not isinstance(bday_adj, BDayAdj):
            raise ValueError("bday_adj should be of type BDayAdj")
        # if not isinstance(stub_conv, StubConvention):
        #     raise ValueError("stub_conv should be of type StunConvention")

        self.unadjusted_start_date = unadjusted_start_date
        self.unadjusted_end_date = unadjusted_end_date
        self.freq = freq
        self.bday_adj = bday_adj
        self.stub_conv = stub_conv
        self.eom = roll_eom
        self.roll_conv = RollConvention(RollConventionType.EOM) if self.eom else None

        self.start_date = self.unadjusted_start_date if start_date is None else start_date
        self.end_date = self.unadjusted_end_date if end_date is None else end_date
        self.start_date_bday_adj = start_date_bday_adj
        self.end_date_bday_adj = end_date_bday_adj
        self.first_regular_start_date = first_regular_start_date
        self.last_regular_end_date = last_regular_end_date
        self.override_start_date = override_start_date

    def _estimate_number_periods(self,
                                 start: datetime,
                                 end: datetime,
                                 freq,
                                 ):
        term_in_years_estimate = end.year - start.year + 2
        return max(freq._events_per_year_estimate, 1) * term_in_years_estimate

    def _calculated_unadjusted_date_from_adjusted(self,
                                                  base_dt: datetime,
                                                  roll_conv: RollConvention,
                                                  bday_adj: BDayAdj,
                                                  cal: HolidayCalendar | None = None) -> datetime:
        roll_dom = roll_conv.get_day_of_month()
        if roll_dom > 0 and base_dt.day() != roll_dom:
            length_of_month = calendar.monthrange(base_dt.year(), base_dt.month())[1]
            act_dom = min(roll_dom, length_of_month)
            if base_dt.month() != act_dom:
                roll_implied_dt = datetime.datetime(base_dt.year(), base_dt.month(), act_dom)
                adj_dt = bday_adj.adjust(roll_implied_dt, cal)
                if adj_dt == base_dt:
                    return roll_implied_dt
        elif roll_dom == 0:
            roll_implied_dt = roll_conv.adjust(base_dt)
            if roll_implied_dt != base_dt:
                adj_dt = bday_adj.adjust(roll_implied_dt, cal)
                if adj_dt == base_dt:
                    return roll_implied_dt
        return base_dt

    def _calculated_unadjusted_start_date(self, cal: HolidayCalendar | None = None) -> datetime:
        if cal is not None and self.roll_conv is not None and (
                self.start_dt_bday_adj == BDayAdj(BDayAdjType.NONE) or
                self.roll_conv == RollConvention(RollConventionType.EOM)
        ):
            return self._calculated_unadjusted_date_from_adjusted(self.start_date, self.roll_conv, self.bday_adj, cal)
        return self.start_date

    def _calculated_unadjusted_end_date(self, cal: HolidayCalendar | None = None) -> datetime:
        if cal is not None and self.roll_conv is not None:
            return self._calculated_unadjusted_date_from_adjusted(self.end_date,
                                                                  self.roll_conv,
                                                                  self._calculated_end_date_bday_adj(),
                                                                  cal)
        return self.end_date

    def _calculated_end_date_bday_adj(self) -> BDayAdj:
        return first_not_null(self.end_date_bday_adj, self.bday_adj)

    def _calculated_start_date_bday_adj(self) -> BDayAdj:
        return first_not_null(self.start_date_bday_adj, self.bday_adj)

    def _calculated_first_regular_start_date(self, unadj_start: datetime,
                                             cal: HolidayCalendar | None = None) -> datetime:
        if self.first_regular_start_date is None:
            return unadj_start
        if cal is not None and self.roll_conv is not None:
            return self._calculated_unadjusted_date_from_adjusted(
                self.first_regular_start_date, self.roll_conv, self.bday_adj, cal
            )
        return self.first_regular_start_date

    def calculated_first_regular_start_date(self):
        return first_not_null(self.first_regular_start_date, self.start_date)

    def calculated_roll_convention(self,
                                   calced_first_reg_start_dt: datetime | None = None,
                                   calced_last_reg_end_dt: datetime | None = None):
        assert (calced_first_reg_start_dt is None and calced_last_reg_end_dt is None) or (
                calced_first_reg_start_dt is not None and calced_last_reg_end_dt is not None)

        if calced_first_reg_start_dt is None and calced_last_reg_end_dt is None:
            calced_first_reg_start_dt = self.calculated_first_regular_start_date()
            calced_last_reg_end_dt = self.calculated_last_regular_end_date()

        stub_conv = first_not_null(self.stub_conv, StubConvention(StubConventionType.NONE))

        if self.roll_conv == RollConvention(RollConventionType.EOM):
            derived = stub_conv.to_roll_convention(calced_first_reg_start_dt, calced_last_reg_end_dt, self.freq, True)
            if derived == RollConvention(RollConventionType.NONE):
                return RollConvention(RollConventionType.EOM)
            else:
                return derived

        if self.roll_conv is None or self.roll_conv == RollConvention(RollConventionType.NONE):
            return stub_conv.to_roll_convention(calced_first_reg_start_dt, calced_last_reg_end_dt, self.freq, False)

        return first_not_null(self.roll_conv, RollConvention(RollConventionType.NONE))

    def _calculated_last_regular_end_date(self, unadj_end: datetime, cal: HolidayCalendar | None = None) -> datetime:
        if self.last_regular_end_date is None:
            return unadj_end

        if cal is not None and self.roll_conv is not None:
            return self._calculated_unadjusted_date_from_adjusted(
                self.last_regulard_end_date, self.roll_conv, self.bday_adj, cal)
        return self.last_regular_end_date

    def calculated_last_regular_end_date(self):
        return first_not_null(self.last_regular_end_date, self.end_date)

    def calculated_start_date(self) -> Tuple[datetime, BDayAdj]:
        if self.override_start_date is not None:
            return self.override_start_date
        return self.start_date, self._calculated_start_date_bday_adj()

    def calculated_end_date(self):
        return self.end_date, self._calculated_end_date_bday_adj()

    def _apply_bday_adj(self, unadj: List[datetime], cal: HolidayCalendar | None = None) -> List[datetime]:
        csd_dt, csd_dc = self.calculated_start_date()
        adj = [csd_dc.adjust(csd_dt, cal)]

        for i in range(1, len(unadj)):
            adj.append(self.bday_adj.adjust(unadj[i], cal))

        ced_dt, ced_dc = self.calculated_end_date()
        adj.append(ced_dc.adjust(ced_dt, cal))
        return adj

    def _generate_forwards(self,
                           start: datetime,
                           end: datetime,
                           freq: Frequency,
                           roll_conv: RollConvention,
                           stub_conv: StubConvention,
                           explicit_init_stub: bool,
                           explicit_start: datetime,
                           explicit_final_stub: bool,
                           explicit_end: datetime):
        if not roll_conv.matches(start):
            raise ValueError(f"start date {start} does not match roll convention {roll_conv}")

        dates = []
        if explicit_init_stub:
            dates.append(explicit_start)
            dates.append(start)
        else:
            dates.append(explicit_start)

        if start != end:
            temp = roll_conv.next(start, freq)
            while temp < end:
                dates.append(temp)
                temp = roll_conv.next(temp, freq)

            stub = not temp == end
            if stub and len(dates) > 1:
                applicable_stub_conv = stub_conv
                if stub_conv == StubConvention(StubConventionType.NONE):
                    if roll_conv == RollConvention(RollConventionType.EOM) and \
                            freq.is_month_based() and \
                            not explicit_final_stub and \
                            start.month == calendar.monthrange(start.year, start.month)[1] and \
                            end.month == calendar.monthrange(end.year, end.month)[1]:
                        applicable_stub_conv = StubConvention(StubConventionType.SMART_FINAL)
                    else:
                        raise ValueError(f'Period {start} to {end} resulted in a disallowed stub with frequenct {freq}')
                if applicable_stub_conv.is_stub_long(dates[len(dates) - 1], end):
                    dates.pop()
            dates.append(end)
            if explicit_final_stub:
                dates.append(explicit_end)
        return dates

    def _generate_backwards(self,
                            start: datetime,
                            end: datetime,
                            freq: Frequency,
                            roll_conv: RollConvention,
                            stub_conv: StubConvention,
                            explicit_start: datetime,
                            explicit_final_stub: bool,
                            explicit_end: datetime):

        if not roll_conv.matches(start):
            raise ValueError(f"start date {start} does not match roll convention {roll_conv}")

        dates = deque()
        if explicit_final_stub:
            dates.appendleft(explicit_end)
        dates.appendleft(end)

        temp = roll_conv.previous(end, freq)
        while temp > start:
            dates.appendleft(temp)
            temp = roll_conv.previous(temp, freq)

        stub = not temp.equals(start)
        if stub and len(dates) > 1 and stub_conv.isstub_long(start, dates[0]):
            dates.popleft()
        dates.appendleft(explicit_start)
        return dates.tolist()

    def _generate_unadjusted_dates(self,
                                   start: datetime,
                                   reg_start: datetime,
                                   reg_end: datetime,
                                   end: datetime,
                                   roll_conv: RollConvention):
        override_start = self.override_start_date[0] if self.override_start_date is not None else start
        explicit_init_stub = start != reg_start
        explicit_final_stub = end != reg_end
        if reg_start == end or reg_end == start:
            return [override_start, end]
        if self.freq.is_term():
            if explicit_init_stub or explicit_final_stub:
                raise ValueError("Explicit stubs must not be specified when using term frequency")
            return [override_start, end]

        stub_conv = self.generate_implicit_stub_conv(explicit_init_stub, explicit_final_stub, reg_start, reg_end)
        if self.override_start_date is not None and \
                self.roll_conv is not None and \
                self.first_reg_start_date is None and \
                not roll_conv.matches(reg_start) and \
                roll_conv.matches(override_start):
            return self._generate_backwards(reg_start, reg_end, self.freq, roll_conv, stub_conv, override_start,
                                            explicit_final_stub, end)
        else:
            return self._generate_forwards(reg_start, reg_end, self.freq, roll_conv, stub_conv, explicit_init_stub,
                                           override_start, explicit_final_stub, end)

    def _gen_unadjusted_dates(self,
                              reg_start: datetime,
                              reg_end: datetime,
                              roll_conv: RollConvention,
                              stub_conv: StubConvention,
                              explicit_init_stub: bool,
                              override_start: datetime,
                              explicit_final_stub: bool,
                              end: datetime):
        if stub_conv.is_calculate_backwards():
            return self._generate_backwards(reg_start, reg_end, self.freq, roll_conv, stub_conv, override_start,
                                            explicit_final_stub, end)
        else:
            return self._generate_forwards(reg_start, reg_end, self.freq, roll_conv, stub_conv, explicit_init_stub,
                                           override_start, explicit_final_stub, end)

    def generate_implicit_stub_conv(self,
                                    explicit_init_stub: bool,
                                    explicit_final_stub: bool,
                                    reg_start: datetime,
                                    reg_end: datetime) -> StubConvention:
        if self.stub_conv is not None:
            return self.stub_conv.to_implicit(explicit_init_stub, explicit_final_stub)

        if self.roll_conv is not None and not explicit_init_stub and not explicit_final_stub:
            if self.roll_conv.get_day_of_month() == reg_end.month:
                return StubConvention(StubConventionType.SMART_INITIAL)
            if self.roll_conv.get_day_of_month() == reg_end.month:
                return StubConvention(StubConventionType.SMART_FINAL)
        return StubConvention(StubConventionType.NONE)

    def unadjusted_dates(self, cal: HolidayCalendar | None = None):
        unadj_start = self._calculated_unadjusted_start_date(cal)
        unadj_end = self._calculated_unadjusted_end_date(cal)
        reg_start = self._calculated_first_regular_start_date(unadj_start, cal)
        reg_end = self._calculated_last_regular_end_date(unadj_start, cal)
        roll_conv = self.calculated_roll_convention(reg_start, reg_end)
        return self._generate_unadjusted_dates(unadj_start, reg_start, reg_end, unadj_end, roll_conv)

    def create_unadjsted_dates(self, cal: HolidayCalendar | None = None):
        if cal is None:
            reg_start = self.calculated_first_regular_start_date()
            reg_end = self.calculated_last_regular_end_date()
            roll_conv = self.calculated_roll_convention(reg_start, reg_end)
            unadj = self._generate_unadjusted_dates(self.start_date, reg_start, reg_end, self.end_date, roll_conv)
            deduplicated = sorted(set(unadj))
            if len(deduplicated) < len(unadj):
                raise BaseException("Schedule calculation resulted in duplicate unadjusted dates")
            return deduplicated
        else:
            unadj = self.unadjusted_dates(cal)
            deduplicated = sorted(set(unadj))
            if len(deduplicated) < len(unadj):
                raise BaseException("Schedule calculation resulted in duplicate unadjusted dates")
            return deduplicated

    def create_adjusted_dates(self, cal: HolidayCalendar | None = None):
        unadj = self.unadjusted_dates(cal)
        adj = self._apply_bday_adj(unadj, cal)
        deduplicated = sorted(set(adj))
        if len(deduplicated) < len(adj):
            raise BaseException("Schedule calculation resulted in duplicate unadjusted dates")
        return deduplicated

    def create_schedule(self, cal: HolidayCalendar | None = None, combine_periods_if_necessary=False) -> Schedule:
        unadj_start = self._calculated_unadjusted_start_date(cal)
        unadj_end = self._calculated_unadjusted_end_date(cal)
        reg_start = self._calculated_first_regular_start_date(unadj_start, cal)
        reg_end = self._calculated_last_regular_end_date(unadj_end, cal)
        roll_conv = self.calculated_roll_convention(reg_start, reg_end)

        unadj = self._generate_unadjusted_dates(unadj_start, reg_start, reg_end, unadj_end, roll_conv)
        adj = self._apply_bday_adj(unadj, cal)
        periods = []

        try:
            if combine_periods_if_necessary:
                adj = adj[:]
                unadj = unadj[:]
                for i in range(len(adj) - 1):
                    while i < len(adj) - 1 and adj[i] == adj[i + 1]:
                        adj.remove(i)
                        unadj.remove(i)
            for i in range(len(unadj) - 1):
                periods.append(SchedulePeriod(adj[i], adj[i + 1], unadj[i], unadj[i + 1]))
        except:
            raise Exception('Schedule calculation resulted in invalid period')
        return Schedule(periods, self.freq, roll_conv)

    def get_start_date(self) -> datetime:
        return self.start_date

    def get_end_date(self) -> datetime:
        return self.end_date

    def get_frequency(self) -> Frequency:
        return self.freq

    def get_bday_adj(self) -> BDayAdj:
        return self.bday_adj

    def get_start_date_bday_adj(self) -> datetime:
        return self.start_date_bday_adj

    def get_end_date_bday_adj(self):
        return self.end_date_bday_adj

    def get_stub_convention(self):
        return self.stub_conv

    def get_roll_convention(self):
        return self.roll_conv

    def get_first_regular_start_date(self):
        return self.first_regular_start_date

    def get_last_regular_end_date(self):
        return self.last_regular_end_date

    def get_override_start_date(self):
        return self.override_start_date

    # def replace_start_date(self, adjusted_start_date: datetime):
    #     if adjusted_start_date > self.end_date:
    #         raise ValueError("Cannot alter leg to have start date after end date")
    #
    #     start_dt = adjusted_start_date
    #     bday = BDayAdj(BDayAdjType.NONE)
    #     first_reg_start_dt = None
    #     override_start_dt = None
    #     stub_conv = None
    #
    #     if self.stub_conv is None or \
    #         self.stub_conv == StubConvention(StubConventionType.BOTH) or \
    #         self.stub_conv == StubConvention(StubConventionType.NONE):
    #         stub_conv = StubConvention(StubConventionType.SMART_INITIAL)
    #     elif self.stub_conv.is_final():
    #         if self.last_regular_end_date is None:
    #             stub_conv = StubConvention(StubConventionType.SMART_INITIAL)
    #         else:
