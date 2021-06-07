import json
import random
from Box2D import *
import time

dt = 0.016

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
                position=(-5,2.5),
                shapes=b2PolygonShape(box=(2,0.1)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(5,2.5),
                shapes=b2PolygonShape(box=(2,0.1)),
        )
        self.objs.append(ground)

        self.acc = {}

    def gen_vertices(self):
        sz = []
        vs = []
        for obj in self.objs:
            for fix in obj.fixtures:
                shape = fix.shape

                sz.append(len(shape.vertices))
                for vertex in shape.vertices:
                    vs.append(vertex[0] + obj.position.x)
                    vs.append(vertex[1] + obj.position.y)
                    vs.extend([0.2, 0.7, 0.4])


        for token in self.players:
            ball = self.players[token]

            sz.append(0)
            vs.extend([ball.position.x, ball.position.y, 0.2])
            vs.extend(self.cols[token])

        return {'sz': sz, 'vs': vs}


    def add_player(self, token):
        p1 = self.world.CreateDynamicBody(position=(0,7.2))
        p1f = p1.CreateFixture(
                shape=b2CircleShape(pos=(0, 0), radius=0.2),
                density=7.95775387622, friction=1.0, restitution=0.12
                )

        self.players[token] = p1
        self.acc[token] = 0
        self.cols[token] = [random.random() + 0.3, random.random() + 0.3, random.random() + 0.3]

    def step(self):
        for token in self.players:
            self.acc[token] = self.players[token].linearVelocity.y
        self.world.Step(dt, 5, 5)
        for token in self.players:
            self.acc[token] = (self.players[token].linearVelocity.y - self.acc[token]) / dt
        time.sleep(dt)

    def parse(self, token, keys):
        if not token in self.players:
            self.add_player(token)

        p1 = self.players[token]
        acc = self.acc[token]
        if keys["L"]:
            p1.ApplyForce(force=(-5,0),point=p1.position,wake=True)
        if keys["R"]:
            p1.ApplyForce(force=(5,0),point=p1.position,wake=True)
        if keys["D"]:
            p1.ApplyForce(force=(0,-5),point=p1.position,wake=True)
        if keys["C"]:
            if acc > -10 * 0.75:
                p1.linearVelocity.y = max(p1.linearVelocity.y, 5.2)
        return json.dumps(self.gen_vertices())

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


 
