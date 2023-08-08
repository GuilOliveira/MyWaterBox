import pygame, sys, moderngl, pymunk
import numpy as np
from array import array
from particle import *
from shader import *
from playground import *
from linetracer import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576
PLAYGROUND_WIDTH = 1004
PLAYGROUND_HEIGHT = 436
PLAYGROUND_POS = (10, 10)
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

        self.playground = Playground(self.space)
        self.dt = 0
        self.total_time = 0
        self.lines = []
        self.actual_line = 0
        self.background = pygame.image.load('./data/back.png')

        self.create_walls()
    
    def render_grid(self):
        rows = 7
        cols = 17
        cell_width = int(PLAYGROUND_WIDTH/cols)
        cell_height = int(PLAYGROUND_HEIGHT/rows)
        grid_color = (0, 255, 0)

        for y in range(15, PLAYGROUND_WIDTH+15, cell_height):
            pygame.draw.line(self.display, grid_color, (y, 29), (y, PLAYGROUND_HEIGHT+6))
            for x in range(29, PLAYGROUND_HEIGHT+29, cell_width):
                pygame.draw.line(self.display, grid_color, (15, x), (PLAYGROUND_WIDTH+3, x))

    def create_walls(self):
        rects = [
            [(SCREEN_WIDTH/2, SCREEN_HEIGHT - 65), (SCREEN_WIDTH,130)],
            [(SCREEN_WIDTH/2, 0), (SCREEN_WIDTH,20)],
            [(SCREEN_WIDTH, SCREEN_HEIGHT/2), (20,SCREEN_HEIGHT)],
            [(0, SCREEN_HEIGHT/2), (20,SCREEN_HEIGHT)]
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

            self.dt = self.clock.tick(60)
            self.total_time+=self.dt

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.playground.particle_spawner(self.particles_list, 40, 70,70,3,200)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                a = self.space.gravity[1]
                self.space.gravity = (0, a*(-1))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.actual_line = Linetracer(self.get_mouse_playground()[0],self.get_mouse_playground()[1], self.space)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.actual_line.end_line(self.get_mouse_playground()[0],self.get_mouse_playground()[1])
                self.lines.append(self.actual_line)
                self.actual_line = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset()

    def get_mouse_playground(self):
        mouse=pygame.mouse.get_pos()
        
        if mouse[0]<10:
            x = 10
        elif mouse[0]>PLAYGROUND_WIDTH+10:
            x = PLAYGROUND_WIDTH+10
        else:
            x=mouse[0]
        if mouse[1]<10:
            y = 10
        elif mouse[1]>PLAYGROUND_HEIGHT+10:
            y = PLAYGROUND_HEIGHT+10
        else:
            y=mouse[1]

        return (x, y)

    def update(self):
        self.playground.update(self.total_time)
        for p in self.particles_list:
            p.update()
        if self.actual_line:
            self.actual_line.update(self.get_mouse_playground()[0], self.get_mouse_playground()[1])
        self.particles_values = self.update_particles_values(self.particles_list)

    def render(self):
        self.display.fill(WHITE)
        self.display.blit(self.background, (0, 0))
        self.render_grid()
        if self.actual_line:
            for i in range(1, len(self.actual_line.points)):
                pygame.draw.line(self.display, (60, 60, 60), self.actual_line.points[i-1], self.actual_line.points[i], 6)
        for l in self.lines:
            for i in l.body.shapes:
                if isinstance(i, pymunk.Segment):
                    a = l.body.local_to_world(i.a)
                    b = l.body.local_to_world(i.b)
                    pygame.draw.line(self.display, (0, 0, 0), a, b, 6)
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
    
    def reset(self):
        self.particles_list=[]
        self.lines=[]
        for shape in self.space.shapes[:]:
            self.space.remove(shape)
        for body in self.space.bodies[:]:
            self.space.remove(body)
        self.create_walls()
    
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