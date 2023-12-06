import pygame
from sys import exit
from character import Character

class Game(object):

    def __init__(self):
        #Config
        self.tps_max = 60.0
        self.tps_delta = 0.0

        #Inicialization
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Rakieta")
        self.tps_clock = pygame.time.Clock()
        #Add players
        self.player = Character(self)

        while True:
            # Handle events
            for event in pygame.event.get():
            # Closing program
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #self.player.shoot()
                    print("Strzał")

            # Cap the frame rate
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            #Drawing
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    def tick(self):
        self.player.tick()

    def draw(self):
        self.player.draw()

if __name__ == "__main__":
    Game()