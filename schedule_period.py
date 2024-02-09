class SchedulePeriod(object):
    def __init__(self, start_dt, end_dt, unadjusted_start_dt, unadjusted_end_dt):
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.unadjusted_start_dt = unadjusted_start_dt
        self.unadjusted_end_dt = unadjusted_end_dt