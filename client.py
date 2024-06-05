import pygame
from grid import Grid
import os
import threading
import socket
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the display position and size
os.environ['SDL_VIDEO_WINDOW_POS'] = '850,100'
surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Tic-tac-toe')

# Creating a TCP socket for the client
HOST = '127.0.0.1'
PORT = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


# Thread function to receive data from the server
def receive_data():
    global turn
    while True:
        data = sock.recv(1)
        while True:
            temp = sock.recv(1)
            if temp == '!'.encode():
                break
            data += temp

        data = data.decode()
        logging.debug(f'Received data: {data}')
        data = data.split('-')

        x, y = int(data[0]), int(data[1])

        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'X')


# Function to create and start a thread
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


# Run the blocking functions in a separate thread
create_thread(receive_data)

# Initialize game state
grid = Grid()
running = True
player = "O"
turn = False
playing = 'True'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    logging.debug(f'Mouse click at: {pos}, Cell: ({cellX}, {cellY})')

                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'

                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing).encode()
                    send_data += '!'.encode()
                    logging.debug(f'Sending data: {send_data}')

                    sock.send(send_data)
                    turn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = 'True'
            elif event.key == pygame.K_ESCAPE:
                running = False

    surface.fill((255, 255, 255))
    grid.draw(surface)
    pygame.display.flip()
