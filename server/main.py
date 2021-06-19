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
        data = self.request[0].strip()
        socket = self.request[1]
        response = wm.parse(json.loads(data.decode('utf-8')))
        socket.sendto(response.encode('utf-8'), self.client_address)

def main():
    game = threading.Thread(target=main_game)
    game.start()

    with socketserver.UDPServer((host, 6969), Server) as a:
        a.serve_forever()

main()

