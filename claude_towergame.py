import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Styled Tower Defense")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game objects
class Enemy:
    def __init__(self, path, enemy_type):
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[0]
        self.enemy_type = enemy_type
        
        if enemy_type == "normal":
            self.color = RED
            self.speed = 1
            self.health = 100
            self.max_health = 100
            self.size = 20
        elif enemy_type == "fast":
            self.color = YELLOW
            self.speed = 2
            self.health = 50
            self.max_health = 50
            self.size = 15
        elif enemy_type == "tank":
            self.color = GREEN
            self.speed = 0.5
            self.health = 200
            self.max_health = 200
            self.size = 25

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.speed:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            else:
                self.path_index += 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        inner_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50))
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), self.size // 2)
        
        # Health bar
        bar_width = 40
        bar_height = 5
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - bar_width // 2, self.y - self.size - 10, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x - bar_width // 2, self.y - self.size - 10, bar_width * health_percentage, bar_height))

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        
        if tower_type == "basic":
            self.color = BLUE
            self.range = 150
            self.damage = 10
            self.cooldown = 60
        elif tower_type == "sniper":
            self.color = PURPLE
            self.range = 250
            self.damage = 30
            self.cooldown = 120
        elif tower_type == "machine_gun":
            self.color = ORANGE
            self.range = 100
            self.damage = 5
            self.cooldown = 20
        
        self.cooldown_timer = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - 20, self.y - 20, 40, 40))
        pygame.draw.rect(screen, WHITE, (self.x - 15, self.y - 15, 30, 30))
        pygame.draw.rect(screen, self.color, (self.x - 10, self.y - 10, 20, 20))

    def attack(self, enemies):
        if self.cooldown_timer <= 0:
            for enemy in enemies:
                distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                if distance <= self.range:
                    enemy.health -= self.damage
                    self.cooldown_timer = self.cooldown
                    # Draw attack line
                    pygame.draw.line(screen, YELLOW, (self.x, self.y), (enemy.x, enemy.y), 2)
                    break
        else:
            self.cooldown_timer -= 1

# Helper functions
def draw_gradient_rect(surface, color, rect):
    color2 = (max(0, color[0] - 100), max(0, color[1] - 100), max(0, color[2] - 100))
    for i in range(rect.height):
        ratio = i / rect.height
        new_color = (
            int(color[0] * (1 - ratio) + color2[0] * ratio),
            int(color[1] * (1 - ratio) + color2[1] * ratio),
            int(color[2] * (1 - ratio) + color2[2] * ratio)
        )
        pygame.draw.line(surface, new_color, (rect.left, rect.top + i), (rect.right, rect.top + i))

# Game state
path = [(0, 300), (200, 300), (200, 100), (600, 100), (600, 500), (800, 500)]
enemies = []
towers = []
player_health = 100
money = 150
wave = 1
spawn_timer = 0

# UI elements
font = pygame.font.Font(None, 36)
tower_types = ["basic", "sniper", "machine_gun"]
selected_tower = None

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = pygame.mouse.get_pos()
                if selected_tower and money >= 50:
                    towers.append(Tower(x, y, selected_tower))
                    money -= 50
            elif event.button == 3:  # Right click
                selected_tower = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_tower = "basic"
            elif event.key == pygame.K_2:
                selected_tower = "sniper"
            elif event.key == pygame.K_3:
                selected_tower = "machine_gun"

    # Spawn enemies
    if spawn_timer <= 0:
        enemy_type = random.choice(["normal", "fast", "tank"])
        enemies.append(Enemy(path, enemy_type))
        spawn_timer = 120 - wave * 5  # Decrease spawn time as waves progress
    else:
        spawn_timer -= 1

    # Update game objects
    for enemy in enemies[:]:
        enemy.move()
        if enemy.path_index == len(path) - 1:
            player_health -= 10
            enemies.remove(enemy)
        elif enemy.health <= 0:
            enemies.remove(enemy)
            money += 10

    for tower in towers:
        tower.attack(enemies)

    # Check game over
    if player_health <= 0:
        print("Game Over!")
        running = False

    # Check for next wave
    if len(enemies) == 0:
        wave += 1
        money += 50

    # Draw everything
    screen.fill((200, 200, 200))  # Light gray background
    
    # Draw stylized path
    pygame.draw.lines(screen, (100, 100, 100), False, path, 40)
    pygame.draw.lines(screen, (150, 150, 150), False, path, 30)
    
    for enemy in enemies:
        enemy.draw(screen)
    
    for tower in towers:
        tower.draw(screen)

    # Draw UI
    ui_rect = pygame.Rect(0, 0, WIDTH, 60)
    draw_gradient_rect(screen, (50, 50, 50), ui_rect)
    
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    money_text = font.render(f"Money: ${money}", True, WHITE)
    wave_text = font.render(f"Wave: {wave}", True, WHITE)
    
    screen.blit(health_text, (10, 10))
    screen.blit(money_text, (200, 10))
    screen.blit(wave_text, (400, 10))

    # Draw tower selection UI
    for i, tower_type in enumerate(tower_types):
        color = BLUE if tower_type == "basic" else PURPLE if tower_type == "sniper" else ORANGE
        pygame.draw.rect(screen, color, (600 + i*65, 10, 60, 40))
        if tower_type == selected_tower:
            pygame.draw.rect(screen, WHITE, (600 + i*65, 10, 60, 40), 2)
        key_text = font.render(str(i+1), True, WHITE)
        screen.blit(key_text, (620 + i*65, 20))

    # Draw selected tower at mouse position
    if selected_tower:
        x, y = pygame.mouse.get_pos()
        color = BLUE if selected_tower == "basic" else PURPLE if selected_tower == "sniper" else ORANGE
        pygame.draw.circle(screen, color, (x, y), 20, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()