import math

class OneEuroFilter:
    def __init__(self, mincutoff=1.0, beta=0.0, dcutoff=1.0):
        self.mincutoff = mincutoff
        self.beta = beta
        self.dcutoff = dcutoff
        self.x_prev = None
        self.dx_prev = None
        self.t_prev = None

    def __call__(self, x, t):
        if self.t_prev is None:
            self.x_prev = x
            self.dx_prev = 0.0
            self.t_prev = t
            return x
            
        dt = t - self.t_prev
        if dt <= 0:
            return self.x_prev
            
        dx = (x - self.x_prev) / dt
        
        # Filter dx
        edx = self._alpha(self.dcutoff, dt)
        dx_hat = edx * dx + (1.0 - edx) * self.dx_prev
        
        # Filter x
        cutoff = self.mincutoff + self.beta * abs(dx_hat)
        ex = self._alpha(cutoff, dt)
        x_hat = ex * x + (1.0 - ex) * self.x_prev
        
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t
        return x_hat

    def _alpha(self, cutoff, dt):
        tau = 1.0 / (2.0 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

class PointFilter:
    def __init__(self, mincutoff=1.0, beta=0.0):
        self.filter_x = OneEuroFilter(mincutoff, beta)
        self.filter_y = OneEuroFilter(mincutoff, beta)
        
    def __call__(self, x, y, t):
        return self.filter_x(x, t), self.filter_y(y, t)
