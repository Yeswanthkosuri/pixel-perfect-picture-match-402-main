# Part 1 of Overhaul Generator
import os, sys

parts = []

# ==========================================
# PART 1: HTML HEAD & COD MOBILE TACTICAL CSS
# ==========================================
parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>ELEMENTAL ARENA — Tactical 3D Action Overhaul</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }

    html, body {
      width: 100vw;
      height: 100vh;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: #05070d;
      font-family: 'Rajdhani', system-ui, -apple-system, sans-serif;
      color: #e2e8f0;
    }

    /* Fullscreen 3D Viewport */
    #canvas-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 1;
      overflow: hidden;
      background: #05070d;
    }

    #canvas-container canvas {
      display: block;
      width: 100vw !important;
      height: 100vh !important;
      outline: none;
    }

    /* HUD Overlay */
    #hud {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 10;
      pointer-events: none;
    }

    .interactive { pointer-events: auto; }

    /* COD Mobile Style Sleek Top-Left Combatant Card */
    #hud-player {
      position: absolute;
      top: 14px;
      left: 16px;
      background: rgba(10, 15, 26, 0.78);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-left: 3px solid #38bdf8;
      border-radius: 8px;
      padding: 10px 14px;
      min-width: 250px;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
      pointer-events: auto;
    }

    #char-name-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .player-header-left {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    #char-avatar-badge {
      width: 26px;
      height: 26px;
      border-radius: 6px;
      background: rgba(56, 189, 248, 0.2);
      border: 1px solid #38bdf8;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
    }

    #player-char-name {
      font-family: 'Orbitron', sans-serif;
      font-weight: 800;
      font-size: 12px;
      letter-spacing: 1px;
      color: #f8fafc;
      text-transform: uppercase;
    }

    #hud-map-badge {
      font-family: 'Orbitron', sans-serif;
      font-size: 9px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.8px;
    }

    .stat-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
    }

    .stat-label {
      font-size: 10px;
      font-weight: 700;
      width: 44px;
      color: #94a3b8;
      letter-spacing: 0.5px;
    }

    .stat-bar-track {
      flex: 1;
      height: 6px;
      background: rgba(15, 23, 42, 0.8);
      border-radius: 3px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.08);
      position: relative;
    }

    .stat-bar-fill {
      height: 100%;
      border-radius: 3px;
      transition: width 0.15s ease-out;
    }

    #bar-hp { background: linear-gradient(90deg, #ef4444, #f87171); width: 100%; box-shadow: 0 0 6px rgba(239, 68, 68, 0.5); }
    #bar-shield { background: linear-gradient(90deg, #0284c7, #38bdf8); width: 100%; box-shadow: 0 0 6px rgba(56, 189, 248, 0.5); }
    #bar-mana { background: linear-gradient(90deg, #9333ea, #c084fc); width: 100%; box-shadow: 0 0 6px rgba(192, 132, 252, 0.5); }
    #bar-stam { background: linear-gradient(90deg, #eab308, #facc15); width: 100%; box-shadow: 0 0 6px rgba(250, 204, 21, 0.5); }

    .stat-num {
      font-family: 'Orbitron', monospace;
      font-size: 9px;
      font-weight: 700;
      width: 26px;
      text-align: right;
      color: #cbd5e1;
    }

    /* Minimalist Tactical Top-Center Target HUD (shown only when aiming or locking) */
    #hud-target {
      position: absolute;
      top: 14px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.82);
      border: 1px solid rgba(239, 68, 68, 0.4);
      border-top: 2px solid #ef4444;
      border-radius: 8px;
      padding: 8px 16px;
      min-width: 220px;
      backdrop-filter: blur(10px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
      display: none;
      pointer-events: auto;
    }

    #hud-target.active { display: block; }

    #hud-target-name {
      font-family: 'Orbitron', sans-serif;
      font-size: 11px;
      font-weight: 800;
      color: #f87171;
      text-align: center;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }

    #hud-target-meta {
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      color: #94a3b8;
      font-weight: 600;
      margin-top: 4px;
    }

    /* Top-Right Menu & Performance HUD */
    #hud-topright {
      position: absolute;
      top: 14px;
      right: 16px;
      display: flex;
      gap: 6px;
      pointer-events: auto;
    }

    .hud-btn {
      background: rgba(15, 23, 42, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #e2e8f0;
      padding: 6px 12px;
      border-radius: 6px;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 11px;
      letter-spacing: 0.6px;
      cursor: pointer;
      backdrop-filter: blur(8px);
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .hud-btn:hover {
      background: rgba(56, 189, 248, 0.25);
      border-color: #38bdf8;
      color: #fff;
      transform: translateY(-1px);
    }

    .cmd-btn {
      background: rgba(56, 189, 248, 0.18);
      border-color: #38bdf8;
      color: #38bdf8;
      font-family: 'Orbitron', sans-serif;
    }

    /* Performance HUD (FPS, Frame Time, Settings) */
    #perf-hud {
      position: absolute;
      top: 52px;
      right: 16px;
      background: rgba(10, 15, 26, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 6px;
      padding: 4px 10px;
      font-family: 'Orbitron', monospace;
      font-size: 9px;
      color: #94a3b8;
      display: flex;
      gap: 10px;
      backdrop-filter: blur(8px);
    }

    #perf-fps { color: #4ade80; font-weight: 700; }
    #perf-ms { color: #38bdf8; }

    /* Minimalist Tactical Crosshair */
    #crosshair-wrap {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      pointer-events: none;
    }

    #crosshair {
      width: 22px;
      height: 22px;
      position: relative;
    }

    .ch-dot {
      width: 4px;
      height: 4px;
      background: #38bdf8;
      border-radius: 50%;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      box-shadow: 0 0 6px #38bdf8;
    }

    .ch-line {
      position: absolute;
      background: rgba(56, 189, 248, 0.6);
    }

    .ch-top { width: 1.5px; height: 6px; top: 0; left: 50%; transform: translateX(-50%); }
    .ch-bot { width: 1.5px; height: 6px; bottom: 0; left: 50%; transform: translateX(-50%); }
    .ch-lft { width: 6px; height: 1.5px; left: 0; top: 50%; transform: translateY(-50%); }
    .ch-rgt { width: 6px; height: 1.5px; right: 0; top: 50%; transform: translateY(-50%); }

    /* Hit Marker */
    #hitmarker {
      position: absolute;
      width: 28px;
      height: 28px;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(45deg);
      opacity: 0;
      transition: opacity 0.08s ease-out;
      pointer-events: none;
    }

    #hitmarker.active { opacity: 1; }
    #hitmarker::before, #hitmarker::after {
      content: '';
      position: absolute;
      background: #ef4444;
    }
    #hitmarker::before { width: 100%; height: 2px; top: 50%; left: 0; transform: translateY(-50%); }
    #hitmarker::after { width: 2px; height: 100%; left: 50%; top: 0; transform: translateX(-50%); }

    /* Bottom-Center: Tactical Ability Hotbar */
    #ability-bar {
      position: absolute;
      bottom: 18px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 10px;
      pointer-events: auto;
    }

    .aslot {
      width: 60px;
      height: 60px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      cursor: pointer;
      backdrop-filter: blur(12px);
      transition: all 0.12s ease;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
    }

    .aslot:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 20px rgba(56, 189, 248, 0.3);
    }

    .aslot.fire { border-color: rgba(249, 115, 22, 0.6); }
    .aslot.lightning { border-color: rgba(56, 189, 248, 0.6); }
    .aslot.ice { border-color: rgba(147, 197, 253, 0.6); }
    .aslot.arcane { border-color: rgba(192, 132, 252, 0.6); }

    .aslot-key {
      position: absolute;
      top: -7px;
      left: 50%;
      transform: translateX(-50%);
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      padding: 1px 5px;
      font-family: 'Orbitron', monospace;
      font-size: 8px;
      font-weight: 700;
      color: #94a3b8;
    }

    .aslot-icon { font-size: 18px; margin-top: 2px; }
    .aslot-name {
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.4px;
      color: #cbd5e1;
      margin-top: 1px;
    }

    .aslot-cost {
      font-family: 'Orbitron', monospace;
      font-size: 8px;
      color: #c084fc;
      position: absolute;
      bottom: 2px;
      right: 4px;
    }

    .cd-overlay {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(10, 15, 28, 0.75);
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Orbitron', monospace;
      font-size: 13px;
      font-weight: 900;
      color: #38bdf8;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.1s ease;
    }

    .cd-overlay.active { opacity: 1; }

    /* Bottom Supernatural Powers Bar */
    #power-bar {
      position: absolute;
      bottom: 86px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 8px;
      pointer-events: auto;
    }

    .pslot {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 6px;
      padding: 4px 12px;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      font-weight: 700;
      color: #e2e8f0;
      cursor: pointer;
      backdrop-filter: blur(8px);
      transition: all 0.12s ease;
    }

    .pslot:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: #38bdf8;
      transform: translateY(-2px);
    }

    .pslot kbd {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 3px;
      padding: 1px 4px;
      font-family: 'Orbitron', monospace;
      font-size: 8px;
      color: #38bdf8;
    }

    /* Minimalist Event Feed / Combat Log */
    #combat-log {
      position: absolute;
      bottom: 18px;
      left: 16px;
      width: 280px;
      max-height: 120px;
      overflow: hidden;
      display: flex;
      flex-direction: column-reverse;
      gap: 3px;
      pointer-events: none;
    }

    .log-item {
      font-size: 11px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(10, 15, 26, 0.65);
      border-left: 2px solid #64748b;
      color: #cbd5e1;
      backdrop-filter: blur(6px);
      animation: fadeIn 0.15s ease-out;
    }

    .log-system { border-color: #38bdf8; color: #bae6fd; }
    .log-damage { border-color: #f87171; color: #fecaca; }
    .log-reward { border-color: #4ade80; color: #bbf7d0; }
    .log-power  { border-color: #fbbf24; color: #fef08a; }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

    /* Tactical Damage Numbers */
    #dmg-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
    .fdmg {
      position: absolute;
      font-family: 'Orbitron', sans-serif;
      font-weight: 900;
      font-size: 16px;
      pointer-events: none;
      animation: floatDmg 0.8s ease-out forwards;
      text-shadow: 0 0 8px rgba(0,0,0,0.8);
    }
    .fdmg.fire { color: #fb923c; }
    .fdmg.lightning { color: #38bdf8; }
    .fdmg.ice { color: #93c5fd; }
    .fdmg.arcane { color: #c084fc; }
    .fdmg.crit { font-size: 22px; color: #facc15; }

    @keyframes floatDmg {
      0% { opacity: 1; transform: translate(-50%, -50%) scale(0.8); }
      20% { transform: translate(-50%, -70%) scale(1.15); }
      100% { opacity: 0; transform: translate(-50%, -120%) scale(0.9); }
    }

    /* Spell Command Input Bar (Priority 5) */
    #spell-cmd-container {
      position: absolute;
      top: 72px;
      left: 50%;
      transform: translateX(-50%);
      width: 440px;
      background: rgba(10, 15, 28, 0.92);
      border: 1px solid #38bdf8;
      border-radius: 8px;
      padding: 8px 12px;
      backdrop-filter: blur(16px);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8), 0 0 16px rgba(56, 189, 248, 0.25);
      display: none;
      flex-direction: column;
      gap: 6px;
      pointer-events: auto;
      z-index: 50;
    }

    #spell-cmd-row {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    #spell-cmd-prefix {
      font-family: 'Orbitron', monospace;
      font-weight: 900;
      font-size: 14px;
      color: #38bdf8;
    }

    #spell-cmd-input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      font-family: 'Rajdhani', sans-serif;
      font-size: 15px;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: 0.5px;
    }

    #spell-cmd-suggestions {
      display: flex;
      flex-direction: column;
      gap: 3px;
      max-height: 160px;
      overflow-y: auto;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 4px;
    }

    .sug-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 4px 8px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 12px;
      color: #cbd5e1;
      transition: background 0.1s;
    }

    .sug-item:hover, .sug-item.selected {
      background: rgba(56, 189, 248, 0.2);
      color: #fff;
    }

    .sug-elem {
      font-size: 9px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
      text-transform: uppercase;
    }

    /* Super Vision 3D HUD Markers Layer */
    #super-vision-overlay {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.3s ease;
      box-shadow: inset 0 0 100px rgba(56, 189, 248, 0.25);
    }

    #super-vision-overlay.active { opacity: 1; }

    .sv-marker {
      position: absolute;
      transform: translate(-50%, -100%);
      pointer-events: none;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .sv-box {
      background: rgba(10, 15, 28, 0.88);
      border: 1px solid #38bdf8;
      border-radius: 4px;
      padding: 3px 7px;
      font-size: 9px;
      font-family: 'Orbitron', sans-serif;
      color: #38bdf8;
      white-space: nowrap;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }

    .sv-box.hostile { border-color: #ef4444; color: #ef4444; box-shadow: 0 0 10px rgba(239, 68, 68, 0.4); }

    .sv-pointer {
      width: 0;
      height: 0;
      border-left: 4px solid transparent;
      border-right: 4px solid transparent;
      border-top: 5px solid #38bdf8;
    }

    /* Modals (Maps, Grimoire, Hero, Settings) */
    .modal-bg {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(4, 6, 12, 0.85);
      backdrop-filter: blur(12px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      pointer-events: auto;
    }

    .modal-bg.active { display: flex; }

    .modal-box {
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 12px;
      padding: 22px;
      width: 760px;
      max-width: 92vw;
      max-height: 86vh;
      overflow-y: auto;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8);
      position: relative;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 10px;
    }

    .modal-title {
      font-family: 'Orbitron', sans-serif;
      font-weight: 800;
      font-size: 15px;
      color: #f8fafc;
      letter-spacing: 1px;
    }

    .close-btn {
      background: none;
      border: none;
      color: #94a3b8;
      font-size: 20px;
      cursor: pointer;
      line-height: 1;
    }

    .close-btn:hover { color: #f87171; }

    .map-grid, .char-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
    }

    .map-card, .char-card {
      background: rgba(10, 15, 26, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      overflow: hidden;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
    }

    .map-card:hover, .char-card:hover {
      border-color: #38bdf8;
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(56, 189, 248, 0.25);
    }

    .map-card.active-map, .char-card.selected {
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
    }

    .map-img-wrap {
      width: 100%;
      height: 110px;
      background: #0f172a;
      overflow: hidden;
      position: relative;
    }

    .map-img { width: 100%; height: 100%; object-fit: cover; }
    .map-info, .char-info { padding: 10px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .map-title, .char-name { font-family: 'Orbitron', sans-serif; font-weight: 700; font-size: 12px; color: #fff; margin-bottom: 4px; }
    .map-desc, .char-desc { font-size: 10px; color: #94a3b8; line-height: 1.3; }

    .btn-primary {
      background: #0284c7;
      border: 1px solid #38bdf8;
      color: #fff;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 700;
      font-size: 11px;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.15s;
    }
    .btn-primary:hover { background: #0369a1; }

    /* Settings Sliders & Radios */
    .setting-group { margin-bottom: 16px; }
    .setting-label { font-size: 12px; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; display: block; }
    .setting-radios { display: flex; gap: 10px; }
    .radio-pill {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      padding: 6px 14px;
      font-size: 11px;
      font-weight: 700;
      color: #94a3b8;
      cursor: pointer;
      transition: all 0.15s;
    }
    .radio-pill.active {
      background: rgba(56, 189, 248, 0.25);
      border-color: #38bdf8;
      color: #38bdf8;
    }

    .toast {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid #38bdf8;
      border-radius: 6px;
      padding: 8px 18px;
      font-family: 'Orbitron', sans-serif;
      font-size: 11px;
      font-weight: 800;
      color: #38bdf8;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
      z-index: 1000;
      opacity: 0;
      transition: opacity 0.2s ease;
      pointer-events: none;
    }
    .toast.active { opacity: 1; }
  </style>
</head>
<body>
''')
''')

