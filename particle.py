import random, math

class Particle:
    def __init__(self,x,y,r,w,h):
        self.x=x
        self.y=y
        self.w=w/3
        self.h=h/3
        self.r=r

        self.angle=random.randint(0,int(2*math.pi))
        self.x_speed=random.randint(12,20)*math.cos(self.angle)
        self.y_speed=random.randint(12,20)*math.sin(self.angle)

    def update(self):
        self.x+=self.x_speed
        self.y+=self.y_speed

        if (self.x>self.w) or (self.x<0):
            self.x_speed*=-1
        if (self.y>self.h) or (self.y<0):
            self.y_speed*=-1
    