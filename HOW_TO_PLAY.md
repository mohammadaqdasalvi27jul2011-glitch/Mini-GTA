# 🎮 HOW TO PLAY MINI GTA - QUICK START GUIDE

## ⚡ 60-SECOND SETUP

### Step 1: Install Python Requirements (30 seconds)
```bash
pip install -r requirements.txt
```

### Step 2: Run the Game (Immediate!)
```bash
python main.py
```

**THAT'S IT! The game will launch immediately!** 🎉

---

## 🎮 PLAYING THE GAME

### Main Menu
- Press **SPACE** to start playing
- Read the instructions on screen

### In-Game Controls

| Key | Action |
|-----|--------|
| **WASD** or **Arrow Keys** | Move your character |
| **Mouse Move** | Look/aim at enemies |
| **Mouse Click** | Shoot |
| **1, 2, 3** | Switch weapons (Pistol, Rifle, Shotgun) |
| **E** | Enter/exit vehicles |
| **ESC** | Pause the game |

---

## 📱 MOBILE VERSION (Optional)

To play the mobile-optimized version instead:
```bash
python app.py
```

Features:
- Touch screen controls
- Responsive design
- Better for tablet testing

---

## 🎯 OBJECTIVE

1. **Explore the open world** - Walk around the 3000×2000 pixel map
2. **Complete missions** - Kill NPCs, earn money, reach wanted level
3. **Collect pickups** - Green=health, Yellow=ammo
4. **Escape police** - Build wanted level by causing chaos
5. **Beat high scores** - Your score is automatically saved

---

## 🚀 TROUBLESHOOTING

### "Command not found: python"
Use `python3` instead:
```bash
python3 main.py
```

### "ModuleNotFoundError: No module named 'pygame'"
Install requirements again:
```bash
pip install -r requirements.txt
```

### Game is too slow
Lower FPS in the code or close other apps

### Can't see game window
- Make sure your screen resolution isn't too small
- Try moving your mouse to wake up the window

---

## 📊 GAME STATS TRACKED

- 💰 **Money** - Earned by killing NPCs
- 🔫 **Kills** - Number of NPCs eliminated
- 🎯 **Accuracy** - Percentage of shots that hit
- ⭐ **Wanted Level** - Police heat (0-5 stars)
- 🎖️ **Missions** - Completed missions
- 💪 **Health** - Your life points

---

## 🏆 GAME TIPS

✅ **Switch weapons** when ammo runs low  
✅ **Drive vehicles** to escape police faster  
✅ **Use shotgun** on groups of enemies  
✅ **Find pickups** to restore health/ammo  
✅ **Avoid police** when wanted level is high  

---

## 📁 FILE LOCATIONS

Your game saves here:
- `highscore.json` - Your best score

Game files:
- `main.py` - Desktop game code
- `app.py` - Mobile game code
- `requirements.txt` - Dependencies list

---

## 🎮 LET'S PLAY!

```bash
# One command to launch:
python main.py

# Then press SPACE in the menu to start!
```

**Enjoy your game!** 🚀

---

## ❓ FREQUENTLY ASKED QUESTIONS

**Q: How do I save my game?**
A: High scores are automatically saved to `highscore.json`

**Q: Can I play on my phone?**
A: Yes! Build APK using: `buildozer -v android debug`

**Q: How do I change game difficulty?**
A: Edit `main.py` and change NPC count or health values

**Q: Where's my high score saved?**
A: In the game directory as `highscore.json`

**Q: Can I modify the game?**
A: Yes! The MIT License allows you to modify and share it

---

## 🚀 NEXT STEPS

1. **Play the game** - `python main.py`
2. **Get familiar** - Learn the controls and gameplay
3. **Beat high scores** - Try to get the highest score
4. **Build for Android** - `buildozer -v android debug`
5. **Share with friends** - Link them the GitHub repo!

---

**Made with Python & Pygame**
**© 2025 Mohammad Aqdas Alvi**
**MIT License - Free to play, modify, and share!**
