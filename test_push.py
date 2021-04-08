# Test key-value storage
import base64
import json
import urllib.request
import urllib.parse


hostName = "ai.church"
serverPort = 19091


def push_data(key_name, data):
    url = 'http://ai.church:{}/push'.format(serverPort)
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'key': key_name,
        'value': data,
    }
    data = bytes(json.dumps(data), "utf-8")
    data = base64.b64encode(data)
    request = urllib.request.Request(url, headers=headers, data=data, method='POST')
    try:
        response = urllib.request.urlopen(request)
    except Exception as e:
        response = e
    return response.read().decode('utf-8')


if __name__ == "__main__":
    data = {
        'figures': [
            {'type': 'rectangle', 'color': 'black', 'x': 0, 'y': 0, 'width': 400, 'height': 400},
            {'type': 'rectangle', 'color': 'lightgreen', 'x': 10, 'y': 10, 'width': 40, 'height': 20},
            {'type': 'rectangle', 'color': 'lightgreen', 'x': 100, 'y': 100, 'width': 40, 'height': 20},
            {'type': 'rectangle', 'color': 'lightgreen', 'x': 150, 'y': 100, 'width': 40, 'height': 20},
            {'type': 'circle', 'color': 'red', 'x': 150, 'y': 250, 'r': 10},
            {'type': 'circle', 'color': 'blue', 'x': 200, 'y': 400, 'r': 50},
        ]
    }
    print(push_data('arkanoid', data))

