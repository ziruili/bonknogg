import socketserver
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

class Server(socketserver.BaseRequestHandler):
    def handle(self):
        #self.request.sendall("test".encode('utf-8'))
        while True:
            response = wm.parse(json.loads(self.request.recv(1024).decode('utf-8')))
            self.request.sendall(response.encode('utf-8'))

def main():
    game = threading.Thread(target=main_game)
    game.start()

    with socketserver.TCPServer((host, 6969), Server) as a:
        aThread = threading.Thread(target=a.serve_forever())
        aThread.daemon=True
        aThread.start()
