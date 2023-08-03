import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)

# Game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("My Pygame Project")
        self.clock = pygame.time.Clock()

    def run(self):
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
        pass  # Add your game logic here

    def render(self):
        self.screen.fill(WHITE)
        # Add code to draw game objects here

        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
