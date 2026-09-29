import time

class ClickDetector:
    def __init__(self, open_threshold=1.2, close_threshold=0.8):
        # Normalized distance threshold
        self.open_threshold = open_threshold
        self.close_threshold = close_threshold
        self.is_open = False
        self.open_time = 0

    def process(self, normalized_thumb_distance):
        # returns True if a click is completed in this frame
        click_event = False
        
        if not self.is_open:
            if normalized_thumb_distance > self.open_threshold:
                self.is_open = True
                self.open_time = time.time()
        else:
            if normalized_thumb_distance < self.close_threshold:
                self.is_open = False
                duration = time.time() - self.open_time
                if 0.02 < duration < 1.0:  # Daha esnek süre: çok hızlı ve biraz yavaş tıklamalara izin ver
                    click_event = True
                    
        return click_event, self.is_open
