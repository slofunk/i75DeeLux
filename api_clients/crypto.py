import urequests

def get_crypto_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    response = urequests.get(url)
    data = response.json()
    price = data['market_data']['current_price']['usd']
    logo_url = data['image']['thumb']
    return price, logo_url

def get_image(url):
    response = urequests.get(url)
    return response.content  # Assuming this is the raw image buffer