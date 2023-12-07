import pygame
from pygame.math import Vector2
from sys import exit
import random

class Game(object):
    def __init__(self):
        # Config
        self.tps_max = 60.0
        self.tps_delta = 0.0
        self.bullets = []

        # Initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Rakieta")
        self.tps_clock = pygame.time.Clock()

        # Add player
        self.player = Character(self)
        #Add enemies
        self.enemies = [Enemy(self) for enemy in range(random.randint(1,20))]

        while True:
            # Handle events
            for event in pygame.event.get():
                # Closing program
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit(0)
                # Shoot
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.shoot()

            # Cap the frame rate
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            # Drawing
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    def tick(self):
        self.player.tick()
        #Update all enemies
        for enemy in self.enemies:
            enemy.tick()

    def draw(self):
        for bullet in self.bullets:
            bullet.tick()
            bullet.draw()

        for obj in [self.player] + self.enemies:
            obj.draw()

class Character(object):
    def __init__(self, game):
        self.game = game
        self.speed = 1.0

        size = self.game.screen.get_size()

        self.pos = Vector2(size[0] / 2, size[1] / 2)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def add_force(self, force):
        self.acc += force

    def tick(self):
        # Input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w] and self.pos[1] > 20:
            self.add_force(Vector2(0, -self.speed))
        if pressed[pygame.K_s] and self.pos[1] < 700:
            self.add_force(Vector2(0, self.speed))
        if pressed[pygame.K_d] and self.pos[0] < 1260:
            self.add_force(Vector2(self.speed, 0))
        if pressed[pygame.K_a] and self.pos[0] > 20:
            self.add_force(Vector2(-self.speed, 0))

        # Physics
        self.vel *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

    def draw(self):
        # Base triangle
        points = [Vector2(0, -20), Vector2(10, 10), Vector2(-10, 10)]

        # Rotation
        angle = self.vel.angle_to(Vector2(0, 1))
        points = [p.rotate(angle) for p in points]

        # Fix Y axis
        points = [Vector2(p.x, p.y * -1) for p in points]

        # Add current position
        points = [self.pos + p for p in points]

        # Draw triangle
        pygame.draw.polygon(self.game.screen, (255, 125, 98), points)

    def shoot(self):
        bullet = Bullet(self.game, self.pos, self.vel.normalize())
        self.game.bullets.append(bullet)


class Bullet(object):
    def __init__(self, game, pos, direction):
        self.bullet_speed = 2.0
        self.game = game
        self.bullet_pos = Vector2(pos)
        self.direction = direction.normalize()

    def tick(self):
        #Changing bulets pos with direction of character
        self.bullet_pos += self.bullet_speed * self.direction
        #delete bullets out of sreen
        if self.bullet_pos[0] < 0 or self.bullet_pos[0] > 1280 or self.bullet_pos[1] < 0 or self.bullet_pos[1] > 720:
            self.game.bullets.remove(self)
            #print(self.game.bullets)

    def draw(self):
        pygame.draw.circle(self.game.screen, (255, 255, 255), (int(self.bullet_pos[0]), int(self.bullet_pos[1])), 4)



class Enemy(object):
    def __init__(self, game):
        self.game = game
        self.enemy_pos = Vector2(random.randint(0, 1280), random.randint(0, 720))
        self.enemy_dir = Vector2(random.randint(-1,1), random.randint(-1, 1))
        self.enemy_speed = 0.7
    
    def tick(self):
        if (
            self.enemy_pos.x < 0
            or self.enemy_pos.x > self.game.screen.get_width()
            or self.enemy_pos.y < 0
            or self.enemy_pos.y > self.game.screen.get_height()
        ):
            # Jeśli przeciwnik opuścił obszar, zmień kierunek ruchu losowo
            self.enemy_dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            
        self.enemy_pos += self.enemy_dir * self.enemy_speed

    def draw(self):
        pygame.draw.rect(self.game.screen, (173, 25, 14), (self.enemy_pos[0], self.enemy_pos[1], 30, 20))

if __name__ == "__main__":
    Game()