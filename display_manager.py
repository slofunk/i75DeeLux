import time
import random
from pimoroni import Hub75, RGB
from font8x8 import Font8x8
from api_client import APIClient
from animations import Animation
import config
import framebuf

class DisplayManager:
    def __init__(self):
        self.display = Hub75(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)  # Initialize with appropriate parameters
        self.font = Font8x8()
        self.api_client = APIClient()
        self.animation = Animation(self.display)
        self.current_mode = 0
        self.modes = [self.show_youtube_subs, self.show_bitcoin_price, self.show_weather, self.show_animation, self.show_pixel_art, self.show_crypto_price]
        self.last_update = time.time()

    def update(self):
        if time.time() - self.last_update > config.DISPLAY_CHANGE_INTERVAL:  # Change mode based on interval
            self.current_mode = (self.current_mode + 1) % len(self.modes)
            self.last_update = time.time()
            self.apply_transition(self.modes[self.current_mode])
        else:
            self.modes[self.current_mode]()

    def show_youtube_subs(self):
        subs = self.api_client.get_youtube_subs()
        self.scroll_text(f"YT Subs: {subs}")

    def show_bitcoin_price(self):
        price = self.api_client.get_bitcoin_price()
        self.scroll_text(f"BTC: ${price}")

    def show_weather(self):
        weather, icon_id = self.api_client.get_weather()
        icon_buffer = self.api_client.get_weather_icon(icon_id)
        
        # Display the weather icon and description
        self.display_weather(weather, icon_buffer)

    def show_animation(self):
        self.animation.play()

    def show_pixel_art(self):
        buffer = self.api_client.get_random_pixel_art()
        self.api_client.display_pixel_art(self.display, buffer)

    def show_crypto_price(self):
        crypto_id = "bitcoin"  # You can change this to any supported cryptocurrency id
        price, logo_url = self.api_client.get_crypto_data(crypto_id)
        logo_buffer = self.api_client.get_image(logo_url)
        
        # Display the logo image and price
        self.display_crypto_price(crypto_id, price, logo_buffer)

    def display_weather(self, weather, icon_buffer):
        # Create a frame buffer for the weather icon
        fb = framebuf.FrameBuffer(icon_buffer, 64, 64, framebuf.RGB565)
        
        # Clear the display
        self.display.fill(RGB(0, 0, 0))
        
        # Draw the weather icon
        self.display.blit(fb, 0, 0)
        
        # Display the weather description next to the icon
        self.font.draw(self.display, weather, 32, self.display.height // 2 - 4, RGB(255, 0, 0))
        
        # Show the display
        self.display.show()

    def display_crypto_price(self, crypto_id, price, logo_buffer):
        # Create a frame buffer for the logo image
        fb = framebuf.FrameBuffer(logo_buffer, 64, 64, framebuf.RGB565)
        
        # Clear the display
        self.display.fill(RGB(0, 0, 0))
        
        # Draw the logo image
        self.display.blit(fb, 0, 0)
        
        # Display the price next to the logo
        self.font.draw(self.display, f"{crypto_id.upper()}: ${price}", 32, self.display.height // 2 - 4, RGB(255, 0, 0))
        
        # Show the display
        self.display.show()

    def scroll_text(self, text):
        text_width = len(text) * 8
        if text_width > self.display.width:
            self.display.fill(RGB(255, 0, 0))  # Display an error message in red
            self.font.draw(self.display, "ERROR", 0, self.display.height // 2 - 4, RGB(255, 255, 255))
            self.display.show()
            time.sleep(2)
        else:
            for offset in range(text_width + self.display.width):
                self.display.fill(RGB(0, 0, 0))
                for i, char in enumerate(text):
                    self.font.draw(self.display, char, self.display.width - offset + i * 8, self.display.height // 2 - 4, RGB(255, 0, 0))
                self.display.show()
                time.sleep(0.1)

    def apply_transition(self, new_mode):
        if config.TRANSITION_EFFECT == 'slide_left':
            self.slide_transition(new_mode, direction='left')
        elif config.TRANSITION_EFFECT == 'slide_right':
            self.slide_transition(new_mode, direction='right')
        elif config.TRANSITION_EFFECT == 'dissolve':
            self.dissolve_transition(new_mode)

    def slide_transition(self, new_mode, direction='left'):
        # Capture the current display state
        current_frame = bytearray(self.display.width * self.display.height * 2)
        self.display.read_framebuffer(current_frame)

        # Prepare a buffer for the new mode
        new_frame = bytearray(self.display.width * self.display.height * 2)
        temp_display = Hub75(self.display.width, self.display.height)
        new_mode(temp_display)
        temp_display.read_framebuffer(new_frame)

        # Slide transition
        for offset in range(self.display.width):
            for y in range(self.display.height):
                for x in range(self.display.width):
                    if direction == 'left':
                        if x + offset < self.display.width:
                            color = framebuf.RGB565(new_frame[(x + offset + y * self.display.width) * 2:(x + 1 + offset + y * self.display.width) * 2])
                        else:
                            color = framebuf.RGB565(current_frame[(x + (y * self.display.width)) * 2:(x + 1 + (y * self.display.width)) * 2])
                    elif direction == 'right':
                        if x - offset >= 0:
                            color = framebuf.RGB565(new_frame[(x - offset + y * self.display.width) * 2:(x + 1 - offset + y * self.display.width) * 2])
                        else:
                            color = framebuf.RGB565(current_frame[(x + (y * self.display.width)) * 2:(x + 1 + (y * self.display.width)) * 2])
                    self.display.pixel(x, y, color)
            self.display.show()
            time.sleep(0.05)

    def dissolve_transition(self, new_mode):
        # Capture the current display state
        current_frame = bytearray(self.display.width * self.display.height * 2)
        self.display.read_framebuffer(current_frame)

        # Prepare a buffer for the new mode
        new_frame = bytearray(self.display.width * self.display.height * 2)
        temp_display = Hub75(self.display.width, self.display.height)
        new_mode(temp_display)
        temp_display.read_framebuffer(new_frame)

        # Dissolve transition
        for step in range(10):
            for y in range(self.display.height):
                for x in range(self.display.width):
                    if random.random() < (step + 1) / 10:
                        color = framebuf.RGB565(new_frame[(x + y * self.display.width) * 2:(x + 1 + y * self.display.width) * 2])
                    else:
                        color = framebuf.RGB565(current_frame[(x + (y * self.display.width)) * 2:(x + 1 + (y * self.display.width)) * 2])
                    self.display.pixel(x, y, color)
            self.display.show()
            time.sleep(0.1)