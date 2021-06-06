from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from Box2D import *
import time
import sys
import json

host = sys.argv[1]

dt = 0.016

world = b2World(gravity=(0, -10))

p1 = world.CreateDynamicBody(position=(6.4,7.2))
p1f = p1.CreateFixture(
        shape=b2CircleShape(pos=(0, 0), radius=0.2),
        density=7.95775387622, friction=1, restitution=0.25
        )

ground = world.CreateStaticBody(
        position=(6.4,-1),
        shapes=b2PolygonShape(box=(6.4,1)),
        )

acc=0

def main_game():
    while True:
        last=p1.linearVelocity.y
        world.Step(dt, 5, 5)
        acc=p1.linearVelocity.y-last
        time.sleep(dt)
        print(f'{p1.position.x} {p1.position.y}:{acc}')

class Server(BaseHTTPRequestHandler):
    jmplast=False
    def do_GET(self):
        print(self.headers)
        tem = json.loads(self.headers['X'])
        if tem["L"]:
            p1.ApplyForce(force=(-5,0),point=p1.position,wake=True)
        if tem["R"]:
            p1.ApplyForce(force=(5,0),point=p1.position,wake=True)
        if tem["D"]:
            p1.ApplyForce(force=(0,-5),point=p1.position,wake=True)
        if tem["U"]:
            if acc > -10*dt+0.0001 and acc < 0.0001 and not jmplast:
                p1.ApplyForce(force=(0,15),point=p1.position,wake=True)
                jmplast=True
            else:
                jmplast=False
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(f'{p1.position.x} {p1.position.y}'.encode('utf-8'))

def main():
    game = threading.Thread(target=main_game)
    game.start()

    A = HTTPServer((host, 6969), Server)
    print('READY')
    A.serve_forever()

main()
