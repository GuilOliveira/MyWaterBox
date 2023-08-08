import pymunk

class Linetracer():
    def __init__(self, x, y, space):
        self.points = []
        
        self.create_points(x, y)
        self.space = space

        self.body = pymunk.Body(20, 80, body_type=pymunk.Body.DYNAMIC)
        self.segments = []
        

    def create_points(self, x, y):
        if len(self.points) >= 1:
            shape = pymunk.Segment(self.body, self.points[-1], (x,y),3)
            shape.mass = 40
            shape.elasticity = 0.5
            shape.friction = 0.2
            shape.density = 80
            
            self.segments.append(shape)
        self.points.append((x,y))
    
    def end_line(self, x, y):
        self.create_points(x, y)
        self.space.add(self.body, *self.segments)

    def update(self, x, y):
        if abs(x-self.points[-1][0])>3 or (abs(y-self.points[-1][1])>3):
            self.create_points(x,y)
    

    
