import pygame, random, os
from .board import Board

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

class Cheese:
    def __init__(self, board: Board):
        self.board = board
        # Preprocess the sprite
        cheese_sprite = pygame.image.load(os.path.join(get_script_path(), "cheese.png"))
        self.image = pygame.transform.scale(cheese_sprite, (0.7 * board.cell_size, 0.7 * board.cell_size))
        # Attributes
        self.position = (0, 0)

    def draw(self):
        draw_x = self.position[0] - self.image.get_rect().centerx
        draw_y = self.position[1] - self.image.get_rect().centery
        self.board.screen.blit(self.image, (draw_x, draw_y))
    
    # Get/set cell position
    def get_pos(self):
        return self.board.get_board_pos(*self.position)

    def set_pos(self, x: int, y: int):
        self.position = self.board.get_win_pos(x, y)

    def set_random_pos(self, exclude = []):
        while True:
            x = random.randrange(self.board.width)
            y = random.randrange(self.board.height)
            if not (x, y) in exclude:
                self.set_pos(x, y)
                break