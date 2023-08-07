import pygame, sys, moderngl, pymunk
import numpy as np
from array import array
from particle import *
from shader import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

FPS = 60
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        # pygame

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Project W")
        self.clock = pygame.time.Clock()
        # opengl

        self.glcontext = moderngl.create_context()
        self.quad_buffer = self.glcontext.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,  
            1.0, 1.0, 1.0, 0.0,   
            -1.0, -1.0, 0.0, 1.0, 
            1.0, -1.0, 1.0, 1.0,  
        ]))

        self.program = self.glcontext.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.glcontext.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.buff = self.glcontext.buffer(reserve=16000)
        self.buff.bind_to_uniform_block(0)
        # ohter things

        self.space = pymunk.Space()

        self.space.gravity = (0,500)
        self.particles_values=[]
        self.particles_list=[]

        self.background = pygame.image.load('./data/back.png')

        self.create_walls()
    
    
    def create_walls(self):
        rects = [
            [(SCREEN_WIDTH/2, SCREEN_HEIGHT - 65), (SCREEN_WIDTH,130)],
            [(SCREEN_WIDTH/2, -10), (SCREEN_WIDTH,20)],
            [(SCREEN_WIDTH + 10 , SCREEN_HEIGHT/2), (20,SCREEN_HEIGHT)],
            [(-10, SCREEN_HEIGHT/2), (20,SCREEN_HEIGHT)]
        ]
        for pos,size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body,size)
            self.space.add(body, shape)
    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.space.step(1/60)
            self.render()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEMOTION:
                #for i in range(2):
                    p = Particle(event.pos[0],event.pos[1], SCREEN_WIDTH, SCREEN_HEIGHT, self.space)
                    self.particles_list.append(p)
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = self.space.gravity[1]
                self.space.gravity = (0, a*(-1))
            

    def update(self):
        for p in self.particles_list:
            p.update()
        self.particles_values = self.update_particles_values(self.particles_list)

    def render(self):
        self.display.fill(WHITE)
        self.display.blit(self.background, (0, 0))
        frame_tex = self.surface_to_texture(self.display)
        frame_tex.use(0)
        self.program['tex'] = 0
        self.program['width'] = SCREEN_WIDTH
        self.program['height'] = SCREEN_HEIGHT
        self.program['list_length'] = len(self.particles_values)
        self.buff.write(self.particles_values.tobytes())
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()
        
        frame_tex.release()

    def quit(self):
        pygame.quit()
        sys.exit()

    def surface_to_texture(self, surf):
        tex = self.glcontext.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
    
    def update_particles_values(pl,a):
        v = []
        for p in (a):
            v.append((p.x,p.y,p.r,0))
        v = np.array(v, dtype=np.float32)
        return v

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()