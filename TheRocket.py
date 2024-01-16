import pygame
from pygame.math import Vector2
from sys import exit
import random
import time

class Game(object):
    def __init__(self):
        # Config
        self.tps_max = 60.0
        self.tps_delta = 0.0
        self.bullets = []
        self.score = 0

        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.elapsed_time = 0

        # Initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("The Rocket")
        self.tps_clock = pygame.time.Clock()

        # Add player
        self.player = Character(self)
        # Add enemies
        self.enemies = [Enemy(self) for enemy in range(random.randint(1, 20))]

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
        # Update all enemies
        for enemy in self.enemies:
            enemy.tick()

        self.check_collision()
        self.check_player_collision()

        # delete enemies who out from screen
        self.enemies = [enemy for enemy in self.enemies if 0 <= enemy.enemy_pos.x <= self.screen.get_width() - 30 and 0 <= enemy.enemy_pos.y <= self.screen.get_height() - 30]

        self.elapsed_time = time.time() - self.start_time

    def draw(self):
        for bullet in self.bullets:
            bullet.tick()
            bullet.draw()

        for obj in [self.player] + self.enemies:
            obj.draw()

        self.draw_score()
        self.draw_time()

    def check_collision(self):
        for bullet in self.bullets:
            for enemy in self.enemies:
                if pygame.Rect(enemy.enemy_pos.x, enemy.enemy_pos.y, 30, 30).colliderect(pygame.Rect(bullet.bullet_pos.x - 2, bullet.bullet_pos.y - 2, 4, 4)):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1
        if not self.enemies:
            self.spawn_enemies()

    def check_player_collision(self):
        player_rect = pygame.Rect(self.player.pos.x - 10, self.player.pos.y - 20, 20, 20)
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.enemy_pos.x, enemy.enemy_pos.y, 30, 30)
            if player_rect.colliderect(enemy_rect):
                self.restart_game()
                self.score = 0

    def restart_game(self):
        self.player = Character(self)
        self.enemies = [Enemy(self) for _ in range(random.randint(1, 20))]
        self.bullets = []

        self.start_time = time.time()
        self.elapsed_time = 0

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_time(self):
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {int(self.elapsed_time)}s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 40))

    def spawn_enemies(self):
        self.enemies = [Enemy(self) for _ in range(random.randint(1, 20))]
        player_rect = pygame.Rect(self.player.pos.x - 10, self.player.pos.y - 20, 20, 20)

        for enemy in self.enemies:
            while True:
                enemy.enemy_pos = Vector2(random.randint(30, self.screen.get_width() - 30),random.randint(30, self.screen.get_height() - 30))
                # check if enemie are enought far from player
                if pygame.Rect(enemy.enemy_pos.x, enemy.enemy_pos.y, 30, 30).colliderect(player_rect.inflate(10, 10)):
                    continue
                else:
                    break

    def check_enemy_collision(self):
        for i, enemy1 in enumerate(self.enemies):
            for j, enemy2 in enumerate(self.enemies):
                if i != j:
                    #check colicion between enemies
                    if pygame.Rect(enemy1.enemy_pos.x, enemy1.enemy_pos.y, 30, 30).colliderect(pygame.Rect(enemy2.enemy_pos.x, enemy2.enemy_pos.y, 30, 30)):
                        # change direction of enemies who colide 
                        enemy1.enemy_dir *= -1
                        enemy2.enemy_dir *= -1

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
        # Inputs
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

        # Draw triangle (player)
        pygame.draw.polygon(self.game.screen, (255, 125, 98), points)

    def shoot(self):
        if self.vel.length() > 0:
            bullet = Bullet(self.game, self.pos, self.vel.normalize())
            self.game.bullets.append(bullet)


class Bullet(object):
    def __init__(self, game, pos, direction):
        self.bullet_speed = 2.0
        self.game = game
        self.bullet_pos = Vector2(pos)
        self.direction = direction.normalize()

    def tick(self):
        # Changing bullets pos with direction of character
        self.bullet_pos += self.bullet_speed * self.direction
        # delete bullets out of screen
        if self.bullet_pos[0] < 0 or self.bullet_pos[0] > 1280 or self.bullet_pos[1] < 0 or self.bullet_pos[1] > 720:
            self.game.bullets.remove(self)

        self.game.check_collision()

    def draw(self):
        pygame.draw.circle(self.game.screen, (255, 255, 255), (int(self.bullet_pos[0]), int(self.bullet_pos[1])), 4)


class Enemy(object):
    def __init__(self, game):
        self.game = game
        self.enemy_pos = Vector2(random.randint(30, self.game.screen.get_width() - 30), random.randint(30, self.game.screen.get_height() - 30))
        self.enemy_dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.enemy_speed = 2.7
        

    def tick(self):
        self.enemy_pos += self.enemy_dir * self.enemy_speed

        # check colision with enemies and change direction
        for other_enemy in self.game.enemies:
            if other_enemy != self:
                if pygame.Rect(self.enemy_pos.x, self.enemy_pos.y, 30, 30).colliderect(pygame.Rect(other_enemy.enemy_pos.x, other_enemy.enemy_pos.y, 30, 30)):
                    self.enemy_dir *= -1
                    other_enemy.enemy_dir *= -1

        # change direction if touch walls
        if self.enemy_pos.x < 0:
            self.enemy_pos.x = 0
            self.enemy_dir.x *= -1
        elif self.enemy_pos.x > self.game.screen.get_width() - 30:
            self.enemy_pos.x = self.game.screen.get_width() - 30
            self.enemy_dir.x *= -1

        if self.enemy_pos.y < 0:
            self.enemy_pos.y = 0
            self.enemy_dir.y *= -1
        elif self.enemy_pos.y > self.game.screen.get_height() - 30:
            self.enemy_pos.y = self.game.screen.get_height() - 30
            self.enemy_dir.y *= -1

    def draw(self):
        pygame.draw.rect(self.game.screen, (173, 25, 14), (self.enemy_pos[0], self.enemy_pos[1], 30, 30))

if __name__ == "__main__":
    Game()
