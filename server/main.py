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

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    game = threading.Thread(target=main_game)
    game.start()

    print('1')

    with ThreadedTCPServer((host, 6969), Server) as a:
        aThread = threading.Thread(target=a.serve_forever)
        aThread.daemon=True
        aThread.start()

        while True:
            time.sleep(60.0)


main()

