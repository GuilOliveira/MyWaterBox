import pygame

class Level_loader:
    def __init__(self, display, x, y, w, h, rows, cols, pipes_tex):
        self.display = display
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cell_width_ammount = int(w/rows)
        self.cell_height_ammount = int(h/cols)
        self.rows = rows
        self.cols = cols
        self.pipes_tex = pipes_tex

        self.actual_level = level_1

    def load_level(self):
        pass

    def render_level(self):
        level = self.actual_level
        for x in range(len(level)):
            for y in range(len(level[x])):  # Corrected the loop to iterate over columns
                if level[x][y] == '0':
                    pass
                if level[x][y] == 'G':
                    self.display.blit(self.pipes_tex[0], (10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
                if level[x][y] == 'B':
                    self.display.blit(self.pipes_tex[1], (10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
                if level[x][y] == 'X':
                    self.display.blit(self.pipes_tex[2], (10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))


level_1 = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', '0'],
    ['0', 'G', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', 'B', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'B']
]