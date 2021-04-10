# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = "ai.church"
serverPort = 19091
globalStorage = dict()


class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        try:
            post_body = json.loads(post_body.decode('utf-8'))
        except:
            post_body = {}
        result = {}
        if 'key' in post_body and 'value' in post_body:
            key_name = post_body['key']
            data = post_body['value']
            globalStorage[key_name] = data
            result['result'] = 'ok'
        else:
            result['result'] = 'fail'
        self.send_response(200)
        answer = bytes(json.dumps(result), 'utf-8')
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', len(answer))
        self.end_headers()
        self.wfile.write(answer)


    def do_GET(self):
        path = self.path if not self.path else self.path[1:]
        answer = globalStorage.get(path, {})
        answer = bytes(json.dumps(answer), 'utf-8')
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', len(answer))
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

