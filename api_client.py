from api_clients import get_youtube_subs, get_weather, get_weather_icon, get_bitcoin_price, get_random_pixel_art, display_pixel_art, get_crypto_data, get_image

class APIClient:
    def get_youtube_subs(self):
        return get_youtube_subs()

    def get_bitcoin_price(self):
        return get_bitcoin_price()

    def get_weather(self, zip_code):
        return get_weather(zip_code)

    def get_weather_icon(self, icon_id):
        return get_weather_icon(icon_id)

    def get_random_pixel_art(self):
        return get_random_pixel_art()

    def display_pixel_art(self, display, buffer):
        return display_pixel_art(display, buffer)

    def get_crypto_data(self, crypto_id):
        return get_crypto_data(crypto_id)

    def get_image(self, url):
        return get_image(url)

    # Add other methods as needed