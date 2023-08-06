import random, math, pymunk

class Particle:
    def __init__(self,x,y,w,h,space):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        
        self.r = 7

        self.body = pymunk.Body(20,80,body_type=pymunk.Body.DYNAMIC)
        self.body.position = (self.x,self.y)
        shape = pymunk.Circle(self.body, self.r)
        shape.mass=40
        shape.elasticity = 0.72
        shape.friction = 0.5
        space.add(self.body, shape)
        

    def update(self):
        self.x=self.body.position.x
        self.y=self.body.position.y
       # print(self.y)
