<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEON REFLEX: SYNAPSE OVERLOAD</title>
    <style>
        :root { --bg: #050505; --red: #ff0055; --green: #00ff9d; --blue: #00ccff; --yellow: #ffcc00; --text: #fff; }
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
        body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; height: 100vh; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        
        /* CRT Effect */
        .crt::before { content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06)); z-index: 2; background-size: 100% 2px, 3px 100%; pointer-events: none; animation: flicker 0.15s infinite; }
        @keyframes flicker { 0% { opacity: 0.97; } 50% { opacity: 1; } 100% { opacity: 0.98; } }

        canvas { position: absolute; top: 0; left: 0; z-index: 1; }
        
        /* UI Overlay */
        .ui-layer { position: relative; z-index: 10; width: 100%; max-width: 600px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 20px; pointer-events: none; }
        
        .hud-top { display: flex; justify-content: space-between; font-size: 1.2em; font-weight: bold; text-shadow: 0 0 10px currentColor; }
        .score-val { color: var(--green); }
        .mult-val { color: var(--yellow); }
        
        .center-msg { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: auto; background: rgba(5,5,5,0.9); padding: 40px; border: 1px solid #333; }
        .btn-start { background: transparent; border: 2px solid var(--green); color: var(--green); padding: 15px 40px; font-size: 1.5em; font-family: inherit; cursor: pointer; transition: 0.2s; text-transform: uppercase; letter-spacing: 3px; box-shadow: 0 0 20px rgba(0,255,157,0.2); margin-top: 20px; }
        .btn-start:hover { background: var(--green); color: #000; box-shadow: 0 0 40px rgba(0,255,157,0.6); }
        
        .controls-hint { text-align: center; font-size: 0.8em; color: #555; margin-bottom: 20px; opacity: 0.7; }
        .key-badge { display: inline-block; border: 1px solid #555; padding: 2px 8px; border-radius: 4px; margin: 0 5px; font-weight: bold; }
        .k-red { color: var(--red); border-color: var(--red); }
        .k-green { color: var(--green); border-color: var(--green); }
        .k-blue { color: var(--blue); border-color: var(--blue); }
        .k-yellow { color: var(--yellow); border-color: var(--yellow); }

        /* Mobile Controls */
        .mobile-controls { display: none; grid-template-columns: 1fr 1fr; gap: 10px; width: 100%; height: 150px; pointer-events: auto; }
        .m-btn { border: 2px solid; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 2em; font-weight: bold; opacity: 0.8; transition: 0.1s; }
        .m-btn:active { transform: scale(0.95); opacity: 1; }
        .mb-red { border-color: var(--red); color: var(--red); background: rgba(255,0,85,0.1); }
        .mb-green { border-color: var(--green); color: var(--green); background: rgba(0,255,157,0.1); }
        .mb-blue { border-color: var(--blue); color: var(--blue); background: rgba(0,204,255,0.1); }
        .mb-yellow { border-color: var(--yellow); color: var(--yellow); background: rgba(255,204,0,0.1); }

        @media (max-width: 768px) {
            .controls-hint { display: none; }
            .mobile-controls { display: grid; }
            .hud-top { font-size: 1em; }
            .center-msg { width: 90%; padding: 20px; }
        }
    </style>
</head>
<body class="crt">

<canvas id="gameCanvas"></canvas>

<div class="ui-layer">
    <div class="hud-top">
        <div>SCORE: <span class="score-val" id="scoreDisplay">0</span></div>
        <div>MULT: x<span class="mult-val" id="multDisplay">1.0</span></div>
    </div>

    <div class="center-msg" id="startScreen">
        <h1 style="font-size: 2em; margin-bottom: 10px; text-shadow: 0 0 20px var(--green);">SYNAPSE OVERLOAD</h1>
        <p style="margin-bottom: 20px; color: #aaa; font-size: 0.9em;">TRAIN YOUR REACTION SPEED</p>
        <button class="btn-start" onclick="startGame()">INITIALIZE</button>
    </div>

    <div class="center-msg" id="gameOverScreen" style="display: none;">
        <h1 style="font-size: 2em; margin-bottom: 10px; color: var(--red); text-shadow: 0 0 20px var(--red);">SYSTEM FAILURE</h1>
        <p style="margin-bottom: 10px;">FINAL SCORE: <span id="finalScore" style="color:var(--green)">0</span></p>
        <p style="margin-bottom: 20px; font-size: 0.9em; color:#aaa;">BEST: <span id="bestScore">0</span></p>
        <button class="btn-start" onclick="startGame()">REBOOT</button>
    </div>

    <div class="controls-hint">
        PRESS <span class="key-badge k-red">W / ↑</span> <span class="key-badge k-green">A / ←</span> <span class="key-badge k-blue">S / ↓</span> <span class="key-badge k-yellow">D / →</span>
    </div>

    <div class="mobile-controls">
        <div class="m-btn mb-red" ontouchstart="handleInput('red')">▲</div>
        <div class="m-btn mb-green" ontouchstart="handleInput('green')">◀</div>
        <div class="m-btn mb-blue" ontouchstart="handleInput('blue')">▼</div>
        <div class="m-btn mb-yellow" ontouchstart="handleInput('yellow')">▶</div>
    </div>
</div>

<script>
/**
 * NEON REFLEX ENGINE v1.0
 * Pure JS/Canvas Reaction Trainer
 */

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let width, height, centerX, centerY;

// Game State
let state = {
    isPlaying: false,
    score: 0,
    multiplier: 1.0,
    bestScore: parseInt(localStorage.getItem('neon_reflex_best') || '0'),
    speed: 3,
    spawnRate: 60, // frames
    frameCount: 0,
    threats: [],
    particles: [],
    shake: 0
};

const COLORS = {
    red: '#ff0055',
    green: '#00ff9d',
    blue: '#00ccff',
    yellow: '#ffcc00'
};

const KEYS = {
    'w': 'red', 'arrowup': 'red',
    'a': 'green', 'arrowleft': 'green',
    's': 'blue', 'arrowdown': 'blue',
    'd': 'yellow', 'arrowright': 'yellow'
};

// Resize Handler
function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    centerX = width / 2;
    centerY = height / 2;
}
window.addEventListener('resize', resize);
resize();

// Audio Engine
let audioCtx;
function initAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
}

function playSound(type) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    const now = audioCtx.currentTime;
    if (type === 'hit') {
        osc.type = 'square';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.1);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
    } else if (type === 'fail') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.linearRampToValueAtTime(50, now + 0.3);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
    } else if (type === 'spawn') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(400, now);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.05);
        osc.start(now);
        osc.stop(now + 0.05);
    }
}

// Particle System
class Particle {
    constructor(x, y, color) {
        this.x = x; this.y = y; this.color = color;
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 5 + 2;
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.life = 1.0;
        this.decay = Math.random() * 0.03 + 0.02;
        this.size = Math.random() * 3 + 1;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life -= this.decay;
        this.size *= 0.95;
    }
    draw() {
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }
}

function spawnParticles(x, y, color, count = 10) {
    for (let i = 0; i < count; i++) {
        state.particles.push(new Particle(x, y, color));
    }
}

// Threat Class
class Threat {
    constructor() {
        const sides = ['top', 'bottom', 'left', 'right'];
        const side = sides[Math.floor(Math.random() * sides.length)];
        const types = Object.keys(COLORS);
        this.type = types[Math.floor(Math.random() * types.length)];
        this.color = COLORS[this.type];
        this.radius = 20;
        this.active = true;
        
        // Spawn position based on side
        switch(side) {
            case 'top': this.x = Math.random() * width; this.y = -this.radius; break;
            case 'bottom': this.x = Math.random() * width; this.y = height + this.radius; break;
            case 'left': this.x = -this.radius; this.y = Math.random() * height; break;
            case 'right': this.x = width + this.radius; this.y = Math.random() * height; break;
        }
        
        // Calculate velocity towards center
        const dx = centerX - this.x;
        const dy = centerY - this.y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        this.vx = (dx / dist) * state.speed;
        this.vy = (dy / dist) * state.speed;
    }
    
    update() {
        this.x += this.vx;
        this.y += this.vy;
        
        // Check collision with center core
        const dx = this.x - centerX;
        const dy = this.y - centerY;
        const dist = Math.sqrt(dx*dx + dy*dy);
        
        if (dist < 30) { // Core radius
            gameOver();
        }
    }
    
    draw() {
        ctx.shadowBlur = 15;
        ctx.shadowColor = this.color;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
        
        // Inner detail
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * 0.6, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Input Handling
function handleInput(color) {
    if (!state.isPlaying) return;
    initAudio();
    
    // Find closest threat of matching color
    let closest = null;
    let minDist = Infinity;
    
    state.threats.forEach(t => {
        if (t.type === color && t.active) {
            const dx = t.x - centerX;
            const dy = t.y - centerY;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < minDist) {
                minDist = dist;
                closest = t;
            }
        }
    });
    
    if (closest && minDist < 300) { // Max interaction range
        closest.active = false;
        state.score += Math.floor(10 * state.multiplier);
        state.multiplier = Math.min(state.multiplier + 0.1, 5.0);
        spawnParticles(closest.x, closest.y, closest.color, 15);
        playSound('hit');
        
        // Increase difficulty
        if (state.score % 100 === 0) {
            state.speed += 0.5;
            state.spawnRate = Math.max(20, state.spawnRate - 2);
        }
    } else {
        // Wrong input or no target
        state.multiplier = Math.max(1.0, state.multiplier - 0.5);
        state.shake = 10;
        playSound('fail');
    }
    
    updateUI();
}

document.addEventListener('keydown', e => {
    const key = e.key.toLowerCase();
    if (KEYS[key]) handleInput(KEYS[key]);
});

// Game Loop
function gameLoop() {
    // Clear canvas with trail effect
    ctx.fillStyle = 'rgba(5, 5, 5, 0.3)';
    ctx.fillRect(0, 0, width, height);
    
    // Screen shake
    if (state.shake > 0) {
        const dx = (Math.random() - 0.5) * state.shake;
        const dy = (Math.random() - 0.5) * state.shake;
        ctx.save();
        ctx.translate(dx, dy);
        state.shake *= 0.9;
        if (state.shake < 0.5) state.shake = 0;
    }
    
    // Draw Core
    ctx.shadowBlur = 20;
    ctx.shadowColor = '#fff';
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 25, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    
    // Core pulse
    const pulse = Math.sin(Date.now() / 200) * 5;
    ctx.strokeStyle = 'rgba(255,255,255,0.5)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 25 + pulse, 0, Math.PI * 2);
    ctx.stroke();
    
    // Update & Draw Threats
    state.threats = state.threats.filter(t => t.active);
    state.threats.forEach(t => {
        t.update();
        t.draw();
    });
    
    // Spawn new threats
    state.frameCount++;
    if (state.frameCount >= state.spawnRate) {
        state.threats.push(new Threat());
        state.frameCount = 0;
        playSound('spawn');
    }
    
    // Update & Draw Particles
    state.particles = state.particles.filter(p => p.life > 0);
    state.particles.forEach(p => {
        p.update();
        p.draw();
    });
    
    if (state.shake > 0) ctx.restore();
    
    if (state.isPlaying) requestAnimationFrame(gameLoop);
}

// Game Control
function startGame() {
    initAudio();
    state = {
        isPlaying: true,
        score: 0,
        multiplier: 1.0,
        bestScore: state.bestScore,
        speed: 3,
        spawnRate: 60,
        frameCount: 0,
        threats: [],
        particles: [],
        shake: 0
    };
    
    document.getElementById('startScreen').style.display = 'none';
    document.getElementById('gameOverScreen').style.display = 'none';
    updateUI();
    gameLoop();
}

function gameOver() {
    state.isPlaying = false;
    playSound('fail');
    
    if (state.score > state.bestScore) {
        state.bestScore = state.score;
        localStorage.setItem('neon_reflex_best', state.bestScore.toString());
    }
    
    document.getElementById('finalScore').innerText = state.score;
    document.getElementById('bestScore').innerText = state.bestScore;
    document.getElementById('gameOverScreen').style.display = 'block';
}

function updateUI() {
    document.getElementById('scoreDisplay').innerText = state.score;
    document.getElementById('multDisplay').innerText = state.multiplier.toFixed(1);
}

// Init
updateUI();
</script>
</body>
</html>
