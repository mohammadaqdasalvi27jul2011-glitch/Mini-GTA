# 🎮 Mini GTA - 100% Python Edition

**Complete Game Suite - No External Files, Pure Python**

A fully-featured GTA-style open world action game with a world clock, entirely written in Python. Everything is embedded in Python - HTML, CSS, and JavaScript are generated dynamically.

## 📋 Overview

Mini GTA is now a **100% Pure Python** implementation featuring:
- **Game Engine**: Complete game logic in Python
- **Web Server**: Built-in HTTP server using Python's `http.server`
- **Game UI**: All HTML/CSS/JavaScript embedded as Python strings
- **No External Files**: Everything generated on-the-fly
- **Single File Deployment**: Just one `server.py` file needed

## 🚀 Quick Start

### Installation

```bash
# No dependencies needed - uses only Python stdlib
python3 server.py
```

### Access

Open your browser and visit:
- **Main Hub**: http://localhost:8000
- **Game**: http://localhost:8000/game
- **Clock**: http://localhost:8000/clock
- **Info**: http://localhost:8000/info

Browser automatically opens on startup!

## 🎮 Game Features

### Core Gameplay
- **Open World**: 4000x3000 pixel explorable map
- **Dynamic Camera**: Follows player position
- **Smooth Controls**: WASD movement, Mouse aim
- **Real-time Physics**: Collision detection and movement

### Combat System
Three weapons with unique characteristics:
- **Pistol**: Fast, low damage (15 dmg, 100ms cooldown)
- **Rifle**: Balanced (30 dmg, 150ms cooldown)
- **Shotgun**: Slow, high damage, spread shots (50 dmg, 300ms cooldown)

### AI System
- **15+ NPCs** spawning dynamically
- **Smart Movement**: Random patrolling with direction changes
- **Combat Response**: Damage feedback, health system
- **Loot Drops**: Health and ammo pickups on defeat

### Vehicles
- **6 Drivable Vehicles**: Cars, trucks, motorcycles
- **Speed Boost**: Increased movement when driving
- **Dynamic Spawning**: Vehicles patrol the world

### Progression System
- **Wave System**: Difficulty increases, more enemies spawn
- **Wanted Level**: 5-star system (displayed with ★ symbols)
- **Money System**: Earn cash from kills ($100 per NPC)
- **Score Tracking**: Points for kills, accuracy, wave completion

### Stats & Metrics
- Health bar with damage tracking
- Ammo counter with fire rates
- Real-time kill counter
- Wave progression display
- Accuracy percentage calculation
- Session time tracking

## ⌨️ Controls

| Key | Action |
|-----|--------|
| **W/↑** | Move Up |
| **S/↓** | Move Down |
| **A/←** | Move Left |
| **D/→** | Move Right |
| **Mouse Move** | Aim |
| **Click** | Shoot |
| **1** | Pistol |
| **2** | Rifle |
| **3** | Shotgun |
| **E** | Enter/Exit Vehicle |
| **ESC** | Pause/Resume |
| **SPACE** | Start Game (from menu) |

## 🕐 World Clock

Separate application showing:
- **System Time**: Current local time
- **Multiple Zones**: UTC, New York, LA, London, Paris, Tokyo, Dubai, Sydney, Mumbai, Singapore
- **Real-time Updates**: Refreshes every second
- **Beautiful UI**: Gradient backgrounds, smooth animations

## 📊 Architecture

### Single File Design

```
server.py (31KB)
├── Game JavaScript (embedded)
├── Game HTML (embedded)
├── Clock HTML (embedded)
├── CSS Styles (embedded)
└── Python HTTP Server
```

### Key Components

**GameServerHandler Class**
- `do_GET()` - Route handler for all requests
- `serve_home()` - Main hub page
- `serve_game()` - Full game page with canvas and controls
- `serve_clock()` - World clock interface
- `serve_info()` - Game information page
- `serve_status()` - API endpoint for game status

**Game Engine (JavaScript)**
- `gameInstance` object manages all game state
- 60 FPS game loop with requestAnimationFrame
- Collision detection and physics
- Particle effects and animations

**Python Features Used**
- `http.server.HTTPServer` - Web server
- `urllib.parse` - URL parsing
- `json` - Status responses
- `threading` - Auto-open browser
- `webbrowser` - Browser launch
- `datetime` - Logging timestamps

## 📈 Game Mechanics

### Player System
```
Health: 0-100 (regenerates with pickups)
Wanted: 0-5 stars (increases from combat)
Money: Earned from NPC eliminations
Ammo: Per-weapon tracking
Score: Combo multipliers for waves
```

### NPC AI
```
- Spawn: 15 base + wave scaling
- Health: 30 HP each
- Movement: Random patrol with direction changes
- Loot: 50% chance to drop ammo/health
```

### Wave System
```
Wave 1: ~15 enemies
Wave 2: ~21 enemies  
Wave 3: ~27 enemies
...scales with (10 + wave * 3)
```

## 🎨 Visual Features

### Game Rendering
- **2D Canvas Graphics**: Optimized rectangle rendering
- **Gradient Backgrounds**: Dynamic world background
- **Grid System**: Visual world structure
- **Particle Effects**: Explosion animations on kills
- **Health Bars**: Red/green indicator on NPCs
- **Wanted Stars**: Unicode star display (★☆)

### Color Scheme
```
Game: Green (#00FF00), Cyan (#00D4FF), Black (#000000)
Menu: Red (#FF0000), Yellow (#FFFF00)
Clock: Cyan, Green gradient backgrounds
```

## 🔧 Technical Details

### Server Implementation
- **Port**: 8000 (configurable via command line)
- **Hostname**: 0.0.0.0 (accessible locally)
- **Routes**: 
  - `/` → Home hub
  - `/game` → Game page
  - `/clock` → Clock page
  - `/info` → Information
  - `/api/status` → JSON status

### Browser Compatibility
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Canvas 2D API**: Full support
- **ES6 JavaScript**: Arrow functions, classes
- **CSS Grid**: Responsive layouts

### Performance
- **Game Loop**: 60 FPS using requestAnimationFrame
- **Rendering**: Optimized canvas drawing
- **Memory**: ~5-10MB typical usage
- **Network**: Minimal - game runs locally in browser

## 📦 Deployment Options

### Local Development
```bash
python3 server.py
# Opens http://localhost:8000 automatically
```

### Custom Port
```bash
python3 server.py 9000
# Runs on http://localhost:9000
```

### Cloud Deployment
Works on any Python 3.6+ environment:
- Heroku
- AWS Lambda (with modifications)
- PythonAnywhere
- Replit
- Glitch

## 🎯 Game Flow

1. **Start Screen**: Press SPACE to begin
2. **Active Play**: 
   - Move with WASD
   - Aim with mouse
   - Shoot with left click
   - Switch weapons with 1/2/3
3. **Progression**: Waves increase as kills accumulate
4. **Game Over**: Health reaches 0
5. **Stats Display**: Final score, accuracy, money earned

## 📝 Code Structure

### Python (server.py)
- Compact game server (~31KB)
- All HTML/CSS/JS embedded as strings
- Dynamic content generation
- Zero external dependencies

### JavaScript (embedded)
- `gameInstance` main game object
- Event listeners for I/O
- Game loop and update logic
- Rendering engine
- HUD management

### HTML/CSS (embedded)
- Semantic markup
- Responsive design
- Gradient backgrounds
- Terminal-style UI

## 🐛 Debugging

### Browser Console
Open DevTools (F12) to see:
- JavaScript errors
- Network requests
- Console logs
- Performance metrics

### Server Logs
```
[2024-01-15 14:30:45] GET / HTTP/1.1
[2024-01-15 14:30:46] GET /game HTTP/1.1
[2024-01-15 14:30:47] GET /clock HTTP/1.1
```

## 🔮 Future Enhancements

Potential additions:
- [ ] Save/load game progress
- [ ] Multiplayer support
- [ ] Custom map editor
- [ ] Achievement system
- [ ] Sound effects
- [ ] Mobile touch controls
- [ ] Advanced AI pathfinding
- [ ] Procedural world generation

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Performance optimization
- Additional weapon types
- More vehicle variety
- Enhanced AI behaviors
- Mobile optimization
- Accessibility features

## 📚 References

- Python `http.server`: https://docs.python.org/3/library/http.server.html
- Canvas API: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- Game Development: Classic arcade game patterns and mechanics

## 🎓 Educational Value

Perfect for learning:
- Python web servers
- JavaScript game development
- HTML/CSS web design
- Game physics and collision detection
- Client-server architecture
- Responsive web design

---

**Made with ❤️ in Pure Python**

No frameworks. No build tools. No external files. Just Python.

```python
python3 server.py
# That's it! 🚀
```
