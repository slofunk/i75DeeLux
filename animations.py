import config

class Animation:
    def __init__(self, display):
        self.display = display

    def play(self):
        # Example animation: simple bouncing ball
        for i in range(config.DISPLAY_HEIGHT):
            self.display.fill(RGB(0, 0, 0))
            self.display.pixel(i, i, RGB(0, 255, 0))
            self.display.show()
            time.sleep(0.05)
        for i in range(config.DISPLAY_HEIGHT, 0, -1):
            self.display.fill(RGB(0, 0, 0))
            self.display.pixel(i, i, RGB(0, 255, 0))
            self.display.show()
            time.sleep(0.05)