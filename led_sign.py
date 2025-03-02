import time
import rp2
from machine import Pin
from hub75 import Hub75, RGB
from font8x8 import Font8x8

# Initialize the Hub75 display
display = Hub75(32, 16, Pin(2), Pin(3), Pin(4), Pin(5), Pin(6), Pin(7), Pin(8), Pin(9), Pin(10), Pin(11), Pin(12), Pin(13), Pin(14), Pin(15), Pin(16), Pin(17))

# Create a font object
font = Font8x8()

# Define the text to scroll
text = "Hello, World!"

# Define a function to scroll text
def scroll_text(display, text, font, speed=0.1):
    text_width = len(text) * 8
    for offset in range(text_width + display.width):
        display.fill(RGB(0, 0, 0))  # Clear the display
        for i, char in enumerate(text):
            font.draw(display, char, display.width - offset + i * 8, 4, RGB(255, 0, 0))
        display.show()
        time.sleep(speed)

# Main loop
while True:
    scroll_text(display, text, font)