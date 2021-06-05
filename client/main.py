import pyglet
import pyglet.window.key as key
import sys
import requests
import json
from pyglet.gl import *

display = pyglet.canvas.Display()
screen = display.get_default_screen()

window = pyglet.window.Window(screen.width, screen.height, caption='bonknogg', fullscreen=True, visible=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)
#window.set_exclusive_mouse(True)

host = sys.argv[1]

def get():
    return requests.get(f'{host}:6969',headers={'X': json.dumps(keys)}).content

pos = []

@window.event
def on_draw():
    window.clear()

    pyglet.graphics.draw(len(pos) // 2, GL_QUADS, (
        'v2f', pos
    ))

def update(dt):
    global pos

    k = float(get())

    pos = [k, k, k + 10, k, k + 10, k + 10, k, k + 10]

pyglet.clock.schedule_interval(update, 0.016)
pyglet.app.run()

