# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        answer = {
            'bricks': [
                {'x': 10, 'y': 10, 'width': 40, 'height': 20},
                {'x': 100, 'y': 100, 'width': 40, 'height': 20},
                {'x': 150, 'y': 100, 'width': 40, 'height': 20},
            ],
            'ball': {'x': 200, 'y': 200, 'r': 10},
            'platform': {'x': 200, 'y': 400, 'r': 50},
        }
        answer = bytes(json.dumps(answer), "utf-8")
        #answer = bytes("test", "utf-8")
        self.send_response(200)
        #print(answer)
        #self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.send_header("Content-length", len(answer))
        self.end_headers()
        self.wfile.write(answer)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
