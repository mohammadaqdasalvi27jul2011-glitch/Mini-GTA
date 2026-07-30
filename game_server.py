#!/usr/bin/env python3
"""
Mini GTA - Complete Python Web Server
100% Pure Python - No HTML files required
Serves all games via HTTP with embedded HTML generation
"""

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import threading
import webbrowser
from datetime import datetime


class GameServerHandler(BaseHTTPRequestHandler):
    """HTTP Handler for all game pages"""

    def log_message(self, format, *args):
        """Custom logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

    def do_GET(self):
        """Handle GET requests"""
        try:
            path = urlparse(self.path).path
            
            if path == '/' or path == '/index.html':
                self.serve_main_page()
            elif path == '/game' or path == '/minigta':
                self.serve_minigta_game()
            elif path == '/clock':
                self.serve_clock_app()
            elif path == '/play':
                self.serve_play_page()
            elif path == '/api/status':
                self.serve_api_status()
            else:
                self.serve_404()
        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error(500, "Internal Server Error")

    def serve_main_page(self):
        """Serve main landing page"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini GTA - Game Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #00ff00;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 4rem;
            color: #ff0000;
            text-shadow: 0 0 20px #ff0000;
            margin-bottom: 20px;
        }
        
        .header p {
            font-size: 1.2rem;
            color: #ffff00;
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .game-card {
            background: rgba(15, 52, 96, 0.8);
            border: 2px solid #00d4ff;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .game-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 0 30px #00d4ff;
            border-color: #00ff00;
        }
        
        .game-card h2 {
            font-size: 2rem;
            margin-bottom: 15px;
            color: #00ff00;
        }
        
        .game-card p {
            color: #aaa;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #00d4ff, #00ff00);
            color: #000;
            padding: 12px 30px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 1rem;
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px #00ff00;
        }
        
        .features {
            background: rgba(15, 52, 96, 0.8);
            border: 2px solid #00d4ff;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
        }
        
        .features h3 {
            color: #ffff00;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }
        
        .features ul {
            list-style: none;
            columns: 2;
        }
        
        .features li {
            color: #00ff00;
            padding: 8px 0;
            border-bottom: 1px solid #00d4ff;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #888;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.5rem;
            }
            
            .games-grid {
                grid-template-columns: 1fr;
            }
            
            .features ul {
                columns: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 MINI GTA</h1>
            <p>Complete Game Suite - 100% Python</p>
        </div>
        
        <div class="games-grid">
            <div class="game-card">
                <h2>🎮 Mini GTA Game</h2>
                <p>Full-featured open-world action game with combat, vehicles, and missions</p>
                <a href="/game" class="btn">PLAY NOW</a>
            </div>
            
            <div class="game-card">
                <h2>🕐 World Clock</h2>
                <p>Real-time digital clock with multiple time zones and customization</p>
                <a href="/clock" class="btn">OPEN CLOCK</a>
            </div>
            
            <div class="game-card">
                <h2>📋 Game Info</h2>
                <p>Learn more about Mini GTA features, controls, and gameplay</p>
                <a href="/play" class="btn">READ MORE</a>
            </div>
        </div>
        
        <div class="features">
            <h3>⭐ Features</h3>
            <ul>
                <li>🎯 Advanced Combat System</li>
                <li>🚗 Vehicle Mechanics</li>
                <li>👥 AI NPCs & Police</li>
                <li>💰 Money & Score System</li>
                <li>🌍 Large Open World</li>
                <li>🎪 Dynamic Wave System</li>
                <li>🕐 Multi-timezone Clock</li>
                <li>📊 Real-time Statistics</li>
                <li>🎨 High-quality Graphics</li>
                <li>⌨️ Responsive Controls</li>
                <li>💾 Game State Management</li>
                <li>📱 Responsive Design</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>🎮 Mini GTA - 100% Pure Python Application</p>
            <p>No external HTML files • All generated dynamically • Fully customizable</p>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_minigta_game(self):
        """Serve Mini GTA game"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini GTA - Game</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; user-select: none; }
        html, body { width: 100%; height: 100%; overflow: hidden; }
        body { font-family: Arial, sans-serif; background: #000; color: #00ff00; }
        .container { width: 100%; height: 100%; display: flex; flex-direction: column; }
        #gameCanvas { display: block; width: 100%; height: 100%; background: #0a0a0a; }
        
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1000; }
        .overlay.hidden { display: none; }
        .overlay-content { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; background: rgba(0,0,0,0.9); border: 3px solid; padding: 40px; border-radius: 10px; }
        
        #menuOverlay .overlay-content { border-color: #00ff00; background: rgba(0,20,0,0.9); }
        #menuOverlay h1 { font-size: 60px; color: #ff0000; text-shadow: 0 0 20px #ff0000; margin-bottom: 20px; }
        #menuOverlay h2 { font-size: 30px; color: #ffff00; margin-bottom: 20px; }
        #menuOverlay p { color: #00ff00; margin: 10px 0; }
        
        #gameOverOverlay .overlay-content { border-color: #ff0000; background: rgba(20,0,0,0.9); }
        #gameOverOverlay h1 { font-size: 60px; color: #ff0000; text-shadow: 0 0 20px #ff0000; margin-bottom: 30px; }
        
        #pauseOverlay .overlay-content { border-color: #ffff00; background: rgba(0,0,0,0.9); }
        #pauseOverlay h1 { font-size: 48px; color: #ffff00; text-shadow: 0 0 20px #ffff00; }
        
        .btn { background: #00ff00; color: #000; border: 3px solid #00ff00; padding: 15px 40px; font-size: 20px; font-weight: bold; cursor: pointer; border-radius: 5px; margin-top: 20px; transition: 0.3s; }
        .btn:hover { background: #ffff00; border-color: #ffff00; transform: scale(1.05); }
        .btn.red { background: #ff0000; color: #fff; border-color: #ff0000; }
        .btn.red:hover { background: #ff3333; }
        
        .hud { position: fixed; z-index: 100; background: rgba(0,0,0,0.8); padding: 15px; border: 2px solid #00ff00; border-radius: 5px; color: #00ff00; font-family: 'Courier New', monospace; font-size: 14px; }
        #hud { top: 20px; left: 20px; }
        #hudTop { top: 20px; right: 20px; text-align: right; }
        #hudBottom { bottom: 20px; left: 20px; font-size: 12px; color: #ffff00; }
        
        .stat-line { margin: 5px 0; }
        .label { color: #ffff00; }
        .value { color: #00ff00; }
        
        .stats-box { background: rgba(0,0,0,0.5); padding: 20px; margin: 20px 0; border: 2px solid #00ff00; border-radius: 5px; }
        .stat-line { font-size: 20px; color: #00ff00; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <canvas id="gameCanvas"></canvas>
    </div>
    
    <div id="menuOverlay" class="overlay">
        <div class="overlay-content">
            <h1>🎮 MINI GTA</h1>
            <h2>4K Web Edition</h2>
            <p>Open World Action Game</p>
            <button class="btn" onclick="gameInstance.startGame()">START GAME</button>
            <p style="font-size: 12px; margin-top: 20px;">Press SPACE to start</p>
        </div>
    </div>
    
    <div id="pauseOverlay" class="overlay hidden">
        <div class="overlay-content">
            <h1>⏸️ PAUSED</h1>
            <p style="font-size: 18px; color: #00ff00; margin-top: 20px;">Press ESC to Resume</p>
        </div>
    </div>
    
    <div id="gameOverOverlay" class="overlay hidden">
        <div class="overlay-content">
            <h1>💀 GAME OVER</h1>
            <div class="stats-box">
                <div class="stat-line">Money: $<span id="finalMoney">0</span></div>
                <div class="stat-line">Kills: <span id="finalKills">0</span></div>
                <div class="stat-line">Accuracy: <span id="finalAccuracy">0</span>%</div>
                <div class="stat-line">Time: <span id="finalTime">0</span>s</div>
                <div class="stat-line">Wave: <span id="finalWave">0</span></div>
            </div>
            <button class="btn red" onclick="location.reload()">PLAY AGAIN</button>
        </div>
    </div>
    
    <div id="hud" class="hud">
        <div class="stat-line"><span class="label">HEALTH:</span> <span class="value" id="health">100</span>/100</div>
        <div class="stat-line"><span class="label">MONEY:</span> $<span class="value" id="money">0</span></div>
        <div class="stat-line"><span class="label">AMMO:</span> <span class="value" id="ammo">30</span>/<span id="maxAmmo">30</span></div>
        <div class="stat-line"><span class="label">WEAPON:</span> <span class="value" id="weapon">PISTOL</span></div>
    </div>
    
    <div id="hudTop" class="hud">
        <div class="stat-line"><span class="label">KILLS:</span> <span class="value" id="kills">0</span></div>
        <div class="stat-line"><span class="label">WAVE:</span> <span class="value" id="wave">1</span></div>
        <div class="stat-line"><span class="label">WANTED:</span> <span class="value" id="wanted">☆☆☆☆☆</span></div>
        <div class="stat-line"><span class="label">SCORE:</span> <span class="value" id="score">0</span></div>
    </div>
    
    <div id="hudBottom" class="hud">
        WASD=Move | Click=Shoot | 1/2/3=Weapons | E=Vehicle | ESC=Pause | SPACE=Start
    </div>
    
    <script src="/static/game.js"></script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_clock_app(self):
        """Serve World Clock App"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>World Clock - Time Zones</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Arial', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #00d4ff; min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 30px; }
        h1 { font-size: 2.5em; color: #00d4ff; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); margin-bottom: 10px; }
        .subtitle { color: #888; font-size: 0.9em; }
        
        .system-time-box { background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); border: 2px solid #00d4ff; border-radius: 15px; padding: 30px; margin-bottom: 30px; text-align: center; box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
        .system-label { font-size: 1.2em; color: #00d4ff; font-weight: bold; margin-bottom: 10px; }
        .system-time { font-size: 4em; font-family: 'Courier New', monospace; color: #00ff00; font-weight: bold; letter-spacing: 3px; text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); margin-bottom: 10px; }
        .system-date { font-size: 1.2em; color: #888; }
        
        .controls { background: #16213e; border-radius: 10px; padding: 20px; margin-bottom: 30px; display: flex; gap: 20px; flex-wrap: wrap; align-items: center; border: 1px solid #0f3460; }
        .format-toggle { display: flex; align-items: center; gap: 10px; }
        .search-box { display: flex; gap: 10px; flex: 1; min-width: 300px; }
        .search-box input { flex: 1; padding: 10px 15px; background: #0f3460; border: 2px solid #00d4ff; color: #00d4ff; border-radius: 5px; font-size: 1em; }
        .search-box input::placeholder { color: #555; }
        
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #0f3460; }
        .tab-btn { padding: 12px 25px; background: #0f3460; color: #00d4ff; border: none; cursor: pointer; font-size: 1em; font-weight: bold; border-bottom: 3px solid transparent; transition: all 0.3s; }
        .tab-btn:hover { background: #16213e; }
        .tab-btn.active { border-bottom-color: #00d4ff; background: #16213e; }
        
        .clocks-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; margin-top: 20px; }
        .clock-card { background: linear-gradient(135deg, #16213e 0%, #0f3460 100%); border: 2px solid #00d4ff; border-radius: 10px; padding: 20px; display: flex; justify-content: space-between; align-items: center; transition: all 0.3s; box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); }
        .clock-card:hover { transform: translateY(-5px); box-shadow: 0 0 25px rgba(0, 212, 255, 0.4); border-color: #00ff00; }
        
        .zone-name { font-size: 1.3em; font-weight: bold; color: #00d4ff; margin-bottom: 5px; }
        .zone-time { font-size: 2.5em; font-family: 'Courier New', monospace; color: #00ff00; font-weight: bold; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); margin-bottom: 5px; }
        .zone-date { font-size: 0.9em; color: #888; }
        
        @media (max-width: 768px) {
            h1 { font-size: 1.8em; }
            .system-time { font-size: 2.5em; }
            .clocks-grid { grid-template-columns: 1fr; }
            .controls { flex-direction: column; }
            .search-box { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌍 WORLD CLOCK</h1>
            <p class="subtitle">Real-time Time Zones</p>
        </header>
        
        <div class="system-time-box">
            <div class="system-label">SYSTEM TIME</div>
            <div class="system-time" id="systemTime">00:00:00</div>
            <div class="system-date" id="systemDate">Loading...</div>
        </div>
        
        <div class="controls">
            <div class="format-toggle">
                <input type="checkbox" id="format24h" checked>
                <label for="format24h">24-Hour Format</label>
            </div>
            <div class="search-box">
                <label for="searchInput">🔍 Search:</label>
                <input type="text" id="searchInput" placeholder="Search by city...">
            </div>
        </div>
        
        <div class="clocks-grid" id="clocksGrid"></div>
    </div>
    
    <script>
        const timeZones = {
            "UTC": "UTC", "New York": "America/New_York", "Los Angeles": "America/Los_Angeles",
            "London": "Europe/London", "Paris": "Europe/Paris", "Tokyo": "Asia/Tokyo",
            "Dubai": "Asia/Dubai", "Sydney": "Australia/Sydney", "Mumbai": "Asia/Kolkata",
            "Singapore": "Asia/Singapore", "Hong Kong": "Asia/Hong_Kong", "Bangkok": "Asia/Bangkok",
            "Istanbul": "Europe/Istanbul", "Moscow": "Europe/Moscow", "São Paulo": "America/Sao_Paulo",
            "Mexico City": "America/Mexico_City", "Toronto": "America/Toronto", "Vancouver": "America/Vancouver",
            "Auckland": "Pacific/Auckland", "Fiji": "Pacific/Fiji"
        };
        
        let is24h = true;
        let searchTerm = "";
        
        function formatTime(date, use24h = true) {
            const h = String(date.getHours()).padStart(2, '0');
            const m = String(date.getMinutes()).padStart(2, '0');
            const s = String(date.getSeconds()).padStart(2, '0');
            if (use24h) return `${h}:${m}:${s}`;
            const hr = date.getHours() % 12 || 12;
            const ap = date.getHours() >= 12 ? 'PM' : 'AM';
            return `${String(hr).padStart(2, '0')}:${m}:${s} ${ap}`;
        }
        
        function formatDate(date) {
            return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        }
        
        function updateClock() {
            const now = new Date();
            document.getElementById('systemTime').textContent = formatTime(now, is24h);
            document.getElementById('systemDate').textContent = formatDate(now);
            
            const grid = document.getElementById('clocksGrid');
            grid.innerHTML = '';
            
            for (const [city, tz] of Object.entries(timeZones)) {
                if (searchTerm && !city.toLowerCase().includes(searchTerm.toLowerCase())) continue;
                
                const tzTime = new Date(now.toLocaleString('en-US', { timeZone: tz }));
                const card = document.createElement('div');
                card.className = 'clock-card';
                card.innerHTML = `<div><div class="zone-name">${city}</div><div class="zone-time">${formatTime(tzTime, is24h)}</div><div class="zone-date">${formatDate(tzTime)}</div></div>`;
                grid.appendChild(card);
            }
        }
        
        document.getElementById('format24h').addEventListener('change', (e) => { is24h = e.target.checked; });
        document.getElementById('searchInput').addEventListener('input', (e) => { searchTerm = e.target.value; });
        
        updateClock();
        setInterval(updateClock, 1000);
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_play_page(self):
        """Serve game info page"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini GTA - How to Play</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: rgba(0, 0, 0, 0.8); border-radius: 15px; padding: 40px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4); text-align: center; color: white; }
        
        h1 { font-size: 3.5rem; color: #ff4444; margin-bottom: 10px; text-shadow: 0 0 10px rgba(255, 68, 68, 0.5); font-weight: bold; }
        .subtitle { font-size: 1.5rem; color: #ffff00; margin-bottom: 30px; text-shadow: 0 0 5px rgba(255, 255, 0, 0.3); }
        
        .description { font-size: 1.1rem; color: #cccccc; margin-bottom: 30px; line-height: 1.6; }
        
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature-card { background: rgba(100, 150, 255, 0.1); border: 2px solid #6496ff; border-radius: 10px; padding: 20px; text-align: left; }
        .feature-card h3 { color: #ffff00; margin-bottom: 10px; }
        .feature-card p { font-size: 0.9rem; color: #aaaaaa; }
        
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-box { background: rgba(100, 100, 100, 0.2); border: 1px solid #666; border-radius: 8px; padding: 15px; }
        .stat-number { font-size: 2rem; color: #ffff00; font-weight: bold; }
        .stat-label { font-size: 0.85rem; color: #aaaaaa; margin-top: 5px; }
        
        .instructions { background: rgba(50, 50, 50, 0.8); border-left: 4px solid #ffff00; padding: 20px; margin: 30px 0; text-align: left; border-radius: 5px; }
        .instructions h3 { color: #ffff00; margin-bottom: 15px; }
        .instructions ul { list-style: none; columns: 2; }
        .instructions li { margin-bottom: 10px; color: #aaaaaa; }
        .instructions strong { color: #ffff00; }
        
        .buttons { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin: 30px 0; }
        .btn { padding: 15px 40px; font-size: 1.1rem; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; transition: all 0.3s; }
        .btn-primary { background: linear-gradient(135deg, #ff4444, #ff6666); color: white; box-shadow: 0 5px 15px rgba(255, 68, 68, 0.4); }
        .btn-primary:hover { transform: scale(1.05); box-shadow: 0 8px 20px rgba(255, 68, 68, 0.6); }
        
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .subtitle { font-size: 1.2rem; }
            .container { padding: 20px; }
            .instructions ul { columns: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 MINI GTA</h1>
        <div class="subtitle">4K Edition - Open World Action Game</div>
        
        <div class="description">
            A fully-featured GTA-style open world action game. Experience dynamic police chases, complete missions, drive vehicles, and build your crime empire!
        </div>
        
        <div class="stats">
            <div class="stat-box"><div class="stat-number">4000x3000</div><div class="stat-label">World Size</div></div>
            <div class="stat-box"><div class="stat-number">15+</div><div class="stat-label">AI NPCs</div></div>
            <div class="stat-box"><div class="stat-number">3</div><div class="stat-label">Weapons</div></div>
            <div class="stat-box"><div class="stat-number">5★</div><div class="stat-label">Wanted Level</div></div>
        </div>
        
        <div class="features">
            <div class="feature-card"><h3>🌍 Open World</h3><p>Explore a massive world with buildings, roads, and vehicles</p></div>
            <div class="feature-card"><h3>🔫 Combat System</h3><p>3 weapons with different damage and fire rates</p></div>
            <div class="feature-card"><h3>🚗 Vehicles</h3><p>Drive cars, trucks, and motorcycles</p></div>
            <div class="feature-card"><h3>👮 Police Chase</h3><p>5-star wanted system with dynamic AI</p></div>
            <div class="feature-card"><h3>🎯 Missions</h3><p>Random missions with rewards</p></div>
            <div class="feature-card"><h3>📊 Progress Tracking</h3><p>High score system and statistics</p></div>
        </div>
        
        <div class="instructions">
            <h3>⌨️ Controls</h3>
            <ul>
                <li><strong>WASD / Arrow Keys</strong> - Move or drive</li>
                <li><strong>Mouse Click</strong> - Shoot</li>
                <li><strong>1, 2, 3</strong> - Switch weapons</li>
                <li><strong>E</strong> - Enter/Exit vehicle</li>
                <li><strong>ESC</strong> - Pause/Menu</li>
                <li><strong>SPACE</strong> - Start Game</li>
            </ul>
        </div>
        
        <div class="buttons">
            <a href="/game" class="btn btn-primary">▶️ PLAY GAME</a>
            <a href="/" class="btn btn-primary">🏠 HOME</a>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_api_status(self):
        """Serve API status"""
        status = {
            "status": "running",
            "version": "1.0.0",
            "games": ["minigta", "clock"],
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode('utf-8'))

    def serve_404(self):
        """Serve 404 page"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
    <style>
        body { background: #000; color: #00ff00; font-family: Arial; text-align: center; padding: 50px; }
        h1 { font-size: 4rem; }
        p { font-size: 1.2rem; }
        a { color: #00d4ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>404 Not Found</h1>
    <p>The page you requested does not exist</p>
    <a href="/">Go back to home</a>
</body>
</html>"""
        
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


def start_server(host='0.0.0.0', port=8000):
    """Start the game server"""
    server = HTTPServer((host, port), GameServerHandler)
    
    print("\n" + "="*70)
    print("🎮 MINI GTA - Python Game Server")
    print("="*70)
    print(f"✅ Server started successfully!")
    print(f"🌐 Local:   http://localhost:{port}")
    print(f"🌐 Network: http://{host}:{port}")
    print(f"📱 Open your browser and navigate to the URL above")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Try to open browser
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
