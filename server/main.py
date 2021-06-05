from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from Box2D import *
import time
import sys

host = sys.argv[1]

dt = 0.016

world = b2World(gravity=(0, -10))
body = world.CreateDynamicBody()

circle = b2CircleShape(pos=(1, 2), radius=0.5)
f1 = body.CreateFixture(shape=circle, density=1, friction=1, restitution=1)

x = 1.0

def main_game():
    global x
    while True:
        x += 40.0 * dt
        world.Step(dt, 3, 3)
        time.sleep(dt)

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.headers)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(f'{x}'.encode('utf-8'))

def main():
    game = threading.Thread(target=main_game)
    game.start()

    A = HTTPServer((host, 6969), Server)
    print('READY')
    A.serve_forever()

main()
