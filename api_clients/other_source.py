import urequests

def get_other_data():
    response = urequests.get("https://api.example.com/other_data")
    data = response.json()
    return data['value']