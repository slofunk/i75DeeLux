import uasyncio as asyncio
import usocket as socket
import ubinascii
import config

html = """<!DOCTYPE html>
<html>
<head>
    <title>LED Sign Configuration</title>
</head>
<body>
    <h1>LED Sign Configuration</h1>
    <form action="/" method="post">
        <label for="wifi_ssid">WiFi SSID:</label>
        <input type="text" id="wifi_ssid" name="wifi_ssid" value="{wifi_ssid}">
        <br>
        <label for="wifi_password">WiFi Password:</label>
        <input type="password" id="wifi_password" name="wifi_password" value="{wifi_password}">
        <br>
        <label for="display_interval">Display Change Interval (s):</label>
        <input type="number" id="display_interval" name="display_interval" value="{display_interval}">
        <br>
        <label for="zip_code">Weather Zip Code:</label>
        <input type="text" id="zip_code" name="zip_code" value="{zip_code}">
        <br>
        <label for="transition_effect">Transition Effect:</label>
        <select id="transition_effect" name="transition_effect">
            <option value="slide_left" {slide_left_selected}>Slide Left</option>
            <option value="slide_right" {slide_right_selected}>Slide Right</option>
            <option value="dissolve" {dissolve_selected}>Dissolve</option>
        </select>
        <br>
        <label for="web_password">Web Interface Password:</label>
        <input type="password" id="web_password" name="web_password" value="{web_password}">
        <br>
        <input type="submit" value="Save">
    </form>
</body>
</html>
"""

async def handle_client(client):
    request = client.recv(1024)
    request = str(request)
    if "Authorization: Basic" not in request:
        response = 'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="LED Sign"\r\n\r\n'
        client.send(response)
        client.close()
        return

    auth_header = request.split("Authorization: Basic ")[1].split("\r\n")[0]
    auth_decoded = ubinascii.a2b_base64(auth_header).decode('utf-8')
    username, password = auth_decoded.split(':')

    if username != config.WEB_USERNAME or password != config.WEB_PASSWORD:
        response = 'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="LED Sign"\r\n\r\n'
        client.send(response)
        client.close()
        return

    if "POST" in request:
        headers, body = request.split('\r\n\r\n')
        params = dict(param.split('=') for param in body.split('&'))
        config.WIFI_SSID = params.get('wifi_ssid', config.WIFI_SSID)
        config.WIFI_PASSWORD = params.get('wifi_password', config.WIFI_PASSWORD)
        config.DISPLAY_CHANGE_INTERVAL = int(params.get('display_interval', config.DISPLAY_CHANGE_INTERVAL))
        config.DEFAULT_ZIP_CODE = params.get('zip_code', config.DEFAULT_ZIP_CODE)
        config.TRANSITION_EFFECT = params.get('transition_effect', config.TRANSITION_EFFECT)
        config.WEB_PASSWORD = params.get('web_password', config.WEB_PASSWORD)

    response = html.format(
        wifi_ssid=config.WIFI_SSID,
        wifi_password=config.WIFI_PASSWORD,
        display_interval=config.DISPLAY_CHANGE_INTERVAL,
        zip_code=config.DEFAULT_ZIP_CODE,
        slide_left_selected="selected" if config.TRANSITION_EFFECT == "slide_left" else "",
        slide_right_selected="selected" if config.TRANSITION_EFFECT == "slide_right" else "",
        dissolve_selected="selected" if config.TRANSITION_EFFECT == "dissolve" else "",
        web_password=config.WEB_PASSWORD
    )
    client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    client.send(response)
    client.close()

async def run_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print('Listening on', addr)

    while True:
        client, addr = s.accept()
        print('Client connected from', addr)
        await handle_client(client)

def start_server():
    loop = asyncio.get_event_loop()
    loop.create_task(run_server())
    loop.run_forever()