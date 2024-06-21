import pygame
import math
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Frames per second
FPS = 60
# Base health
BASE_HEALTH = 100

class Tower:
    def __init__(self, x, y, damage=10, range=100, cooldown_max=60):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.cooldown = 0
        self.cooldown_max = cooldown_max

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 20)

    def attack(self, enemies):
        if self.cooldown == 0:
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance <= self.range:
                    enemy.hp -= self.damage
                    self.cooldown = self.cooldown_max
                    break
        else:
            self.cooldown -= 1

class Enemy:
    def __init__(self, path, hp=100, speed=2, color=RED):
        self.path = path
        self.x, self.y = path[0]
        self.hp = hp
        self.speed = speed
        self.path_index = 0
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            angle = math.atan2(target_y - self.y, target_x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
            if math.hypot(target_x - self.x, target_y - self.y) < self.speed:
                self.path_index += 1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Enhanced Tower Defence Game")
        self.clock = pygame.time.Clock()
        self.towers = []
        self.path = [(50, 300), (200, 300), (200, 500), (600, 500), (600, 200), (750, 200)]
        self.enemies = [Enemy(self.path)]
        self.base_health = BASE_HEALTH
        self.font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.towers.append(Tower(x, y))

            self.screen.fill(WHITE)

            for tower in self.towers:
                tower.draw(self.screen)
                tower.attack(self.enemies)

            for enemy in self.enemies[:]:
                enemy.move()
                enemy.draw(self.screen)
                if enemy.path_index == len(self.path) - 1:
                    self.base_health -= 10
                    self.enemies.remove(enemy)
                elif enemy.hp <= 0:
                    self.enemies.remove(enemy)

            if random.randint(0, 100) < 2:
                self.enemies.append(Enemy(self.path))

            health_text = self.font.render(f"Base Health: {self.base_health}", True, BLACK)
            self.screen.blit(health_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
