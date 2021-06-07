import pyglet
import numpy as np
import pyglet.window.key as key
import sys
import requests
import json
import random
import string
from pyglet.gl import *

display = pyglet.canvas.Display()
screen = display.get_default_screen()

window = pyglet.window.Window(1320, 760, caption='bonknogg', visible=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)
#window.set_exclusive_mouse(True)
batch = pyglet.graphics.Batch()

host = sys.argv[1]

window.set_exclusive_keyboard()

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
    return requests.get(f'{host}:6969',headers={'token': token, 'X': json.dumps(tem)}).content.decode('utf-8')

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

    scl = 60
    obj = json.loads(get())
    ptr = 0
    vs = list(map(float, obj['vs']))

    polygons = []
    cols = []
    for s in obj['sz']:
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

pyglet.clock.schedule_interval(update, 0.016)
pyglet.app.run()
