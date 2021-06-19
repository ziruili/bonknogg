import threading
import socket
import time
import sys
import json
from server.world import WorldManager

host = sys.argv[1]

wm = WorldManager()

def main_game():
    while True:
        wm.step()

def main():
    game = threading.Thread(target=main_game)
    game.start()

    print('Ready')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 6969))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                response = wm.parse(json.loads(conn.recv(1024).decode('utf-8')))
                conn.sendall(response.encode('utf-8'))

main()
