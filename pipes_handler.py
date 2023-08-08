import pymunk

class Pipes_handler:
    def __init__(self, space):
        self.space = space
        self.blue_pipes = []
        self.dark_pipes = []

    def load_pipes(self, pipes):
        fds, blue_pipes, dark_pipes, size = pipes
        for i in blue_pipes:
            self.blue_pipes.append(Pipes(self.space, i, 1, size))
        for i in dark_pipes:
            self.dark_pipes.append(Pipes(self.space, i, 2, size))

    def clear_pipes(self):
        self.blue_pipes = []
        self.dark_pipes = []

class Pipes:
    def __init__(self, space, pos, t, size):
        print(pos)
        body = pymunk.Body(20, 0.1, body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        shape = pymunk.Circle(body, 24)
        shape.sensor = True
        shape.collision_type = t
        
        
        space.add(body, shape)