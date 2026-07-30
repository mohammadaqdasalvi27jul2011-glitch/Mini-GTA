#!/usr/bin/env python3
"""
Mini GTA - Complete Python Implementation
100% Pure Python - Game Engine + Web Server + All UI
No external files needed - Everything generated dynamically
"""

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import threading
import webbrowser
from datetime import datetime
import base64


# Game JavaScript embedded as Python string
GAME_JS = """
'use strict';

const gameInstance = {
    canvas: null,
    ctx: null,
    width: 0,
    height: 0,
    gameState: 'menu',
    running: false,
    startTime: 0,
    worldWidth: 4000,
    worldHeight: 3000,
    cameraX: 0,
    cameraY: 0,
    
    player: {
        x: 2000, y: 1500, width: 30, height: 30,
        speedX: 0, speedY: 0, speed: 6, angle: 0,
        health: 100, maxHealth: 100, money: 0, kills: 0,
        wanted: 0, weapon: 'pistol', ammo: 30, maxAmmo: 30,
        inVehicle: false, shotsFired: 0, shotsHit: 0,
        lastShot: 0, mouseX: 0, mouseY: 0
    },
    
    bullets: [],
    npcs: [],
    vehicles: [],
    pickups: [],
    particles: [],
    keys: {},
    mouse: { x: 0, y: 0, down: false },
    wave: 1,
    score: 0,

    init() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        
        this.setupEvents();
        this.spawnEntities();
        this.gameLoop();
    },

    setupEvents() {
        const self = this;
        
        document.addEventListener('keydown', (e) => {
            self.keys[e.key.toLowerCase()] = true;
            if (e.key === ' ') { e.preventDefault(); if (self.gameState === 'menu') self.startGame(); }
            if (e.key === 'Escape') { e.preventDefault(); self.togglePause(); }
            if (e.key === '1') self.player.weapon = 'pistol';
            if (e.key === '2') self.player.weapon = 'rifle';
            if (e.key === '3') self.player.weapon = 'shotgun';
            if (e.key.toLowerCase() === 'e') self.toggleVehicle();
        });

        document.addEventListener('keyup', (e) => { self.keys[e.key.toLowerCase()] = false; });
        
        document.addEventListener('mousemove', (e) => {
            const rect = self.canvas.getBoundingClientRect();
            self.mouse.x = e.clientX - rect.left;
            self.mouse.y = e.clientY - rect.top;
            self.player.mouseX = self.mouse.x + self.cameraX;
            self.player.mouseY = self.mouse.y + self.cameraY;
            self.player.angle = Math.atan2(self.player.mouseY - self.player.y, self.player.mouseX - self.player.x);
        });

        document.addEventListener('click', () => { if (self.gameState === 'playing') self.shoot(); });
        
        window.addEventListener('resize', () => {
            self.width = window.innerWidth;
            self.height = window.innerHeight;
            self.canvas.width = self.width;
            self.canvas.height = self.height;
        });
    },

    spawnEntities() {
        for (let i = 0; i < 15; i++) this.npcs.push(this.createNPC());
        for (let i = 0; i < 6; i++) this.vehicles.push(this.createVehicle());
        for (let i = 0; i < 10; i++) this.pickups.push(this.createPickup());
    },

    createNPC() {
        return {
            x: Math.random() * this.worldWidth, y: Math.random() * this.worldHeight,
            width: 28, height: 28, health: 30, maxHealth: 30,
            speed: 3, angle: Math.random() * Math.PI * 2,
            moveTimer: 0, moveInterval: 120, color: '#FF00FF'
        };
    },

    createVehicle() {
        const types = ['car', 'truck', 'bike'];
        const type = types[Math.floor(Math.random() * 3)];
        let w = 50, h = 30, c = '#FF3333', s = 7;
        if (type === 'truck') { w = 70; h = 40; c = '#FFA500'; s = 5; }
        else if (type === 'bike') { w = 40; h = 24; c = '#00FFFF'; s = 9; }
        return { x: Math.random() * this.worldWidth, y: Math.random() * this.worldHeight,
            width: w, height: h, health: 100, maxHealth: 100, speed: s,
            angle: Math.random() * Math.PI * 2, type: type, color: c, moveTimer: 0 };
    },

    createPickup() {
        return { x: Math.random() * this.worldWidth, y: Math.random() * this.worldHeight,
            type: Math.random() > 0.5 ? 'health' : 'ammo', size: 12,
            lifetime: 300, age: 0 };
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
                if (Math.hypot(this.player.x - v.x, this.player.y - v.y) < 50) {
                    this.player.inVehicle = true; return;
                }
            }
        } else { this.player.inVehicle = false; }
    },

    shoot() {
        const now = Date.now();
        const fireRates = { pistol: 100, rifle: 150, shotgun: 300 };
        const damages = { pistol: 15, rifle: 30, shotgun: 50 };
        
        if (now - this.player.lastShot < fireRates[this.player.weapon]) return;
        if (this.player.ammo <= 0) return;

        const count = this.player.weapon === 'shotgun' ? 5 : 1;
        const dmg = damages[this.player.weapon];

        for (let i = 0; i < count; i++) {
            let angle = this.player.angle;
            if (this.player.weapon === 'shotgun') angle += (Math.random() - 0.5) * 0.8;
            
            this.bullets.push({
                x: this.player.x + Math.cos(angle) * 20,
                y: this.player.y + Math.sin(angle) * 20,
                angle: angle, speed: 14, damage: dmg, lifetime: 3000, age: 0
            });
        }
        
        this.player.ammo--;
        this.player.lastShot = now;
        this.player.shotsFired++;
    },

    update() {
        if (this.gameState !== 'playing') return;

        this.player.speedX = 0;
        this.player.speedY = 0;

        if (this.keys['w'] || this.keys['arrowup']) this.player.speedY = -this.player.speed;
        if (this.keys['s'] || this.keys['arrowdown']) this.player.speedY = this.player.speed;
        if (this.keys['a'] || this.keys['arrowleft']) this.player.speedX = -this.player.speed;
        if (this.keys['d'] || this.keys['arrowright']) this.player.speedX = this.player.speed;

        if (this.player.inVehicle) { this.player.speedX *= 1.5; this.player.speedY *= 1.5; }

        this.player.x += this.player.speedX;
        this.player.y += this.player.speedY;
        this.player.x = Math.max(0, Math.min(this.player.x, this.worldWidth));
        this.player.y = Math.max(0, Math.min(this.player.y, this.worldHeight));

        this.cameraX = this.player.x - this.width / 2;
        this.cameraY = this.player.y - this.height / 2;
        this.cameraX = Math.max(0, Math.min(this.cameraX, this.worldWidth - this.width));
        this.cameraY = Math.max(0, Math.min(this.cameraY, this.worldHeight - this.height));

        for (let i = this.bullets.length - 1; i >= 0; i--) {
            const b = this.bullets[i];
            b.x += Math.cos(b.angle) * b.speed;
            b.y += Math.sin(b.angle) * b.speed;
            b.age++;

            if (b.age > b.lifetime || b.x < 0 || b.x > this.worldWidth || b.y < 0 || b.y > this.worldHeight) {
                this.bullets.splice(i, 1); continue;
            }

            for (let j = this.npcs.length - 1; j >= 0; j--) {
                const npc = this.npcs[j];
                if (Math.hypot(b.x - npc.x, b.y - npc.y) < 20) {
                    npc.health -= b.damage;
                    this.player.shotsHit++;
                    this.score += 10;

                    if (npc.health <= 0) {
                        this.player.money += 100;
                        this.player.kills++;
                        this.player.wanted += 0.5;
                        this.score += 500;

                        for (let k = 0; k < 8; k++) {
                            this.particles.push({
                                x: npc.x, y: npc.y,
                                vx: (Math.random() - 0.5) * 8,
                                vy: (Math.random() - 0.5) * 8,
                                life: 30, maxLife: 30, color: '#FF6600'
                            });
                        }

                        this.npcs.splice(j, 1);

                        if (Math.random() > 0.5) {
                            this.pickups.push({
                                x: npc.x, y: npc.y,
                                type: Math.random() > 0.6 ? 'ammo' : 'health',
                                size: 12, lifetime: 300, age: 0
                            });
                        }
                    }

                    this.bullets.splice(i, 1); break;
                }
            }
        }

        for (let npc of this.npcs) {
            npc.moveTimer++;
            if (npc.moveTimer > npc.moveInterval) {
                npc.angle = Math.random() * Math.PI * 2;
                npc.moveTimer = 0;
            }
            npc.x += Math.cos(npc.angle) * npc.speed;
            npc.y += Math.sin(npc.angle) * npc.speed;
            npc.x = Math.max(0, Math.min(npc.x, this.worldWidth));
            npc.y = Math.max(0, Math.min(npc.y, this.worldHeight));

            if (Math.hypot(this.player.x - npc.x, this.player.y - npc.y) < 40) {
                this.player.health -= 0.3;
                this.player.wanted += 0.05;
            }
        }

        for (let v of this.vehicles) {
            v.moveTimer++;
            if (v.moveTimer > 150) { v.angle = Math.random() * Math.PI * 2; v.moveTimer = 0; }
            v.x += Math.cos(v.angle) * v.speed;
            v.y += Math.sin(v.angle) * v.speed;
            v.x = Math.max(0, Math.min(v.x, this.worldWidth));
            v.y = Math.max(0, Math.min(v.y, this.worldHeight));
        }

        for (let i = this.pickups.length - 1; i >= 0; i--) {
            const p = this.pickups[i];
            p.age++;
            if (p.age > p.lifetime) { this.pickups.splice(i, 1); continue; }
            if (Math.hypot(this.player.x - p.x, this.player.y - p.y) < 40) {
                if (p.type === 'health') this.player.health = Math.min(this.player.health + 30, this.player.maxHealth);
                else this.player.ammo = Math.min(this.player.ammo + 50, this.player.maxAmmo);
                this.pickups.splice(i, 1);
            }
        }

        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx; p.y += p.vy; p.life--;
            if (p.life <= 0) this.particles.splice(i, 1);
        }

        if (this.npcs.length < 10 + this.wave * 3) this.npcs.push(this.createNPC());
        if (this.pickups.length < 8) this.pickups.push(this.createPickup());

        if (this.player.health <= 0) this.endGame();
        if (this.player.kills > this.wave * 15) this.wave++;
    },

    draw() {
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.ctx.fillStyle = '#1a1a3a';
        this.ctx.fillRect(-this.cameraX, -this.cameraY, this.worldWidth, this.worldHeight);
        
        this.ctx.strokeStyle = '#003300';
        this.ctx.lineWidth = 1;
        for (let x = 0; x < this.worldWidth; x += 200) {
            this.ctx.beginPath();
            this.ctx.moveTo(x - this.cameraX, -this.cameraY);
            this.ctx.lineTo(x - this.cameraX, this.worldHeight - this.cameraY);
            this.ctx.stroke();
        }
        
        this.ctx.fillStyle = '#444444';
        for (let x = 0; x < this.worldWidth; x += 400) {
            for (let y = 0; y < this.worldHeight; y += 400) {
                if (Math.hypot(x - this.player.x, y - this.player.y) < 2000) {
                    this.ctx.fillRect(x - this.cameraX, y - this.cameraY, 300, 300);
                }
            }
        }

        for (let v of this.vehicles) {
            const sx = v.x - this.cameraX, sy = v.y - this.cameraY;
            this.ctx.fillStyle = v.color;
            this.ctx.save();
            this.ctx.translate(sx, sy);
            this.ctx.rotate(v.angle);
            this.ctx.fillRect(-v.width / 2, -v.height / 2, v.width, v.height);
            this.ctx.restore();
        }

        for (let npc of this.npcs) {
            const sx = npc.x - this.cameraX, sy = npc.y - this.cameraY;
            this.ctx.fillStyle = npc.color;
            this.ctx.fillRect(sx - npc.width / 2, sy - npc.height / 2, npc.width, npc.height);
            this.ctx.fillStyle = '#FF0000';
            this.ctx.fillRect(sx - 15, sy - 20, 30, 3);
            this.ctx.fillStyle = '#00FF00';
            this.ctx.fillRect(sx - 15, sy - 20, (npc.health / npc.maxHealth) * 30, 3);
        }

        for (let p of this.pickups) {
            const sx = p.x - this.cameraX, sy = p.y - this.cameraY;
            this.ctx.fillStyle = p.type === 'health' ? '#00FF00' : '#FFFF00';
            this.ctx.beginPath();
            this.ctx.arc(sx, sy, p.size, 0, Math.PI * 2);
            this.ctx.fill();
        }

        for (let b of this.bullets) {
            const sx = b.x - this.cameraX, sy = b.y - this.cameraY;
            this.ctx.fillStyle = '#FFFF00';
            this.ctx.beginPath();
            this.ctx.arc(sx, sy, 5, 0, Math.PI * 2);
            this.ctx.fill();
        }

        for (let p of this.particles) {
            const sx = p.x - this.cameraX, sy = p.y - this.cameraY;
            const alpha = p.life / p.maxLife;
            this.ctx.fillStyle = p.color;
            this.ctx.globalAlpha = alpha;
            this.ctx.beginPath();
            this.ctx.arc(sx, sy, 5, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.globalAlpha = 1;
        }

        const px = this.player.x - this.cameraX, py = this.player.y - this.cameraY;
        this.ctx.fillStyle = '#00FF00';
        this.ctx.fillRect(px - this.player.width / 2, py - this.player.height / 2, this.player.width, this.player.height);
        
        this.ctx.strokeStyle = '#00FFFF';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(px, py);
        this.ctx.lineTo(px + Math.cos(this.player.angle) * 60, py + Math.sin(this.player.angle) * 60);
        this.ctx.stroke();
    },

    updateHUD() {
        document.getElementById('health').textContent = Math.max(0, Math.floor(this.player.health));
        document.getElementById('money').textContent = this.player.money;
        document.getElementById('ammo').textContent = Math.max(0, this.player.ammo);
        document.getElementById('weapon').textContent = this.player.weapon.toUpperCase();
        document.getElementById('kills').textContent = this.player.kills;
        document.getElementById('wave').textContent = this.wave;
        document.getElementById('score').textContent = this.score;
        
        const stars = '★'.repeat(Math.min(5, Math.floor(this.player.wanted))) + 
                     '☆'.repeat(Math.max(0, 5 - Math.floor(this.player.wanted)));
        document.getElementById('wanted').textContent = stars;
    },

    endGame() {
        this.gameState = 'gameover';
        const time = Math.floor((Date.now() - this.startTime) / 1000);
        const acc = this.player.shotsFired > 0 ? Math.floor((this.player.shotsHit / this.player.shotsFired) * 100) : 0;
        
        document.getElementById('finalMoney').textContent = this.player.money;
        document.getElementById('finalKills').textContent = this.player.kills;
        document.getElementById('finalAccuracy').textContent = acc;
        document.getElementById('finalTime').textContent = time;
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

window.addEventListener('load', () => gameInstance.init());
"""


class GameServerHandler(BaseHTTPRequestHandler):
    """HTTP Handler - Everything generated in Python"""

    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

    def do_GET(self):
        try:
            path = urlparse(self.path).path
            
            if path == '/' or path == '/index.html':
                self.serve_home()
            elif path == '/game':
                self.serve_game()
            elif path == '/clock':
                self.serve_clock()
            elif path == '/info':
                self.serve_info()
            elif path == '/api/status':
                self.serve_status()
            else:
                self.serve_404()
        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500)

    def serve_home(self):
        html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mini GTA - Game Hub</title><style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);color:#00ff00;min-height:100vh;padding:20px;display:flex;justify-content:center;align-items:center}
.container{max-width:1000px;width:100%}.header{text-align:center;margin-bottom:50px}h1{font-size:4rem;color:#ff0000;text-shadow:0 0 20px #ff0000;margin-bottom:20px}
.subtitle{font-size:1.2rem;color:#ffff00}.games-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:30px;margin-bottom:40px}
.game-card{background:rgba(15,52,96,0.8);border:2px solid #00d4ff;border-radius:15px;padding:30px;text-align:center;transition:all 0.3s}
.game-card:hover{transform:translateY(-10px);box-shadow:0 0 30px #00d4ff}.game-card h2{font-size:2rem;margin-bottom:15px;color:#00ff00}
.game-card p{color:#aaa;margin-bottom:20px;line-height:1.6}.btn{display:inline-block;background:linear-gradient(135deg,#00d4ff,#00ff00);color:#000;padding:12px 30px;border-radius:5px;text-decoration:none;font-weight:bold;border:none;cursor:pointer;font-size:1rem;transition:all 0.3s}
.btn:hover{transform:scale(1.05);box-shadow:0 0 20px #00ff00}.features{background:rgba(15,52,96,0.8);border:2px solid #00d4ff;border-radius:15px;padding:30px;margin-top:30px}
.features h3{color:#ffff00;margin-bottom:20px;font-size:1.5rem}.features ul{list-style:none;columns:2}.features li{color:#00ff00;padding:8px 0;border-bottom:1px solid #00d4ff}
</style></head><body><div class="container"><div class="header"><h1>🎮 MINI GTA</h1><p class="subtitle">Complete Game Suite - 100% Python</p></div>
<div class="games-grid"><div class="game-card"><h2>🎮 Mini GTA Game</h2><p>Open-world action game with combat, vehicles & missions</p><a href="/game" class="btn">PLAY NOW</a></div>
<div class="game-card"><h2>🕐 World Clock</h2><p>Real-time digital clock with multiple time zones</p><a href="/clock" class="btn">OPEN CLOCK</a></div>
<div class="game-card"><h2>📋 Game Info</h2><p>Learn about Mini GTA features & controls</p><a href="/info" class="btn">READ MORE</a></div></div>
<div class="features"><h3>⭐ Features</h3><ul><li>🎯 Advanced Combat System</li><li>🚗 Vehicle Mechanics</li><li>👥 AI NPCs & Police</li><li>💰 Money & Score System</li><li>🌍 Large Open World</li><li>🎪 Dynamic Wave System</li><li>🕐 Multi-timezone Clock</li><li>📊 Real-time Statistics</li></ul></div></div></body></html>"""
        self._send_html(html)

    def serve_game(self):
        html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Mini GTA - Game</title>
<style>*{{margin:0;padding:0;box-sizing:border-box;user-select:none}}html,body{{width:100%;height:100%;overflow:hidden}}
body{{font-family:Arial;background:#000;color:#00ff00}}#gameCanvas{{display:block;width:100%;height:100%;background:#0a0a0a}}
.overlay{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1000}}
.overlay.hidden{{display:none}}.overlay-content{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;background:rgba(0,0,0,0.9);border:3px solid;padding:40px;border-radius:10px}}
#menuOverlay .overlay-content{{border-color:#00ff00;background:rgba(0,20,0,0.9)}}#menuOverlay h1{{font-size:60px;color:#ff0000;text-shadow:0 0 20px #ff0000;margin-bottom:20px}}
#menuOverlay h2{{font-size:30px;color:#ffff00;margin-bottom:20px}}#menuOverlay p{{color:#00ff00;margin:10px 0}}
#gameOverOverlay .overlay-content{{border-color:#ff0000;background:rgba(20,0,0,0.9)}}
#pauseOverlay .overlay-content{{border-color:#ffff00}}
.btn{{background:#00ff00;color:#000;border:3px solid #00ff00;padding:15px 40px;font-size:20px;font-weight:bold;cursor:pointer;border-radius:5px;margin-top:20px;transition:0.3s}}
.btn:hover{{background:#ffff00;border-color:#ffff00;transform:scale(1.05)}}.btn.red{{background:#ff0000;color:#fff;border-color:#ff0000}}
.hud{{position:fixed;z-index:100;background:rgba(0,0,0,0.8);padding:15px;border:2px solid #00ff00;border-radius:5px;color:#00ff00;font-family:'Courier New',monospace;font-size:14px}}
#hud{{top:20px;left:20px}}#hudTop{{top:20px;right:20px;text-align:right}}#hudBottom{{bottom:20px;left:20px;font-size:12px;color:#ffff00}}
.stat-line{{margin:5px 0}}.label{{color:#ffff00}}.value{{color:#00ff00}}.stats-box{{background:rgba(0,0,0,0.5);padding:20px;margin:20px 0;border:2px solid #00ff00;border-radius:5px}}
</style></head><body><canvas id="gameCanvas"></canvas>
<div id="menuOverlay" class="overlay"><div class="overlay-content"><h1>🎮 MINI GTA</h1><h2>4K Web Edition</h2><p>Open World Action Game</p><button class="btn" onclick="gameInstance.startGame()">START GAME</button></div></div>
<div id="pauseOverlay" class="overlay hidden"><div class="overlay-content"><h1>⏸️ PAUSED</h1><p style="font-size:18px;color:#00ff00;margin-top:20px">Press ESC to Resume</p></div></div>
<div id="gameOverOverlay" class="overlay hidden"><div class="overlay-content"><h1>💀 GAME OVER</h1><div class="stats-box">
<div class="stat-line">Money: $<span id="finalMoney">0</span></div><div class="stat-line">Kills: <span id="finalKills">0</span></div><div class="stat-line">Accuracy: <span id="finalAccuracy">0</span>%</div><div class="stat-line">Time: <span id="finalTime">0</span>s</div><div class="stat-line">Wave: <span id="finalWave">0</span></div></div>
<button class="btn red" onclick="location.reload()">PLAY AGAIN</button></div></div>
<div id="hud" class="hud"><div class="stat-line"><span class="label">HEALTH:</span> <span class="value" id="health">100</span>/100</div><div class="stat-line"><span class="label">MONEY:</span> $<span class="value" id="money">0</span></div><div class="stat-line"><span class="label">AMMO:</span> <span class="value" id="ammo">30</span>/<span id="maxAmmo">30</span></div><div class="stat-line"><span class="label">WEAPON:</span> <span class="value" id="weapon">PISTOL</span></div></div>
<div id="hudTop" class="hud"><div class="stat-line"><span class="label">KILLS:</span> <span class="value" id="kills">0</span></div><div class="stat-line"><span class="label">WAVE:</span> <span class="value" id="wave">1</span></div><div class="stat-line"><span class="label">WANTED:</span> <span class="value" id="wanted">☆☆☆☆☆</span></div><div class="stat-line"><span class="label">SCORE:</span> <span class="value" id="score">0</span></div></div>
<div id="hudBottom" class="hud">WASD=Move | Click=Shoot | 1/2/3=Weapons | E=Vehicle | ESC=Pause | SPACE=Start</div>
<script>{GAME_JS}</script></body></html>"""
        self._send_html(html)

    def serve_clock(self):
        html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>World Clock</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:Arial;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);color:#00d4ff;min-height:100vh;padding:20px}}
.container{{max-width:1200px;margin:0 auto}}header{{text-align:center;margin-bottom:30px}}h1{{font-size:2.5em;color:#00d4ff;text-shadow:0 0 10px rgba(0,212,255,0.5)}}
.system-time-box{{background:linear-gradient(135deg,#0f3460 0%,#16213e 100%);border:2px solid #00d4ff;border-radius:15px;padding:30px;margin-bottom:30px;text-align:center}}
.system-time{{font-size:4em;font-family:'Courier New',monospace;color:#00ff00;font-weight:bold;letter-spacing:3px;text-shadow:0 0 10px rgba(0,255,0,0.5)}}
.clocks-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:20px;margin-top:20px}}
.clock-card{{background:linear-gradient(135deg,#16213e 0%,#0f3460 100%);border:2px solid #00d4ff;border-radius:10px;padding:20px;transition:all 0.3s}}
.clock-card:hover{{transform:translateY(-5px);box-shadow:0 0 25px rgba(0,212,255,0.4)}}
.zone-name{{font-size:1.3em;font-weight:bold;color:#00d4ff;margin-bottom:5px}}.zone-time{{font-size:2.5em;font-family:'Courier New',monospace;color:#00ff00;font-weight:bold;letter-spacing:2px;text-shadow:0 0 10px rgba(0,255,0,0.5)}}
</style></head><body><div class="container"><header><h1>🌍 WORLD CLOCK</h1></header>
<div class="system-time-box"><div style="color:#00d4ff">SYSTEM TIME</div><div class="system-time" id="systemTime">00:00:00</div><div id="systemDate" style="color:#888;margin-top:10px">Loading...</div></div>
<div class="clocks-grid" id="clocksGrid"></div></div>
<script>
const zones={{"UTC":"UTC","New York":"America/New_York","Los Angeles":"America/Los_Angeles","London":"Europe/London","Paris":"Europe/Paris","Tokyo":"Asia/Tokyo","Dubai":"Asia/Dubai","Sydney":"Australia/Sydney","Mumbai":"Asia/Kolkata","Singapore":"Asia/Singapore"}};
function formatTime(d,use24=true){{const h=String(d.getHours()).padStart(2,'0'),m=String(d.getMinutes()).padStart(2,'0'),s=String(d.getSeconds()).padStart(2,'0');if(use24)return`${{h}}:${{m}}:${{s}}`;const hr=d.getHours()%12||12,ap=d.getHours()>=12?'PM':'AM';return`${{String(hr).padStart(2,'0')}}:${{m}}:${{s}} ${{ap}}`}}
function update(){{const now=new Date();document.getElementById('systemTime').textContent=formatTime(now);document.getElementById('systemDate').textContent=now.toLocaleDateString('en-US',{{weekday:'long',year:'numeric',month:'long',day:'numeric'}});const grid=document.getElementById('clocksGrid');grid.innerHTML='';for(const[city,tz]of Object.entries(zones)){{const tzTime=new Date(now.toLocaleString('en-US',{{timeZone:tz}}));const card=document.createElement('div');card.className='clock-card';card.innerHTML=`<div class="zone-name">${{city}}</div><div class="zone-time">${{formatTime(tzTime)}}</div>`;grid.appendChild(card)}}}}
update();setInterval(update,1000);
</script></body></html>"""
        self._send_html(html)

    def serve_info(self):
        html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Mini GTA - Info</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px;display:flex;justify-content:center;align-items:center}}
.container{{max-width:900px;width:100%;background:rgba(0,0,0,0.8);border-radius:15px;padding:40px;text-align:center;color:white}}h1{{font-size:3.5rem;color:#ff4444;margin-bottom:10px;text-shadow:0 0 10px rgba(255,68,68,0.5)}}
.subtitle{{font-size:1.5rem;color:#ffff00;margin-bottom:30px}}.description{{font-size:1.1rem;color:#cccccc;margin-bottom:30px;line-height:1.6}}
.features{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin:30px 0}}
.feature-card{{background:rgba(100,150,255,0.1);border:2px solid #6496ff;border-radius:10px;padding:20px;text-align:left}}
.feature-card h3{{color:#ffff00;margin-bottom:10px}}.feature-card p{{font-size:0.9rem;color:#aaaaaa}}.btn{{padding:15px 40px;font-size:1.1rem;border:none;border-radius:8px;cursor:pointer;font-weight:bold;text-decoration:none;display:inline-block;background:linear-gradient(135deg,#ff4444,#ff6666);color:white;margin:20px 10px;transition:0.3s}}
.btn:hover{{transform:scale(1.05)}}
</style></head><body><div class="container"><h1>🎮 MINI GTA</h1><div class="subtitle">4K Edition - Open World Action Game</div>
<div class="description">A fully-featured GTA-style open world action game with dynamic combat, vehicles, and missions!</div>
<div class="features">
<div class="feature-card"><h3>🌍 Open World</h3><p>Explore a massive world with buildings, roads, and vehicles</p></div>
<div class="feature-card"><h3>🔫 Combat System</h3><p>3 weapons with different damage and fire rates</p></div>
<div class="feature-card"><h3>🚗 Vehicles</h3><p>Drive cars, trucks, and motorcycles</p></div>
<div class="feature-card"><h3>👮 Police Chase</h3><p>5-star wanted system with dynamic AI</p></div>
</div><div style="margin-top:30px"><a href="/game" class="btn">▶️ PLAY GAME</a><a href="/" class="btn">🏠 HOME</a></div></div></body></html>"""
        self._send_html(html)

    def serve_status(self):
        status = json.dumps({"status": "running", "version": "1.0.0", "timestamp": datetime.now().isoformat()})
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(status.encode())

    def serve_404(self):
        html = """<html><body style="background:#000;color:#00ff00;font-family:Arial;text-align:center;padding:50px"><h1>404 Not Found</h1><a href="/" style="color:#00d4ff">Go Home</a></body></html>"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_html(self, html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


def start_server(port=8000):
    """Start the 100% Python game server"""
    server = HTTPServer(('0.0.0.0', port), GameServerHandler)
    
    print("\n" + "="*70)
    print("🎮 MINI GTA - 100% Python Game Server")
    print("="*70)
    print(f"✅ Server started successfully!")
    print(f"🌐 Open your browser: http://localhost:{port}")
    print(f"⏹️  Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    try:
        threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    except:
        pass
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
        server.shutdown()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_server(port=port)
