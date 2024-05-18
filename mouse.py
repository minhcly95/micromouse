import pygame, os
from .tweens import *
from math import sqrt
from .board import Board

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

class Mouse:
    def __init__(self, board: Board):
        self.board = board
        # Preprocess the sprite
        centered = pygame.Surface((200, 200), pygame.SRCALPHA)
        mouse_sprite = pygame.image.load(os.path.join(get_script_path(), "mouse.png"))
        centered.blit(mouse_sprite, (100 - 25, 100 - 35))
        self.image = pygame.transform.scale(centered, (2 * board.cell_size, 2 * board.cell_size))
        self.image = pygame.transform.rotate(self.image, -90)
        # Attributes
        self.position = (0, 0)
        self.rotation = 0
        self.tweens = []
        # Parameters
        self.move_speed = 0.8   # seconds per cell
        self.rot_speed = 2      # seconds per revolution

    def draw(self):
        rotated = pygame.transform.rotate(self.image, self.rotation)
        draw_x = self.position[0] - rotated.get_rect().centerx
        draw_y = self.position[1] - rotated.get_rect().centery
        self.board.screen.blit(rotated, (draw_x, draw_y))

    # Tweening
    def update(self, dt):
        if (len(self.tweens) > 0):              # If there's a tween, update the first tween
            if (self.tweens[0].update(dt)):     # Returning True means the tween is done
                self.tweens.pop(0)
    
    def is_idle(self):
        return len(self.tweens) == 0
    
    # Get/set cell position
    def get_pos(self):
        return self.board.get_board_pos(*self.position)

    def set_pos(self, x: int, y: int):
        self.position = self.board.get_win_pos(x, y)

    # Get/set cell rotation (0 is east, 2 is north, 4 is west, 6 is south, odd numbers for diagonals)
    def get_rot(self):
        return int((self.rotation + 22.5) // 45) % 8

    def set_rot(self, r: int):
        self.rotation = r * 45

    # Tween queueing functions
    def step_to(self, r, dx, dy):
        if self.get_rot() != r:
            dr = (self.get_rot() - r) % 8
            if dr > 4: dr -= 8
            self.tweens.append(RotTween(self, r * 45, self.rot_speed * abs(dr) / 8))

        ds = sqrt(dx * dx + dy * dy)
        x, y = self.get_pos()
        xx, yy = x + dx, y + dy

        if self.board.can_move(x, y, xx, yy):
            self.tweens.append(PosTween(self, self.board.get_win_pos(xx, yy), self.move_speed * ds))
            return True
        else:
            xi, yi = x + 0.2 * dx, y + 0.2 * dy
            self.tweens.append(PosTween(self, self.board.get_win_pos(xi, yi), self.move_speed * ds * 0.4))
            self.tweens.append(PrintTween(f"Can't go from {(x, y)} to {(xx, yy)} :("))
            self.tweens.append(PosTween(self, self.board.get_win_pos(x, y), self.move_speed * ds * 0.4))
            self.tweens.append(WaitTween(0.1))
            return False
    
    def wait(self, t):
        self.tweens.append(WaitTween(t))

    # Extra functions
    def paint(self):
        self.board.painted.add(self.get_pos())