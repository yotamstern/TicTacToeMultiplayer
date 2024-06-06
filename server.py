import pygame
from grid import Grid
import threading
import socket
import os
import logging

# Configure logging to output debug information
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Pygame and set up the display window
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'
surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Tic Tac Toe Server')

# Networking setup: Define the host and port for the server
HOST = '127.0.0.1'
PORT = 65432
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

# Variables to manage the connection state
connection_established = False
conn, addr = None, None

# Initialize the game grid
grid = Grid()


def receive_data():
    """
    Function to receive data from the client. It continuously listens for
    data, processes it via a communications protocol, and updates the game accordingly.
    """
    global turn
    while True:
        try:
            data = conn.recv(1)
            while True:
                temp = conn.recv(1)
                if temp == '!'.encode():
                    break
                data += temp

            data = data.decode()
            logging.debug(f'Received data: {data}')
            x, y, turn_flag, game_over_flag = data.split('-')

            x, y = int(x), int(y)

            if turn_flag == 'yourturn':
                turn = True
            if game_over_flag == 'False':
                grid.game_over = True
            if grid.get_cell_value(x, y) == 0:
                grid.set_cell_value(x, y, 'O')
        except socket.error as e:
            logging.error(f"Error receiving data: {e}")
            break


def waiting_for_connection():
    """
    Function to wait for a client to connect. Once a client connects,
    it starts the receive_data function in a new thread.
    """
    global connection_established, conn, addr
    try:
        conn, addr = sock.accept()  # wait for a connection, it is a blocking method
        logging.info('Client is connected')
        connection_established = True
        receive_data()
    except socket.error as e:
        logging.error(f"Error accepting connection: {e}")


def create_thread(target):
    """
    Function to create and start a new thread for the given target function.
    """
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


def main():
    """
    Main function to run the game server. It initializes the connection,
    handles game events, and updates the display.
    """
    create_thread(waiting_for_connection)

    running = True
    player = "X"
    global turn
    turn = True
    playing = 'True'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
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

                        try:
                            conn.send(send_data)
                        except socket.error as e:
                            logging.error(f"Error sending data: {e}")
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

    pygame.quit()


if __name__ == "__main__":
    main()
