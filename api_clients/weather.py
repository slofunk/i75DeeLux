import urequests
import config

def get_weather(zip_code=config.DEFAULT_ZIP_CODE):
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&units=imperial&appid={config.WEATHER_API_KEY}"
    response = urequests.get(url)
    data = response.json()
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    icon = data['weather'][0]['icon']
    return f"{temp}F {description}", icon

def get_weather_icon(icon_id):
    url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    response = urequests.get(url)
    return response.content  # Assuming this is the raw image buffer