class MotionPhysics:

    def __init__(self, t):
        self.d = 0.0
        self.d0 = 0.0
        self.v = 0.0
        self.v0 = 0.0
        self.a = 0.0
        self.t0 = t
        self.t = t
        self.dt = 0.0
        self.d_zero_cb = None
        self.v_zero_cb = None

    def _update_no_cb(self, t):
        self.t = t
        self.dt = t - self.t0
        self.v = self.v0 + 2*self.a*self.dt
        self.d = self.d0 + self.dt*(self.v0 + self.a*self.dt)        

    def update(self, t):
        old_d = self.d
        old_v = self.v
        self._update_no_cb(t)
        if self.v_zero_cb:
            if (old_v > 0.0 and self.v <= 0.0) or (
                    old_v < 0.0 and self.v >= 0.0):
                # find time when velocity was zero, then call callback
                # "at" that time.
                zt = self.t0 - self.v0 / (2.0*self.a)
                self._update_no_cb(zt)
                self.v_zero_cb()
                self._update_no_cb(t)
        if self.d_zero_cb:
            if (old_d > 0.0 and self.d <= 0.0) or (
                    old_d < 0.0 and self.d >= 0.0):
                self.d_zero_cb()

    def recalc(self):
        self.d0 = self.d       
        self.v0 = self.v
        self.t0 = self.t
        self.dt = 0.0
        self.update(self.t)

    def set_veloc_zero_callback(self, cb):
        self.v_zero_cb = cb

    def set_dist_zero_callback(self, cb):
        self.d_zero_cb = cb
        
