import json
import math
import random
from Box2D import *
import time

dt = 0.01369
damp = 0.98

class World:
    def __init__(self):
        self.players = {}
        self.world = b2World(gravity=(0, -10), fixedRotation=True)

        self.objs = []
        self.cols = {}

        ground = self.world.CreateStaticBody(
                position=(0,1),
                shapes=b2PolygonShape(box=(5,1)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(-5,2.6),
                shapes=b2PolygonShape(box=(2,0.1)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(5,2.6),
                shapes=b2PolygonShape(box=(2,0.1)),
        )
        self.objs.append(ground)

        self.acc = {}

        # dash
        self.dashes_left = {}
        self.pf = {}
        self.dash_frame = {}
        self.dash_dir = {}

    def gen_vertices(self, token):
        sz = [self.dashes_left[token]]
        vs = []
        for obj in self.objs:
            for fix in obj.fixtures:
                shape = fix.shape

                sz.append(len(shape.vertices))
                for vertex in shape.vertices:
                    vs.append(f'{vertex[0] + obj.position.x:.4f}')
                    vs.append(f'{vertex[1] + obj.position.y:.4f}')
                    vs.extend([0.2, 0.5, 0.2])


        for token in self.players:
            ball = self.players[token]

            sz.append(0)
            vs.extend([f'{ball.position.x:.4f}', f'{ball.position.y:.4f}', 0.2])
            vs.extend(self.cols[token])

        return {'sz': sz, 'vs': vs}


    def add_player(self, token):
        p1 = self.world.CreateDynamicBody(position=(0,7.2))
        p1f = p1.CreateFixture(
                shape=b2CircleShape(pos=(0, 0), radius=0.2),
                density=7.95775387622, friction=0.2, restitution=0.15
                )

        self.players[token] = p1
        self.acc[token] = 0
        self.cols[token] = [random.random() + 0.3, random.random() + 0.3, random.random() + 0.3]

        # dash
        self.dashes_left[token] = 1
        self.pf[token] = p1f
        self.dash_frame[token] = 0
        self.dash_dir[token] = {}

    def step(self):
        for token in self.players:
            if self.dash_frame[token] > 0:
                p1 = self.players[token]
                p1.linearVelocity = (0,0)
                if self.dash_dir[token]["L"]:
                    p1.linearVelocity.x = min(p1.linearVelocity.y, -1)
                if self.dash_dir[token]["R"]:
                    p1.linearVelocity.x = max(p1.linearVelocity.y, 1)
                if self.dash_dir[token]["D"]:
                    p1.linearVelocity.y = min(p1.linearVelocity.y, -1)
                if self.dash_dir[token]["U"]:
                    p1.linearVelocity.y = max(p1.linearVelocity.y, 1)
                x = p1.linearVelocity.x
                y = p1.linearVelocity.y
                l2 = math.sqrt(x * x + y * y)
                p1.linearVelocity *= 15.0 / (l2 + 1e-5)
                p1.linearVelocity.y += 69 * dt
            if self.dash_frame[token] == 0:
                p1 = self.players[token]
                p1.linearVelocity.x*=0.3
                p1.linearVelocity.y*=0.3
                self.players[token].linearVelocity *= damp
            self.acc[token] = self.players[token].linearVelocity.y
        self.world.Step(dt, 5, 5)
        for token in self.players:
            self.acc[token] = (self.players[token].linearVelocity.y - self.acc[token]) / dt

            if self.acc[token] > -10 * 0.9:
                self.dashes_left[token] = 1

            self.dash_frame[token] -= 1

            #if self.dash_frame[token] <= 0:
                #self.pf[token].restitution = 0.15
        time.sleep(dt)

    def parse(self, token, keys):
        if not token in self.players:
            self.add_player(token)

        p1 = self.players[token]
        acc = self.acc[token]
        if keys['X'] and self.dashes_left[token] > 0 and self.dash_frame[token] < -10:
            self.dash_dir[token]['L'] = keys['L']
            self.dash_dir[token]['R'] = keys['R']
            self.dash_dir[token]['D'] = keys['D']
            self.dash_dir[token]['U'] = keys['U']
            self.dashes_left[token] -= 1
            self.dash_frame[token] = 8
        else:
            if keys["L"] and p1.linearVelocity.x > -12:
                p1.ApplyForce(force=(-10,0),point=p1.position,wake=True)
            if keys["R"] and p1.linearVelocity.x < 12:
                p1.ApplyForce(force=(10,0),point=p1.position,wake=True)
            if keys["D"]:
                p1.ApplyForce(force=(0,-5),point=p1.position,wake=True)
            if keys["C"]:
                if acc > -10 * 0.9:
                    p1.linearVelocity.y = max(p1.linearVelocity.y, 6) 

                    if self.dash_frame[token] > 100000:
                        self.pf[token].restitution = 1

        return json.dumps(self.gen_vertices(token))

class WorldManager:
    def __init__(self):
        self.worlds = [World()]

    def step(self):
        for world in self.worlds:
            world.step()

    def parse(self, headers):
        keys = json.loads(headers['X'])
        # TODO: choose a world
        # right now, every client that connects share a world
        return self.worlds[0].parse(headers['token'], keys)


