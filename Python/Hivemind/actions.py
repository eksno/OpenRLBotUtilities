import time

class Dodger:
    """Class for making dodging easier and more efficient."""

    def __init__(self, wait=2.2):
        """'wait' is the wait period until next dodge is possible. Value is capped to be over 1"""
        self.timer = time.time()
        self.wait = max(wait, 1)

    def attempt_dodging(self):
        """Dodges if time since last dodge is over wait. Returns jump and pitch"""
        time_difference = time.time() - self.timer
        if time_difference > self.wait:
            self.timer = time.time()
            jump, pitch = False, 0
        elif time_difference <= 0.1:
            jump, pitch = True, -1
        elif 0.1 <= time_difference <= 0.15:
            jump, pitch = False, -1
        elif 0.15 <= time_difference < 1:
            jump, pitch = True, -1
        else:
            jump, pitch = False, 0
        return jump, pitch
