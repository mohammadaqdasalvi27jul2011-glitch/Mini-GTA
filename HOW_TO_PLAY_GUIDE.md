# 🎮 HOW TO PLAY - COMPLETE GUIDE

## 📌 IMPORTANT: Which File Should You Play?

You have **multiple applications** in this repository. Here's what each one does:

---

## 🎮 MINI GTA GAME (What You Probably Want!)

### **To Play Mini GTA:**

#### **Option 1: Desktop Version (RECOMMENDED)**
```bash
python main.py
```

**What you need:**
- Python installed
- Run this command in terminal/command prompt

**What it does:**
- Opens a window with the Mini GTA game
- Play immediately with mouse & keyboard controls

---

#### **Option 2: Mobile Version (Testing)**
```bash
python app.py
```

**What you need:**
- Python installed
- For testing touch controls

---

## 🕐 DIGITAL CLOCK (Separate Application)

### **To Use Digital Clock:**

#### **Option 1: Python Desktop Clock**
```bash
python clock.py
```

**What it does:**
- Shows current time in 24+ time zones
- NOT a game - it's a utility app

---

#### **Option 2: Web Clock (No Installation!)**
1. Find the file: **clock.html**
2. Double-click it
3. It opens in your browser
4. Shows world time zones

---

## 🎯 STEP-BY-STEP GUIDE TO PLAY MINI GTA

### **Step 1: Open Terminal/Command Prompt**

**Windows:**
1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter

**Mac:**
1. Press `Command + Space`
2. Type: `terminal`
3. Press Enter

**Linux:**
- Open terminal from applications

---

### **Step 2: Navigate to Your Game Folder**

```bash
cd C:\Users\YourUsername\Mini-GTA
```

(Replace `YourUsername` with your actual username)

Or if you cloned from GitHub:
```bash
cd Mini-GTA
```

---

### **Step 3: Install Dependencies** (First time only)

```bash
pip install -r requirements.txt
```

Wait for it to complete. You should see:
```
Successfully installed pygame-2.x.x
```

---

### **Step 4: Launch Mini GTA!**

```bash
python main.py
```

**You should see:**
- A window opening with the game
- Main menu with title "MINI GTA"
- Instructions on screen

---

### **Step 5: Play the Game!**

**Press SPACE** to start playing

---

## 🎮 GAME CONTROLS

Once the game starts, here are the controls:

| Key | Action |
|-----|--------|
| **W** or **UP Arrow** | Move Forward |
| **A** or **LEFT Arrow** | Move Left |
| **S** or **DOWN Arrow** | Move Backward |
| **D** or **RIGHT Arrow** | Move Right |
| **Mouse Move** | Aim/Look |
| **Mouse Click** | Shoot |
| **1** | Switch to Pistol |
| **2** | Switch to Rifle |
| **3** | Switch to Shotgun |
| **E** | Enter/Exit Vehicle |
| **ESC** | Pause Menu |
| **SPACE** | Start Game (from menu) |

---

## 🎯 GAME OBJECTIVES

1. **Explore** - Walk around the open world
2. **Kill NPCs** - Shoot at enemies to earn money
3. **Complete Missions** - Follow mission objectives on screen
4. **Collect Pickups** - Green boxes = health, Yellow boxes = ammo
5. **Escape Police** - Avoid getting caught when wanted
6. **Beat High Scores** - Your score is automatically saved

---

## 📊 WHAT YOU SEE ON SCREEN

- **Top Left:** Your health, weapons, money
- **Center:** Your character (small yellow figure)
- **Around:** NPCs (pink figures), Police (blue cars), Vehicles (red/orange cars)
- **Yellow Circles:** Bullets you fire
- **Green/Yellow Boxes:** Pickups to collect

---

## ✅ QUICK CHECKLIST

- [ ] Python installed? (Check: `python --version`)
- [ ] In the Mini-GTA folder? (Check: `ls` shows main.py)
- [ ] Dependencies installed? (Ran `pip install -r requirements.txt`)
- [ ] Run `python main.py`
- [ ] Window opens?
- [ ] Press SPACE to play!
- [ ] 🎮 Start gaming!

---

## ❌ TROUBLESHOOTING

### **"Command not found: python"**
**Solution:** Use `python3` instead
```bash
python3 main.py
```

### **"ModuleNotFoundError: No module named 'pygame'"**
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### **"No such file or directory: main.py"**
**Solution:** You're in the wrong folder
```bash
# Navigate to correct folder
cd path/to/Mini-GTA
python main.py
```

### **Game window opens but nothing displays**
**Solution:** Wait a few seconds for it to load

### **Game is very slow**
**Solution:** 
- Close other programs
- Try `python app.py` instead (mobile version)
- Lower graphics if possible

---

## 🌍 ALL FILES IN THIS REPOSITORY

| File | What It Does | How to Play |
|------|-------------|-----------|
| **main.py** | Mini GTA Game (Desktop) | `python main.py` |
| **app.py** | Mini GTA Game (Mobile Version) | `python app.py` |
| **clock.py** | Digital Clock (24+ Time Zones) | `python clock.py` |
| **clock.html** | Digital Clock (Web Version) | Double-click or open in browser |
| **play.html** | Game Landing Page | Open in browser |
| **requirements.txt** | Dependencies | `pip install -r requirements.txt` |

---

## 🎮 WHICH FILE SHOULD I PLAY?

**If you want to PLAY A GAME:**
```bash
python main.py
```
✅ This is the Mini GTA game!

**If you want a DIGITAL CLOCK:**
```bash
python clock.py
```
or double-click `clock.html`

**For MOBILE/TOUCH version of game:**
```bash
python app.py
```

---

## 🚀 FASTEST WAY TO PLAY

1. **Windows:** 
   ```bash
   pip install pygame && python main.py
   ```

2. **Mac/Linux:**
   ```bash
   pip install pygame && python main.py
   ```

3. **Press SPACE to start playing!**

---

## 💡 TIPS FOR BETTER GAMEPLAY

1. **Early Game:** Shoot NPCs to earn money
2. **Get Vehicles:** Press E near cars to drive them
3. **Switch Weapons:** Use 1, 2, 3 keys for different weapons
4. **Collect Pickups:** Walk over green/yellow boxes
5. **Escape Police:** If wanted level is high, run!
6. **Check High Scores:** Look at `highscore.json` file

---

## 📂 FILE LOCATIONS

**Your game files are:**
```
C:\Users\YourUsername\Mini-GTA\
├── main.py          ← PLAY THIS!
├── app.py           ← Or this (mobile)
├── clock.py         ← Digital clock
├── clock.html       ← Web clock
├── requirements.txt ← Dependencies
└── [other files]
```

---

## ✨ WHAT YOU'LL SEE WHEN YOU PLAY

```
┌──────────────────────────────────────┐
│     MINI GTA - Open World Game       │
├──────────────────────────────────────┤
│ Health: 100/100                      │
│ Pistol: 50/100                       │
│ Money: $0                            │
│ Wanted: ☆☆☆☆☆                      │
├──────────────────────────────────────┤
│                                      │
│     YOU (yellow) in open world       │
│     Shoot NPCs (pink)                │
│     Avoid police (blue)              │
│     Drive vehicles (red)             │
│                                      │
│     WASD to move, Mouse to aim       │
│     Click to shoot!                  │
│                                      │
└──────────────────────────────────────┘
```

---

## 🎯 MISSION EXAMPLES

**Kill 5 NPCs**
- Walk around
- Click to shoot NPCs
- Get $500 when complete

**Earn $1000**
- Kill NPCs (worth $50 each)
- Collect 20 kills to earn $1000

**Reach 5-Star Wanted**
- Kill lots of NPCs
- Police will chase you
- Reach 5-star rating

---

## 🏆 SUCCESS CRITERIA

You'll know you're playing correctly when you see:

✅ Game window opens
✅ You see your character (yellow)
✅ You see NPCs, vehicles, pickups
✅ WASD keys move your character
✅ Mouse click fires bullets
✅ Money counter goes up after kills
✅ Wanted level increases when you cause trouble
✅ You're having fun!

---

## 📞 QUICK REFERENCE

**To Play Mini GTA:**
```bash
python main.py
```

**To Use Digital Clock:**
```bash
python clock.py
```

**To Use Web Clock:**
Double-click `clock.html`

**To Install Dependencies:**
```bash
pip install -r requirements.txt
```

---

## 🎮 START PLAYING NOW!

**Copy and paste this into your terminal:**

```bash
pip install pygame && python main.py
```

**Then press SPACE when the game opens!**

---

## 📖 STILL CONFUSED?

1. **Where do I find these files?**
   - In your Mini-GTA folder on your computer

2. **What do I type in terminal?**
   - Copy the command exactly from above
   - Paste it in terminal
   - Press Enter

3. **Where is terminal?**
   - Windows: `cmd`
   - Mac: `terminal`
   - Linux: Terminal app

4. **Is it free?**
   - Yes! MIT License - completely free

5. **Can I modify it?**
   - Yes! It's open source

---

## ✅ YOU'RE READY!

1. Open terminal
2. Navigate to Mini-GTA folder
3. Type: `python main.py`
4. Press SPACE to play
5. Enjoy! 🎮

---

**🎉 HAVE FUN PLAYING MINI GTA! 🎮**

**Questions? Check this file or README.md**

Made with ❤️ using Python & Pygame
© 2025 Mohammad Aqdas Alvi
