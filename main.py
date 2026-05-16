import pygame
import math
import random
import json
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional
import os
from pathlib import Path

# Initialize Pygame
pygame.init()

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

# Asset paths
ASSETS_DIR = Path("assets")
IMAGES_DIR = ASSETS_DIR / "images"
GUN_IMAGES_DIR = IMAGES_DIR / "guns"
CAR_IMAGES_DIR = IMAGES_DIR / "cars"
CHARACTER_IMAGES_DIR = IMAGES_DIR / "characters"
POLICE_IMAGES_DIR = IMAGES_DIR / "police"
PICKUP_IMAGES_DIR = IMAGES_DIR / "pickups"


class ImageCache:
    """Cache for loaded images to avoid reloading"""
    _cache = {}
    
    @classmethod
    def get_image(cls, path, width=None, height=None, fallback_color=WHITE):
        """Load or get cached image. Returns surface or colored rectangle fallback"""
        key = f"{path}_{width}_{height}"
        
        if key in cls._cache:
            return cls._cache[key]
        
        try:
            if not os.path.exists(path):
                # Return fallback colored surface
                surface = pygame.Surface((width or 40, height or 40))
                surface.fill(fallback_color)
                cls._cache[key] = surface
                return surface
            
            image = pygame.image.load(path)
            if width and height:
                image = pygame.transform.scale(image, (width, height))
            cls._cache[key] = image
            return image
        except Exception as e:
            # Fallback to colored rectangle if image fails to load
            surface = pygame.Surface((width or 40, height or 40))
            surface.fill(fallback_color)
            cls._cache[key] = surface
            return surface


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
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 12
        self.damage = damage
        self.lifetime = 300
        self.age = 0
        self.owner_type = owner_type
        
        self.width = 5
        self.height = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW if owner_type == "player" else RED)
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.age += 1
        self.rect.center = (self.x, self.y)
    
    def is_alive(self):
        return self.age < self.lifetime


class Pickup(pygame.sprite.Sprite):
    def __init__(self, x, y, pickup_type):
        super().__init__()
        self.x = x
        self.y = y
        self.pickup_type = pickup_type  # "health" or "ammo"
        self.lifetime = 300
        self.age = 0
        self.blink = True
        
        self.width = 15
        self.height = 15
        
        # Try loading image, fallback to colored surface
        if pickup_type == "health":
            image_path = str(PICKUP_IMAGES_DIR / "health.png")
            fallback_color = LIGHT_GREEN
        else:
            image_path = str(PICKUP_IMAGES_DIR / "ammo.png")
            fallback_color = YELLOW
        
        self.image = ImageCache.get_image(image_path, self.width, self.height, fallback_color)
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.age += 1
        self.blink = (self.age // 10) % 2 == 0
        
        if not self.blink:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
    
    def is_alive(self):
        return self.age < self.lifetime


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x, y, vehicle_type="car"):
        super().__init__()
        self.x = x
        self.y = y
        self.vehicle_type = vehicle_type
        
        # Vehicle stats
        if vehicle_type == "car":
            self.width, self.height = 40, 25
            self.max_health = 100
            self.speed = 8.0
            color = RED
            image_name = "car.png"
        elif vehicle_type == "truck":
            self.width, self.height = 50, 30
            self.max_health = 150
            self.speed = 5.6
            color = ORANGE
            image_name = "truck.png"
        else:  # motorcycle
            self.width, self.height = 35, 20
            self.max_health = 100
            self.speed = 10.4
            color = CYAN
            image_name = "motorcycle.png"
        
        image_path = str(CAR_IMAGES_DIR / image_name)
        self.base_image = ImageCache.get_image(image_path, self.width, self.height, color)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0
        self.vy = 0
        self.angle = 0
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
        self.x = x
        self.y = y
        self.width = 18
        self.height = 18
        
        # Load NPC character image
        image_path = str(CHARACTER_IMAGES_DIR / "civilian.png")
        self.image = ImageCache.get_image(image_path, self.width, self.height, GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0
        self.vy = 0
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
        self.x = x
        self.y = y
        self.width = 45
        self.height = 25
        
        # Load police car/officer image
        image_path = str(POLICE_IMAGES_DIR / "police.png")
        self.base_image = ImageCache.get_image(image_path, self.width, self.height, DARK_BLUE)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.health = 50
        self.max_health = 50
        self.angle = 0
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
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        
        # Load player character image
        image_path = str(CHARACTER_IMAGES_DIR / "player.png")
        self.base_image = ImageCache.get_image(image_path, self.width, self.height, BLUE)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.angle = 0
        self.in_vehicle = False
        self.vehicle = None
        self.money = 0
        self.wanted_level = 0
        self.distance_driven = 0
        
        self.weapons = {
            WeaponType.PISTOL: Weapon("Pistol", 10, 100, 100, 5, WeaponType.PISTOL),
            WeaponType.RIFLE: Weapon("Rifle", 25, 60, 60, 8, WeaponType.RIFLE),
            WeaponType.SHOTGUN: Weapon("Shotgun", 40, 30, 30, 10, WeaponType.SHOTGUN),
        }
        self.current_weapon = WeaponType.PISTOL
        self.last_shot = 0
        self.shots_fired = 0
        self.shots_hit = 0
        
        # Load weapon images
        self.weapon_images = {
            WeaponType.PISTOL: ImageCache.get_image(str(GUN_IMAGES_DIR / "pistol.png"), 30, 15, YELLOW),
            WeaponType.RIFLE: ImageCache.get_image(str(GUN_IMAGES_DIR / "rifle.png"), 40, 10, YELLOW),
            WeaponType.SHOTGUN: ImageCache.get_image(str(GUN_IMAGES_DIR / "shotgun.png"), 35, 12, YELLOW),
        }
    
    def handle_input(self, keys, mouse_pos):
        if self.in_vehicle:
            return
        
        self.vx = 0
        self.vy = 0
        
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mini GTA - Complete Edition with 4K Assets")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        self.world_width = 3000
        self.world_height = 2000
        
        self.camera_x = 0
        self.camera_y = 0
        
        self.init_game()
    
    def init_game(self):
        self.player = Player(500, 500)
        self.vehicles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.police = pygame.sprite.Group()
        self.bullets = []
        self.pickups = []
        
        # Spawn vehicles
        for _ in range(8):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            vehicle_type = random.choice(["car", "truck", "motorcycle"])
            self.vehicles.add(Vehicle(x, y, vehicle_type))
        
        # Spawn NPCs
        for _ in range(25):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            self.npcs.add(NPC(x, y))
        
        # Spawn police
        for _ in range(3):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            self.police.add(Police(x, y))
        
        self.missions = [Mission(i) for i in range(3)]
        self.npcs_killed = 0
        self.money_start = 0
        self.total_shots = 0
        self.total_hits = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
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
                    elif event.key == pygame.K_2:
                        self.player.switch_weapon(WeaponType.RIFLE)
                    elif event.key == pygame.K_3:
                        self.player.switch_weapon(WeaponType.SHOTGUN)
                    elif event.key == pygame.K_e:
                        self.try_enter_vehicle()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.PLAYING and event.button == 1:
                    self.player.shoot(pygame.time.get_ticks(), self.bullets)
    
    def try_enter_vehicle(self):
        if self.player.in_vehicle:
            self.player.in_vehicle = False
            self.player.x = self.player.vehicle.x + 50
            self.player.y = self.player.vehicle.y
            self.player.vehicle = None
        else:
            for vehicle in self.vehicles:
                dist = math.sqrt((self.player.x - vehicle.x)**2 + (self.player.y - vehicle.y)**2)
                if dist < 40:
                    self.player.in_vehicle = True
                    self.player.vehicle = vehicle
                    break
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        world_mouse_x = mouse_pos[0] + self.camera_x
        world_mouse_y = mouse_pos[1] + self.camera_y
        
        if self.player.in_vehicle:
            self.player.vehicle.handle_input(keys)
            self.player.vehicle.update(self.world_width, self.world_height)
            old_x, old_y = self.player.x, self.player.y
            self.player.x = self.player.vehicle.x
            self.player.y = self.player.vehicle.y
            self.player.distance_driven += math.sqrt((self.player.x - old_x)**2 + (self.player.y - old_y)**2)
        else:
            self.player.handle_input(keys, (world_mouse_x, world_mouse_y))
        
        self.player.update(self.world_width, self.world_height)
        
        for vehicle in self.vehicles:
            vehicle.update(self.world_width, self.world_height)
        
        for npc in self.npcs:
            npc.update(self.world_width, self.world_height, self.player, self.police)
        
        for police_unit in self.police:
            police_unit.update(self.world_width, self.world_height, self.player)
        
        # Update and handle bullets
        for bullet in self.bullets[:]:
            bullet.update()
            
            if not bullet.is_alive():
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
                            
                            # Spawn pickup
                            if random.random() < 0.3:
                                self.pickups.append(Pickup(npc.x, npc.y, "health"))
                            elif random.random() < 0.2:
                                self.pickups.append(Pickup(npc.x, npc.y, "ammo"))
                        
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
                
                for police_unit in self.police:
                    if police_unit.rect.collidepoint(bullet.x, bullet.y):
                        police_unit.take_damage(bullet.damage)
                        self.player.shots_hit += 1
                        if not police_unit.is_alive():
                            self.player.add_money(200)
                            self.player.increase_wanted(2.0)
                        
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
                
                for vehicle in self.vehicles:
                    if vehicle.rect.collidepoint(bullet.x, bullet.y):
                        vehicle.take_damage(bullet.damage)
                        if not vehicle.is_alive():
                            self.player.increase_wanted(1.0)
                        
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
            else:
                if self.player.rect.collidepoint(bullet.x, bullet.y):
                    self.player.take_damage(bullet.damage)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
            
            if bullet.x < 0 or bullet.x > self.world_width or bullet.y < 0 or bullet.y > self.world_height:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
        
        # Police shooting
        for police_unit in self.police:
            if police_unit.state == "chasing" and police_unit.target:
                dist = math.sqrt((police_unit.x - self.player.x)**2 + (police_unit.y - self.player.y)**2)
                if dist < 300 and random.random() < 0.05:
                    dx = self.player.x - police_unit.x
                    dy = self.player.y - police_unit.y
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist > 0:
                        angle = math.atan2(dy, dx)
                        bx = police_unit.x + math.cos(angle) * 20
                        by = police_unit.y + math.sin(angle) * 20
                        self.bullets.append(Bullet(bx, by, angle, 15, "police"))
        
        # Pickups
        for pickup in self.pickups[:]:
            pickup.update()
            
            if not pickup.is_alive():
                self.pickups.remove(pickup)
                continue
            
            dist = math.sqrt((self.player.x - pickup.x)**2 + (self.player.y - pickup.y)**2)
            if dist < 30:
                if pickup.pickup_type == "health":
                    self.player.heal(25)
                else:
                    self.player.add_ammo(30)
                self.pickups.remove(pickup)
        
        # Respawn vehicles
        dead_vehicles = [v for v in self.vehicles if not v.is_alive()]
        for vehicle in dead_vehicles:
            self.vehicles.remove(vehicle)
        
        if len(self.vehicles) < 8:
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            vehicle_type = random.choice(["car", "truck", "motorcycle"])
            self.vehicles.add(Vehicle(x, y, vehicle_type))
        
        # Respawn NPCs
        dead_npcs = [npc for npc in self.npcs if not npc.is_alive()]
        for npc in dead_npcs:
            self.npcs.remove(npc)
        
        if len(self.npcs) < 25:
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            self.npcs.add(NPC(x, y))
        
        # Respawn police
        dead_police = [p for p in self.police if not p.is_alive()]
        for p in dead_police:
            self.police.remove(p)
        
        if len(self.police) < 3 + int(self.player.wanted_level):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            self.police.add(Police(x, y))
        
        # Update missions
        money_earned = self.player.money - self.money_start
        for mission in self.missions:
            mission.update(self.npcs_killed, money_earned, int(self.player.wanted_level))
        
        # Update wanted level
        if self.player.wanted_level > 0:
            self.player.decrease_wanted(0.01)
        
        # Update camera
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, self.world_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.world_height - SCREEN_HEIGHT))
        
        # Game over check
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
            self.save_high_scores()
    
    def save_high_scores(self):
        scores = {"money": 0, "kills": 0}
        if os.path.exists("highscore.json"):
            try:
                with open("highscore.json", "r") as f:
                    scores = json.load(f)
            except Exception:
                pass
        
        scores["money"] = max(scores["money"], self.player.money)
        scores["kills"] = max(scores["kills"], self.npcs_killed)
        
        with open("highscore.json", "w") as f:
            json.dump(scores, f)
    
    def load_high_scores(self):
        if os.path.exists("highscore.json"):
            try:
                with open("highscore.json", "r") as f:
                    return json.load(f)
            except Exception:
                return {"money": 0, "kills": 0}
        return {"money": 0, "kills": 0}
    
    def draw(self):
        self.screen.fill(DARK_GRAY)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            self.draw_game()
            if self.state == GameState.PAUSED:
                self.draw_pause_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        font_title = pygame.font.Font(None, 80)
        font_subtitle = pygame.font.Font(None, 40)
        font_normal = pygame.font.Font(None, 30)
        
        title = font_title.render("MINI GTA", True, RED)
        subtitle = font_subtitle.render("Open World Action Game - 4K Assets", True, YELLOW)
        start = font_normal.render("Press SPACE to Start", True, WHITE)
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))
        
        # Controls
        font_small = pygame.font.Font(None, 20)
        controls = [
            "WASD/Arrows: Move",
            "1,2,3: Weapons",
            "E: Enter Vehicle",
            "Click: Shoot",
            "ESC: Pause/Menu",
            "",
            "Gameplay:",
            "- Eliminate NPCs for money and wanted level",
            "- Complete missions for bonuses",
            "- Manage police wanted level",
            "- Collect health/ammo pickups",
            "- Drive vehicles to escape danger",
            "- Now with 4K Images for Guns, Cars, Characters & More!"
        ]
        
        y = 300
        for control in controls:
            text = font_small.render(control, True, CYAN if control else BLACK)
            self.screen.blit(text, (50, y))
            y += 25
        
        self.screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, SCREEN_HEIGHT - 100))
    
    def draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_title = pygame.font.Font(None, 60)
        font_normal = pygame.font.Font(None, 40)
        
        pause_text = font_title.render("PAUSED", True, WHITE)
        resume_text = font_normal.render("Press ESC to Resume", True, YELLOW)
        menu_text = font_normal.render("Press ESC Again for Menu", True, YELLOW)
        
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_title = pygame.font.Font(None, 80)
        font_normal = pygame.font.Font(None, 30)
        
        game_over_text = font_title.render("GAME OVER", True, RED)
        
        stats = [
            f"Money Earned: ${self.player.money}",
            f"NPCs Eliminated: {self.npcs_killed}",
            f"Accuracy: {self.player.get_accuracy():.1f}%",
            f"Missions Completed: {sum(1 for m in self.missions if m.completed)}/3",
            f"Wanted Level: {int(self.player.wanted_level)}",
        ]
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 50))
        
        y = 200
        for stat in stats:
            text = font_normal.render(stat, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 50
        
        high_scores = self.load_high_scores()
        hs_text = font_normal.render(f"High Score: ${high_scores['money']}", True, YELLOW)
        self.screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, y + 50))
        
        restart = font_normal.render("Press SPACE to Return to Menu", True, CYAN)
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT - 100))
    
    def draw_game(self):
        # Draw grid
        for x in range(0, self.world_width, 100):
            sx = x - self.camera_x
            if 0 <= sx < SCREEN_WIDTH:
                pygame.draw.line(self.screen, GRAY, (sx, 0), (sx, SCREEN_HEIGHT), 1)
        
        for y in range(0, self.world_height, 100):
            sy = y - self.camera_y
            if 0 <= sy < SCREEN_HEIGHT:
                pygame.draw.line(self.screen, GRAY, (0, sy), (SCREEN_WIDTH, sy), 1)
        
        # Draw vehicles
        for vehicle in self.vehicles:
            sx = vehicle.x - self.camera_x
            sy = vehicle.y - self.camera_y
            if -50 < sx < SCREEN_WIDTH + 50 and -50 < sy < SCREEN_HEIGHT + 50:
                self.screen.blit(vehicle.image, (sx - vehicle.rect.width // 2, sy - vehicle.rect.height // 2))
                
                if vehicle.health < vehicle.max_health:
                    bar_width = 40
                    bar_height = 4
                    health_ratio = vehicle.health / vehicle.max_health
                    pygame.draw.rect(self.screen, RED, (sx - bar_width // 2, sy - 25, bar_width, bar_height))
                    pygame.draw.rect(self.screen, GREEN, (sx - bar_width // 2, sy - 25, bar_width * health_ratio, bar_height))
        
        # Draw police
        for police_unit in self.police:
            sx = police_unit.x - self.camera_x
            sy = police_unit.y - self.camera_y
            if -50 < sx < SCREEN_WIDTH + 50 and -50 < sy < SCREEN_HEIGHT + 50:
                self.screen.blit(police_unit.image, (sx - police_unit.rect.width // 2, sy - police_unit.rect.height // 2))
                
                bar_width = 40
                bar_height = 4
                health_ratio = police_unit.health / police_unit.max_health
                pygame.draw.rect(self.screen, RED, (sx - bar_width // 2, sy - 30, bar_width, bar_height))
                pygame.draw.rect(self.screen, GREEN, (sx - bar_width // 2, sy - 30, bar_width * health_ratio, bar_height))
        
        # Draw NPCs
        for npc in self.npcs:
            sx = npc.x - self.camera_x
            sy = npc.y - self.camera_y
            if -50 < sx < SCREEN_WIDTH + 50 and -50 < sy < SCREEN_HEIGHT + 50:
                self.screen.blit(npc.image, (sx - npc.width // 2, sy - npc.height // 2))
                
                if npc.health < npc.max_health:
                    bar_width = 20
                    bar_height = 3
                    health_ratio = npc.health / npc.max_health
                    pygame.draw.rect(self.screen, RED, (sx - bar_width // 2, sy - 15, bar_width, bar_height))
                    pygame.draw.rect(self.screen, GREEN, (sx - bar_width // 2, sy - 15, bar_width * health_ratio, bar_height))
        
        # Draw pickups
        for pickup in self.pickups:
            sx = pickup.x - self.camera_x
            sy = pickup.y - self.camera_y
            if -20 < sx < SCREEN_WIDTH + 20 and -20 < sy < SCREEN_HEIGHT + 20:
                self.screen.blit(pickup.image, (sx - pickup.width // 2, sy - pickup.height // 2))
        
        # Draw player
        sx = self.player.x - self.camera_x
        sy = self.player.y - self.camera_y
        self.screen.blit(self.player.image, (sx - self.player.rect.width // 2, sy - self.player.rect.height // 2))
        
        # Draw bullets
        for bullet in self.bullets:
            sx = bullet.x - self.camera_x
            sy = bullet.y - self.camera_y
            if -10 < sx < SCREEN_WIDTH + 10 and -10 < sy < SCREEN_HEIGHT + 10:
                pygame.draw.circle(self.screen, bullet.image.get_at((0, 0)), (int(sx), int(sy)), 3)
        
        # Draw HUD
        self.draw_hud()
    
    def draw_hud(self):
        font_small = pygame.font.Font(None, 24)
        font_large = pygame.font.Font(None, 32)
        
        # Left side stats
        health_text = font_small.render(f"Health: {int(self.player.health)}/{int(self.player.max_health)}", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        weapon = self.player.weapons[self.player.current_weapon]
        ammo_text = font_small.render(f"{weapon.name}: {weapon.ammo}/{weapon.max_ammo}", True, YELLOW)
        self.screen.blit(ammo_text, (10, 35))
        
        money_text = font_small.render(f"Money: ${self.player.money}", True, YELLOW)
        self.screen.blit(money_text, (10, 60))
        
        wanted_text = font_small.render(f"Wanted: {'*' * int(self.player.wanted_level)}", True, RED)
        self.screen.blit(wanted_text, (10, 85))
        
        npcs_text = font_small.render(f"NPCs: {len(self.npcs)} | Police: {len(self.police)}", True, GREEN)
        self.screen.blit(npcs_text, (10, 110))
        
        accuracy_text = font_small.render(f"Accuracy: {self.player.get_accuracy():.1f}%", True, CYAN)
        self.screen.blit(accuracy_text, (10, 135))
        
        # Right side missions
        missions_title = font_large.render("MISSIONS", True, YELLOW)
        self.screen.blit(missions_title, (SCREEN_WIDTH - 300, 10))
        
        y = 50
        for i, mission in enumerate(self.missions):
            status = "✓" if mission.completed else "○"
            color = GREEN if mission.completed else WHITE
            mission_text = font_small.render(f"{status} {mission.description}", True, color)
            self.screen.blit(mission_text, (SCREEN_WIDTH - 300, y))
            
            progress_text = font_small.render(f"   Progress: {mission.get_progress_text()}", True, color)
            self.screen.blit(progress_text, (SCREEN_WIDTH - 300, y + 22))
            
            y += 55
        
        # Instructions
        font_tiny = pygame.font.Font(None, 18)
        instructions = "WASD:Move | 1,2,3:Weapon | E:Vehicle | Click:Shoot | ESC:Menu"
        instr_text = font_tiny.render(instructions, True, GRAY)
        self.screen.blit(instr_text, (10, SCREEN_HEIGHT - 25))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
