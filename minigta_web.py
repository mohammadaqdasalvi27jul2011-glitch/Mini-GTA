"""
Mini GTA - 4K Web Edition
HTML to Python conversion - Web-based GTA-style game
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MINI GTA - 4K Web Edition</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-user-select: none;
            user-select: none;
        }

        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: #000;
            color: #00ff00;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .main-container {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            background: #000;
        }

        #gameCanvas {
            display: block;
            width: 100%;
            height: 100%;
            background: #0a0a0a;
        }

        .menu-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            font-family: 'Arial', sans-serif;
        }

        .menu-overlay.hidden {
            display: none;
        }

        .menu-content {
            text-align: center;
            color: #00ff00;
            border: 3px solid #00ff00;
            padding: 40px;
            background: rgba(0, 20, 0, 0.8);
            border-radius: 10px;
            max-width: 600px;
        }

        .menu-content h1 {
            font-size: 72px;
            margin-bottom: 20px;
            color: #ff0000;
            text-shadow: 0 0 20px #ff0000;
            font-weight: bold;
            letter-spacing: 3px;
        }

        .menu-content h2 {
            font-size: 32px;
            margin-bottom: 30px;
            color: #ffff00;
        }

        .menu-content p {
            font-size: 18px;
            margin: 15px 0;
            color: #00ff00;
            line-height: 1.6;
        }

        .start-button {
            background: #00ff00;
            color: #000;
            border: 3px solid #00ff00;
            padding: 20px 50px;
            font-size: 24px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 30px;
            border-radius: 5px;
            transition: all 0.3s;
        }

        .start-button:hover {
            background: #ffff00;
            border-color: #ffff00;
            transform: scale(1.05);
        }

        .start-button:active {
            transform: scale(0.95);
        }

        .hud {
            position: fixed;
            top: 20px;
            left: 20px;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            z-index: 100;
            background: rgba(0, 0, 0, 0.7);
            padding: 15px;
            border: 2px solid #00ff00;
            border-radius: 5px;
        }

        .hud-line {
            margin: 5px 0;
            font-weight: bold;
        }

        .hud-label {
            color: #ffff00;
        }

        .hud-value {
            color: #00ff00;
        }

        .top-right-hud {
            position: fixed;
            top: 20px;
            right: 20px;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            z-index: 100;
            background: rgba(0, 0, 0, 0.7);
            padding: 15px;
            border: 2px solid #00ff00;
            border-radius: 5px;
            text-align: right;
        }

        .bottom-hud {
            position: fixed;
            bottom: 20px;
            left: 20px;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            z-index: 100;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border: 2px solid #00ff00;
            border-radius: 5px;
        }

        .game-over-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
        }

        .game-over-overlay.hidden {
            display: none;
        }

        .game-over-content {
            text-align: center;
            color: #ff0000;
            border: 3px solid #ff0000;
            padding: 40px;
            background: rgba(20, 0, 0, 0.8);
            border-radius: 10px;
            max-width: 600px;
        }

        .game-over-content h1 {
            font-size: 64px;
            margin-bottom: 30px;
            text-shadow: 0 0 20px #ff0000;
            font-weight: bold;
        }

        .stats-box {
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            margin: 20px 0;
            border: 2px solid #00ff00;
            border-radius: 5px;
        }

        .stat-line {
            font-size: 20px;
            color: #00ff00;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
        }

        .restart-button {
            background: #ff0000;
            color: #fff;
            border: 3px solid #ff0000;
            padding: 20px 50px;
            font-size: 24px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 30px;
            border-radius: 5px;
            transition: all 0.3s;
        }

        .restart-button:hover {
            background: #ff3333;
            border-color: #ff3333;
            transform: scale(1.05);
        }

        .pause-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1500;
        }

        .pause-overlay.hidden {
            display: none;
        }

        .pause-content {
            text-align: center;
            color: #ffff00;
            border: 3px solid #ffff00;
            padding: 40px;
            background: rgba(0, 0, 0, 0.9);
            border-radius: 10px;
        }

        .pause-content h1 {
            font-size: 48px;
            margin-bottom: 30px;
            text-shadow: 0 0 20px #ffff00;
        }

        .pause-content p {
            font-size: 18px;
            margin: 15px 0;
        }

        @media (max-width: 1024px) {
            .hud, .top-right-hud, .bottom-hud {
                font-size: 12px;
                padding: 10px;
            }

            .menu-content {
                padding: 30px;
                max-width: 90%;
            }

            .menu-content h1 {
                font-size: 48px;
            }

            .menu-content h2 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <canvas id="gameCanvas"></canvas>
    </div>

    <!-- Menu Overlay -->
    <div id="menuOverlay" class="menu-overlay">
        <div class="menu-content">
            <h1>🎮 MINI GTA</h1>
            <h2>4K Web Edition</h2>
            <p>Open World Action Game</p>
            <p style="font-size: 14px; color: #888;">Full Gameplay in Your Browser</p>
            <button class="start-button" onclick="gameInstance.startGame()">START GAME</button>
            <p style="margin-top: 30px; font-size: 12px; color: #666;">Press SPACE to start</p>
        </div>
    </div>

    <!-- Pause Overlay -->
    <div id="pauseOverlay" class="pause-overlay hidden">
        <div class="pause-content">
            <h1>⏸️ PAUSED</h1>
            <p>Press ESC to Resume</p>
            <p style="font-size: 14px; color: #888;">or click outside to continue</p>
        </div>
    </div>

    <!-- Game Over Overlay -->
    <div id="gameOverOverlay" class="game-over-overlay hidden">
        <div class="game-over-content">
            <h1>💀 GAME OVER</h1>
            <div class="stats-box">
                <div class="stat-line">Money Earned: $<span id="finalMoney">0</span></div>
                <div class="stat-line">Enemies Killed: <span id="finalKills">0</span></div>
                <div class="stat-line">Accuracy: <span id="finalAccuracy">0</span>%</div>
                <div class="stat-line">Time Survived: <span id="finalTime">0</span>s</div>
                <div class="stat-line">Wave Completed: <span id="finalWave">0</span></div>
            </div>
            <button class="restart-button" onclick="location.reload()">PLAY AGAIN</button>
        </div>
    </div>

    <!-- HUD Display -->
    <div class="hud">
        <div class="hud-line"><span class="hud-label">HEALTH:</span> <span class="hud-value" id="hudHealth">100</span>/100</div>
        <div class="hud-line"><span class="hud-label">MONEY:</span> $<span class="hud-value" id="hudMoney">0</span></div>
        <div class="hud-line"><span class="hud-label">AMMO:</span> <span class="hud-value" id="hudAmmo">30</span>/<span id="hudMaxAmmo">30</span></div>
        <div class="hud-line"><span class="hud-label">WEAPON:</span> <span class="hud-value" id="hudWeapon">PISTOL</span></div>
    </div>

    <div class="top-right-hud">
        <div class="hud-line"><span class="hud-label">KILLS:</span> <span class="hud-value" id="hudKills">0</span></div>
        <div class="hud-line"><span class="hud-label">WAVE:</span> <span class="hud-value" id="hudWave">1</span></div>
        <div class="hud-line"><span class="hud-label">WANTED:</span> <span class="hud-value" id="hudWanted">☆☆☆☆☆</span></div>
        <div class="hud-line"><span class="hud-label">SCORE:</span> <span class="hud-value" id="hudScore">0</span></div>
    </div>

    <div class="bottom-hud">
        <div style="color: #ffff00;">CONTROLS: WASD=Move | Mouse=Aim | Click=Shoot | 1/2/3=Weapons | E=Vehicle | ESC=Pause</div>
    </div>

    <script>
        const gameInstance = {
            // Canvas
            canvas: null,
            ctx: null,
            width: 0,
            height: 0,

            // Game State
            gameState: 'menu', // menu, playing, paused, gameover
            running: false,
            startTime: 0,
            
            // World
            worldWidth: 4000,
            worldHeight: 3000,
            cameraX: 0,
            cameraY: 0,

            // Player
            player: {
                x: 2000,
                y: 1500,
                width: 30,
                height: 30,
                speedX: 0,
                speedY: 0,
                speed: 6,
                angle: 0,
                health: 100,
                maxHealth: 100,
                money: 0,
                kills: 0,
                wanted: 0,
                weapon: 'pistol',
                ammo: 30,
                maxAmmo: 30,
                inVehicle: false,
                shotsFired: 0,
                shotsHit: 0,
                lastShot: 0,
                mouseX: 0,
                mouseY: 0
            },

            // Game Arrays
            bullets: [],
            npcs: [],
            vehicles: [],
            pickups: [],
            particles: [],

            // Input
            keys: {},
            mouse: { x: 0, y: 0, down: false },

            // Game Variables
            wave: 1,
            waveEnemies: 10,
            enemiesSpawned: 0,
            score: 0,
            gameSpeed: 1,

            // Initialize Game
            init() {
                this.canvas = document.getElementById('gameCanvas');
                this.ctx = this.canvas.getContext('2d', { alpha: false });
                
                // Set canvas resolution
                this.width = window.innerWidth * (window.devicePixelRatio || 1);
                this.height = window.innerHeight * (window.devicePixelRatio || 1);
                
                this.canvas.width = this.width;
                this.canvas.height = this.height;
                
                // Set display size
                this.canvas.style.width = window.innerWidth + 'px';
                this.canvas.style.height = window.innerHeight + 'px';

                this.setupEventListeners();
                this.spawnInitialEntities();
                this.gameLoop();
            },

            setupEventListeners() {
                document.addEventListener('keydown', (e) => {
                    this.keys[e.key.toLowerCase()] = true;
                    
                    if (e.key === ' ') {
                        e.preventDefault();
                        if (this.gameState === 'menu') this.startGame();
                    }
                    
                    if (e.key === 'Escape') {
                        e.preventDefault();
                        this.togglePause();
                    }
                    
                    if (e.key === '1') this.player.weapon = 'pistol';
                    if (e.key === '2') this.player.weapon = 'rifle';
                    if (e.key === '3') this.player.weapon = 'shotgun';
                    
                    if (e.key.toLowerCase() === 'e') this.toggleVehicle();
                });

                document.addEventListener('keyup', (e) => {
                    this.keys[e.key.toLowerCase()] = false;
                });

                document.addEventListener('mousemove', (e) => {
                    const rect = this.canvas.getBoundingClientRect();
                    this.mouse.x = (e.clientX - rect.left) * (this.width / rect.width);
                    this.mouse.y = (e.clientY - rect.top) * (this.height / rect.height);
                    
                    this.player.mouseX = this.mouse.x + this.cameraX;
                    this.player.mouseY = this.mouse.y + this.cameraY;
                    
                    const dx = this.player.mouseX - this.player.x;
                    const dy = this.player.mouseY - this.player.y;
                    this.player.angle = Math.atan2(dy, dx);
                });

                document.addEventListener('click', () => {
                    if (this.gameState === 'playing') {
                        this.shoot();
                    }
                });

                window.addEventListener('resize', () => {
                    this.width = window.innerWidth * (window.devicePixelRatio || 1);
                    this.height = window.innerHeight * (window.devicePixelRatio || 1);
                    this.canvas.width = this.width;
                    this.canvas.height = this.height;
                    this.canvas.style.width = window.innerWidth + 'px';
                    this.canvas.style.height = window.innerHeight + 'px';
                });
            },

            spawnInitialEntities() {
                // Spawn enemies
                for (let i = 0; i < 20; i++) {
                    this.npcs.push(this.createNPC());
                }

                // Spawn vehicles
                for (let i = 0; i < 8; i++) {
                    this.vehicles.push(this.createVehicle());
                }

                // Spawn pickups
                for (let i = 0; i < 15; i++) {
                    this.pickups.push(this.createPickup());
                }
            },

            createNPC() {
                return {
                    x: Math.random() * this.worldWidth,
                    y: Math.random() * this.worldHeight,
                    width: 28,
                    height: 28,
                    health: 30,
                    maxHealth: 30,
                    speedX: 0,
                    speedY: 0,
                    speed: 3,
                    angle: Math.random() * Math.PI * 2,
                    moveTimer: 0,
                    moveInterval: 120,
                    color: '#FF00FF'
                };
            },

            createVehicle() {
                const types = ['car', 'truck', 'bike'];
                const type = types[Math.floor(Math.random() * types.length)];
                let width = 50, height = 30, color = '#FF3333', speed = 7;

                if (type === 'truck') {
                    width = 70; height = 40; color = '#FFA500'; speed = 5;
                } else if (type === 'bike') {
                    width = 40; height = 24; color = '#00FFFF'; speed = 9;
                }

                return {
                    x: Math.random() * this.worldWidth,
                    y: Math.random() * this.worldHeight,
                    width: width,
                    height: height,
                    health: 100,
                    maxHealth: 100,
                    speedX: 0,
                    speedY: 0,
                    speed: speed,
                    angle: Math.random() * Math.PI * 2,
                    type: type,
                    color: color,
                    moveTimer: 0
                };
            },

            createPickup() {
                return {
                    x: Math.random() * this.worldWidth,
                    y: Math.random() * this.worldHeight,
                    type: Math.random() > 0.5 ? 'health' : 'ammo',
                    size: 12
                };
            },

            startGame() {
                this.gameState = 'playing';
                this.running = true;
                this.startTime = Date.now();
                document.getElementById('menuOverlay').classList.add('hidden');
            },

            togglePause() {
                if (this.gameState === 'playing') {
                    this.gameState = 'paused';
                    document.getElementById('pauseOverlay').classList.remove('hidden');
                } else if (this.gameState === 'paused') {
                    this.gameState = 'playing';
                    document.getElementById('pauseOverlay').classList.add('hidden');
                }
            },

            toggleVehicle() {
                if (this.gameState !== 'playing') return;

                if (!this.player.inVehicle) {
                    for (let v of this.vehicles) {
                        const dist = Math.hypot(this.player.x - v.x, this.player.y - v.y);
                        if (dist < 50) {
                            this.player.inVehicle = true;
                            return;
                        }
                    }
                } else {
                    this.player.inVehicle = false;
                }
            },

            shoot() {
                if (this.gameState !== 'playing') return;

                const now = Date.now();
                const fireRates = { pistol: 100, rifle: 150, shotgun: 300 };
                const damages = { pistol: 15, rifle: 30, shotgun: 50 };

                if (now - this.player.lastShot < fireRates[this.player.weapon]) return;
                if (this.player.ammo <= 0) return;

                const bulletCount = this.player.weapon === 'shotgun' ? 5 : 1;
                const damage = damages[this.player.weapon];

                for (let i = 0; i < bulletCount; i++) {
                    let angle = this.player.angle;
                    if (this.player.weapon === 'shotgun') {
                        angle += (Math.random() - 0.5) * 0.8;
                    }

                    this.bullets.push({
                        x: this.player.x + Math.cos(angle) * 20,
                        y: this.player.y + Math.sin(angle) * 20,
                        angle: angle,
                        speed: 14,
                        damage: damage,
                        lifetime: 3000,
                        age: 0
                    });
                }

                this.player.ammo--;
                this.player.lastShot = now;
                this.player.shotsFired++;
            },

            update() {
                if (this.gameState !== 'playing') return;

                // Update player movement
                this.player.speedX = 0;
                this.player.speedY = 0;

                if (this.keys['w'] || this.keys['arrowup']) this.player.speedY = -this.player.speed;
                if (this.keys['s'] || this.keys['arrowdown']) this.player.speedY = this.player.speed;
                if (this.keys['a'] || this.keys['arrowleft']) this.player.speedX = -this.player.speed;
                if (this.keys['d'] || this.keys['arrowright']) this.player.speedX = this.player.speed;

                if (this.player.inVehicle) {
                    this.player.speedX *= 1.5;
                    this.player.speedY *= 1.5;
                }

                this.player.x += this.player.speedX;
                this.player.y += this.player.speedY;

                // Keep player in world
                this.player.x = Math.max(0, Math.min(this.player.x, this.worldWidth));
                this.player.y = Math.max(0, Math.min(this.player.y, this.worldHeight));

                // Update camera
                this.cameraX = this.player.x - this.width / 2;
                this.cameraY = this.player.y - this.height / 2;
                this.cameraX = Math.max(0, Math.min(this.cameraX, this.worldWidth - this.width));
                this.cameraY = Math.max(0, Math.min(this.cameraY, this.worldHeight - this.height));

                // Update bullets
                for (let i = this.bullets.length - 1; i >= 0; i--) {
                    const b = this.bullets[i];
                    b.x += Math.cos(b.angle) * b.speed;
                    b.y += Math.sin(b.angle) * b.speed;
                    b.age++;

                    if (b.age > b.lifetime || b.x < 0 || b.x > this.worldWidth || b.y < 0 || b.y > this.worldHeight) {
                        this.bullets.splice(i, 1);
                        continue;
                    }

                    // Check collision with NPCs
                    for (let j = this.npcs.length - 1; j >= 0; j--) {
                        const npc = this.npcs[j];
                        const dist = Math.hypot(b.x - npc.x, b.y - npc.y);
                        if (dist < 20) {
                            npc.health -= b.damage;
                            this.player.shotsHit++;
                            this.score += 10;

                            if (npc.health <= 0) {
                                this.player.money += 100;
                                this.player.kills++;
                                this.player.wanted += 0.5;
                                this.score += 500;

                                // Create explosion particles
                                for (let k = 0; k < 8; k++) {
                                    this.particles.push({
                                        x: npc.x,
                                        y: npc.y,
                                        vx: (Math.random() - 0.5) * 8,
                                        vy: (Math.random() - 0.5) * 8,
                                        life: 30,
                                        maxLife: 30,
                                        color: '#FF6600'
                                    });
                                }

                                this.npcs.splice(j, 1);

                                // Spawn pickup
                                if (Math.random() > 0.5) {
                                    this.pickups.push({
                                        x: npc.x,
                                        y: npc.y,
                                        type: Math.random() > 0.6 ? 'ammo' : 'health',
                                        size: 12
                                    });
                                }
                            }

                            this.bullets.splice(i, 1);
                            break;
                        }
                    }
                }

                // Update NPCs
                for (let npc of this.npcs) {
                    npc.moveTimer++;
                    if (npc.moveTimer > npc.moveInterval) {
                        npc.angle = Math.random() * Math.PI * 2;
                        npc.moveTimer = 0;
                    }

                    npc.x += Math.cos(npc.angle) * npc.speed;
                    npc.y += Math.sin(npc.angle) * npc.speed;

                    // Keep in world
                    npc.x = Math.max(0, Math.min(npc.x, this.worldWidth));
                    npc.y = Math.max(0, Math.min(npc.y, this.worldHeight));

                    // Collision with player
                    const dist = Math.hypot(this.player.x - npc.x, this.player.y - npc.y);
                    if (dist < 40) {
                        this.player.health -= 0.5;
                        this.player.wanted += 0.1;
                    }
                }

                // Update vehicles
                for (let v of this.vehicles) {
                    v.moveTimer++;
                    if (v.moveTimer > 150) {
                        v.angle = Math.random() * Math.PI * 2;
                        v.moveTimer = 0;
                    }

                    v.x += Math.cos(v.angle) * v.speed;
                    v.y += Math.sin(v.angle) * v.speed;

                    v.x = Math.max(0, Math.min(v.x, this.worldWidth));
                    v.y = Math.max(0, Math.min(v.y, this.worldHeight));
                }

                // Update pickups
                for (let i = this.pickups.length - 1; i >= 0; i--) {
                    const p = this.pickups[i];
                    const dist = Math.hypot(this.player.x - p.x, this.player.y - p.y);
                    if (dist < 40) {
                        if (p.type === 'health') {
                            this.player.health = Math.min(this.player.health + 30, this.player.maxHealth);
                        } else {
                            this.player.ammo = Math.min(this.player.ammo + 50, this.player.maxAmmo);
                        }
                        this.pickups.splice(i, 1);
                    }
                }

                // Update particles
                for (let i = this.particles.length - 1; i >= 0; i--) {
                    const p = this.particles[i];
                    p.x += p.vx;
                    p.y += p.vy;
                    p.life--;
                    if (p.life <= 0) this.particles.splice(i, 1);
                }

                // Spawn more enemies if needed
                if (this.npcs.length < 10 + this.wave * 5) {
                    this.npcs.push(this.createNPC());
                }

                // Spawn pickups
                if (this.pickups.length < 10) {
                    this.pickups.push(this.createPickup());
                }

                // Game over condition
                if (this.player.health <= 0) {
                    this.endGame();
                }

                // Wave progression
                if (this.player.kills > this.wave * 20) {
                    this.wave++;
                }
            },

            draw() {
                // Clear canvas
                this.ctx.fillStyle = '#0a0a0a';
                this.ctx.fillRect(0, 0, this.width, this.height);

                // Draw world background
                this.ctx.fillStyle = '#1a1a3a';
                this.ctx.fillRect(-this.cameraX, -this.cameraY, this.worldWidth, this.worldHeight);

                // Draw grid
                this.ctx.strokeStyle = '#003300';
                this.ctx.lineWidth = 1;
                for (let x = 0; x < this.worldWidth; x += 200) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(x - this.cameraX, -this.cameraY);
                    this.ctx.lineTo(x - this.cameraX, this.worldHeight - this.cameraY);
                    this.ctx.stroke();
                }
                for (let y = 0; y < this.worldHeight; y += 200) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(-this.cameraX, y - this.cameraY);
                    this.ctx.lineTo(this.worldWidth - this.cameraX, y - this.cameraY);
                    this.ctx.stroke();
                }

                // Draw buildings
                this.ctx.fillStyle = '#444444';
                for (let x = 0; x < this.worldWidth; x += 400) {
                    for (let y = 0; y < this.worldHeight; y += 400) {
                        if (Math.hypot(x - this.player.x, y - this.player.y) < 2000) {
                            this.ctx.fillRect(x - this.cameraX, y - this.cameraY, 300, 300);
                            this.ctx.strokeStyle = '#888888';
                            this.ctx.lineWidth = 3;
                            this.ctx.strokeRect(x - this.cameraX, y - this.cameraY, 300, 300);
                        }
                    }
                }

                // Draw vehicles
                for (let v of this.vehicles) {
                    const sx = v.x - this.cameraX;
                    const sy = v.y - this.cameraY;
                    this.ctx.fillStyle = v.color;
                    this.ctx.save();
                    this.ctx.translate(sx, sy);
                    this.ctx.rotate(v.angle);
                    this.ctx.fillRect(-v.width / 2, -v.height / 2, v.width, v.height);
                    this.ctx.restore();
                    this.ctx.strokeStyle = '#FFFFFF';
                    this.ctx.lineWidth = 2;
                    this.ctx.strokeRect(sx - v.width / 2, sy - v.height / 2, v.width, v.height);
                }

                // Draw NPCs
                for (let npc of this.npcs) {
                    const sx = npc.x - this.cameraX;
                    const sy = npc.y - this.cameraY;
                    this.ctx.fillStyle = npc.color;
                    this.ctx.fillRect(sx - npc.width / 2, sy - npc.height / 2, npc.width, npc.height);
                    
                    // Health bar
                    this.ctx.fillStyle = '#FF0000';
                    this.ctx.fillRect(sx - 15, sy - 20, 30, 3);
                    this.ctx.fillStyle = '#00FF00';
                    this.ctx.fillRect(sx - 15, sy - 20, (npc.health / npc.maxHealth) * 30, 3);
                }

                // Draw pickups
                for (let p of this.pickups) {
                    const sx = p.x - this.cameraX;
                    const sy = p.y - this.cameraY;
                    this.ctx.fillStyle = p.type === 'health' ? '#00FF00' : '#FFFF00';
                    this.ctx.beginPath();
                    this.ctx.arc(sx, sy, p.size, 0, Math.PI * 2);
                    this.ctx.fill();
                    this.ctx.strokeStyle = '#FFFFFF';
                    this.ctx.lineWidth = 2;
                    this.ctx.stroke();
                }

                // Draw bullets
                for (let b of this.bullets) {
                    const sx = b.x - this.cameraX;
                    const sy = b.y - this.cameraY;
                    this.ctx.fillStyle = '#FFFF00';
                    this.ctx.beginPath();
                    this.ctx.arc(sx, sy, 5, 0, Math.PI * 2);
                    this.ctx.fill();
                }

                // Draw particles
                for (let p of this.particles) {
                    const sx = p.x - this.cameraX;
                    const sy = p.y - this.cameraY;
                    const alpha = p.life / p.maxLife;
                    this.ctx.fillStyle = p.color;
                    this.ctx.globalAlpha = alpha;
                    this.ctx.beginPath();
                    this.ctx.arc(sx, sy, 5, 0, Math.PI * 2);
                    this.ctx.fill();
                    this.ctx.globalAlpha = 1;
                }

                // Draw player
                const px = this.player.x - this.cameraX;
                const py = this.player.y - this.cameraY;
                this.ctx.fillStyle = '#00FF00';
                this.ctx.fillRect(px - this.player.width / 2, py - this.player.height / 2, this.player.width, this.player.height);

                // Draw aiming line
                this.ctx.strokeStyle = '#00FFFF';
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.moveTo(px, py);
                this.ctx.lineTo(
                    px + Math.cos(this.player.angle) * 60,
                    py + Math.sin(this.player.angle) * 60
                );
                this.ctx.stroke();

                // Draw health bar
                this.ctx.fillStyle = '#FF0000';
                this.ctx.fillRect(px - 25, py - 35, 50, 4);
                this.ctx.fillStyle = '#00FF00';
                this.ctx.fillRect(px - 25, py - 35, (this.player.health / this.player.maxHealth) * 50, 4);
            },

            updateHUD() {
                document.getElementById('hudHealth').textContent = Math.floor(this.player.health);
                document.getElementById('hudMoney').textContent = this.player.money;
                document.getElementById('hudAmmo').textContent = this.player.ammo;
                document.getElementById('hudMaxAmmo').textContent = this.player.maxAmmo;
                document.getElementById('hudWeapon').textContent = this.player.weapon.toUpperCase();
                document.getElementById('hudKills').textContent = this.player.kills;
                document.getElementById('hudWave').textContent = this.wave;
                
                const stars = '★'.repeat(Math.min(5, Math.floor(this.player.wanted))) + 
                             '☆'.repeat(Math.max(0, 5 - Math.floor(this.player.wanted)));
                document.getElementById('hudWanted').textContent = stars;
                
                document.getElementById('hudScore').textContent = this.score;
            },

            endGame() {
                this.gameState = 'gameover';
                this.running = false;
                
                const survivalTime = Math.floor((Date.now() - this.startTime) / 1000);
                const accuracy = this.player.shotsFired > 0 ? 
                    Math.floor((this.player.shotsHit / this.player.shotsFired) * 100) : 0;
                
                document.getElementById('finalMoney').textContent = this.player.money;
                document.getElementById('finalKills').textContent = this.player.kills;
                document.getElementById('finalAccuracy').textContent = accuracy;
                document.getElementById('finalTime').textContent = survivalTime;
                document.getElementById('finalWave').textContent = this.wave;
                
                document.getElementById('gameOverOverlay').classList.remove('hidden');
            },

            gameLoop() {
                this.update();
                this.draw();
                this.updateHUD();
                requestAnimationFrame(() => this.gameLoop());
            }
        };

        // Start game when page loads
        window.addEventListener('load', () => {
            gameInstance.init();
        });
    </script>
</body>
</html>
"""

def get_html_content():
    """Returns the HTML content for the Mini GTA web game"""
    return HTML_CONTENT

def serve_minigta(port=8001):
    """
    Serve the Mini GTA game on a local server
    Requires http.server (built-in Python module)
    """
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class MiniGTAHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(HTML_CONTENT.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            """Suppress default logging"""
            pass
    
    server = HTTPServer(('localhost', port), MiniGTAHandler)
    print(f"Mini GTA server running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    server.serve_forever()

if __name__ == "__main__":
    # Serve the Mini GTA game
    serve_minigta(port=8001)
