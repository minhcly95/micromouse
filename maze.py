import random, pygame
from .board import Board

class MazeBoard(Board):
    def __init__(self, width, height, cell_size):
        super().__init__(width, height, cell_size)
        self.wallcolor = 64, 37, 3
        self.generate()

    # New draw function to draw the walls
    def draw(self):
        super().draw()
        cell_size = self.cell_size
        for (x1, y1, x2, y2) in self.walls:
            if (x1 == x2):
                # Horizontal wall
                x_start = x1 * cell_size
                x_end = x_start + cell_size
                y = (self.height - y2) * cell_size
                pygame.draw.line(self.screen, self.wallcolor, (x_start, y), (x_end, y), 6)
            elif (y1 == y2):
                # Vertical wall
                y_start = (self.height - 1 - y1) * cell_size
                y_end = y_start + cell_size
                x = x2 * cell_size
                pygame.draw.line(self.screen, self.wallcolor, (x, y_start), (x, y_end), 6)

    # Generate the maze
    def generate(self):
        w, h = self.width, self.height
        # List all possible walls
        walls = {(x, y, x + 1, y) for x in range(w - 1) for y in range(h)}
        walls |= {(x, y, x, y + 1) for x in range(w) for y in range(h - 1)}
        # Assign random weights (both directions)
        weights = dict()
        for (x1, y1, x2, y2) in walls:
            weight = random.random()
            weights[(x1, y1, x2, y2)] = weight
            weights[(x2, y2, x1, y1)] = weight
        # Find minimum spanning tree using Prim's algorithm
        visited = {(0, 0)}
        candidates = {(0, 0, 1, 0), (0, 0, 0, 1)}
        # If there're still unvisited cells
        while len(candidates) > 0:
            # Find the minimum weight candidate
            min_weight = min(weights[i] for i in candidates)
            x1, y1, x2, y2 = next(filter(lambda i: weights[i] == min_weight, candidates))
            # Remove the candidate wall
            candidates.remove((x1, y1, x2, y2))
            walls -= {(x1, y1, x2, y2), (x2, y2, x1, y1)}
            # Flag the visited cell
            visited.add((x2, y2))
            # Add new candidates (neighbors of (x2, y2))
            for (x3, y3) in self.get_adjs_no_wall((x2, y2)):
                candidates.add((x2, y2, x3, y3))
            # Filter out all visited candidates
            candidates = {c for c in candidates if (c[2], c[3]) not in visited}
        # Finalize
        self.walls = walls
        self.double_walls = walls | {(x2, y2, x1, y1) for (x1, y1, x2, y2) in walls}

    # Get adjacent cells (with walls)
    def get_adjs(self, pos):
        x, y = pos
        adjs = self.get_adjs_no_wall(pos)
        # Check wall
        return [(ax, ay) for (ax, ay) in adjs if (x, y, ax, ay) not in self.double_walls]
    
    # Prevent moving through walls
    def can_move(self, x1, y1, x2, y2):
        return super().can_move(x1, y1, x2, y2) and (x1, y1, x2, y2) not in self.double_walls