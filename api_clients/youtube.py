import urequests

def get_youtube_subs():
    response = urequests.get("https://api.example.com/youtube_subs")
    data = response.json()
    return data['subscriberCount']