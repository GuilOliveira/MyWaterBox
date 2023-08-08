from particle import *
import random

class Playground():
    def __init__(self, space):
        self.particles_remaining=0
        self.space = space
        self.x_p_spawner = 0
        self.y_p_spawner = 0
        self.p_spread = 0
        self.particle_list = []
        self.p_freq = 0
        self.last_time = 0

    def particle_spawner(self, particle_list, amount, x, y, spread, freq):
        self.particles_remaining=amount-1
        self.x_p_spawner = x
        self.y_p_spawner = y
        self.p_spread = spread
        self.particle_list = particle_list
        self.p_freq = freq

        self.particle_list.append(
            Particle(x+random.randint(-spread,spread), y+random.randint(int(-spread/2),
                    int(spread/2)), self.space))

    def update(self ,time):
        if time>=self.last_time and self.particles_remaining>0:
            self.last_time = time
            self.particle_spawner(self.particle_list, self.particles_remaining, 
                                  self.x_p_spawner, self.y_p_spawner, self.p_spread, self.p_freq)
