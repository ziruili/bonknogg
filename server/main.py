from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time
import sys
import json
from server.world import WorldManager

host = sys.argv[1]

wm = WorldManager()

def main_game():
    while True:
        wm.step()

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        response = wm.parse(self.headers)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

def main():
    game = threading.Thread(target=main_game)
    game.start()

    A = HTTPServer((host, 6969), Server)
    print('READY')
    A.serve_forever()

main()
