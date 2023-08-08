import pygame, json

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
        self.levels = self.load_level()
        self.actual_level = self.levels["1"]
        self.actual_level_id = 1

    def get_pipes(self):
        g=[]
        b=[]
        d=[]

        level = self.actual_level["Level"]
        for x in range(len(level)):
            for y in range(len(level[x])):
                if level[x][y] == '0':
                    pass
                if level[x][y] == 'G':
                    g.append((10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
                if level[x][y] == 'B':
                    b.append((10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
                if level[x][y] == 'X':
                    d.append((10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
        return(g,b,d,(self.cell_width_ammount,self.cell_height_ammount))
    
    def get_level_data(self):
        return self.actual_level
    
    def next_level(self):
        l = len(self.levels)
        if self.actual_level_id == l:
            return{"End":1}
        self.actual_level = self.levels[str(self.actual_level_id+1)]
        self.actual_level_id+=1


    def load_level(self):
        with open('./data/levels.json', 'r') as f:
            return json.load(f)

    def render_level(self):
        level = self.actual_level["Level"]
        for x in range(len(level)):
            for y in range(len(level[x])):
                if level[x][y] == '0':
                    pass
                if level[x][y] == 'G':
                    self.display.blit(self.pipes_tex[0], (10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
                if level[x][y] == 'B':
                    self.display.blit(self.pipes_tex[1], (10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
                if level[x][y] == 'X':
                    self.display.blit(self.pipes_tex[2], (10 + (self.cell_width_ammount * y), 11 + (self.cell_height_ammount * x)))
