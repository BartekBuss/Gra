import pygame
from pygame.math import Vector2

class Character(object):
    
    def __init__(self, game):
        self.game = game
        self.speed = 1.0

        size = self.game.screen.get_size()

        self.pos = Vector2(size[0]/2, size[1]/2)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def add_force(self, force):
        self.acc += force

    def tick(self):
        #Input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.add_force(Vector2(0, -self.speed))
        if pressed[pygame.K_s]:
            self.add_force(Vector2(0, self.speed))
        if pressed[pygame.K_d]:
            self.add_force(Vector2(self.speed, 0))
        if pressed[pygame.K_a]:
            self.add_force(Vector2(-self.speed, 0))
        
        
        #add shooting


        #Physics
        self.vel *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

    def draw(self):
        #Drawing main Character
        #rect = pygame.Rect(self.pos.x, self.pos.y, 50, 50)
        #pygame.draw.rect(self.game.screen, (255, 125, 98), rect)
        
        #Base triangle
        points = [Vector2(0, -20), Vector2(10, 10), Vector2(-10, 10)]

        #Rotation
        angle = self.vel.angle_to(Vector2(0, 1))
        
        points = [p.rotate(angle) for p in points]

        #Fix Y axis
        points = [Vector2(p.x, p.y * -1) for p in points]

        #Add current position
        points = [self.pos+p for p in points]

        #Draw triangle
        pygame.draw.polygon(self.game.screen, (255,125,98), points)