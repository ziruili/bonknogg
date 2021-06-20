import pyglet
import numpy as np
import pyglet.window.key as key
import sys
import socket
import requests
import json
import random
import string
from pyglet.gl import *

display = pyglet.canvas.Display()
screen = display.get_default_screen()

window = pyglet.window.Window(1440, 860, caption='bonknogg', visible=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pyglet.graphics.Batch()

host = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

token = ''.join(random.choices('0123456789abcdef', k=8))

options = {
    "U":key.UP,
    "D":key.DOWN,
    "L":key.LEFT,
    "R":key.RIGHT,
    "X":key.X,
    "C":key.C,
    "Z":key.Z
}

def get():
    tem = {}
    for i in options:
        tem[i]=keys[options[i]]
    sock.sendto(json.dumps({'token': token, 'X': json.dumps(tem)}).encode('utf-8'), (host, 6969))
    W = sock.recvfrom(65535)[0]
    return W

polygons = []
cols = []

@window.event
def on_draw():
    window.clear()

    for i, p in enumerate(polygons):
        c = cols[i]
        pyglet.graphics.draw(len(p) // 2, GL_POLYGON,
            ('v2f', p), ('c3f', c)
        )

def update(dt):
    global polygons
    global cols

    scl = 80
    temp=get()
    if len(temp) == 0:
       return 
    obj = json.loads(temp.decode('utf-8'))
    ptr = 0
    vs = list(map(float, obj['vs']))

    polygons = []
    cols = []

    dashes = int(obj['sz'][0])

    polygons.append([0, window.height - 50, 0, window.height, window.width, window.height, window.width, window.height - 50])
    if dashes == 0:
        cols.append([0.5, 1.0, 1.0] * 4)
    elif dashes == 1:
        cols.append([0.9, 0.2, 0.2] * 4)
    else:
        cols.append([0.9, 0.6, 1.0] * 4)

    for s in obj['sz'][1:]:
        sz = int(s)

        w = []
        c = []
        if sz == 0:
            px, py, r = vs[ptr], vs[ptr + 1], vs[ptr + 2]

            for a in range(0, 20):
                v = 2 * np.pi / 20 * a
                w.append(px*scl+np.cos(v)*r*scl+window.width / 2)
                w.append(py*scl+np.sin(v)*r*scl)
                c.extend(vs[ptr + 3:ptr + 6])
            ptr += 6
        else:
            for i in range(sz):
                x = scl * vs[ptr] + window.width / 2
                y = scl * vs[ptr + 1]
                w.extend([x, y])
                c.extend(vs[ptr + 2:ptr + 5])
                ptr += 5
        polygons.append(w)
        cols.append(c)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()

