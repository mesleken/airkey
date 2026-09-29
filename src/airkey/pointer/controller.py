import time
from pointer.filters import PointFilter
from pointer.mapper import RelativeMapper

class CursorController:
    def __init__(self, screen_w, screen_h):
        self.mapper = RelativeMapper(screen_w, screen_h)
        self.filter = PointFilter(mincutoff=1.0, beta=1.0)
        
        self.is_locked = False
        self.locked_x = screen_w / 2
        self.locked_y = screen_h / 2
        
        self.history = []
        self.history_duration = 0.2 # 200 ms
        
    def update(self, raw_x, raw_y, hand_size, is_clutched, thumb_is_moving, t):
        # 1. Filter raw coordinates slightly to reduce camera noise before mapping
        fx, fy = self.filter(raw_x, raw_y, t)
        
        # 2. Map relative movement
        cx, cy = self.mapper.update(fx, fy, hand_size, is_clutched)
        
        # 3. Maintain history for click lock
        self.history.append((t, cx, cy))
        # keep only recent history
        self.history = [h for h in self.history if t - h[0] <= self.history_duration]
        
        # 4. Click Lock ("Heisenberg" compensation)
        if thumb_is_moving:
            if not self.is_locked:
                self.is_locked = True
                # Lock to the oldest position in history (before the thumb started moving)
                if len(self.history) > 0:
                    _, self.locked_x, self.locked_y = self.history[0]
                else:
                    self.locked_x, self.locked_y = cx, cy
            
            return int(self.locked_x), int(self.locked_y), True
        else:
            self.is_locked = False
            return cx, cy, False
