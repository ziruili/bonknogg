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
import time
import datetime
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

name = 'n00bmaster69'
colour = (int(255 * random.random()),int(255 * random.random()),int(255 * random.random()))
host = 'localhost'
port = 6969
room = '1234'
difficulty = 0
ohno = False

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
'n00bmaster69'
def get():
    try:
        keys = pygame.key.get_pressed()
        tem = {}
        for i in options:
            # print(i)
            tem[i]=keys[options[i]]
        # print(tem)
        sock.sendto(json.dumps({'room': room, 'token': token, 'difficulty': difficulty, 'colour': colour, 'X': json.dumps(tem)}).encode('utf-8'), (host, port))
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
        global ohno
        ohno=True
        return 
    obj = json.loads(temp.decode('utf-8'))
    ptr = 0
    vs = list(map(float, obj['vs']))
    # print(vs)

    polygons = []
    cols = []
    if obj['rn'] == False:
        # print("test")
        return

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

def gameHackySolu():
    game()

flag=True
def cursed():
    global flag
    flag=False

width, height = pygame.display.get_surface().get_size()
menu = pygame_menu.Menu(width=width, height=height, title='Bonknogg', theme=pygame_menu.themes.THEME_DARK)
game_menu = pygame_menu.Menu(width=width, height=height, title='Join', theme=pygame_menu.themes.THEME_DARK)
rules_menu = pygame_menu.Menu(width=width, height=height, title='about', theme=pygame_menu.themes.THEME_DARK)
certificate = pygame_menu.Menu(width=width, height=height, title='Rippus', theme=pygame_menu.themes.THEME_DARK)

menu.add.text_input('Name : ', default='n00bmaster69', onchange=lambda x:globals().update(name=x))
menu.add.color_input('Colour : ', color_type='rgb', default=colour, onchange=lambda x:globals().update(colour=x))
menu.add.button('Play', game_menu)
menu.add.button('Game Rules', rules_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

def difficulty_change(x,y):
    global difficulty,token
    difficulty = y
    token = ''.join(random.choices('0123456789abcdef', k=8))

game_menu.add.text_input('Host : ', default='localhost', onchange=lambda x:globals().update(host=x))
game_menu.add.text_input('Port : ', default='6969', onchange=lambda x:globals().update(port=int(x)))
game_menu.add.text_input('Room : ', default='1234', onchange=lambda x:globals().update(room=x))
items=[('Beginner', 0),
        ('Apprentice', 1),
        ('Knight', 2),
        ('Master', 3),
        ('Sage', 4)]
game_menu.add.selector('Difficulty: ', items=items, onchange=difficulty_change)
game_menu.add.button('Start', gameHackySolu)
game_menu.add.button('Back', pygame_menu.events.BACK)

rules_menu.add.button('Back', pygame_menu.events.BACK)

def game():
    global token
    global ohno
    ohno = False
    print(host, port, room)
    start = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == pygame.QUIT:
                running = False

        update(1/60)
        screen.fill((44, 45, 40))
        if polygons == []:
            token = ''.join(random.choices('0123456789abcdef', k=8))
            #certificate.mainloop(screen)
            global flag
            global survivedTime
            flag = True
            if ohno:
                certificate.clear()
                certificate.add.label("Failed to connect")
            else:
                end = time.time()
                print(end-start)
                certificate.clear()
                certificate.add.label(name)
                certificate.add.label(str(datetime.timedelta(seconds=int(end-start))))
            certificate.add.button('Back', cursed)
            while flag:
                certificate.draw(screen)
                certificate.update(pygame.event.get())
                pygame.display.update()
            running = False
        for i, p in enumerate(polygons):
            #c = cols[i]
            #pyglet.graphics.draw(len(p) // 2, GL_POLYGON,
                #('v2f', p), ('c3f', c):w

            #)
            pygame.draw.polygon(surface=screen, color=cols[i], points=p)
        screen.blit(pygame.transform.flip(screen,False,True),(0,0))
        pygame.display.flip()
        clock.tick(60)

menu.mainloop(screen)
#pyglet.clock.schedule_interval(update, 1/60)
#pyglet.app.run()
