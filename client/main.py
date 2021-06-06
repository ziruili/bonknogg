import pyglet
import numpy as np
import pyglet.window.key as key
import sys
import requests
import json
from pyglet.gl import *

display = pyglet.canvas.Display()
screen = display.get_default_screen()

window = pyglet.window.Window(1280, 720, caption='bonknogg', visible=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)
#window.set_exclusive_mouse(True)
batch = pyglet.graphics.Batch()

host = sys.argv[1]

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
    return requests.get(f'{host}:6969',headers={'X': json.dumps(tem)}).content

pos = []

@window.event
def on_draw():
    window.clear()

    pyglet.graphics.draw(len(pos) // 2, GL_POLYGON, (
        'v2f', pos
    ))

def update(dt):
    global pos

    temp=get().decode("utf-8")
    if temp!="":
        px,py = map(float, temp.split())
        px*=100
        py*=100
        print(f'{px} {py}')
        pos = []
        for a in range(0,30):
            v = 2 * np.pi / 30 * a
            pos.append(px+np.cos(v)*20)
            pos.append(py+np.sin(v)*20)

pyglet.clock.schedule_interval(update, 0.016)
pyglet.app.run()

