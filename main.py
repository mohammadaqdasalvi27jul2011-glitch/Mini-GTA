import pygame
import math
import random
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
import os
from pathlib import Path
import sys

# Initialize Pygame
try:
    pygame.init()
    print("✅ Pygame initialized")
except Exception as e:
    print(f"❌ Failed to initialize Pygame: {e}")
    sys.exit(1)

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 0, 139)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
LIGHT_GREEN = (144, 238, 144)
LIGHT_GRAY = (192, 192, 192)
DARK_GREEN = (34, 139, 34)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
LIGHT_BLUE = (173, 216, 230)


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


class WeaponType(Enum):
    PISTOL = 1
    RIFLE = 2
    SHOTGUN = 3


@dataclass
class Weapon:
    name: str
    damage: int
    ammo: int
    max_ammo: int
    fire_rate: int
    type: WeaponType


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage, owner_type="player"):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.angle = angle
        self.speed = 12
        self.damage = damage
        self.lifetime = 300
        self.age = 0
        self.owner_type = owner_type
        
        self.width = 8
        self.height = 8
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if owner_type == "player":
            pygame.draw.circle(self.image, YELLOW, (4, 4), 4)
            pygame.draw.circle(self.image, WHITE, (4, 4), 2)
        else:
            pygame.draw.circle(self.image, RED, (4, 4), 4)
            pygame.draw.circle(self.image, ORANGE, (4, 4), 2)
        
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.age += 1
        self.rect.center = (int(self.x), int(self.y))
    
    def is_alive(self):
        return self.age < self.lifetime


class Pickup(pygame.sprite.Sprite):
    def __init__(self, x, y, pickup_type):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.pickup_type = pickup_type
        self.lifetime = 300
        self.age = 0
        self.blink = True
        
        self.width = 24
        self.height = 24
        
        self.base_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if pickup_type == "health":
            pygame.draw.circle(self.base_image, LIGHT_GREEN, (12, 12), 12)
            pygame.draw.circle(self.base_image, RED, (12, 12), 10)
            pygame.draw.line(self.base_image, WHITE, (12, 6), (12, 18), 2)
            pygame.draw.line(self.base_image, WHITE, (6, 12), (18, 12), 2)
        else:
            pygame.draw.circle(self.base_image, YELLOW, (12, 12), 12)
            pygame.draw.circle(self.base_image, ORANGE, (12, 12), 9)
            pygame.draw.line(self.base_image, RED, (8, 12), (16, 12), 2)
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.age += 1
        self.blink = (self.age // 10) % 2 == 0
        
        if self.blink:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(150)
    
    def is_alive(self):
        return self.age < self.lifetime


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x, y, vehicle_type="car"):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.vehicle_type = vehicle_type
        
        if vehicle_type == "car":
            self.width, self.height = 50, 30
            self.max_health = 100
            self.speed = 8.0
            color = RED
        elif vehicle_type == "truck":
            self.width, self.height = 70, 40
            self.max_health = 150
            self.speed = 5.6
            color = ORANGE
        else:
            self.width, self.height = 40, 25
            self.max_health = 100
            self.speed = 10.4
            color = CYAN
        
        self.base_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.base_image, color, (0, 0, self.width, self.height), border_radius=8)
        pygame.draw.polygon(self.base_image, DARK_GRAY, [(self.width//4, self.height//3), 
                                                          (3*self.width//4, self.height//3),
                                                          (3*self.width//4, 2*self.height//3),
                                                          (self.width//4, 2*self.height//3)])
        pygame.draw.circle(self.base_image, BLACK, (self.width//3, self.height), 4)
        pygame.draw.circle(self.base_image, BLACK, (2*self.width//3, self.height), 4)
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0.0
        self.vy = 0.0
        self.angle = 0.0
        self.health = self.max_health
    
    def handle_input(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vx = math.cos(self.angle) * self.speed
            self.vy = math.sin(self.angle) * self.speed
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle -= 0.1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += 0.1
    
    def update(self, world_width, world_height):
        self.x += self.vx
        self.y += self.vy
        
        self.x = max(0, min(self.x, world_width))
        self.y = max(0, min(self.y, world_height))
        
        self.vx *= 0.95
        self.vy *= 0.95
        
        rotated = pygame.transform.rotate(self.base_image, -math.degrees(self.angle))
        self.rect = rotated.get_rect(center=(self.x, self.y))
        self.image = rotated
    
    def take_damage(self, damage):
        self.health -= damage
    
    def is_alive(self):
        return self.health > 0


class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.width = 24
        self.height = 24
        
        self.base_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(self.base_image, PINK, (self.width//2, self.height//4), 6)
        pygame.draw.rect(self.base_image, GREEN, (self.width//3, self.height//3, self.width//3, self.height//2))
        pygame.draw.line(self.base_image, PINK, (self.width//3, self.height//2), (2, self.height//2), 3)
        pygame.draw.line(self.base_image, PINK, (2*self.width//3, self.height//2), (self.width-2, self.height//2), 3)
        pygame.draw.line(self.base_image, BROWN, (5*self.width//12, 5*self.height//6), (5*self.width//12, self.height), 3)
        pygame.draw.line(self.base_image, BROWN, (7*self.width//12, 5*self.height//6), (7*self.width//12, self.height), 3)
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 2
        self.health = 30
        self.max_health = 30
        self.state = "walking"
        self.state_timer = random.randint(60, 300)
        self.angle = random.uniform(0, 2 * math.pi)
        self.flee_from = None
    
    def update(self, world_width, world_height, player, police_vehicles):
        dist_to_player = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        
        if dist_to_player < 150 and player.wanted_level > 0:
            self.state = "fleeing"
            self.flee_from = player
            self.state_timer = 0
        elif self.state == "fleeing" and dist_to_player > 200:
            self.state = "walking"
            self.state_timer = random.randint(60, 300)
        
        self.state_timer -= 1
        if self.state_timer <= 0:
            if self.state == "walking":
                self.state = "idle"
                self.state_timer = random.randint(30, 150)
                self.vx = 0
                self.vy = 0
            else:
                self.state = "walking"
                self.state_timer = random.randint(60, 300)
                self.angle = random.uniform(0, 2 * math.pi)
        
        if self.state == "fleeing" and self.flee_from:
            dx = self.x - self.flee_from.x
            dy = self.y - self.flee_from.y
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                self.vx = (dx / dist) * self.speed * 1.5
                self.vy = (dy / dist) * self.speed * 1.5
        elif self.state == "walking":
            self.vx = math.cos(self.angle) * self.speed
            self.vy = math.sin(self.angle) * self.speed
        
        self.x += self.vx
        self.y += self.vy
        
        self.x = max(0, min(self.x, world_width))
        self.y = max(0, min(self.y, world_height))
        
        self.rect.center = (self.x, self.y)
    
    def take_damage(self, damage):
        self.health -= damage
    
    def is_alive(self):
        return self.health > 0


class Police(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.width = 50
        self.height = 30
        
        self.base_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.base_image, DARK_BLUE, (0, 0, self.width, self.height), border_radius=8)
        pygame.draw.rect(self.base_image, RED, (self.width//4, 5, self.width//2, 10), border_radius=4)
        pygame.draw.circle(self.base_image, CYAN, (self.width//3, self.height), 5)
        pygame.draw.circle(self.base_image, CYAN, (2*self.width//3, self.height), 5)
        pygame.draw.line(self.base_image, WHITE, (10, 12), (self.width-10, 12), 2)
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 5
        self.health = 50
        self.max_health = 50
        self.angle = 0.0
        self.target = None
        self.shoot_timer = 0
        self.state = "patrolling"
        self.patrol_timer = 0
    
    def update(self, world_width, world_height, player):
        if player.wanted_level > 0:
            self.state = "chasing"
            self.target = player
            dist = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
            
            if dist > 500:
                self.state = "patrolling"
                self.target = None
            else:
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist > 0:
                    self.vx = (dx / dist) * self.speed
                    self.vy = (dy / dist) * self.speed
                    self.angle = math.atan2(dy, dx)
        else:
            self.state = "patrolling"
            self.patrol_timer += 1
            if self.patrol_timer > 300:
                angle = random.uniform(0, 2 * math.pi)
                self.vx = math.cos(angle) * self.speed * 0.5
                self.vy = math.sin(angle) * self.speed * 0.5
                self.patrol_timer = 0
        
        self.x += self.vx
        self.y += self.vy
        
        self.x = max(0, min(self.x, world_width))
        self.y = max(0, min(self.y, world_height))
        
        self.vx *= 0.95
        self.vy *= 0.95
        
        rotated = pygame.transform.rotate(self.base_image, -math.degrees(self.angle))
        self.rect = rotated.get_rect(center=(self.x, self.y))
        self.image = rotated
    
    def take_damage(self, damage):
        self.health -= damage
    
    def is_alive(self):
        return self.health > 0


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.width = 28
        self.height = 28
        
        self.base_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(self.base_image, YELLOW, (self.width//2, self.height//4), 7)
        pygame.draw.rect(self.base_image, BLUE, (self.width//3-2, self.height//3, self.width//3+4, self.height//2), border_radius=4)
        pygame.draw.line(self.base_image, YELLOW, (self.width//3, self.height//2), (2, self.height//2+2), 4)
        pygame.draw.line(self.base_image, YELLOW, (2*self.width//3, self.height//2), (self.width-2, self.height//2+2), 4)
        pygame.draw.line(self.base_image, BROWN, (5*self.width//12, 5*self.height//6), (5*self.width//12, self.height), 4)
        pygame.draw.line(self.base_image, BROWN, (7*self.width//12, 5*self.height//6), (7*self.width//12, self.height), 4)
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.angle = 0.0
        self.in_vehicle = False
        self.vehicle = None
        self.money = 0
        self.wanted_level = 0.0
        self.distance_driven = 0.0
        
        self.weapons = {
            WeaponType.PISTOL: Weapon("Pistol", 10, 100, 100, 5, WeaponType.PISTOL),
            WeaponType.RIFLE: Weapon("Rifle", 25, 60, 60, 8, WeaponType.RIFLE),
            WeaponType.SHOTGUN: Weapon("Shotgun", 40, 30, 30, 10, WeaponType.SHOTGUN),
        }
        self.current_weapon = WeaponType.PISTOL
        self.last_shot = 0
        self.shots_fired = 0
        self.shots_hit = 0
    
    def handle_input(self, keys, mouse_pos):
        if self.in_vehicle:
            return
        
        self.vx = 0.0
        self.vy = 0.0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vy = self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.speed
        
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.atan2(dy, dx)
    
    def update(self, world_width, world_height):
        if not self.in_vehicle:
            self.x += self.vx
            self.y += self.vy
            self.x = max(0, min(self.x, world_width))
            self.y = max(0, min(self.y, world_height))
        
        self.rect.center = (self.x, self.y)
        rotated = pygame.transform.rotate(self.base_image, -math.degrees(self.angle))
        self.image = rotated
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def shoot(self, current_time, bullets):
        weapon = self.weapons[self.current_weapon]
        
        if weapon.ammo > 0 and current_time - self.last_shot > weapon.fire_rate:
            bullet_count = 1 if self.current_weapon != WeaponType.SHOTGUN else 3
            
            for i in range(bullet_count):
                if self.current_weapon == WeaponType.SHOTGUN:
                    spread = 0.3
                    angle = self.angle + random.uniform(-spread, spread)
                else:
                    angle = self.angle
                
                bx = self.x + math.cos(angle) * 15
                by = self.y + math.sin(angle) * 15
                bullets.append(Bullet(bx, by, angle, weapon.damage, "player"))
            
            weapon.ammo -= 1
            self.shots_fired += 1
            self.last_shot = current_time
    
    def switch_weapon(self, weapon_type):
        if weapon_type in self.weapons:
            self.current_weapon = weapon_type
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
    
    def add_ammo(self, amount):
        self.weapons[self.current_weapon].ammo = min(
            self.weapons[self.current_weapon].ammo + amount,
            self.weapons[self.current_weapon].max_ammo
        )
    
    def add_money(self, amount):
        self.money += amount
    
    def increase_wanted(self, amount):
        self.wanted_level = min(self.wanted_level + amount, 5)
    
    def decrease_wanted(self, amount):
        self.wanted_level = max(self.wanted_level - amount, 0)
    
    def get_accuracy(self):
        if self.shots_fired == 0:
            return 100
        return (self.shots_hit / self.shots_fired) * 100


class Mission:
    def __init__(self, mission_id):
        self.mission_id = mission_id
        self.mission_type = random.choice(["kill", "money", "wanted"])
        
        if self.mission_type == "kill":
            self.target = random.randint(5, 15)
            self.description = f"Kill {self.target} NPCs"
            self.reward = self.target * 100
        elif self.mission_type == "money":
            self.target = random.randint(500, 2000)
            self.description = f"Earn ${self.target}"
            self.reward = self.target // 2
        else:
            self.target = 5
            self.description = "Reach 5-Star Wanted Level"
            self.reward = 1000
        
        self.progress = 0
        self.completed = False
    
    def update(self, npcs_killed, money_earned, wanted_level):
        if self.completed:
            return
        
        if self.mission_type == "kill":
            self.progress = npcs_killed
        elif self.mission_type == "money":
            self.progress = money_earned
        else:
            self.progress = wanted_level
        
        if self.progress >= self.target:
            self.completed = True
    
    def get_progress_text(self):
        if self.mission_type == "wanted":
            return f"{int(self.progress)}/5"
        return f"{int(self.progress)}/{self.target}"


class Game:
    def __init__(self):
        print("🎮 Initializing Mini GTA...")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mini GTA - 4K Enhanced Edition | Play Mode")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        self.world_width = 3000
        self.world_height = 2000
        
        self.camera_x = 0.0
        self.camera_y = 0.0
        
        print("🎨 Creating background...")
        self.background = self.create_background()
        
        print("✅ Mini GTA initialized!")
    
    def create_background(self):
        """Create background"""
        background = pygame.Surface((self.world_width, self.world_height))
        
        # Gradient
        for y in range(0, self.world_height, 50):
            color_factor = int((y / self.world_height) * 50)
            color = (100 + color_factor, 150 + color_factor, 100 + color_factor)
            pygame.draw.line(background, color, (0, y), (self.world_width, y), 50)
        
        # Roads
        pygame.draw.rect(background, (100, 100, 100), (0, self.world_height//2 - 40, self.world_width, 80))
        pygame.draw.rect(background, (100, 100, 100), (self.world_width//2 - 40, 0, 80, self.world_height))
        
        # Road markings
        for i in range(0, self.world_width, 100):
            pygame.draw.line(background, YELLOW, (i, self.world_height//2), (i + 50, self.world_height//2), 2)
        
        for i in range(0, self.world_height, 100):
            pygame.draw.line(background, YELLOW, (self.world_width//2, i), (self.world_width//2, i + 50), 2)
        
        # Buildings
        for i in range(0, self.world_width, 400):
            for j in range(0, self.world_height, 400):
                if abs(i - self.world_width//2) > 100 or abs(j - self.world_height//2) > 100:
                    color = random.choice([LIGHT_GRAY, LIGHT_BLUE, PINK])
                    pygame.draw.rect(background, color, (i, j, 300, 300), border_radius=10)
                    pygame.draw.rect(background, GRAY, (i, j, 300, 300), 3, border_radius=10)
        
        # Trees
        for _ in range(50):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            if abs(x - self.world_width//2) > 150 or abs(y - self.world_height//2) > 150:
                pygame.draw.circle(background, DARK_GREEN, (x, y), 15)
                pygame.draw.rect(background, BROWN, (x-3, y, 6, 20))
        
        return background
    
    def init_game(self):
        print("🎮 Starting new game...")
        self.player = Player(500, 500)
        self.vehicles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.police = pygame.sprite.Group()
        self.bullets = []
        self.pickups = []
        
        # Spawn fewer entities for better performance
        print("🚗 Spawning vehicles...")
        for _ in range(5):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            vehicle_type = random.choice(["car", "truck", "motorcycle"])
            self.vehicles.add(Vehicle(x, y, vehicle_type))
        
        print("👥 Spawning NPCs...")
        for _ in range(15):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            self.npcs.add(NPC(x, y))
        
        print("🚓 Spawning police...")
        for _ in range(2):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            self.police.add(Police(x, y))
        
        self.missions = [Mission(i) for i in range(3)]
        self.npcs_killed = 0
        self.money_start = 0
        
        print(f"✅ Game ready! Vehicles: {len(self.vehicles)}, NPCs: {len(self.npcs)}, Police: {len(self.police)}")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("📋 Quit requested")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        print("⏸️  Paused")
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        print("▶️  Resumed")
                    else:
                        self.state = GameState.MENU
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                        self.init_game()
                    elif self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_1:
                        self.player.switch_weapon(WeaponType.PISTOL)
                        print("🔫 Pistol")
                    elif event.key == pygame.K_2:
                        self.player.switch_weapon(WeaponType.RIFLE)
                        print("🔫 Rifle")
                    elif event.key == pygame.K_3:
                        self.player.switch_weapon(WeaponType.SHOTGUN)
                        print("🔫 Shotgun")
                    elif event.key == pygame.K_e:
                        if self.player.in_vehicle:
                            self.player.in_vehicle = False
                            print("👤 Exited vehicle")
                        else:
                            for vehicle in self.vehicles:
                                dist = math.sqrt((self.player.x - vehicle.x)**2 + (self.player.y - vehicle.y)**2)
                                if dist < 40:
                                    self.player.in_vehicle = True
                                    self.player.vehicle = vehicle
                                    print("🚗 Entered vehicle")
                                    break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.PLAYING and event.button == 1:
                    self.player.shoot(pygame.time.get_ticks(), self.bullets)
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        world_mouse_x = mouse_pos[0] + self.camera_x
        world_mouse_y = mouse_pos[1] + self.camera_y
        
        if self.player.in_vehicle and self.player.vehicle:
            self.player.vehicle.handle_input(keys)
            self.player.vehicle.update(self.world_width, self.world_height)
            self.player.x = self.player.vehicle.x
            self.player.y = self.player.vehicle.y
        else:
            self.player.handle_input(keys, (world_mouse_x, world_mouse_y))
        
        self.player.update(self.world_width, self.world_height)
        
        # Update vehicles
        for vehicle in self.vehicles:
            vehicle.update(self.world_width, self.world_height)
        
        # Update NPCs
        for npc in self.npcs:
            npc.update(self.world_width, self.world_height, self.player, self.police)
        
        # Update police
        for police_unit in self.police:
            police_unit.update(self.world_width, self.world_height, self.player)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            
            if not bullet.is_alive():
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                continue
            
            if bullet.owner_type == "player":
                for npc in self.npcs:
                    if npc.rect.collidepoint(bullet.x, bullet.y):
                        npc.take_damage(bullet.damage)
                        self.player.shots_hit += 1
                        if not npc.is_alive():
                            self.player.add_money(50)
                            self.player.increase_wanted(0.5)
                            self.npcs_killed += 1
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
        
        # Update pickups
        for pickup in self.pickups[:]:
            pickup.update()
            
            if not pickup.is_alive():
                if pickup in self.pickups:
                    self.pickups.remove(pickup)
                continue
            
            dist = math.sqrt((self.player.x - pickup.x)**2 + (self.player.y - pickup.y)**2)
            if dist < 30:
                if pickup.pickup_type == "health":
                    self.player.heal(25)
                    print("💚 Health!")
                else:
                    self.player.add_ammo(30)
                    print("📦 Ammo!")
                if pickup in self.pickups:
                    self.pickups.remove(pickup)
        
        # Update camera
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, self.world_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.world_height - SCREEN_HEIGHT))
        
        # Game over check
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
            print("💀 Game Over!")
    
    def draw(self):
        self.screen.fill(DARK_GRAY)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        for y in range(SCREEN_HEIGHT):
            color_factor = int((y / SCREEN_HEIGHT) * 100)
            color = (50 + color_factor, 100 + color_factor, 200 + color_factor)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        font_title = pygame.font.Font(None, 80)
        font_subtitle = pygame.font.Font(None, 40)
        font_normal = pygame.font.Font(None, 30)
        font_small = pygame.font.Font(None, 20)
        
        title = font_title.render("MINI GTA", True, RED)
        subtitle = font_subtitle.render("4K Edition", True, YELLOW)
        start = font_normal.render("Press SPACE to Start", True, WHITE)
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))
        
        instructions = [
            "WASD: Move | Click: Shoot",
            "1,2,3: Weapons | E: Vehicle",
            "ESC: Menu",
        ]
        
        y = 350
        for instruction in instructions:
            text = font_small.render(instruction, True, CYAN)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 40
        
        self.screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, SCREEN_HEIGHT - 100))
    
    def draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 60)
        text = font.render("PAUSED - Press ESC", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_title = pygame.font.Font(None, 80)
        font_normal = pygame.font.Font(None, 30)
        
        text = font_title.render("GAME OVER", True, RED)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
        
        stats = [
            f"Money: ${self.player.money}",
            f"Kills: {self.npcs_killed}",
            f"Accuracy: {self.player.get_accuracy():.1f}%",
        ]
        
        y = 250
        for stat in stats:
            text = font_normal.render(stat, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 50
        
        restart = font_normal.render("Press SPACE to Return to Menu", True, CYAN)
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT - 100))
    
    def draw_game(self):
        # Draw background
        self.screen.blit(self.background, (-int(self.camera_x), -int(self.camera_y)))
        
        # Draw vehicles
        for vehicle in self.vehicles:
            sx = vehicle.x - self.camera_x
            sy = vehicle.y - self.camera_y
            if -100 < sx < SCREEN_WIDTH + 100 and -100 < sy < SCREEN_HEIGHT + 100:
                self.screen.blit(vehicle.image, (int(sx - vehicle.rect.width // 2), int(sy - vehicle.rect.height // 2)))
        
        # Draw NPCs
        for npc in self.npcs:
            sx = npc.x - self.camera_x
            sy = npc.y - self.camera_y
            if -50 < sx < SCREEN_WIDTH + 50 and -50 < sy < SCREEN_HEIGHT + 50:
                self.screen.blit(npc.image, (int(sx - npc.width // 2), int(sy - npc.height // 2)))
        
        # Draw police
        for police_unit in self.police:
            sx = police_unit.x - self.camera_x
            sy = police_unit.y - self.camera_y
            if -100 < sx < SCREEN_WIDTH + 100 and -100 < sy < SCREEN_HEIGHT + 100:
                self.screen.blit(police_unit.image, (int(sx - police_unit.rect.width // 2), int(sy - police_unit.rect.height // 2)))
        
        # Draw pickups
        for pickup in self.pickups:
            sx = pickup.x - self.camera_x
            sy = pickup.y - self.camera_y
            if -30 < sx < SCREEN_WIDTH + 30 and -30 < sy < SCREEN_HEIGHT + 30:
                self.screen.blit(pickup.image, (int(sx - pickup.width // 2), int(sy - pickup.height // 2)))
        
        # Draw player
        sx = self.player.x - self.camera_x
        sy = self.player.y - self.camera_y
        self.screen.blit(self.player.image, (int(sx - self.player.rect.width // 2), int(sy - self.player.rect.height // 2)))
        pygame.draw.circle(self.screen, CYAN, (int(sx), int(sy)), 35, 2)
        
        # Draw bullets
        for bullet in self.bullets:
            sx = bullet.x - self.camera_x
            sy = bullet.y - self.camera_y
            if -20 < sx < SCREEN_WIDTH + 20 and -20 < sy < SCREEN_HEIGHT + 20:
                pygame.draw.circle(self.screen, YELLOW if bullet.owner_type == "player" else RED, (int(sx), int(sy)), 5)
        
        # Draw HUD
        font_small = pygame.font.Font(None, 24)
        health_text = font_small.render(f"Health: {int(self.player.health)}/{int(self.player.max_health)}", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        weapon = self.player.weapons[self.player.current_weapon]
        ammo_text = font_small.render(f"{weapon.name}: {weapon.ammo}/{weapon.max_ammo}", True, YELLOW)
        self.screen.blit(ammo_text, (10, 40))
        
        money_text = font_small.render(f"Money: ${self.player.money}", True, YELLOW)
        self.screen.blit(money_text, (10, 70))
        
        wanted_text = font_small.render(f"Wanted: {'★' * int(self.player.wanted_level)}", True, RED)
        self.screen.blit(wanted_text, (10, 100))
    
    def run(self):
        print("\n🎮 Starting game loop...")
        frame_count = 0
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            frame_count += 1
            
            if frame_count % 300 == 0:
                print(f"✅ Running... FPS: {self.clock.get_fps():.1f}")
        
        print("✅ Game closed!")
        pygame.quit()


if __name__ == "__main__":
    print("=" * 60)
    print("🎮 MINI GTA - 4K Edition")
    print("=" * 60)
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
