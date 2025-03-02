import network

# WiFi configuration
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# Display configuration
DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 64

# Interval between display changes (in seconds)
DISPLAY_CHANGE_INTERVAL = 10

# Weather configuration
WEATHER_API_KEY = "your_openweathermap_api_key"
DEFAULT_ZIP_CODE = "your_default_zip_code"

# Transition configuration
TRANSITION_EFFECT = "slide_left"  # Options: 'slide_left', 'slide_right', 'dissolve'

# Generate default password based on MAC address
wlan = network.WLAN(network.STA_IF)
mac = wlan.config('mac')
DEFAULT_PASSWORD = ''.join(['{:02x}'.format(b) for b in mac])

# Web interface credentials
WEB_USERNAME = "admin"
WEB_PASSWORD = DEFAULT_PASSWORD  # Can be changed via the web interface