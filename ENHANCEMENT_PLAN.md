# Mini-GTA Enhancement Plan: Unlimited Ammo & High-Resolution Assets

## 🎮 Project Overview
Enhancement to Mini-GTA with unlimited ammo system, multiple weapon types, and professional 4K/8K game assets.

---

## Phase 1: Unlimited Ammo System

### 1.1 Ammo Management Module
**File: `game/systems/ammo_system.py`**

```python
class AmmoSystem:
    """Manages unlimited ammo and weapon types"""
    
    def __init__(self):
        self.unlimited_ammo = True
        self.weapon_types = {
            'pistol': {
                'damage': 25,
                'fire_rate': 0.15,
                'magazine_size': float('inf'),
                'ammo_per_shot': 1
            },
            'rifle': {
                'damage': 50,
                'fire_rate': 0.10,
                'magazine_size': float('inf'),
                'ammo_per_shot': 1
            },
            'shotgun': {
                'damage': 75,
                'fire_rate': 0.50,
                'magazine_size': float('inf'),
                'ammo_per_shot': 2
            },
            'machine_gun': {
                'damage': 30,
                'fire_rate': 0.05,
                'magazine_size': float('inf'),
                'ammo_per_shot': 1
            },
            'sniper': {
                'damage': 100,
                'fire_rate': 1.0,
                'magazine_size': float('inf'),
                'ammo_per_shot': 1
            },
            'grenade_launcher': {
                'damage': 150,
                'fire_rate': 1.5,
                'magazine_size': float('inf'),
                'ammo_per_shot': 1
            }
        }
        self.current_weapon = 'pistol'
        self.ammo_count = float('inf')
    
    def shoot(self):
        """Fire weapon with unlimited ammo"""
        if self.unlimited_ammo:
            return True
        return self.ammo_count > 0
    
    def switch_weapon(self, weapon_name):
        """Switch between available weapons"""
        if weapon_name in self.weapon_types:
            self.current_weapon = weapon_name
            self.ammo_count = float('inf')
            return True
        return False
    
    def get_weapon_stats(self, weapon_name):
        """Get stats for any weapon"""
        return self.weapon_types.get(weapon_name, {})
```

### 1.2 Weapon Selection UI
**File: `game/ui/weapon_selection.py`**

```python
class WeaponSelectionUI:
    """Displays available weapons and ammunition"""
    
    WEAPONS_ORDER = ['pistol', 'rifle', 'shotgun', 'machine_gun', 'sniper', 'grenade_launcher']
    
    def display_weapons(self, screen, ammo_system):
        """Render weapon selection interface"""
        weapons_list = []
        for i, weapon in enumerate(self.WEAPONS_ORDER):
            is_selected = weapon == ammo_system.current_weapon
            weapons_list.append({
                'name': weapon,
                'stats': ammo_system.get_weapon_stats(weapon),
                'selected': is_selected,
                'position': (50 + i * 150, 20)
            })
        return weapons_list
    
    def get_ammo_display(self, ammo_system):
        """Get ammo display for HUD"""
        if ammo_system.unlimited_ammo:
            return "∞ AMMO"
        return f"{ammo_system.ammo_count}"
```

---

## Phase 2: High-Resolution Game Assets

### 2.1 Asset Directory Structure
```
assets/
├── characters/
│   ├── protagonist/
│   │   ├── idle_8k.png (8K - 7680x4320px)
│   │   ├── running_8k.png
│   │   ├── jumping_8k.png
│   │   ├── shooting_8k.png
│   │   └── idle_4k.png (4K - 3840x2160px) [fallback]
│   ├── police/
│   │   ├── npc_8k.png
│   │   ├── uniform_variants_8k.png
│   │   └── idle_4k.png
│   ├── civilians/
│   │   ├── pedestrian_set_8k.png
│   │   ├── business_character_8k.png
│   │   └── variants_4k.png
│   └── enemies/
│       ├── gang_member_8k.png
│       ├── rival_gang_8k.png
│       └── boss_characters_8k.png
│
├── vehicles/
│   ├── cars/
│   │   ├── sedan_8k.png (8K detail)
│   │   ├── sports_car_8k.png
│   │   ├── suv_8k.png
│   │   ├── sedan_4k.png (4K fallback)
│   │   └── sedan_360_views/ (multiple angles)
│   ├── motorcycles/
│   │   ├── street_bike_8k.png
│   │   ├── cruiser_8k.png
│   │   └── motorcycle_4k.png
│   ├── trucks/
│   │   ├── pickup_truck_8k.png
│   │   └── truck_4k.png
│   └── special/
│       ├── police_cruiser_8k.png
│       ├── ambulance_8k.png
│       └── fire_truck_8k.png
│
├── weapons/
│   ├── pistol_8k.png
│   ├── rifle_8k.png
│   ├── shotgun_8k.png
│   ├── machine_gun_8k.png
│   ├── sniper_rifle_8k.png
│   └── grenade_launcher_8k.png
│
├── environments/
│   ├── urban_8k/
│   │   ├── street_01_8k.png
│   │   ├── building_01_8k.png
│   │   └── alley_01_8k.png
│   └── district_maps_4k/
│       ├── downtown_4k.png
│       ├── residential_4k.png
│       └── industrial_4k.png
│
└── ui/
    ├── hud_elements_4k.png
    ├── menu_background_8k.png
    └── icons_4k.png
```

### 2.2 Asset Loading System
**File: `game/systems/asset_manager.py`**

```python
import pygame
from pathlib import Path

class AssetManager:
    """Manages high-resolution game assets with fallback system"""
    
    def __init__(self):
        self.assets = {}
        self.resolution_preference = 'auto'  # auto, 8k, 4k
        self.asset_base_path = Path('assets')
        self.loaded_assets = {}
    
    def get_optimal_resolution(self):
        """Determine optimal resolution based on display"""
        import platform
        if self.resolution_preference == 'auto':
            # Default to 4K, with 8K available for high-end systems
            return '4k'
        return self.resolution_preference
    
    def load_character_sprite(self, character_type, action='idle'):
        """Load character sprite with automatic resolution selection"""
        resolution = self.get_optimal_resolution()
        
        # Try 8K first, fall back to 4K
        paths_to_try = [
            self.asset_base_path / f'characters/{character_type}/{action}_8k.png',
            self.asset_base_path / f'characters/{character_type}/{action}_4k.png',
            self.asset_base_path / f'characters/{character_type}/{action}.png'
        ]
        
        for path in paths_to_try:
            if path.exists():
                try:
                    surface = pygame.image.load(str(path))
                    self.loaded_assets[str(path)] = surface
                    print(f"Loaded: {path} (Resolution: {surface.get_size()})")
                    return surface
                except Exception as e:
                    print(f"Error loading {path}: {e}")
                    continue
        
        return None
    
    def load_vehicle_sprite(self, vehicle_type, angle=0):
        """Load vehicle sprite with rotation support"""
        path = self.asset_base_path / f'vehicles/{vehicle_type}_8k.png'
        
        try:
            surface = pygame.image.load(str(path))
            if angle != 0:
                surface = pygame.transform.rotate(surface, angle)
            return surface
        except Exception as e:
            print(f"Error loading vehicle: {e}")
            return None
    
    def load_weapon_icon(self, weapon_name):
        """Load weapon icon for HUD"""
        path = self.asset_base_path / f'weapons/{weapon_name}_8k.png'
        
        try:
            surface = pygame.image.load(str(path))
            # Scale to HUD size
            hud_surface = pygame.transform.scale(surface, (64, 64))
            return hud_surface
        except Exception as e:
            print(f"Error loading weapon icon: {e}")
            return None
    
    def preload_assets(self, asset_list):
        """Preload assets during game initialization"""
        for asset in asset_list:
            asset_type, asset_name = asset.split(':')
            if asset_type == 'character':
                self.load_character_sprite(*asset_name.split('/'))
            elif asset_type == 'vehicle':
                self.load_vehicle_sprite(asset_name)
    
    def get_asset(self, asset_key):
        """Retrieve cached asset"""
        return self.loaded_assets.get(asset_key)
    
    def cache_stats(self):
        """Get cache statistics"""
        return {
            'total_loaded': len(self.loaded_assets),
            'memory_usage': sum(s.get_size()[0] * s.get_size()[1] * 4 for s in self.loaded_assets.values())
        }
```

### 2.3 Image Processing & Optimization
**File: `game/utils/image_optimizer.py`**

```python
from PIL import Image
import os

class ImageOptimizer:
    """Optimizes 8K/4K images for gaming"""
    
    @staticmethod
    def optimize_image(input_path, output_path, max_resolution=None):
        """Optimize image while maintaining quality"""
        img = Image.open(input_path)
        
        if max_resolution:
            img.thumbnail(max_resolution, Image.Resampling.LANCZOS)
        
        # Use high-quality settings
        img.save(output_path, quality=95, optimize=True)
        
        return output_path
    
    @staticmethod
    def create_resolution_variants(source_image_path):
        """Create 8K and 4K variants from high-res source"""
        img = Image.open(source_image_path)
        base_name = os.path.splitext(source_image_path)[0]
        
        # Create 8K version (7680x4320)
        img_8k = img.resize((7680, 4320), Image.Resampling.LANCZOS)
        img_8k.save(f'{base_name}_8k.png', quality=95)
        
        # Create 4K version (3840x2160)
        img_4k = img.resize((3840, 2160), Image.Resampling.LANCZOS)
        img_4k.save(f'{base_name}_4k.png', quality=95)
        
        print(f"Created 8K and 4K variants for {source_image_path}")
```

---

## Phase 3: Weapon Systems Integration

### 3.1 Firing Mechanics
**File: `game/systems/weapon_mechanics.py`**

```python
import pygame
import math
from typing import Tuple

class WeaponMechanics:
    """Handles weapon firing and ballistics"""
    
    def __init__(self, ammo_system):
        self.ammo_system = ammo_system
        self.projectiles = []
        self.muzzle_flashes = []
    
    def fire_weapon(self, position: Tuple[int, int], direction: Tuple[float, float]) -> bool:
        """Fire the current weapon"""
        if not self.ammo_system.shoot():
            return False
        
        weapon = self.ammo_system.current_weapon
        stats = self.ammo_system.get_weapon_stats(weapon)
        
        # Create projectile
        projectile = {
            'position': list(position),
            'direction': direction,
            'damage': stats['damage'],
            'speed': 10,  # pixels per frame
            'active': True,
            'weapon_type': weapon
        }
        
        self.projectiles.append(projectile)
        
        # Add muzzle flash effect
        self.create_muzzle_flash(position, direction)
        
        return True
    
    def create_muzzle_flash(self, position, direction):
        """Create visual muzzle flash effect"""
        muzzle_flash = {
            'position': position,
            'direction': direction,
            'lifetime': 0.1,  # seconds
            'created_at': pygame.time.get_ticks()
        }
        self.muzzle_flashes.append(muzzle_flash)
    
    def update_projectiles(self, dt, obstacles):
        """Update all active projectiles"""
        for projectile in self.projectiles[:]:
            if not projectile['active']:
                self.projectiles.remove(projectile)
                continue
            
            # Update position
            projectile['position'][0] += projectile['direction'][0] * projectile['speed']
            projectile['position'][1] += projectile['direction'][1] * projectile['speed']
            
            # Check boundaries
            if (projectile['position'][0] < 0 or projectile['position'][0] > 1280 or
                projectile['position'][1] < 0 or projectile['position'][1] > 720):
                projectile['active'] = False
```

---

## Phase 4: Integration Guide

### 4.1 Main Game Loop Update
**File: `game/main.py` - Key Updates**

```python
from game.systems.ammo_system import AmmoSystem
from game.systems.weapon_mechanics import WeaponMechanics
from game.systems.asset_manager import AssetManager
from game.ui.weapon_selection import WeaponSelectionUI

class MiniGTAGame:
    def __init__(self):
        self.ammo_system = AmmoSystem()
        self.weapon_mechanics = WeaponMechanics(self.ammo_system)
        self.asset_manager = AssetManager()
        self.weapon_ui = WeaponSelectionUI()
        
        # Preload critical assets
        self.asset_manager.preload_assets([
            'character:protagonist/idle',
            'vehicle:sedan',
            'weapon:pistol'
        ])
    
    def handle_weapon_switch(self, weapon_name):
        """Handle weapon selection"""
        self.ammo_system.switch_weapon(weapon_name)
    
    def handle_shooting(self, player_pos, direction):
        """Handle player shooting"""
        self.weapon_mechanics.fire_weapon(player_pos, direction)
    
    def render_hud(self, surface):
        """Render HUD with weapon and ammo info"""
        current_weapon = self.ammo_system.current_weapon
        ammo_display = self.weapon_ui.get_ammo_display(self.ammo_system)
        
        # Display weapon name and ammo
        font = pygame.font.Font(None, 36)
        weapon_text = font.render(f"Weapon: {current_weapon.upper()}", True, (255, 255, 255))
        ammo_text = font.render(f"Ammo: {ammo_display}", True, (0, 255, 0))
        
        surface.blit(weapon_text, (10, 10))
        surface.blit(ammo_text, (10, 50))
```

---

## Asset Requirements & Sourcing

### 4K/8K Asset Specifications

| Asset Type | Resolution | Count | Format | Color Space |
|-----------|-----------|-------|--------|------------|
| Characters | 8K (7680×4320) | 20+ | PNG/WebP | sRGB |
| Vehicles | 8K (7680×4320) | 15+ | PNG/WebP | sRGB |
| Weapons | 4K (3840×2160) | 6 | PNG | sRGB |
| Environments | 4K (3840×2160) | 10+ | PNG | sRGB |
| UI Elements | 4K (3840×2160) | Full set | PNG | sRGB |

### Recommended Asset Sources
- **Professional 3D Renders**: Use Blender for original character/vehicle creation
- **High-Resolution Photography**: Stock images or original photography (8K cameras)
- **Post-Processing**: Upscaling with AI tools (Topaz Gigapixel AI, Real-ESRGAN)
- **Game Asset Packages**: Licensed from reputable creators

---

## Implementation Roadmap

### Week 1: Core Systems
- [ ] Implement `AmmoSystem` with unlimited ammo
- [ ] Create weapon switching mechanics
- [ ] Build weapon selection UI

### Week 2: Asset Infrastructure
- [ ] Set up asset directory structure
- [ ] Implement `AssetManager` with resolution fallbacks
- [ ] Create image optimization pipeline

### Week 3: Visual Implementation
- [ ] Integrate 4K assets for all characters
- [ ] Integrate 4K assets for all vehicles
- [ ] Test performance and memory usage

### Week 4: Enhancement & Polish
- [ ] Add 8K assets for critical characters/vehicles
- [ ] Implement muzzle flash and projectile effects
- [ ] Performance optimization and caching

---

## Performance Considerations

### Memory Management
```python
# Recommended max memory for asset cache: 2-4GB
# Implement dynamic asset unloading for inactive areas
# Use texture atlasing for UI elements
```

### File Size Optimization
- **8K PNG**: ~15-25MB per image
- **4K PNG**: ~5-8MB per image
- **Recommended**: Use WebP format for 30-40% size reduction
- **Streaming**: Load assets asynchronously during gameplay

### Resolution Scaling
```python
# Adaptive resolution based on system capabilities
if gpu_vram > 8000:  # 8GB+
    resolution = '8k'
elif gpu_vram > 4000:  # 4GB+
    resolution = '4k'
else:
    resolution = '2k'  # Fallback
```

---

## Testing & Validation

### Unit Tests
```python
# test_ammo_system.py
def test_unlimited_ammo():
    ammo = AmmoSystem()
    assert ammo.shoot() == True
    assert ammo.shoot() == True

def test_weapon_switching():
    ammo = AmmoSystem()
    ammo.switch_weapon('rifle')
    assert ammo.current_weapon == 'rifle'

# test_asset_manager.py
def test_asset_loading():
    am = AssetManager()
    sprite = am.load_character_sprite('protagonist', 'idle')
    assert sprite is not None
```

### Performance Testing
- Target FPS: 60 FPS minimum
- Memory usage: < 4GB with full 4K assets
- Load time: < 5 seconds for level startup

---

## Deployment Instructions

1. **Clone/Pull Latest**: `git pull origin main`
2. **Extract Assets**: Unzip high-resolution asset pack
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Run Optimization**: `python -m game.utils.image_optimizer`
5. **Launch Game**: `python main.py`

---

## Contributors
- Lead Developer: Aqm2227-AI
- Asset Director: [Your Name]
- Testing Team: [Team Members]

---

**Last Updated**: June 3, 2026
**Status**: In Development
