class PeriodicSchedule(object):
    def __init__(self, unadjusted_start_dt, unadjusted_end_dt, freq, bday_adj, stub_conv, eom):
        self.unadjusted_start_dt = unadjusted_start_dt
        self.unadjusted_end_dt = unadjusted_end_dt
        self.freq = freq
        self.bday_adj = bday_adj
        self.stub_conv = stub_conv
        self.eom = eom
