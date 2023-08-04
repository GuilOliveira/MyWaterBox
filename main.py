import pygame, sys, random, moderngl
from array import array
from particle import *
from shader import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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


    def run(self):
        self.particles_values=[]
        self.particles_list=[]
        for i in range(30):
            p = Particle(random.randint(1,SCREEN_WIDTH), random.randint(1,SCREEN_HEIGHT), random.randint(40,70), SCREEN_WIDTH, SCREEN_HEIGHT)
            self.particles_list.append(p)
        running = True
        while running:
            self.handle_events()
            self.update()
            self.render()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        for p in self.particles_list:
            p.update()
        self.particles_values = self.update_particles_values(self.particles_list)

    def render(self):
        self.display.fill(WHITE)
        frame_tex = self.surface_to_texture(self.display)
        frame_tex.use(0)
        self.program['tex'] = 0
        self.program['width'] = SCREEN_WIDTH
        self.program['height'] = SCREEN_HEIGHT
        self.program['list_length'] = len(self.particles_values)
        self.program['particle_list'] = self.particles_values
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
            v.append((p.x,p.y,p.r))
        return v

if __name__ == "__main__":
    game = Game()
    game.run()
