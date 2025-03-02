import urequests

def get_bitcoin_price():
    response = urequests.get("https://api.example.com/bitcoin_price")
    data = response.json()
    return data['price']