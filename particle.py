import random, pymunk

class Particle:
    def __init__(self, x, y, w, h, space):
        self.x = x
        self.y = y
        self.pos = (x, y)  # Store the position as a tuple
        self.w = w
        self.h = h
        self.r = 4

        self.body = pymunk.Body(20, 80, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (self.x, self.y)
        shape = pymunk.Circle(self.body, self.r)
        shape.mass = 40
        shape.elasticity = random.randint(50, 80)/100
        shape.friction = random.randint(20, 80)/100
        shape.density = random.randint(50, 80)
        space.add(self.body, shape)
        
    
    def update(self):
        self.x = self.body.position.x
        self.y = self.body.position.y
        self.pos = (self.x, self.y)

    
