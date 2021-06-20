import pyglet
import numpy as np
import pyglet.window.key as key
import sys
import socket
import requests
import json
import random
import string
import pygame
import pygame_menu
from pygame.locals import *
clock = pygame.time.Clock()
#from pyglet.gl import *

#display = pyglet.canvas.Display()
#screen = display.get_default_screen()

#window = pyglet.window.Window(1440, 860, caption='bonknogg', visible=True)
#window.push_handlers(keys)
#batch = pyglet.graphics.Batch()

pygame.init()
screen = pygame.display.set_mode([1440, 860], #pygame.FULLSCREEN, 
        )

host = 'localhost'
port = 6969
room = '1234'
difficulty = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.05)

token = ''.join(random.choices('0123456789abcdef', k=8))

options = {
    "U":pygame.K_UP,
    "D":pygame.K_DOWN,
    "L":pygame.K_LEFT,
    "R":pygame.K_RIGHT,
    "X":pygame.K_x,
    "C":pygame.K_c,
    "Z":pygame.K_z
}

sess = requests.Session()

def get():
    try:
        keys = pygame.key.get_pressed()
        tem = {}
        for i in options:
            # print(i)
            tem[i]=keys[options[i]]
        # print(tem)
        sock.sendto(json.dumps({'room': room, 'token': token, 'X': json.dumps(tem)}).encode('utf-8'), (host, port))
        W = sock.recvfrom(65535)[0]
        return W
    except:
        pass
    return ''.encode('utf-8')

polygons = []
cols = []

#@window.event
#def on_draw():
    #window.clear()

    #for i, p in enumerate(polygons):
        #c = cols[i]
        #pyglet.graphics.draw(len(p) // 2, GL_POLYGON,
            #('v2f', p), ('c3f', c)
        #)

def update(dt):
    global polygons
    global cols

    scl = 80
    temp=get()
    if len(temp) == 0:
        print("ohno")
        return 
    obj = json.loads(temp.decode('utf-8'))
    ptr = 0
    vs = list(map(float, obj['vs']))
    # print(vs)

    polygons = []
    cols = []

    dashes = int(obj['sz'][0])

    width, height = pygame.display.get_surface().get_size()
    polygons.append([(0, height - 50), (0, height), (width, height), (width, height - 50)])
    if dashes == 0:
        cols.append((127, 255, 255))
    elif dashes == 1:
        cols.append((230, 51, 51))
    else:
        cols.append((230, 153, 255))

    for s in obj['sz'][1:]:
        sz = int(s)

        w = []
        c = []
        if sz == 0:
            px, py, r = vs[ptr], vs[ptr + 1], vs[ptr + 2]

            for a in range(0, 20):
                v = 2 * np.pi / 20 * a
                w.append((px*scl+np.cos(v)*r*scl+width / 2, 
                    py*scl+np.sin(v)*r*scl))
            c=tuple(vs[ptr + 3:ptr + 6])
            ptr += 6
        else:
            for i in range(sz):
                x = scl * vs[ptr] + width / 2
                y = scl * vs[ptr + 1]
                w.append((x, y))
                ptr += 5
            c=tuple(vs[ptr + 2:ptr + 5])
        polygons.append(w)
        cols.append(c)

def game():
    print(host, port, room)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update(1/60)
        screen.fill((0, 0, 0))
        for i, p in enumerate(polygons):
            #c = cols[i]
            #pyglet.graphics.draw(len(p) // 2, GL_POLYGON,
                #('v2f', p), ('c3f', c):w

            #)
            pygame.draw.polygon(surface=screen, color=cols[i], points=p)
        screen.blit(pygame.transform.flip(screen,False,True),(0,0))
        pygame.display.flip()
        clock.tick(60)

width, height = pygame.display.get_surface().get_size()
menu = pygame_menu.Menu(width=width, height=height, title='Bonknogg', theme=pygame_menu.themes.THEME_DARK)
game_menu = pygame_menu.Menu(width=width, height=height, title='Join', theme=pygame_menu.themes.THEME_DARK)
rules_menu = pygame_menu.Menu(width=width, height=height, title='about', theme=pygame_menu.themes.THEME_DARK)

menu.add.text_input('Name : ', default='n00bmaster69')
menu.add.button('Play', game_menu)
menu.add.button('Game Rules', rules_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

game_menu.add.text_input('Host : ', default='localhost', onchange=lambda x:globals().update(host=x))
game_menu.add.text_input('Port : ', default='6969', onchange=lambda x:globals().update(port=int(x)))
game_menu.add.text_input('Room : ', default='1234', onchange=lambda x:globals().update(room=x))
items=[('Beginner', 0),
        ('Apprentice', 1),
        ('Knight', 2),
        ('Master', 3),
        ('Sage', 4)]
game_menu.add.selector('Difficulty: ', items=items)
game_menu.add.button('Start', game)
game_menu.add.button('Back', pygame_menu.events.BACK, onchange=lambda x,y:globals().update(difficulty=y), accept_kwargs=True)

rules_menu.add.button('Back', pygame_menu.events.BACK)
menu.mainloop(screen)
#pyglet.clock.schedule_interval(update, 1/60)
#pyglet.app.run()
