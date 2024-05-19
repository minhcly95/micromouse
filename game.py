import sys, pygame
from .tweens import *
from .board import Board
from .maze import MazeBoard
from .mouse import Mouse
from .cheese import Cheese

pygame.init()
pygame.display.set_caption('Micromouse')

clock = pygame.time.Clock()
board = Board(5, 5, 80)
mouse = Mouse(board)
cheese = Cheese(board)
cheese_times = 0
mouse_speed = 1

def exit_when_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def set_cheese_pos():
    global cheese_times
    if cheese_times > 0:
        cheese.set_random_pos([mouse.get_pos()])
        cheese_times -= 1
    else:
        cheese.set_pos(-1, -1)

def game_draw():
    board.draw()
    cheese.draw()
    mouse.draw()
    pygame.display.flip()

def game_loop_until_idle():
    while not mouse.is_idle():
        exit_when_quit()
        dt = clock.tick(60) / 1000
        mouse.update(dt * mouse_speed)
        game_draw()

def game_loop_infinite():
    while True:
        exit_when_quit()
        game_draw()
        
def check_cheese(mouse: Mouse, cheese: Cheese):
    if mouse.get_pos() == cheese.get_pos():
        print("Nom nom nom :D")
        set_cheese_pos()

def init(width = 5, height = 5, scale = 1.):
    global board, mouse, cheese
    board = Board(width, height, scale * 80)
    mouse = Mouse(board)
    cheese = Cheese(board)
    mouse.set_pos(1, 1)
    set_cheese_pos()

def init_maze(width = 5, height = 5, scale = 1.):
    global board, mouse, cheese
    board = MazeBoard(width, height, scale * 80)
    mouse = Mouse(board)
    cheese = Cheese(board)
    mouse.set_pos(1, 1)
    set_cheese_pos()

def show_cheese(times = 1):
    global cheese_times
    cheese_times = times
    set_cheese_pos()

def set_mouse_speed(speed = 1):
    global mouse_speed
    mouse_speed = speed

def step(r, x, y):
    result = mouse.step_to(r, x, y)
    game_loop_until_idle()
    check_cheese(mouse, cheese)
    return result

def east(): return step(0, 1, 0)
def north(): return step(2, 0, 1)
def west(): return step(4, -1, 0)
def south(): return step(6, 0, -1)

def get_mouse_pos(): return mouse.get_pos()
def get_cheese_pos(): return cheese.get_pos()
def get_neighbors(x, y): return board.get_adjs((x, y))

def paint():
    mouse.wait(0.2)
    game_loop_until_idle()
    mouse.paint()
    mouse.wait(0.2)
    game_loop_until_idle()

def done():
    game_loop_infinite()
