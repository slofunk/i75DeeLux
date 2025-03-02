import urequests
from machine import Pin, SPI
import framebuf

def get_random_pixel_art():
    response = urequests.get("https://api.lospec.com/random/pixel-art")
    data = response.json()
    image_url = data['url']
    
    # Fetch the image
    image_response = urequests.get(image_url)
    
    # Assuming the image is in a compatible format (e.g., BMP, PNG)
    # Convert the image to frame buffer for display
    # Note: You may need to adjust this based on the actual image format

    buffer = image_response.content  # Assuming this is the raw image buffer
    return buffer

def display_pixel_art(display, buffer):
    # Create a frame buffer
    fb = framebuf.FrameBuffer(buffer, 64, 64, framebuf.RGB565)
    display.blit(fb, 0, 0)
    display.show()