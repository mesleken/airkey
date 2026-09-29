class RelativeMapper:
    def __init__(self, screen_w, screen_h, base_gain=3.0, accel_factor=2.0):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.base_gain = base_gain
        self.accel_factor = accel_factor
        
        # Start at center
        self.cursor_x = screen_w / 2
        self.cursor_y = screen_h / 2
        
        self.prev_x = None
        self.prev_y = None

    def update(self, raw_x, raw_y, hand_size, is_clutched=False):
        # We need raw_x and raw_y to calculate delta
        # Since MediaPipe coordinates are normalized to [0,1], we can use them directly
        # hand_size is also in [0,1] space.
        
        if self.prev_x is None or self.prev_y is None:
            self.prev_x = raw_x
            self.prev_y = raw_y
            return int(self.cursor_x), int(self.cursor_y)
            
        dx = raw_x - self.prev_x
        dy = raw_y - self.prev_y
        
        self.prev_x = raw_x
        self.prev_y = raw_y
        
        if is_clutched:
            return int(self.cursor_x), int(self.cursor_y)
            
        # Normalize delta by hand size so movement feels consistent regardless of distance to camera
        # To avoid division by zero or huge jumps if hand size is tiny:
        safe_size = max(hand_size, 0.05)
        norm_dx = dx / safe_size
        norm_dy = dy / safe_size
        
        # Calculate speed (distance per frame)
        speed = (norm_dx**2 + norm_dy**2)**0.5
        
        # Apply acceleration: faster movement -> higher gain
        gain = self.base_gain * (1.0 + speed * self.accel_factor)
        
        # Update cursor position in screen space
        # We use screen_w for both dx and dy scaling to keep aspect ratio 1:1 for movement
        move_x = norm_dx * gain * self.screen_w
        move_y = norm_dy * gain * self.screen_w
        
        self.cursor_x += move_x
        self.cursor_y += move_y
        
        # Clamp to screen
        self.cursor_x = max(0, min(self.screen_w, self.cursor_x))
        self.cursor_y = max(0, min(self.screen_h, self.cursor_y))
        
        return int(self.cursor_x), int(self.cursor_y)
