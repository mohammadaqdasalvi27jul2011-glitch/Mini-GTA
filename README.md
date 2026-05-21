# Mini GTA - Complete Edition 🎮

A fully-featured GTA-style open world action game built with Pygame featuring vehicles, police, missions, and more!

## ✨ Features

### **Core Gameplay**
✅ **Massive Open World** - 3000x2000 pixel explorable map  
✅ **Player Movement** - Smooth WASD/Arrow key controls  
✅ **3 Weapons System** - Pistol, Rifle, Shotgun with unique stats  
✅ **3 Vehicle Types** - Cars, Trucks, Motorcycles (each with unique speed/health)  
✅ **Realistic Physics** - Friction, acceleration, vehicle handling  

### **Combat & Police**
✅ **Dynamic Police System** - Police patrol and chase wanted players  
✅ **Police Combat** - Officers shoot back with AI targeting  
✅ **5-Star Wanted System** - Progressive consequences for crimes  
✅ **Vehicle Destruction** - Damage and destroy vehicles  

### **AI & NPCs**
✅ **25 AI Pedestrians** - Dynamic NPCs with pathfinding  
✅ **Fleeing Behavior** - NPCs run when you're wanted  
✅ **Varied NPC States** - Walking, idle, fleeing  
✅ **Dynamic Spawning** - NPCs respawn as you play  

### **Mission System**
✅ **3 Dynamic Missions** - Kill targets, earn money, reach wanted levels  
✅ **Mission Tracking** - Real-time progress display  
✅ **Reward System** - Earn bonuses for completing missions  

### **Items & Pickups**
✅ **Health Pickups** - Green packages restore 25 health  
✅ **Ammo Pickups** - Yellow packages restore 30 ammo  
✅ **Auto-Collection** - Pick up items by proximity  
✅ **Drop Chance** - 30% health / 20% ammo when NPCs die  

### **Progression & Tracking**
✅ **High Score System** - Persistent JSON save file  
✅ **Statistics** - Money, kills, accuracy, missions  
✅ **Accuracy Tracking** - Monitor shot success rate  

### **User Interface**
✅ **Main Menu** - Professional menu with instructions  
✅ **Dynamic HUD** - Real-time stats & mission display  
✅ **Pause System** - Pause/resume gameplay  
✅ **Game Over Screen** - Final stats & high scores  

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| **SPACE** | Start Game (from menu) |
| **WASD** / **Arrow Keys** | Move player or vehicle |
| **1, 2, 3** | Switch weapons (Pistol, Rifle, Shotgun) |
| **E** | Enter/Exit vehicle |
| **Mouse Click** | Shoot |
| **ESC** | Pause/Resume or Menu |

---

## 🚀 Installation

### Quick Start (Desktop)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Requirements

- Python 3.8+
- Pygame 2.5.2+
- NumPy

See [requirements.txt](requirements.txt) for full list.

---

## 🎯 Gameplay Guide

### **Starting Out**
1. Press **SPACE** from the menu to start
2. You spawn with 100 health and 100 pistol ammo
3. NPCs (green squares) walk around the world
4. Police (dark blue vehicles) patrol and respond to crimes

### **Combat System**
```
- Point mouse at enemies
- Click to shoot (hold for rapid fire)
- Switch weapons: 1, 2, 3
- Each weapon has different damage/fire rate:
  • Pistol: 10 damage, fast fire rate, 100 ammo
  • Rifle: 25 damage, medium fire rate, 60 ammo
  • Shotgun: 40 damage, slow fire rate, 30 ammo (3 bullets)
```

### **Vehicles**
```
- Press E near a vehicle to enter
- Drive with WASD
- Rotate with A/D keys (only while driving)
- Press E to exit
- Vehicles take damage from bullets
```

### **Police System**
```
- Police patrol the world
- Eliminate NPCs = +0.5 wanted level
- Damage police = +1.0 wanted level
- Destroy police vehicle = +2.0 wanted level
- Higher wanted = more aggressive police
- Wanted decreases over time when you stop
```

### **Missions**
```
You get 3 random missions:
✓ Kill N NPCs - Eliminate specific enemies for bonus
✓ Earn $N - Accumulate money through killings
✓ Reach 5-Star - Get maximum wanted level

Complete missions for extra cash!
```

### **Pickups**
```
GREEN packages (30% drop): Restore 25 health
YELLOW packages (20% drop): Restore 30 ammo

Walk over them to automatically collect
Pickups disappear after 10 seconds if not collected
```

---

## 🚗 Vehicle Types

| Vehicle | Speed | Health | Best For |
|---------|-------|--------|----------|
| **Car** | 8.0 | 100 | Balanced gameplay |
| **Truck** | 5.6 | 150 | Ramming, durability |
| **Motorcycle** | 10.4 | 100 | Speed, escaping |

---

## 💡 Pro Tips

✅ **Weapon Management** - Switch weapons when ammo runs low  
✅ **Vehicle Escape** - Drive away to reduce wanted level  
✅ **Shotgun Groups** - Use on groups of NPCs  
✅ **Pickup Farming** - Farm NPCs in one area for pickups  
✅ **Mission Chaining** - Complete missions for extra cash  
✅ **Police Evasion** - Use tight spaces to lose police  
✅ **Accuracy Matters** - Better accuracy = efficiency  

---

## 🏆 Challenge Ideas

🎯 **Try These Challenges:**
- 🔫 **Sharpshooter** - Achieve 80%+ accuracy
- 💰 **Millionaire** - Earn $5000+
- 🎖️ **Mission Master** - Complete all 3 missions
- ⭐ **Most Wanted** - Reach & maintain 5-star wanted
- 🚗 **Vehicle Wrecker** - Destroy 10 vehicles
- 🔫 **Head Honcho** - Eliminate 100+ NPCs
- 👮 **Police Chase** - Evade police for 5+ minutes

---

## 📊 Game Statistics Tracked

- **Money Earned** - Total cash accumulated
- **NPCs Eliminated** - Total kills
- **Missions Completed** - Successful mission count
- **Accuracy** - Percentage of shots that hit
- **Distance Driven** - Total vehicle distance
- **High Score** - Best money earned (saved!)
- **Best Kills** - Record NPC count (saved!)

---

## 📁 File Structure

```
Mini-GTA/
├── main.py                    # Complete game code (1400+ lines)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── play.html                  # Web interface & landing page
├── LICENSE                    # MIT License
├── PRIVACY_POLICY.md          # Privacy policy for app stores
├── PLAYSTORE_DEPLOYMENT.md    # Google Play Store guide
├── DEPLOYMENT_CHECKLIST.md    # Pre-launch checklist
├── buildozer.spec             # Buildozer configuration
└── highscore.json             # Auto-generated high scores
```

---

## 🎓 What You'll Learn

This game demonstrates:
- **Game Architecture** - State management, game loops
- **Sprite Management** - Groups, collisions, lifecycle
- **AI Systems** - Pathfinding, state machines
- **Physics** - Velocity, acceleration, friction
- **File I/O** - JSON persistence, high scores
- **UI Design** - Menus, HUD, displays
- **Game Mechanics** - Missions, progression, rewards

---

## 📝 Weapon Specs

| Weapon | Damage | Fire Rate | Ammo | Best For |
|--------|--------|-----------|------|----------|
| **Pistol** | 10 | 5ms | 100 | Quick shots, general use |
| **Rifle** | 25 | 8ms | 60 | Balanced damage/speed |
| **Shotgun** | 40 | 10ms | 30 | Close combat, groups (3 bullets) |

---

## 🐛 Troubleshooting

**Game won't start?**
- Ensure pygame is installed: `pip install pygame==2.5.2`
- Run from the repository directory
- Check Python version: 3.8+

**Can't find pickups?**
- Yellow = ammo, Green = health
- They spawn when NPCs die (30%/20% chance)
- They disappear after 10 seconds

**Performance issues?**
- Reduce NPC count in `init_game()` method
- Lower FPS from 60 to 30 if needed
- Close other applications

---

## 📱 Android & Google Play Store

### Deploy to Google Play Store

Mini GTA can be packaged as an Android app and published to the Google Play Store!

**Quick Start:**
1. Review [PLAYSTORE_DEPLOYMENT.md](PLAYSTORE_DEPLOYMENT.md) for detailed guide
2. Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) before submission
3. Use provided [buildozer.spec](buildozer.spec) configuration

**Requirements:**
- Buildozer and Kivy installed
- Java Development Kit (JDK)
- Android SDK
- Google Play Developer account ($25 fee)

**Build Commands:**
```bash
# Install tools
pip install kivy buildozer

# Debug build
buildozer -v android debug

# Release build for Play Store
buildozer -v android release
```

See [PLAYSTORE_DEPLOYMENT.md](PLAYSTORE_DEPLOYMENT.md) for complete instructions.

---

## 🎮 Enjoy!

You now have a complete, fully playable GTA-style game! Have fun exploring the open world, completing missions, and building your crime empire! 🚗💥

**Made with Pygame | Open World Action Game | Complete Edition**

---

## 📸 Game Features Summary

- 🌍 **3000x2000 Open World**
- 👮 **Dynamic Police System**
- 🎯 **3 Mission Types**
- 🚗 **3 Vehicle Types**
- 🔫 **3 Weapon Types**
- 👥 **25 AI NPCs**
- 💰 **Money & Rewards**
- 📊 **High Score System**
- ⏸️ **Pause/Resume**
- 🎮 **Full Menu System**
- 📱 **Android Ready** (Google Play Store)

---

## 📜 License & Copyright

**© 2025 Mohammad Aqdas Alvi (mohammadaqdasalvi27jul2011-glitch)**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### License Summary:
- ✅ **Free to use** - Personal and educational purposes
- ✅ **Free to modify** - Create your own versions
- ✅ **Free to distribute** - Share with others
- ⚠️ **Attribution required** - Please credit the original author
- ⚠️ **No warranty** - Use at your own risk

### Citation:
If you use this project in your work, please cite it as:
```
Mini GTA - Open World Action Game
Author: Mohammad Aqdas Alvi
URL: https://github.com/mohammadaqdasalvi27jul2011-glitch/Mini-GTA
Year: 2025
License: MIT
```

### Important Links:
- 🔗 **Repository:** https://github.com/mohammadaqdasalvi27jul2011-glitch/Mini-GTA
- 📄 **License:** https://github.com/mohammadaqdasalvi27jul2011-glitch/Mini-GTA/blob/main/LICENSE
- 🔐 **Privacy Policy:** https://github.com/mohammadaqdasalvi27jul2011-glitch/Mini-GTA/blob/main/PRIVACY_POLICY.md
- 📱 **Play Store Guide:** https://github.com/mohammadaqdasalvi27jul2011-glitch/Mini-GTA/blob/main/PLAYSTORE_DEPLOYMENT.md
- ✅ **Deployment Checklist:** https://github.com/mohammadaqdasalvi27jul2011-glitch/Mini-GTA/blob/main/DEPLOYMENT_CHECKLIST.md

---

## 👤 Author

**Mohammad Aqdas Alvi**
- GitHub: [@mohammadaqdasalvi27jul2011-glitch](https://github.com/mohammadaqdasalvi27jul2011-glitch)
- Email: mohammadaqdasalvi27jul2011@gmail.com

---

**Made with ❤️ using Python & Pygame**

Join thousands of players experiencing the complete Mini GTA action game! 🎮🚗💥
