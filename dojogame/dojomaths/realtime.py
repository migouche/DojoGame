# realtime.py

import time


class RealTime:
    t = time.monotonic()  # init time
    delta_time = 1 / 60

    @staticmethod
    def set_dt(dt):
        RealTime.delta_time = dt

    @staticmethod
    def wait_for_real_time(dt):
        RealTime.t = RealTime.t + dt
        wait = RealTime.t - time.monotonic()
        if wait > 0:
            time.sleep(wait)
