import pygame

class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.bgcolor = 204, 170, 102
        self.fgcolor = 186, 156, 93
        self.paintcolor = 204, 102, 192
        self.screen = pygame.display.set_mode((cell_size * width, cell_size * height))
        self.painted = set()
        
    def draw(self):
        cell_size = self.cell_size
        # Background
        self.screen.fill(self.bgcolor)
        # Painted cells
        for cell in self.painted:
            x = cell[0] * cell_size
            y = (self.height - cell[1] - 1) * cell_size
            pygame.draw.rect(self.screen, self.paintcolor, pygame.Rect(x, y, cell_size, cell_size))
        # Grid lines
        for i in range(1, self.width):
            x = self.cell_size * i
            pygame.draw.line(self.screen, self.fgcolor, (x, 0), (x, cell_size * self.height), 2)
        for j in range(1, self.height):
            y = self.cell_size * j
            pygame.draw.line(self.screen, self.fgcolor, (0, y), (cell_size * self.width, y), 2)
    
    def get_win_pos(self, x, y):
        return (x + 0.5) * self.cell_size, (self.height - y - 0.5) * self.cell_size
    
    def get_board_pos(self, wx, wy):
        return int(wx // self.cell_size), self.height - int(wy // self.cell_size) - 1
    
    def is_valid_pos(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    # Get adjacent cells (ignore walls)
    def get_adjs_no_wall(self, pos):
        adjs = []
        x, y = pos
        # Check boundary
        if x > 0: adjs.append((x - 1, y))
        if x < self.width - 1: adjs.append((x + 1, y))
        if y > 0: adjs.append((x, y - 1))
        if y < self.height - 1: adjs.append((x, y + 1))
        return adjs
    
    # Get adjacent cells (with walls)
    def get_adjs(self, pos):
        return self.get_adjs_no_wall(pos)

    def can_move(self, x1, y1, x2, y2):
        return self.is_valid_pos(x2, y2)