import time
import network
from display_manager import DisplayManager
import config
from web_server import start_server

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print('network config:', wlan.ifconfig())

# Connect to WiFi
connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)

# Start the web server
start_server()

# Initialize the display manager
display_manager = DisplayManager()

# Main loop
while True:
    display_manager.update()
    time.sleep(0.1)