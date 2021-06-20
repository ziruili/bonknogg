import json
import math
import random
from Box2D import *
import copy
import time

dt = 1/60
damp = 1
E = 0.01

class World:
    def __init__(self):
        self.players = {}
        self.world = b2World(gravity=(0, -10), fixedRotation=True)
        self.world.velocityThreshold = (1e10)

        self.objs = []
        self.cols = {}
        self.dp = {}

        ground = self.world.CreateStaticBody(
                position=(0,3),
                shapes=b2PolygonShape(box=(18,0.3)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(0,1),
                shapes=b2PolygonShape(box=(20,0.35)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(-5,4.2),
                shapes=b2PolygonShape(box=(2,0.35)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(5,4.2),
                shapes=b2PolygonShape(box=(2,0.35)),
        )
        self.objs.append(ground)

        ground = self.world.CreateStaticBody(
                position=(0,1),
                shapes=b2PolygonShape(box=(0.1,3)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(-21,5),
                shapes=b2PolygonShape(box=(0.22,7)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(21,5),
                shapes=b2PolygonShape(box=(0.22,7)),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(-5,4),
                shapes=b2PolygonShape(vertices=[(2, 3), (0, 4), (3, 7)]),
        )
        self.objs.append(ground)
        ground = self.world.CreateStaticBody(
                position=(5,4),
                shapes=b2PolygonShape(vertices=[(6, 1), (0.24, 4.24), (3, 7)]),
        )
        self.objs.append(ground)
        self.acc = {}

        # dash
        self.dashes_left = {}
        self.mana = {}
        self.pf = {}
        self.dash_frame = {}
        self.dash_dir = {}

    def gen_vertices(self, token):
        # print(token)
        dpe = self.dp[token]
        sz = [self.dashes_left[token]]
        vs = []
        for obj in self.objs:
            for fix in obj.fixtures:
                shape = fix.shape

                sz.append(len(shape.vertices))
                for vertex in shape.vertices:
                    vs.append(f'{vertex[0] + obj.position.x - dpe[0]:.4f}')
                    vs.append(f'{vertex[1] + obj.position.y - dpe[1] + 5:.4f}')
                    vs.extend([51, 127, 51])


        for tmptoken in self.players:
            # print(tmptoken)
            ball = self.players[tmptoken]

            sz.append(0)
            vs.extend([f'{ball.position.x - dpe[0]:.4f}', f'{ball.position.y - dpe[1] + 5:.4f}', 0.2])
            vs.extend(self.cols[tmptoken])
        # print(vs)

        return {'sz': sz, 'vs': vs}


    def add_player(self, token):
        p1 = self.world.CreateDynamicBody(position=(0,7.2))
        p1f = p1.CreateFixture(
                shape=b2CircleShape(pos=(0, 0), radius=0.2),
                density=7.95775387622, friction=0.2, restitution=0.5
                )
        
        p1.linearDamping = 0

        self.players[token] = p1
        self.dp[token] = [p1.position.x, p1.position.y]
        self.acc[token] = 0
        self.cols[token] = [int(255 * random.random()), int(255 * random.random()), int(255 * random.random())]

        # dash
        self.dashes_left[token] = 1
        self.mana[token] = 0
        self.pf[token] = p1f
        self.dash_frame[token] = 0
        self.dash_dir[token] = {}

    def step(self):
        for token in self.players:
            self.players[token].linearVelocity *= damp
            self.acc[token] = self.players[token].linearVelocity.y

            self.dp[token][0] += E * (self.players[token].position.x - self.dp[token][0]) ** 3
            self.dp[token][1] += E * (self.players[token].position.y - self.dp[token][1]) ** 3
        self.world.Step(dt, 50, 50)
        for token in self.players:
            self.acc[token] = (self.players[token].linearVelocity.y - self.acc[token]) / dt
            
            if self.dash_frame[token] > 0:
                p1 = self.players[token]
                Tempx,Tempy = p1.linearVelocity
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
                p1.linearVelocity *= 10.0 / (l2 + 1e-5)
                if p1.linearVelocity == (0,0):
                    p1.linearVelocity = (Tempx,Tempy)
                elif self.acc[token] <= -10 * 0.99:
                    p1.linearVelocity.y += 20 * dt
                else:
                    p1.linearVelocity.y -= 50 * dt
            if self.dash_frame[token] == 0:
                p1 = self.players[token]
                p1.linearVelocity*=0.35

            if self.dash_frame[token] < 0 and self.acc[token] > -10 * 0.99:
                self.dashes_left[token] = 1

            self.dash_frame[token] -= 1

    def parse(self, token, keys):
        if not token in self.players:
            self.add_player(token)

        p1 = self.players[token]
        acc = self.acc[token]
        if keys['X'] and self.dashes_left[token] > 0 and self.dash_frame[token] < -15:
            self.dash_dir[token]['L'] = keys['L']
            self.dash_dir[token]['R'] = keys['R']
            self.dash_dir[token]['D'] = keys['D']
            self.dash_dir[token]['U'] = keys['U']
            self.dashes_left[token] -= 1
            if self.mana[token] < 15:
                self.mana[token] += 1
            self.dash_frame[token] = 14
        elif keys['Z'] and self.mana[token] >= 3:
            p1.linearVelocity = (0,0)
            # print("\n\n\n\n\n\n\n\n\n\n\n")
            for tmptoken in self.players:
                if tmptoken == token:
                    continue
                p2 = self.players[tmptoken]
                x = p2.position.x-p1.position.x
                y = p2.position.y-p1.position.y
                dist = math.sqrt(x*x+y*y)
                # print(dist)
                p2.ApplyForce(force=(500*x/(dist*dist),500*y/(dist*dist)),point=p2.position,wake=True)

            self.mana[token]-=3
        else:
            if keys["L"] and p1.linearVelocity.x > -3.2:
                p1.ApplyForce(force=(-18,0),point=p1.position,wake=True)
            if keys["R"] and p1.linearVelocity.x < 3.2:
                p1.ApplyForce(force=(18,0),point=p1.position,wake=True)
            if keys["D"]:
                p1.ApplyForce(force=(0,-12),point=p1.position,wake=True)
            if keys["C"]:
                if acc > -10 * 0.99:
                    p1.linearVelocity.y = max(p1.linearVelocity.y, 6) 

                    if self.dash_frame[token] > 0:
                        p1.linearVelocity.x *= 1.79234
                        p1.linearVelocity.y *= 1.4311239
                        self.dash_frame[token] = -1
                        self.dashes_left[token] = 1

        return json.dumps(self.gen_vertices(token))

class WorldManager:
    def __init__(self):
        self.worlds = [World()]

    def step(self):
        for world in self.worlds:
            world.step()
        time.sleep(dt)

    def parse(self, headers):
        keys = json.loads(headers['X'])
        # TODO: choose a world
        # right now, every client that connects share a world
        return self.worlds[0].parse(headers['token'], keys)


