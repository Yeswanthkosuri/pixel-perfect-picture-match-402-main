import os, sys, shutil

print("Building Phase 4 Elemental Arena...")

parts = []

# PART 1: HTML HEAD & CSS STYLES
parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>ELEMENTAL ARENA — Phase 4: Open World, Wildlife, Superpowers & Spell Input</title>
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
      background: #060810;
      font-family: 'Rajdhani', system-ui, -apple-system, sans-serif;
      color: #e5e9f0;
    }

    /* ---- 100% FULL-SCREEN 3D VIEWPORT ---- */
    #canvas-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 1;
      overflow: hidden;
      background: #060810;
    }

    #canvas-container canvas {
      display: block;
      width: 100vw !important;
      height: 100vh !important;
      outline: none;
    }

    /* ---- RESPONSIVE HUD OVERLAY ---- */
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

    /* --- TOP-LEFT: COMBATANT STATUS --- */
    #hud-player {
      position: absolute;
      top: 18px;
      left: 20px;
      background: rgba(10, 15, 28, 0.88);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 12px;
      padding: 14px 18px;
      min-width: 290px;
      backdrop-filter: blur(16px);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7), 0 0 16px rgba(56, 189, 248, 0.15);
      pointer-events: auto;
    }

    #char-name-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .player-header-left {
      display: flex;
      align-items: center;
      gap: 9px;
    }

    #char-avatar-badge {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(168, 85, 247, 0.25));
      border: 1px solid rgba(56, 189, 248, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    #player-char-name {
      font-family: 'Orbitron', sans-serif;
      font-size: 13px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      text-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
    }

    .cbadge {
      font-size: 9px;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(147, 51, 234, 0.25);
      border: 1px solid rgba(168, 85, 247, 0.55);
      color: #c084fc;
      font-weight: 700;
      font-family: 'Orbitron', sans-serif;
    }

    .mbadge {
      font-size: 9px;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(56, 189, 248, 0.2);
      border: 1px solid rgba(56, 189, 248, 0.5);
      color: #38bdf8;
      font-weight: 700;
      letter-spacing: 1px;
      font-family: 'Orbitron', sans-serif;
    }

    .bar-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 5px;
    }

    .bar-lbl {
      width: 52px;
      font-family: 'Orbitron', sans-serif;
      font-size: 9px;
      font-weight: 700;
      color: #94a3b8;
      letter-spacing: 0.5px;
    }

    .bar-track {
      flex: 1;
      height: 7px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 4px;
      overflow: hidden;
      position: relative;
    }

    .bar-fill {
      height: 100%;
      width: 100%;
      transition: width 0.12s cubic-bezier(0.2, 0.9, 0.3, 1);
      border-radius: 3px;
    }

    .bar-fill.hp     { background: linear-gradient(90deg, #dc2626, #f97316); box-shadow: 0 0 10px rgba(239, 68, 68, 0.6); }
    .bar-fill.shield { background: linear-gradient(90deg, #0284c7, #38bdf8); box-shadow: 0 0 10px rgba(56, 189, 248, 0.6); }
    .bar-fill.mana   { background: linear-gradient(90deg, #7c3aed, #c084fc); box-shadow: 0 0 10px rgba(168, 85, 247, 0.6); }
    .bar-fill.stam   { background: linear-gradient(90deg, #059669, #34d399); box-shadow: 0 0 10px rgba(16, 185, 129, 0.6); }

    .bar-val {
      width: 34px;
      text-align: right;
      font-family: 'Orbitron', sans-serif;
      font-size: 10px;
      font-weight: 700;
      color: #cbd5e1;
    }

    /* Active Buff Indicators */
    #buff-row {
      display: flex;
      gap: 6px;
      margin-top: 6px;
      min-height: 20px;
    }
    .buff-pill {
      font-size: 9px;
      font-family: 'Orbitron', sans-serif;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      animation: pulse 1s infinite alternate;
    }
    .buff-speed { background: rgba(56, 189, 248, 0.25); border: 1px solid #38bdf8; color: #38bdf8; }
    .buff-power { background: rgba(239, 68, 68, 0.25); border: 1px solid #ef4444; color: #f87171; }
    .buff-vision { background: rgba(168, 85, 247, 0.25); border: 1px solid #a855f7; color: #c084fc; }

    @keyframes pulse {
      from { opacity: 0.8; }
      to { opacity: 1; transform: scale(1.02); }
    }

    /* --- TOP-CENTER: TARGET RETICLE & STATUS --- */
    #hud-target {
      position: absolute;
      top: 18px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(10, 15, 28, 0.88);
      border: 1px solid rgba(239, 68, 68, 0.45);
      border-radius: 12px;
      padding: 10px 22px;
      min-width: 270px;
      text-align: center;
      backdrop-filter: blur(16px);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7), 0 0 16px rgba(239, 68, 68, 0.2);
    }

    #hud-target-name {
      font-family: 'Orbitron', sans-serif;
      font-size: 12px;
      font-weight: 800;
      color: #f87171;
      letter-spacing: 1.5px;
      margin-bottom: 6px;
      text-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
    }

    #hud-target .bar-track { height: 10px; }

    /* --- TOP-RIGHT: NAVIGATION & MENUS --- */
    #hud-topright {
      position: absolute;
      top: 18px;
      right: 20px;
      display: flex;
      gap: 10px;
      pointer-events: auto;
    }

    .hud-btn {
      background: rgba(12, 18, 32, 0.9);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #93c5fd;
      font-family: 'Orbitron', sans-serif;
      font-size: 10px;
      font-weight: 700;
      padding: 9px 14px;
      border-radius: 8px;
      cursor: pointer;
      backdrop-filter: blur(12px);
      transition: all 0.2s cubic-bezier(0.2, 0.9, 0.3, 1);
      display: flex;
      align-items: center;
      gap: 6px;
      letter-spacing: 0.8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    .hud-btn:hover {
      background: rgba(56, 189, 248, 0.22);
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.5);
      transform: translateY(-1px);
    }

    .hud-btn.cmd-btn {
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
    }

    /* --- ANIMATION / LOCOMOTION BADGE --- */
    #anim-state {
      position: absolute;
      top: 76px;
      right: 20px;
      background: rgba(10, 15, 28, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 8px;
      padding: 6px 14px;
      font-family: 'Orbitron', sans-serif;
      font-size: 10px;
      color: #94a3b8;
      letter-spacing: 0.8px;
      backdrop-filter: blur(10px);
    }
    #anim-state span {
      color: #38bdf8;
      font-weight: 800;
    }

    /* --- CENTER CROSSHAIR & ADS --- */
    #crosshair {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 44px;
      height: 44px;
      pointer-events: none;
      z-index: 12;
      transition: transform 0.15s ease-out;
    }

    .ch-line {
      position: absolute;
      background: rgba(56, 189, 248, 0.9);
      box-shadow: 0 0 6px rgba(56, 189, 248, 0.75);
      transition: all 0.12s ease-out;
    }

    .ch-top    { width: 2px; height: 9px; top: 0; left: 50%; transform: translateX(-50%); }
    .ch-bottom { width: 2px; height: 9px; bottom: 0; left: 50%; transform: translateX(-50%); }
    .ch-left   { height: 2px; width: 9px; left: 0; top: 50%; transform: translateY(-50%); }
    .ch-right  { height: 2px; width: 9px; right: 0; top: 50%; transform: translateY(-50%); }

    .ch-dot {
      position: absolute;
      width: 4px;
      height: 4px;
      background: #38bdf8;
      border-radius: 50%;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      box-shadow: 0 0 8px #38bdf8;
      transition: all 0.12s ease-out;
    }

    #crosshair.spread .ch-top    { transform: translateX(-50%) translateY(-6px); }
    #crosshair.spread .ch-bottom { transform: translateX(-50%) translateY(6px); }
    #crosshair.spread .ch-left   { transform: translateY(-50%) translateX(-6px); }
    #crosshair.spread .ch-right  { transform: translateY(-50%) translateX(6px); }

    /* ADS mode: Call of Duty style precision red dot */
    #crosshair.ads .ch-dot {
      background: #f43f5e;
      box-shadow: 0 0 12px #f43f5e, 0 0 4px #fff;
      transform: translate(-50%, -50%) scale(1.8);
    }
    #crosshair.ads .ch-line {
      opacity: 0.18;
    }

    /* --- HIT MARKER --- */
    #hitmarker {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 36px;
      height: 36px;
      pointer-events: none;
      z-index: 13;
      opacity: 0;
      transition: opacity 0.05s ease-out;
    }
    #hitmarker.active { opacity: 1; }
    .hm {
      position: absolute;
      width: 9px;
      height: 2px;
      background: #ef4444;
      box-shadow: 0 0 8px #ef4444;
    }
    .hm.tl { top: 7px; left: 7px; transform: rotate(45deg); }
    .hm.tr { top: 7px; right: 7px; transform: rotate(-45deg); }
    .hm.bl { bottom: 7px; left: 7px; transform: rotate(-45deg); }
    .hm.br { bottom: 7px; right: 7px; transform: rotate(45deg); }

    /* --- BOTTOM-CENTER: SPELL HOTBAR --- */
    #ability-bar {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 12px;
      background: rgba(10, 15, 28, 0.92);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 16px;
      padding: 10px 18px;
      backdrop-filter: blur(18px);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(56, 189, 248, 0.15);
      pointer-events: auto;
    }

    .aslot {
      position: relative;
      width: 62px;
      height: 62px;
      background: rgba(18, 24, 38, 0.9);
      border: 2px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      overflow: hidden;
      transition: all 0.2s cubic-bezier(0.2, 0.9, 0.3, 1);
    }

    .aslot:hover {
      border-color: rgba(56, 189, 248, 0.8);
      transform: translateY(-3px);
      box-shadow: 0 6px 18px rgba(56, 189, 248, 0.3);
    }

    .aslot.fire      { border-color: rgba(249, 115, 22, 0.7); box-shadow: 0 0 12px rgba(249, 115, 22, 0.3); }
    .aslot.lightning { border-color: rgba(56, 189, 248, 0.7); box-shadow: 0 0 12px rgba(56, 189, 248, 0.3); }
    .aslot.ice       { border-color: rgba(147, 197, 253, 0.7); box-shadow: 0 0 12px rgba(147, 197, 253, 0.3); }
    .aslot.arcane    { border-color: rgba(192, 132, 252, 0.7); box-shadow: 0 0 12px rgba(192, 132, 252, 0.3); }
    .aslot.power     { border-color: rgba(250, 204, 21, 0.7); box-shadow: 0 0 12px rgba(250, 204, 21, 0.3); }

    .aslot-key {
      position: absolute;
      top: 3px;
      left: 4px;
      font-family: 'Orbitron', sans-serif;
      font-size: 8px;
      font-weight: 800;
      color: #94a3b8;
      background: rgba(0, 0, 0, 0.75);
      padding: 1px 4px;
      border-radius: 3px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .aslot-cost {
      position: absolute;
      top: 3px;
      right: 4px;
      font-family: 'Orbitron', sans-serif;
      font-size: 8px;
      font-weight: 700;
      color: #c084fc;
      background: rgba(0, 0, 0, 0.6);
      padding: 1px 3px;
      border-radius: 3px;
    }

    .aslot-icon {
      font-size: 22px;
      margin-bottom: 2px;
      filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.3));
    }

    .aslot-name {
      font-size: 8px;
      font-weight: 800;
      text-transform: uppercase;
      color: #e2e8f0;
      letter-spacing: 0.5px;
    }

    .cd-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 0%;
      background: rgba(5, 8, 16, 0.88);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Orbitron', sans-serif;
      font-size: 15px;
      font-weight: 900;
      color: #38bdf8;
      text-shadow: 0 0 8px rgba(56, 189, 248, 0.7);
      pointer-events: none;
      transition: height 0.05s linear;
    }

    /* --- QUICK POWER SLOTS (Ultra Jump, Speed, Vision) --- */
    #power-bar {
      position: absolute;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 10px;
      pointer-events: auto;
    }
    .pslot {
      background: rgba(10, 15, 28, 0.9);
      border: 1px solid rgba(250, 204, 21, 0.5);
      border-radius: 8px;
      padding: 6px 12px;
      font-family: 'Orbitron', sans-serif;
      font-size: 10px;
      font-weight: 700;
      color: #fef08a;
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      backdrop-filter: blur(12px);
      box-shadow: 0 0 10px rgba(250, 204, 21, 0.2);
      transition: all 0.2s;
    }
    .pslot:hover {
      background: rgba(250, 204, 21, 0.2);
      border-color: #facc15;
      transform: translateY(-2px);
      box-shadow: 0 0 16px rgba(250, 204, 21, 0.5);
    }
    .pslot kbd {
      background: rgba(0, 0, 0, 0.6);
      padding: 1px 5px;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      font-size: 9px;
      color: #38bdf8;
    }

    /* --- SPELL COMMAND INTERFACE (Priority 5) --- */
    #spell-cmd-container {
      position: fixed;
      top: 24px;
      left: 50%;
      transform: translateX(-50%);
      width: 580px;
      max-width: 90vw;
      z-index: 1000;
      display: none;
      pointer-events: auto;
      flex-direction: column;
    }

    #spell-cmd-bar {
      display: flex;
      align-items: center;
      background: rgba(8, 14, 28, 0.96);
      border: 2px solid #38bdf8;
      border-radius: 12px;
      padding: 10px 16px;
      box-shadow: 0 10px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(56, 189, 248, 0.45);
      backdrop-filter: blur(20px);
    }

    #spell-cmd-prompt {
      font-family: 'Orbitron', sans-serif;
      font-weight: 900;
      font-size: 16px;
      color: #38bdf8;
      margin-right: 12px;
      text-shadow: 0 0 8px #38bdf8;
    }

    #spell-cmd-input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      font-family: 'Rajdhani', sans-serif;
      font-size: 19px;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: 1px;
    }
    #spell-cmd-input::placeholder {
      color: #64748b;
      font-style: italic;
    }

    #spell-cmd-close {
      cursor: pointer;
      color: #94a3b8;
      font-size: 16px;
      padding: 2px 6px;
    }
    #spell-cmd-close:hover { color: #fff; }

    #spell-cmd-suggestions {
      margin-top: 6px;
      background: rgba(10, 16, 32, 0.98);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 10px;
      overflow: hidden;
      max-height: 240px;
      overflow-y: auto;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7);
    }

    .cmd-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 9px 16px;
      cursor: pointer;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      transition: background 0.15s;
    }
    .cmd-item:hover, .cmd-item.selected {
      background: rgba(56, 189, 248, 0.22);
      border-left: 4px solid #38bdf8;
    }
    .cmd-item-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .cmd-icon { font-size: 18px; }
    .cmd-name {
      font-family: 'Orbitron', sans-serif;
      font-size: 12px;
      font-weight: 800;
      color: #f1f5f9;
    }
    .cmd-elem-badge {
      font-size: 9px;
      padding: 2px 6px;
      border-radius: 3px;
      font-weight: 700;
      text-transform: uppercase;
      font-family: 'Orbitron', sans-serif;
    }
    .cmd-meta {
      font-size: 11px;
      color: #94a3b8;
      display: flex;
      gap: 12px;
      font-family: 'Orbitron', sans-serif;
    }

    #spell-cmd-hint {
      margin-top: 5px;
      font-size: 10px;
      color: #64748b;
      font-family: 'Orbitron', sans-serif;
      display: flex;
      justify-content: space-between;
      padding: 0 6px;
    }
    #spell-cmd-hint kbd {
      background: rgba(255, 255, 255, 0.1);
      padding: 1px 4px;
      border-radius: 3px;
      color: #93c5fd;
    }

    /* --- SUPER VISION 3D HUD OVERLAY (Priority 4C) --- */
    #super-vision-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 15;
      display: none;
    }
    #super-vision-overlay.active {
      display: block;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.04) 0%, rgba(147, 51, 234, 0.08) 100%);
      box-shadow: inset 0 0 80px rgba(56, 189, 248, 0.25);
    }
    .sv-marker {
      position: absolute;
      transform: translate(-50%, -100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      pointer-events: none;
      transition: transform 0.08s linear;
    }
    .sv-box {
      border: 1px solid #38bdf8;
      background: rgba(10, 16, 32, 0.85);
      border-radius: 6px;
      padding: 4px 8px;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.6);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      min-width: 90px;
    }
    .sv-box.hostile {
      border-color: #ef4444;
      box-shadow: 0 0 14px rgba(239, 68, 68, 0.6);
    }
    .sv-title {
      font-family: 'Orbitron', sans-serif;
      font-size: 9px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: 0.5px;
    }
    .sv-box.hostile .sv-title { color: #f87171; }
    .sv-dist {
      font-family: 'Orbitron', sans-serif;
      font-size: 8px;
      color: #94a3b8;
    }
    .sv-hp {
      width: 100%;
      height: 3px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
      overflow: hidden;
      margin-top: 2px;
    }
    .sv-hp-fill {
      height: 100%;
      background: #22c55e;
      transition: width 0.1s;
    }
    .sv-pointer {
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 6px solid #38bdf8;
      margin-top: -1px;
    }
    .sv-box.hostile + .sv-pointer { border-top-color: #ef4444; }

    /* Ultra Speed Wind Tunnel lines */
    #speed-lines-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9;
      opacity: 0;
      transition: opacity 0.3s;
      background: radial-gradient(circle, transparent 60%, rgba(56, 189, 248, 0.15) 100%);
    }
    #speed-lines-overlay.active { opacity: 1; }

    /* --- BOTTOM-LEFT: EVENT LOG --- */
    #combat-log {
      position: absolute;
      bottom: 20px;
      left: 20px;
      background: rgba(10, 15, 28, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 10px 14px;
      width: 320px;
      height: 110px;
      overflow: hidden;
      font-size: 12px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      gap: 3px;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    .log-line {
      line-height: 1.35;
      animation: fadein 0.2s ease-out;
    }
    @keyframes fadein {
      from { opacity: 0; transform: translateY(3px); }
      to { opacity: 1; transform: none; }
    }
    .log-fire      { color: #fb923c; font-weight: 600; }
    .log-lightning { color: #38bdf8; font-weight: 600; }
    .log-ice       { color: #93c5fd; font-weight: 600; }
    .log-arcane    { color: #c084fc; font-weight: 600; }
    .log-power     { color: #facc15; font-weight: 700; }
    .log-reward    { color: #4ade80; font-weight: 700; }
    .log-damage    { color: #f87171; font-weight: 700; }
    .log-system    { color: #94a3b8; font-style: italic; }

    /* --- BOTTOM-RIGHT: CONTROL GUIDE --- */
    #controls-guide {
      position: absolute;
      bottom: 20px;
      right: 20px;
      background: rgba(10, 15, 28, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 12px;
      padding: 12px 16px;
      font-size: 11px;
      line-height: 1.6;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    #controls-guide kbd {
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.25);
      padding: 1px 6px;
      border-radius: 4px;
      font-family: 'Orbitron', sans-serif;
      font-size: 9px;
      color: #38bdf8;
      font-weight: 700;
    }
    #controls-guide .cg-title {
      font-family: 'Orbitron', sans-serif;
      font-size: 10px;
      font-weight: 800;
      color: #38bdf8;
      margin-bottom: 5px;
      letter-spacing: 0.8px;
    }

    /* --- START / POINTER LOCK OVERLAY --- */
    #start-hint {
      position: fixed;
      top: 55%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(10, 16, 32, 0.94);
      border: 1px solid rgba(56, 189, 248, 0.6);
      border-radius: 14px;
      padding: 20px 32px;
      font-family: 'Orbitron', sans-serif;
      font-size: 15px;
      font-weight: 700;
      color: #38bdf8;
      letter-spacing: 1.5px;
      text-align: center;
      z-index: 15;
      pointer-events: none;
      box-shadow: 0 0 40px rgba(56, 189, 248, 0.35);
      transition: opacity 0.4s ease-out;
    }

    /* --- NOTIFICATION TOAST --- */
    #toast {
      position: fixed;
      top: 85px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(10, 16, 32, 0.95);
      border: 1px solid rgba(56, 189, 248, 0.5);
      box-shadow: 0 0 24px rgba(56, 189, 248, 0.35);
      padding: 9px 24px;
      border-radius: 8px;
      font-family: 'Orbitron', sans-serif;
      font-size: 11px;
      font-weight: 800;
      color: #38bdf8;
      pointer-events: none;
      opacity: 0;
      z-index: 25;
      transition: opacity 0.3s, transform 0.3s;
    }
    #toast.show { opacity: 1; transform: translateX(-50%) translateY(6px); }

    /* --- FLOATING DAMAGE NUMBERS --- */
    #dmg-layer {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 14;
    }
    .fdmg {
      position: absolute;
      font-family: 'Orbitron', sans-serif;
      font-weight: 900;
      font-size: 20px;
      text-shadow: 0 0 10px rgba(0, 0, 0, 0.9);
      pointer-events: none;
      animation: floatup 0.85s ease-out forwards;
      transform: translate(-50%, -50%);
    }
    .fdmg.fire     { color: #fb923c; text-shadow: 0 0 10px rgba(249, 115, 22, 0.9); }
    .fdmg.lightning{ color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.9); }
    .fdmg.ice      { color: #e0f2fe; text-shadow: 0 0 10px rgba(186, 230, 253, 0.9); }
    .fdmg.arcane   { color: #c084fc; text-shadow: 0 0 10px rgba(192, 132, 252, 0.9); }
    .fdmg.crit     { font-size: 26px; }
    @keyframes floatup {
      0%   { opacity: 0; transform: translate(-50%, -20%) scale(0.6); }
      15%  { opacity: 1; transform: translate(-50%, -55%) scale(1.15); }
      70%  { opacity: 0.9; transform: translate(-50%, -110%) scale(1.0); }
      100% { opacity: 0; transform: translate(-50%, -165%) scale(0.85); }
    }

    /* ======== MODALS (MAPS, LOADOUT, GRIMOIRE, AUDIO) ======== */
    .modal-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(4, 6, 14, 0.88);
      backdrop-filter: blur(20px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      pointer-events: auto;
    }
    .modal-box {
      background: #0d1322;
      border: 1px solid rgba(56, 189, 248, 0.45);
      box-shadow: 0 0 60px rgba(56, 189, 248, 0.25);
      border-radius: 18px;
      width: 940px;
      max-width: 95vw;
      max-height: 90vh;
      overflow-y: auto;
      padding: 26px;
    }
    .modal-box.purple-border {
      border-color: rgba(168, 85, 247, 0.45);
      box-shadow: 0 0 60px rgba(168, 85, 247, 0.25);
    }
    .modal-title {
      font-family: 'Orbitron', sans-serif;
      font-size: 17px;
      color: #38bdf8;
      letter-spacing: 1.5px;
      font-weight: 800;
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 14px;
      margin-bottom: 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .close-btn {
      background: none;
      border: none;
      color: #94a3b8;
      font-size: 26px;
      cursor: pointer;
      line-height: 1;
      padding: 0 6px;
    }
    .close-btn:hover { color: #ffffff; }

    /* --- MAP SELECTION GRID (Priority 1) --- */
    .map-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .map-card {
      background: rgba(18, 25, 42, 0.85);
      border: 2px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.2, 0.9, 0.3, 1);
    }
    .map-card:hover {
      border-color: #38bdf8;
      transform: translateY(-4px);
      box-shadow: 0 10px 28px rgba(56, 189, 248, 0.35);
    }
    .map-card.active-map {
      border-color: #38bdf8;
      box-shadow: 0 0 24px rgba(56, 189, 248, 0.45);
      background: rgba(56, 189, 248, 0.1);
    }
    .map-img-wrap { width: 100%; height: 135px; overflow: hidden; background: #000; position: relative; }
    .map-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
    .map-card:hover .map-img { transform: scale(1.06); }
    .map-badge-tag {
      position: absolute;
      top: 8px;
      right: 8px;
      font-family: 'Orbitron', sans-serif;
      font-size: 9px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(0, 0, 0, 0.85);
      color: #38bdf8;
      border: 1px solid #38bdf8;
    }
    .map-badge-tag.official { color: #4ade80; border-color: #4ade80; }
    .map-info { padding: 14px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .map-title { font-family: 'Orbitron', sans-serif; font-size: 13px; font-weight: 800; color: #f1f5f9; margin-bottom: 5px; }
    .map-desc { font-size: 12px; color: #94a3b8; line-height: 1.45; margin-bottom: 12px; }
    .btn-primary {
      background: #0284c7;
      color: #fff;
      font-family: 'Orbitron', sans-serif;
      font-size: 10px;
      font-weight: 800;
      padding: 9px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
      letter-spacing: 0.8px;
    }
    .btn-primary:hover {
      background: #38bdf8;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
    }

    /* --- GRIMOIRE / SPELLBOOK MODAL (Priority 6) --- */
    .spell-tabs { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .tab-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #94a3b8;
      font-family: 'Orbitron', sans-serif;
      font-size: 10px;
      font-weight: 700;
      padding: 7px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tab-btn:hover, .tab-btn.active {
      background: rgba(56, 189, 248, 0.2);
      border-color: #38bdf8;
      color: #38bdf8;
    }
    .grimoire-search-bar {
      margin-bottom: 16px;
      display: flex;
      gap: 10px;
    }
    .search-input {
      flex: 1;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 8px;
      padding: 8px 14px;
      color: #fff;
      font-family: 'Rajdhani', sans-serif;
      font-size: 15px;
      outline: none;
    }
    .search-input:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }

    .spells-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 12px;
      max-height: 520px;
      overflow-y: auto;
      padding-right: 4px;
    }
    .spell-card {
      background: rgba(18, 25, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s;
    }
    .spell-card:hover {
      border-color: #38bdf8;
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
    }
    .spell-card.fire { border-left: 4px solid #fb923c; }
    .spell-card.lightning { border-left: 4px solid #38bdf8; }
    .spell-card.ice { border-left: 4px solid #93c5fd; }
    .spell-card.arcane { border-left: 4px solid #c084fc; }
    .spell-card.power { border-left: 4px solid #facc15; }

    .sc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
    .sc-title { font-family: 'Orbitron', sans-serif; font-size: 12px; font-weight: 800; color: #f1f5f9; display: flex; align-items: center; gap: 6px; }
    .sc-desc { font-size: 11px; color: #94a3b8; line-height: 1.4; margin-bottom: 10px; }
    .sc-stats { display: flex; gap: 10px; font-family: 'Orbitron', sans-serif; font-size: 9px; color: #cbd5e1; margin-bottom: 10px; }
    .sc-cmd-pill {
      font-size: 9px;
      font-family: 'Orbitron', sans-serif;
      padding: 3px 6px;
      border-radius: 4px;
      background: rgba(0, 0, 0, 0.5);
      border: 1px dashed rgba(56, 189, 248, 0.5);
      color: #93c5fd;
      display: inline-block;
      margin-bottom: 8px;
    }
    .sc-footer { display: flex; justify-content: space-between; align-items: center; }

    /* --- HERO LOADOUT & 3D FACE SCAN (Priority 8) --- */
    .loadout-tabs { display: flex; gap: 10px; margin-bottom: 18px; }
    .char-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 18px; }
    .char-card {
      background: rgba(255, 255, 255, 0.04);
      border: 2px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 16px;
      cursor: pointer;
      text-align: center;
      transition: all 0.22s;
    }
    .char-card:hover {
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.1);
      transform: translateY(-2px);
    }
    .char-card.selected {
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.18);
      box-shadow: 0 0 22px rgba(56, 189, 248, 0.45);
    }
    .char-icon { font-size: 34px; margin-bottom: 8px; }
    .char-name { font-family: 'Orbitron', sans-serif; font-size: 12px; font-weight: 800; color: #f1f5f9; }
    .char-desc { font-size: 11px; color: #94a3b8; margin-top: 5px; line-height: 1.4; }

    /* Face Scan UI */
    #facescan-container {
      display: none;
      flex-direction: column;
      gap: 16px;
    }
    .privacy-notice {
      background: rgba(30, 41, 59, 0.7);
      border-left: 4px solid #38bdf8;
      padding: 12px 16px;
      border-radius: 6px;
      font-size: 12px;
      line-height: 1.5;
      color: #cbd5e1;
    }
    .scan-work-area {
      display: flex;
      gap: 20px;
      align-items: flex-start;
    }
    .camera-frame {
      position: relative;
      width: 380px;
      height: 280px;
      background: #000;
      border: 2px solid rgba(56, 189, 248, 0.4);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    #webcam-video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transform: scaleX(-1);
    }
    #face-guide-oval {
      position: absolute;
      width: 160px;
      height: 210px;
      border: 2px dashed #38bdf8;
      border-radius: 50%;
      pointer-events: none;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
    .scan-controls {
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
    }
    .provider-status-box {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(250, 204, 21, 0.4);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 11px;
      line-height: 1.5;
      color: #fde047;
    }
    .provider-status-box code {
      background: rgba(0,0,0,0.5);
      padding: 1px 4px;
      border-radius: 3px;
      color: #fff;
    }

    /* Audio Settings Sliders */
    .slider-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }
    .slider-lbl { font-family: 'Orbitron', sans-serif; font-size: 11px; color: #cbd5e1; width: 140px; }
    .slider-inp { flex: 1; margin: 0 16px; accent-color: #38bdf8; }
    .slider-val { font-family: 'Orbitron', sans-serif; font-size: 11px; color: #38bdf8; width: 40px; text-align: right; }
  </style>
</head>
<body>
''')

print("Part 1 added.")

# PART 2: HTML BODY & HUD DOM
parts.append('''
  <!-- 3D VIEWPORT -->
  <div id="canvas-container"></div>

  <!-- SUPER VISION OVERLAY (Priority 4C) -->
  <div id="super-vision-overlay">
    <div id="super-vision-markers"></div>
  </div>

  <!-- ULTRA SPEED LINES OVERLAY (Priority 4B) -->
  <div id="speed-lines-overlay"></div>

  <!-- CENTER RETICLE & HITMARKER -->
  <div id="crosshair">
    <div class="ch-line ch-top"></div>
    <div class="ch-line ch-bottom"></div>
    <div class="ch-line ch-left"></div>
    <div class="ch-line ch-right"></div>
    <div class="ch-dot"></div>
  </div>
  <div id="hitmarker">
    <div class="hm tl"></div>
    <div class="hm tr"></div>
    <div class="hm bl"></div>
    <div class="hm br"></div>
  </div>

  <!-- DAMAGE NUMBERS LAYER -->
  <div id="dmg-layer"></div>

  <!-- SPELL COMMAND INPUT INTERFACE (Priority 5) -->
  <div id="spell-cmd-container">
    <div id="spell-cmd-bar">
      <span id="spell-cmd-prompt">/</span>
      <input type="text" id="spell-cmd-input" placeholder="Type spell or power name (e.g. 'fireball', 'thunder', 'ultra jump')..." autocomplete="off" spellcheck="false" />
      <span id="spell-cmd-close">&times;</span>
    </div>
    <div id="spell-cmd-suggestions"></div>
    <div id="spell-cmd-hint">
      <span><kbd>&uarr;</kbd> <kbd>&darr;</kbd> Navigate</span>
      <span><kbd>Enter</kbd> Cast Spell / Activate Power</span>
      <span><kbd>Esc</kbd> Close</span>
    </div>
  </div>

  <!-- HUD OVERLAYS -->
  <div id="hud">
    <!-- TOP-LEFT: PLAYER STATUS -->
    <div id="hud-player">
      <div id="char-name-row">
        <div class="player-header-left">
          <div id="char-avatar-badge">🗿</div>
          <span id="player-char-name">ARMORED STONE GOLEM</span>
        </div>
        <span class="mbadge" id="hud-map-badge">SCHOOL</span>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">HEALTH</span>
        <div class="bar-track"><div id="bar-hp" class="bar-fill hp" style="width: 100%;"></div></div>
        <span class="bar-val" id="val-hp">100</span>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">SHIELD</span>
        <div class="bar-track"><div id="bar-shield" class="bar-fill shield" style="width: 100%;"></div></div>
        <span class="bar-val" id="val-shield">50</span>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">MANA</span>
        <div class="bar-track"><div id="bar-mana" class="bar-fill mana" style="width: 100%;"></div></div>
        <span class="bar-val" id="val-mana">100</span>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">STAMINA</span>
        <div class="bar-track"><div id="bar-stam" class="bar-fill stam" style="width: 100%;"></div></div>
        <span class="bar-val" id="val-stam">100</span>
      </div>
      <!-- Active buffs row -->
      <div id="buff-row"></div>
    </div>

    <!-- TOP-CENTER: TARGET RETICLE STATUS -->
    <div id="hud-target">
      <div id="hud-target-name">TARGET ACQUIRED</div>
      <div class="bar-row">
        <span class="bar-lbl" id="lbl-target-hp">HP</span>
        <div class="bar-track"><div id="bar-target-hp" class="bar-fill hp" style="width: 100%;"></div></div>
        <span class="bar-val" id="val-target-hp">100</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; font-family: 'Orbitron', sans-serif; margin-top: 3px;">
        <span>RANGE: <strong id="val-target-dist" style="color: #38bdf8;">--</strong></span>
        <span>STATUS: <strong id="val-target-status" style="color: #4ade80;">ACTIVE</strong></span>
      </div>
    </div>

    <!-- TOP-RIGHT: MENUS & ACTIONS -->
    <div id="hud-topright">
      <button class="hud-btn cmd-btn" id="btn-spell-cmd" title="Open Spell Terminal [/]"><span style="color:#38bdf8;">/</span> SPELL INPUT</button>
      <button class="hud-btn" id="btn-maps"><span style="color:#38bdf8;">🗺</span> MAPS [M]</button>
      <button class="hud-btn" id="btn-spells"><span style="color:#c084fc;">📖</span> GRIMOIRE [G]</button>
      <button class="hud-btn" id="btn-loadout"><span style="color:#fb923c;">⚔</span> HERO [TAB]</button>
      <button class="hud-btn" id="btn-audio"><span style="color:#22c55e;">🔊</span> AUDIO</button>
    </div>

    <!-- ANIMATION & SPEED BADGE -->
    <div id="anim-state">
      MODE: <span id="anim-state-val">IDLE</span> | SPEED: <span id="player-speed-val">0.0</span> m/s
    </div>

    <!-- BOTTOM-CENTER: SUPERNATURAL POWERS BAR (Priority 4) -->
    <div id="power-bar">
      <div class="pslot" id="pslot-jump" onclick="activatePower('ultra-jump')">
        <span>🚀 ULTRA JUMP</span> <kbd>V</kbd> <span id="pcd-jump" style="color:#38bdf8; font-weight:800;"></span>
      </div>
      <div class="pslot" id="pslot-speed" onclick="activatePower('ultra-speed')">
        <span>⚡ ULTRA SPEED</span> <kbd>B</kbd> <span id="pcd-speed" style="color:#38bdf8; font-weight:800;"></span>
      </div>
      <div class="pslot" id="pslot-vision" onclick="activatePower('super-vision')">
        <span>👁️ SUPER VISION</span> <kbd>X</kbd> <span id="pcd-vision" style="color:#38bdf8; font-weight:800;"></span>
      </div>
    </div>

    <!-- BOTTOM-CENTER: SPELL HOTBAR -->
    <div id="ability-bar">
      <div class="aslot fire" id="slot-0" onclick="castSlot(0)">
        <span class="aslot-key">LMB</span>
        <span class="aslot-cost">20</span>
        <span class="aslot-icon" id="si-0">🔥</span>
        <span class="aslot-name" id="sn-0">FIREBALL</span>
        <div class="cd-overlay" id="cd-0"></div>
      </div>
      <div class="aslot fire" id="slot-1" onclick="castSlot(1)">
        <span class="aslot-key">Q</span>
        <span class="aslot-cost">25</span>
        <span class="aslot-icon" id="si-1">💥</span>
        <span class="aslot-name" id="sn-1">FLAME</span>
        <div class="cd-overlay" id="cd-1"></div>
      </div>
      <div class="aslot lightning" id="slot-2" onclick="castSlot(2)">
        <span class="aslot-key">E</span>
        <span class="aslot-cost">22</span>
        <span class="aslot-icon" id="si-2">⚡</span>
        <span class="aslot-name" id="sn-2">THUNDER</span>
        <div class="cd-overlay" id="cd-2"></div>
      </div>
      <div class="aslot ice" id="slot-3" onclick="castSlot(3)">
        <span class="aslot-key">R</span>
        <span class="aslot-cost">15</span>
        <span class="aslot-icon" id="si-3">❄️</span>
        <span class="aslot-name" id="sn-3">ICE SHARD</span>
        <div class="cd-overlay" id="cd-3"></div>
      </div>
      <div class="aslot arcane" id="slot-4" onclick="castSlot(4)">
        <span class="aslot-key">F</span>
        <span class="aslot-cost">24</span>
        <span class="aslot-icon" id="si-4">🔮</span>
        <span class="aslot-name" id="sn-4">ARCANE</span>
        <div class="cd-overlay" id="cd-4"></div>
      </div>
    </div>

    <!-- BOTTOM-LEFT: COMBAT & WILDLIFE LOG -->
    <div id="combat-log"></div>

    <!-- BOTTOM-RIGHT: CONTROL GUIDE -->
    <div id="controls-guide">
      <div class="cg-title">TACTICAL CONTROLS</div>
      <div><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> Locomotion</div>
      <div><kbd>Shift</kbd> Sprint (Tuned Human Speed)</div>
      <div><kbd>Space</kbd> Jump / Climb Steps</div>
      <div><kbd>LMB</kbd> Cast Primary | <kbd>RMB</kbd> Aim Down Sights</div>
      <div><kbd>/</kbd> Open Spell Terminal (Type to Cast)</div>
      <div><kbd>V</kbd> Ultra Jump | <kbd>B</kbd> Ultra Speed | <kbd>X</kbd> Super Vision</div>
      <div><kbd>E</kbd> Collect Animal Rewards</div>
      <div><kbd>G</kbd> Grimoire | <kbd>M</kbd> Maps | <kbd>Tab</kbd> Loadout</div>
    </div>
  </div>

  <!-- START / POINTER LOCK HINT -->
  <div id="start-hint">
    CLICK ANYWHERE TO ENGAGE COMBAT LOCK<br>
    <span style="font-size: 11px; color: #94a3b8; font-weight: 500;">PRESS ESC TO RELEASE MOUSE &bull; PRESS [/] TO TYPE SPELLS</span>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast"></div>

  <!-- ======== MODALS ======== -->

  <!-- MAP SELECTION MODAL (Priority 1) -->
  <div class="modal-bg" id="map-modal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title">EXPLORABLE WORLD SELECTION</div>
        <button class="close-btn" id="close-maps">&times;</button>
      </div>
      <div class="map-grid">
        <!-- School Card -->
        <div class="map-card active-map" data-map="school">
          <div class="map-img-wrap">
            <img src="/assets/maps/previews/school.jpg" class="map-img" alt="School Campus" />
            <span class="map-badge-tag official">SUPPLIED ASSET (GLB)</span>
          </div>
          <div class="map-info">
            <div>
              <div class="map-title">Raimon School Campus</div>
              <div class="map-desc">Your supplied Japanese academic campus loaded from CollegeRaimon.glb. Features academic wings, courtyards, sports field, and clock tower. Native wildlife roaming campus grounds.</div>
            </div>
            <button class="btn-primary" onclick="loadMap('school'); toggleModal('map-modal');">DEPLOY TO SCHOOL</button>
          </div>
        </div>

        <!-- Village Card -->
        <div class="map-card" data-map="village">
          <div class="map-img-wrap">
            <img src="/assets/maps/previews/village.jpg" class="map-img" alt="Fantastic Village" />
            <span class="map-badge-tag official">SUPPLIED ASSET (FBX PACK)</span>
          </div>
          <div class="map-info">
            <div>
              <div class="map-title">Fantastic Medieval Village</div>
              <div class="map-desc">Your supplied Fantastic Village environment built from the 83 building & 337 prop FBX pack. Timber cottages, watchtower, market stalls, cobblestone streets, and woodland wildlife.</div>
            </div>
            <button class="btn-primary" onclick="loadMap('village'); toggleModal('map-modal');">DEPLOY TO VILLAGE</button>
          </div>
        </div>

        <!-- Colosseum Card -->
        <div class="map-card" data-map="colosseum">
          <div class="map-img-wrap">
            <img src="/assets/maps/previews/colosseum.jpg" class="map-img" alt="Colosseum" />
            <span class="map-badge-tag">GLADIATORIAL ARENA</span>
          </div>
          <div class="map-info">
            <div>
              <div class="map-title">Roman Training Colosseum</div>
              <div class="map-desc">High-tech gladiatorial arena with ancient columns, tactical elevated battlements, and automated combat training automata.</div>
            </div>
            <button class="btn-primary" onclick="loadMap('colosseum'); toggleModal('map-modal');">DEPLOY TO ARENA</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- GRIMOIRE / SPELLBOOK MODAL (Priority 6) -->
  <div class="modal-bg" id="spellbook-modal">
    <div class="modal-box purple-border">
      <div class="modal-header">
        <div class="modal-title">📖 MAGICAL GRIMOIRE — SPELL & POWER CATALOGUE</div>
        <button class="close-btn" id="close-spells">&times;</button>
      </div>
      <div class="grimoire-search-bar">
        <input type="text" id="grimoire-search" class="search-input" placeholder="Search spells by name, element, or supernatural power..." oninput="filterGrimoire()" />
      </div>
      <div class="spell-tabs">
        <button class="tab-btn active" onclick="switchGrimoireTab('all')">ALL ABILITIES</button>
        <button class="tab-btn" onclick="switchGrimoireTab('fire')">FIRE 🔥</button>
        <button class="tab-btn" onclick="switchGrimoireTab('lightning')">LIGHTNING ⚡</button>
        <button class="tab-btn" onclick="switchGrimoireTab('ice')">ICE ❄️</button>
        <button class="tab-btn" onclick="switchGrimoireTab('arcane')">ARCANE 🔮</button>
        <button class="tab-btn" onclick="switchGrimoireTab('power')">SUPERPOWERS ✨</button>
      </div>
      <div class="spells-grid" id="grimoire-grid"></div>
    </div>
  </div>

  <!-- HERO LOADOUT & 3D FACE SCAN MODAL (Priority 8) -->
  <div class="modal-bg" id="loadout-modal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title">HERO LOADOUT & AVATAR WORKSHOP</div>
        <button class="close-btn" id="close-loadout">&times;</button>
      </div>
      <div class="loadout-tabs">
        <button class="tab-btn active" id="tab-btn-presets" onclick="switchLoadoutTab('presets')">CHAMPIONS</button>
        <button class="tab-btn" id="tab-btn-facescan" onclick="switchLoadoutTab('facescan')">📷 3D FACE SCANNER</button>
      </div>

      <!-- Presets Tab -->
      <div id="presets-container">
        <div class="char-grid">
          <div class="char-card selected" data-char="golem" onclick="selectChar('golem')">
            <div class="char-icon">🗿</div>
            <div class="char-name">Armored Stone Golem</div>
            <div class="char-desc">Ancient heavy automaton (2.40m). High kinetic resilience and earth-shattering elemental force.</div>
            <span class="cbadge" style="margin-top:8px; display:inline-block;">SUPPLIED FBX RIG</span>
          </div>

          <div class="char-card" data-char="rogue" onclick="selectChar('rogue')">
            <div class="char-icon">🗡️</div>
            <div class="char-name">Shadow Rogue</div>
            <div class="char-desc">Agile void assassin (1.83m human scale). Retargeted 318-bone humanoid locomotion and dual-dagger cast sockets.</div>
            <span class="cbadge" style="margin-top:8px; display:inline-block;">SUPPLIED FBX RIG</span>
          </div>

          <div class="char-card" data-char="assassin" onclick="selectChar('assassin')">
            <div class="char-icon">🥷</div>
            <div class="char-name">Medieval Assassin</div>
            <div class="char-desc">Lethal stealth blade-weaver (1.81m). High agility, lightning cast speed, and twin enchanted daggers.</div>
            <span class="cbadge" style="margin-top:8px; display:inline-block; border-color:#c084fc; color:#c084fc;">SUPPLIED GLTF</span>
          </div>

          <div class="char-card" data-char="scifi" onclick="selectChar('scifi')">
            <div class="char-icon">🛡️</div>
            <div class="char-name">Sci-Fi Trooper</div>
            <div class="char-desc">High-tech elemental exo-soldier (1.82m). Nanoweave armor with glowing power lines and heavy plasma core.</div>
            <span class="cbadge" style="margin-top:8px; display:inline-block; border-color:#38bdf8; color:#38bdf8;">SUPPLIED FBX RIG</span>
          </div>

          <div class="char-card" data-char="mech" onclick="selectChar('mech')">
            <div class="char-icon">🤖</div>
            <div class="char-name">Elemental Mech</div>
            <div class="char-desc">Arcane cybernetic frame (2.0m). Floating shoulder pylons and chest plasma projection core.</div>
            <span class="cbadge" style="margin-top:8px; display:inline-block;">ARCANE CHASSIS</span>
          </div>
        </div>
        <div style="text-align: right;">
          <button class="btn-primary" id="btn-apply-loadout" style="padding: 10px 24px;">CONFIRM CHAMPION</button>
        </div>
      </div>

      <!-- Face Scan Tab (Priority 8) -->
      <div id="facescan-container">
        <div class="privacy-notice">
          <strong>🔒 Privacy & Biometric Consent:</strong> Your camera is used solely to capture a facial reference photo on your local device. The photo is never published or transmitted without explicit action. You can cancel or retake at any time.
        </div>
        <div class="scan-work-area">
          <div class="camera-frame">
            <video id="webcam-video" autoplay playsinline muted></video>
            <div id="face-guide-oval"></div>
            <canvas id="photo-canvas" style="display:none;"></canvas>
            <img id="photo-preview-img" style="display:none; width:100%; height:100%; object-fit:cover;" />
          </div>
          <div class="scan-controls">
            <div style="display:flex; gap:10px;">
              <button class="btn-primary" id="btn-start-camera" onclick="startCamera()">📷 START WEBCAM</button>
              <button class="btn-primary" id="btn-capture-photo" onclick="capturePhoto()" style="display:none; background:#22c55e;">📸 CAPTURE PHOTO</button>
              <button class="btn-primary" id="btn-retake-photo" onclick="retakePhoto()" style="display:none; background:#eab308;">RETAKE</button>
            </div>
            <div>
              <label class="hud-btn" style="display:inline-flex; cursor:pointer;">
                📁 OR UPLOAD PHOTO
                <input type="file" id="file-upload-face" accept="image/*" style="display:none;" onchange="handlePhotoUpload(event)" />
              </label>
            </div>
            
            <div class="provider-status-box" id="provider-box">
              <strong>Avatar Generation Pipeline:</strong><br>
              Status: <span id="avatar-api-status" style="color:#f87171; font-weight:800;">PROVIDER NOT CONFIGURED</span><br>
              <span id="avatar-api-details" style="font-size:10px; color:#cbd5e1;">
                To generate live 3D avatars, configure <code>AVATAR_API_KEY</code> in server environment (supports Ready Player Me or Tripo3D GLB export). Local GLB test chassis is available.
              </span>
            </div>

            <div style="display:flex; gap:10px; margin-top:8px;">
              <button class="btn-primary" id="btn-generate-avatar" onclick="generateAvatarFromPhoto()" style="display:none; background:#8b5cf6;">GENERATE 3D AVATAR</button>
              <button class="btn-primary" id="btn-equip-custom-avatar" onclick="equipCustomAvatar()" style="background:#059669;">EQUIP CUSTOM AVATAR</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- AUDIO SETTINGS MODAL (Priority 7) -->
  <div class="modal-bg" id="audio-modal">
    <div class="modal-box" style="max-width: 500px;">
      <div class="modal-header">
        <div class="modal-title">🔊 3D AUDIO CONFIGURATION</div>
        <button class="close-btn" id="close-audio">&times;</button>
      </div>
      <div class="slider-row">
        <span class="slider-lbl">MASTER VOLUME</span>
        <input type="range" class="slider-inp" min="0" max="100" value="85" id="vol-master" oninput="updateVolumes()" />
        <span class="slider-val" id="val-vol-master">85%</span>
      </div>
      <div class="slider-row">
        <span class="slider-lbl">SOUND EFFECTS (SFX)</span>
        <input type="range" class="slider-inp" min="0" max="100" value="90" id="vol-sfx" oninput="updateVolumes()" />
        <span class="slider-val" id="val-vol-sfx">90%</span>
      </div>
      <div class="slider-row">
        <span class="slider-lbl">AMBIENCE & WIND</span>
        <input type="range" class="slider-inp" min="0" max="100" value="50" id="vol-amb" oninput="updateVolumes()" />
        <span class="slider-val" id="val-vol-amb">50%</span>
      </div>
      <div style="font-size: 11px; color: #94a3b8; line-height: 1.5; margin-top: 14px;">
        Featuring synchronized footsteps with surface variation (Asphalt, Grass, Stone, Wood), distinct elemental sound synthesis, wildlife vocalizations, and supernatural power audio.
      </div>
    </div>
  </div>

  <!-- 3D LIBRARIES -->
  <script src="/assets/libs/three.min.js"></script>
  <script src="/assets/libs/fflate.min.js"></script>
  <script src="/assets/libs/FBXLoader.js"></script>
  <script src="/assets/libs/GLTFLoader.js"></script>
''')

print("Part 2 added.")

# PART 3: AUDIO ENGINE, SPELLS, POWERS, CORE STATE
parts.append('''
<script>
window.addEventListener("error", e => console.error("WINDOW ERROR:", e.error || e.message));
try {

  // ══════════════════════════════════════════════════════════
  //  1. IMMERSIVE 3D GAME AUDIO ENGINE (Priority 7)
  // ══════════════════════════════════════════════════════════
  const SFX = (() => {
    let ctx = null;
    let masterGain = null;
    let sfxGain = null;
    let ambGain = null;
    let ambientSource = null;

    const init = () => {
      if (!ctx) {
        const AC = window.AudioContext || window.webkitAudioContext;
        if (AC) {
          ctx = new AC();
          masterGain = ctx.createGain();
          sfxGain = ctx.createGain();
          ambGain = ctx.createGain();

          masterGain.gain.setValueAtTime(0.85, ctx.currentTime);
          sfxGain.gain.setValueAtTime(0.9, ctx.currentTime);
          ambGain.gain.setValueAtTime(0.5, ctx.currentTime);

          sfxGain.connect(masterGain);
          ambGain.connect(masterGain);
          masterGain.connect(ctx.destination);

          startAmbience();
        }
      }
      if (ctx && ctx.state === 'suspended') ctx.resume();
    };

    const setMasterVol = v => { if (masterGain) masterGain.gain.setValueAtTime(v, ctx.currentTime); };
    const setSfxVol    = v => { if (sfxGain) sfxGain.gain.setValueAtTime(v, ctx.currentTime); };
    const setAmbVol    = v => { if (ambGain) ambGain.gain.setValueAtTime(v, ctx.currentTime); };

    // Procedural Ambient Outdoor Wind Loop
    const startAmbience = () => {
      if (!ctx || ambientSource) return;
      try {
        const sr = ctx.sampleRate;
        const dur = 4.0;
        const buf = ctx.createBuffer(1, Math.floor(sr * dur), sr);
        const d = buf.getChannelData(0);
        let b0 = 0, b1 = 0, b2 = 0;
        for (let i = 0; i < d.length; i++) {
          const white = Math.random() * 2 - 1;
          b0 = 0.997 * b0 + white * 0.05;
          b1 = 0.985 * b1 + white * 0.08;
          b2 = 0.950 * b2 + white * 0.12;
          d[i] = (b0 + b1 + b2) * 0.25;
        }
        ambientSource = ctx.createBufferSource();
        ambientSource.buffer = buf;
        ambientSource.loop = true;

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(320, ctx.currentTime);

        ambientSource.connect(filter);
        filter.connect(ambGain);
        ambientSource.start();
      } catch (e) { console.warn('Ambience init error:', e); }
    };

    const osc = (type, f0, f1, dur, vol = 0.25) => {
      if (!ctx) return;
      const now = ctx.currentTime;
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = type;
      o.frequency.setValueAtTime(f0, now);
      if (f1) o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), now + dur);
      g.gain.setValueAtTime(vol, now);
      g.gain.exponentialRampToValueAtTime(0.001, now + dur);
      o.connect(g);
      g.connect(sfxGain);
      o.start();
      o.stop(now + dur);
    };

    const noise = (dur, vol = 0.35, lp = 450, lp2 = 60) => {
      if (!ctx) return;
      const now = ctx.currentTime, sr = ctx.sampleRate;
      const buf = ctx.createBuffer(1, Math.floor(sr * dur), sr);
      const d = buf.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (d.length * 0.2));
      const s = ctx.createBufferSource();
      s.buffer = buf;
      const f = ctx.createBiquadFilter();
      f.type = 'lowpass';
      f.frequency.setValueAtTime(lp, now);
      f.frequency.exponentialRampToValueAtTime(Math.max(10, lp2), now + dur);
      const g = ctx.createGain();
      g.gain.setValueAtTime(vol, now);
      g.gain.exponentialRampToValueAtTime(0.001, now + dur);
      s.connect(f);
      f.connect(g);
      g.connect(sfxGain);
      s.start();
    };

    return {
      init,
      setMasterVol,
      setSfxVol,
      setAmbVol,

      // Locomotion Footsteps with Surface Discrimination
      step: (surface = 'stone', speedRatio = 1.0) => {
        if (!ctx) return;
        const vol = 0.08 * speedRatio;
        if (surface === 'asphalt') {
          // Sharp pavement slap
          noise(0.07, vol * 1.1, 750, 180);
        } else if (surface === 'grass') {
          // Soft turf rustle
          noise(0.08, vol * 0.85, 340, 80);
        } else if (surface === 'wood') {
          // Hollow timber clop
          osc('triangle', 380, 120, 0.06, vol * 1.2);
          noise(0.05, vol * 0.7, 400, 120);
        } else {
          // Cobblestone / stone
          noise(0.07, vol, 520, 140);
        }
      },

      jump: () => {
        osc('sine', 180, 480, 0.18, 0.22);
        noise(0.12, 0.15, 300, 80);
      },
      land: () => {
        noise(0.22, 0.28, 260, 40);
        osc('sine', 120, 40, 0.15, 0.3);
      },

      // Spell Audio
      fireball: () => {
        osc('sawtooth', 140, 360, 0.32, 0.35);
        noise(0.25, 0.3, 600, 120);
      },
      flameBurst: () => {
        noise(0.48, 0.45, 800, 70);
        osc('triangle', 220, 70, 0.4, 0.3);
      },
      infernoWave: () => {
        noise(0.65, 0.42, 450, 50);
        osc('sine', 160, 45, 0.6, 0.35);
      },
      thunder: () => {
        osc('sawtooth', 2400, 160, 0.22, 0.4);
        noise(0.28, 0.35, 1200, 150);
      },
      ice: () => {
        osc('sine', 1200, 2600, 0.16, 0.28);
        noise(0.18, 0.24, 1800, 400);
      },
      arcane: () => {
        osc('sine', 420, 880, 0.28, 0.3);
        osc('triangle', 880, 240, 0.22, 0.2);
      },

      // Combat Impacts & Chimes
      hit: () => osc('triangle', 1500, 280, 0.08, 0.24),
      crit: () => {
        osc('sawtooth', 1800, 350, 0.12, 0.32);
        osc('sine', 880, 1760, 0.14, 0.2);
      },
      beep: () => osc('sine', 880, 880, 0.08, 0.1),

      // Supernatural Powers Audio (Priority 4)
      ultraJump: () => {
        if (!ctx) return;
        osc('sine', 90, 680, 0.45, 0.45);
        osc('sawtooth', 180, 920, 0.35, 0.25);
        noise(0.5, 0.4, 900, 120);
      },
      ultraSpeed: () => {
        if (!ctx) return;
        osc('sawtooth', 300, 1600, 0.25, 0.35);
        noise(0.45, 0.38, 1400, 250);
      },
      superVision: () => {
        if (!ctx) return;
        osc('sine', 523.25, 1046.5, 0.35, 0.28); // C5 to C6
        setTimeout(() => osc('sine', 659.25, 1318.5, 0.35, 0.25), 60); // E5 to E6
        setTimeout(() => osc('sine', 783.99, 1567.98, 0.4, 0.25), 120); // G5 to G6
      },

      // Wildlife Vocalizations & Reward Chime
      monkeyRoar: () => {
        if (!ctx) return;
        osc('sawtooth', 600, 1800, 0.22, 0.3);
        setTimeout(() => osc('sawtooth', 1600, 700, 0.28, 0.35), 80);
      },
      animalHit: () => {
        osc('triangle', 750, 200, 0.12, 0.28);
        noise(0.1, 0.25, 400, 90);
      },
      rewardPickup: () => {
        if (!ctx) return;
        // Ascending major arpeggio
        osc('sine', 523.25, 523.25, 0.12, 0.25); // C5
        setTimeout(() => osc('sine', 659.25, 659.25, 0.12, 0.25), 70); // E5
        setTimeout(() => osc('sine', 783.99, 783.99, 0.14, 0.25), 140); // G5
        setTimeout(() => osc('sine', 1046.5, 1046.5, 0.28, 0.3), 210); // C6
      }
    };
  })();

  // ══════════════════════════════════════════════════════════
  //  2. UNIFIED SPELL & SUPERNATURAL POWER CATALOGUES
  // ══════════════════════════════════════════════════════════
  const SPELLS = [
    { id:'fireball',         name:'Fireball',         elem:'fire',      icon:'🔥', desc:'Combustion sphere detonating on impact.',                dmg:45,  cd:3.5, range:60, cost:20, playable:true, command:'fireball' },
    { id:'flame-burst',      name:'Flame Burst',      elem:'fire',      icon:'💥', desc:'Incandescent radial shockwave incinerating foes.',       dmg:50,  cd:5.0, range:12, cost:25, playable:true, command:'flame burst' },
    { id:'inferno-wave',     name:'Inferno Wave',     elem:'fire',      icon:'🌊', desc:'Rolling wave of geothermal magma across terrain.',        dmg:38,  cd:6.0, range:35, cost:30, playable:true, command:'inferno wave' },
    { id:'meteor-strike',    name:'Meteor Strike',    elem:'fire',      icon:'☄️', desc:'Calls down a cataclysmic orbital meteorite.',           dmg:120, cd:18.0,range:50, cost:60, playable:false, command:'meteor strike' },
    { id:'flame-dash',       name:'Flame Dash',       elem:'fire',      icon:'💨', desc:'High-speed forward surge leaving a burning trail.',      dmg:20,  cd:8.0, range:18, cost:15, playable:false, command:'flame dash' },
    { id:'firestorm',        name:'Firestorm',        elem:'fire',      icon:'🌪', desc:'Summons a rotating vortex of continuous flame.',          dmg:85,  cd:22.0,range:30, cost:70, playable:false, command:'firestorm' },
    { id:'thunder-surge',    name:'Thunder Surge',    elem:'lightning', icon:'⚡', desc:'High-velocity pinpoint electric discharge.',             dmg:65,  cd:3.2, range:75, cost:22, playable:true, command:'thunder surge' },
    { id:'chain-lightning',  name:'Chain Lightning',  elem:'lightning', icon:'🌩', desc:'Electric arc jumping across multiple adjacent targets.', dmg:55,  cd:7.0, range:45, cost:35, playable:false, command:'chain lightning' },
    { id:'lightning-strike', name:'Lightning Strike', elem:'lightning', icon:'⚡️', desc:'Piercing vertical lightning discharge from above.',    dmg:90,  cd:12.0,range:50, cost:45, playable:false, command:'lightning strike' },
    { id:'thunder-dash',     name:'Thunder Dash',     elem:'lightning', icon:'⚡', desc:'Instantaneous electric blink with discharge burst.',     dmg:30,  cd:6.0, range:20, cost:20, playable:false, command:'thunder dash' },
    { id:'electric-field',   name:'Electric Field',   elem:'lightning', icon:'🌐', desc:'Hazardous electrified grid paralyzing targets.',         dmg:45,  cd:14.0,range:25, cost:40, playable:false, command:'electric field' },
    { id:'overcharge',       name:'Overcharge',       elem:'lightning', icon:'🔋', desc:'Empowers active attacks with bonus electrical energy.',  dmg:0,   cd:25.0,range:0,  cost:50, playable:false, command:'overcharge' },
    { id:'ice-shard',        name:'Ice Shard',        elem:'ice',       icon:'❄️', desc:'Razor-sharp crystalline glacial dart shattering foes.',  dmg:40,  cd:2.5, range:65, cost:15, playable:true, command:'ice shard' },
    { id:'frost-nova',       name:'Frost Nova',       elem:'ice',       icon:'💠', desc:'Radial permafrost ring freezing opponents on contact.',   dmg:35,  cd:8.0, range:12, cost:30, playable:false, command:'frost nova' },
    { id:'ice-wall',         name:'Ice Wall',         elem:'ice',       icon:'🧊', desc:'Solid glacial fortress wall blocking projectiles.',       dmg:0,   cd:16.0,range:20, cost:35, playable:false, command:'ice wall' },
    { id:'frozen-ground',    name:'Frozen Ground',    elem:'ice',       icon:'❄', desc:'Covers ground in slick frost inhibiting movement.',      dmg:20,  cd:10.0,range:30, cost:25, playable:false, command:'frozen ground' },
    { id:'blizzard',         name:'Blizzard',         elem:'ice',       icon:'🌨', desc:'Localized hail blizzard inflicting continuous ice damage.',dmg:70, cd:20.0,range:40, cost:65, playable:false, command:'blizzard' },
    { id:'frost-shield',     name:'Frost Shield',     elem:'ice',       icon:'🛡', desc:'Crystallizes a defensive permafrost layer.',              dmg:0,   cd:15.0,range:0,  cost:40, playable:false, command:'frost shield' },
    { id:'arcane-bolt',      name:'Arcane Bolt',      elem:'arcane',    icon:'🔮', desc:'Concentrated mana projectile causing spatial implosion.', dmg:55,  cd:4.0, range:70, cost:24, playable:true, command:'arcane bolt' },
    { id:'energy-beam',      name:'Energy Beam',      elem:'arcane',    icon:'✨', desc:'Sustained channel of coherent photonic laser energy.',    dmg:60,  cd:9.0, range:45, cost:50, playable:false, command:'energy beam' },
    { id:'blink',            name:'Blink',            elem:'arcane',    icon:'🌀', desc:'Spacetime displacement teleporting 14m forward.',        dmg:0,   cd:7.0, range:14, cost:20, playable:false, command:'blink' },
    { id:'arcane-shield',    name:'Arcane Shield',    elem:'arcane',    icon:'🟣', desc:'Deflective spherical mana ward absorbing damage.',       dmg:0,   cd:18.0,range:0,  cost:35, playable:false, command:'arcane shield' },
    { id:'gravity-pulse',    name:'Gravity Pulse',    elem:'arcane',    icon:'🌌', desc:'Micro-singularity vortex drawing adversaries inward.',    dmg:30,  cd:12.0,range:35, cost:45, playable:false, command:'gravity pulse' },
    { id:'energy-wave',      name:'Energy Wave',      elem:'arcane',    icon:'💫', desc:'Broad crescent wave piercing through multiple targets.',  dmg:45,  cd:7.5, range:40, cost:30, playable:false, command:'energy wave' }
  ];

  // Supernatural Powers (Priority 4)
  const POWERS = [
    {
      id: 'ultra-jump',
      name: 'Ultra Jump',
      elem: 'power',
      icon: '🚀',
      desc: 'Superhuman leap propelling the caster 16m high into the air with ascending energy pillar.',
      cost: 25,
      cd: 10.0,
      command: 'ultra jump',
      duration: 0
    },
    {
      id: 'ultra-speed',
      name: 'Ultra Speed',
      elem: 'power',
      icon: '⚡',
      desc: 'Supernatural kinetic surge boosting movement speed by 240% with zero stamina depletion.',
      cost: 30,
      cd: 18.0,
      command: 'ultra speed',
      duration: 8.0
    },
    {
      id: 'super-vision',
      name: 'Super Vision',
      elem: 'power',
      icon: '👁️',
      desc: 'Heightened clairvoyance marking all wildlife and adversaries with distance and live health.',
      cost: 20,
      cd: 22.0,
      command: 'super vision',
      duration: 12.0
    }
  ];

  // ══════════════════════════════════════════════════════════
  //  3. CORE GAMEPLAY STATE
  // ══════════════════════════════════════════════════════════
  const STATE = {
    map: 'school', // default to user's supplied School map!
    player: {
      maxHp: 100, hp: 100,
      maxShield: 50, shield: 50,
      maxMana: 100, mana: 100,
      maxStam: 100, stam: 100,

      // Locomotion tuning
      walkSpeed: 5.5,
      sprintSpeed: 9.8,
      adsSpeed: 3.4,
      currentSpeed: 0,
      jumpForce: 9.5,
      gravity: 24.0,

      pos: new THREE.Vector3(0, 0.4, 0),
      vel: new THREE.Vector3(0, 0, 0),
      yaw: 0,
      pitch: 0,
      facingYaw: 0,
      grounded: true,
      moveState: 'idle',
      sprinting: false,
      ads: false,
      char: 'golem',

      height: 2.4,
      radius: 0.65,
      eyeHeight: 2.1,

      castTimer: 0,
      stepTimer: 0,
      activeSurface: 'stone'
    },
    powers: {
      ultraJump: { cd: 0, maxCd: 10.0 },
      ultraSpeed: { active: false, timer: 0, maxDur: 8.0, cd: 0, maxCd: 18.0 },
      superVision: { active: false, timer: 0, maxDur: 12.0, cd: 0, maxCd: 22.0 }
    },
    buffs: {
      powerSurge: 0 // +25% spell damage buff from hunting Tiger
    },
    dummy: {
      pos: new THREE.Vector3(0, 0, 22),
      hp: 100, maxHp: 100, dead: false
    },
    slots: ['fireball', 'flame-burst', 'thunder-surge', 'ice-shard', 'arcane-bolt'],
    cds: [0, 0, 0, 0, 0],
    settings: {
      sens: 0.0022,
      volMaster: 0.85,
      volSfx: 0.90,
      volAmb: 0.50
    }
  };
''')

print("Part 3 added.")

# PART 4: THREE.JS SETUP & MAPS (SCHOOL GLB, VILLAGE FBX, COLOSSEUM)
parts.append('''
  // ══════════════════════════════════════════════════════════
  //  4. THREE.JS ENGINE SETUP
  // ══════════════════════════════════════════════════════════
  const container = document.getElementById('canvas-container');
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x7dd3fc);

  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1500);
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'default' });
  } catch(e) {
    renderer = new THREE.WebGLRenderer({ antialias: false });
  }
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  container.appendChild(renderer.domElement);

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  const clock = new THREE.Clock();

  // Environmental Lighting
  const ambLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambLight);

  const sunLight = new THREE.DirectionalLight(0xffffff, 1.3);
  sunLight.position.set(60, 100, 50);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 2048;
  sunLight.shadow.mapSize.height = 2048;
  sunLight.shadow.camera.near = 0.5;
  sunLight.shadow.camera.far = 400;
  const d = 120;
  sunLight.shadow.camera.left = -d;
  sunLight.shadow.camera.right = d;
  sunLight.shadow.camera.top = d;
  sunLight.shadow.camera.bottom = -d;
  sunLight.shadow.bias = -0.0004;
  scene.add(sunLight);

  const spellLight = new THREE.PointLight(0x38bdf8, 0, 30);
  scene.add(spellLight);

  // Map & Collision Roots
  const mapRoot = new THREE.Group();
  scene.add(mapRoot);
  const colliders = [];

  function clearMap() {
    while (mapRoot.children.length > 0) {
      const c = mapRoot.children[0];
      mapRoot.remove(c);
      if (c.geometry) c.geometry.dispose();
      if (c.material) {
        if (Array.isArray(c.material)) c.material.forEach(m => m.dispose());
        else c.material.dispose();
      }
    }
    colliders.length = 0;
    clearWildlife();
    clearRewards();
    if (typeof clearBirdsFlock === 'function') clearBirdsFlock();
  }

  function addColliderBox(box, isStep = false) {
    colliders.push({
      box: box,
      min: box.min.clone(),
      max: box.max.clone(),
      isStep: isStep
    });
  }

  function loadMap(id) {
    STATE.map = id;
    clearMap();
    document.getElementById('hud-map-badge').innerText = id.toUpperCase();

    // Update active state in map selection modal
    document.querySelectorAll('.map-card').forEach(c => {
      c.classList.toggle('active-map', c.getAttribute('data-map') === id);
    });

    if (id === 'school') buildSchool();
    else if (id === 'village') buildVillage();
    else if (id === 'colosseum') buildColosseum();

    // Reset player position & kinematics
    playerGroup.position.copy(STATE.player.pos);
    STATE.player.vel.set(0, 0, 0);
    STATE.player.facingYaw = STATE.player.yaw;
    playerGroup.rotation.y = STATE.player.yaw;
    dummyGroup.position.copy(STATE.dummy.pos);

    // Initial camera position smoothly behind character
    camPos.copy(playerGroup.position).add(new THREE.Vector3(0, 3.5, -6));
    camTarget.copy(playerGroup.position).add(new THREE.Vector3(0, STATE.player.eyeHeight, 0));

    log(`Deployed to [${id.toUpperCase()}]`, 'log-system');
    toast(`WORLD: ${id.toUpperCase()}`);
  }

  // ══════════════════════════════════════════════════════════
  //  MAP 1: SUPPLIED SCHOOL CAMPUS (College Raimon GLB)
  // ══════════════════════════════════════════════════════════
  let schoolGltfLoaded = null;

  function buildSchool() {
    scene.background.setHex(0x7dd3fc);
    scene.fog = new THREE.FogExp2(0xbae6fd, 0.0035);
    ambLight.color.setHex(0xf1f5f9);
    ambLight.intensity = 0.85;
    sunLight.color.setHex(0xfef08a);
    sunLight.intensity = 1.35;
    sunLight.position.set(70, 110, 60);

    STATE.player.activeSurface = 'asphalt';

    // Walkable Ground Plane (Courtyard & sports turf)
    const gnd = new THREE.Mesh(
      new THREE.PlaneGeometry(360, 360),
      new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.9 })
    );
    gnd.rotation.x = -Math.PI / 2;
    gnd.receiveShadow = true;
    mapRoot.add(gnd);

    // Load User's Actual School Model: CollegeRaimon.glb
    const gltfLoader = new THREE.GLTFLoader();
    gltfLoader.load('/assets/maps/school/CollegeRaimon.glb', (gltf) => {
      schoolGltfLoaded = gltf.scene;
      // Scale 0.1 gives authentic ~160m explorable campus footprint
      gltf.scene.scale.setScalar(0.1);
      gltf.scene.position.set(0, 0, 0);

      gltf.scene.traverse(node => {
        if (node.isMesh) {
          node.castShadow = true;
          node.receiveShadow = true;
          if (node.material) {
            node.material.roughness = Math.min(1.0, (node.material.roughness || 0.6) + 0.15);
          }
        }
      });

      mapRoot.add(gltf.scene);

      // Building AABB Colliders for Academy Walls, Gym, & Fences


      // Async GLB mesh attached
    }, undefined, (err) => {
      console.warn("School GLB load error:", err);
    });

    // Immediate Campus Bounding & Architecture Colliders
    addColliderBox(new THREE.Box3(new THREE.Vector3(-45, 0, 20), new THREE.Vector3(45, 18, 55)), false); // Main Academy Wing
    addColliderBox(new THREE.Box3(new THREE.Vector3(-65, 0, -30), new THREE.Vector3(-40, 14, 25)), false); // West Classroom Wing
    addColliderBox(new THREE.Box3(new THREE.Vector3(35, 0, 15), new THREE.Vector3(70, 16, 60)), false); // East Athletic Pavilion
    addColliderBox(new THREE.Box3(new THREE.Vector3(-100, 0, -90), new THREE.Vector3(100, 4, -85)), false); // North Fence
    addColliderBox(new THREE.Box3(new THREE.Vector3(-100, 0, 85), new THREE.Vector3(100, 4, 90)), false); // South Fence
    addColliderBox(new THREE.Box3(new THREE.Vector3(-95, 0, -90), new THREE.Vector3(-90, 4, 90)), false); // West Fence
    addColliderBox(new THREE.Box3(new THREE.Vector3(90, 0, -90), new THREE.Vector3(95, 4, 90)), false); // East Fence

    // Player ground-level spawn in Central Courtyard
    STATE.player.pos.set(0, 0.4, 0);
    STATE.dummy.pos.set(22, 0, 26);

    // Populate Supplied Wildlife in School Environment (Priority 2)
    spawnSchoolWildlife();
    spawnBirdsFlock('school');
  }

  // ══════════════════════════════════════════════════════════
  //  MAP 2: SUPPLIED FANTASTIC MEDIEVAL VILLAGE (FBX Pack)
  // ══════════════════════════════════════════════════════════
  function buildVillage() {
    scene.background.setHex(0xfde68a);
    scene.fog = new THREE.FogExp2(0xfef3c7, 0.005);
    ambLight.color.setHex(0xffedd5);
    ambLight.intensity = 0.9;
    sunLight.color.setHex(0xfb923c);
    sunLight.intensity = 1.4;
    sunLight.position.set(50, 85, 45);

    STATE.player.activeSurface = 'cobblestone';

    const texLdr = new THREE.TextureLoader();
    const grassTex = texLdr.load('/assets/maps/village/textures/T_ENV_TERRAIN_grass_01_BC.png');
    grassTex.wrapS = grassTex.wrapT = THREE.RepeatWrapping;
    grassTex.repeat.set(18, 18);

    const paveTex = texLdr.load('/assets/maps/village/textures/T_ENV_pavingstone_01_BC.png');
    paveTex.wrapS = paveTex.wrapT = THREE.RepeatWrapping;
    paveTex.repeat.set(5, 16);

    // Village Green Grass Terrain
    const gnd = new THREE.Mesh(
      new THREE.PlaneGeometry(280, 280),
      new THREE.MeshStandardMaterial({ map: grassTex, roughness: 0.88 })
    );
    gnd.rotation.x = -Math.PI / 2;
    gnd.receiveShadow = true;
    mapRoot.add(gnd);

    // Main Cobblestone Avenues & Town Plaza
    const rMat = new THREE.MeshStandardMaterial({ map: paveTex, roughness: 0.82 });
    const r1 = new THREE.Mesh(new THREE.PlaneGeometry(16, 200), rMat);
    r1.rotation.x = -Math.PI / 2; r1.position.set(0, 0.02, 10);
    r1.receiveShadow = true;
    mapRoot.add(r1);

    const r2 = new THREE.Mesh(new THREE.PlaneGeometry(160, 16), rMat);
    r2.rotation.x = -Math.PI / 2; r2.position.set(0, 0.03, 10);
    r2.receiveShadow = true;
    mapRoot.add(r2);

    // Town Central Plaza Cobblestone Roundel
    const plaza = new THREE.Mesh(new THREE.CircleGeometry(24, 32), rMat);
    plaza.rotation.x = -Math.PI / 2; plaza.position.set(0, 0.04, 10);
    plaza.receiveShadow = true;
    mapRoot.add(plaza);

    const fbxLdr = new THREE.FBXLoader();

    // 1. Town Central Well (Centerpiece of the square)
    fbxLdr.load('/assets/maps/village/models/SM_PROP_well.fbx', (well) => {
      well.scale.setScalar(0.01);
      well.position.set(0, 0, 10);
      well.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
      mapRoot.add(well);
      addColliderBox(new THREE.Box3(new THREE.Vector3(-2.2, 0, 7.8), new THREE.Vector3(2.2, 3.2, 12.2)), false);
    });

    // 2. Market Stalls Surrounding the Square
    const marketConfigs = [
      { fbx: 'SM_PROP_market_v01_01.fbx', x: -10, z: 18, rot: 0.3 },
      { fbx: 'SM_PROP_market_v03_01.fbx', x: 10, z: 18, rot: -0.3 },
      { fbx: 'SM_PROP_market_v02_01.fbx', x: -14, z: 4, rot: 1.57 },
      { fbx: 'SM_PROP_market_v01_02.fbx', x: 14, z: 4, rot: -1.57 }
    ];
    marketConfigs.forEach(mc => {
      fbxLdr.load('/assets/maps/village/models/' + mc.fbx, (stall) => {
        stall.scale.setScalar(0.01);
        stall.position.set(mc.x, 0, mc.z);
        stall.rotation.y = mc.rot;
        stall.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
        mapRoot.add(stall);
        addColliderBox(new THREE.Box3().setFromObject(stall), false);
      });
    });

    // 3. Campfire & Braziers with Warm Dynamic Lighting
    fbxLdr.load('/assets/maps/village/models/SM_PROP_campfire.fbx', (camp) => {
      camp.scale.setScalar(0.01);
      camp.position.set(0, 0, 26);
      camp.traverse(c => { if (c.isMesh) c.castShadow = true; });
      mapRoot.add(camp);
      const campLight = new THREE.PointLight(0xf97316, 2.2, 18);
      campLight.position.set(0, 1.2, 26);
      mapRoot.add(campLight);
    });

    [-18, 18].forEach(x => {
      fbxLdr.load('/assets/maps/village/models/SM_PROP_brazier_04.fbx', (brazier) => {
        brazier.scale.setScalar(0.01);
        brazier.position.set(x, 0, 10);
        brazier.traverse(c => { if (c.isMesh) c.castShadow = true; });
        mapRoot.add(brazier);
        const bLight = new THREE.PointLight(0xfb923c, 1.4, 12);
        bLight.position.set(x, 1.6, 10);
        mapRoot.add(bLight);
      });
    });

    // 4. Streetlamps along cobblestone avenues with Golden Light
    const lampPositions = [
      { x: -7, z: -18 }, { x: 7, z: -18 },
      { x: -7, z: 38 }, { x: 7, z: 38 },
      { x: -35, z: 10 }, { x: 35, z: 10 }
    ];
    lampPositions.forEach(lp => {
      fbxLdr.load('/assets/maps/village/models/SM_PROP_streetlamp_v01_01.fbx', (lamp) => {
        lamp.scale.setScalar(0.01);
        lamp.position.set(lp.x, 0, lp.z);
        lamp.traverse(c => { if (c.isMesh) c.castShadow = true; });
        mapRoot.add(lamp);
        const lLight = new THREE.PointLight(0xfef08a, 1.2, 14);
        lLight.position.set(lp.x, 3.8, lp.z);
        mapRoot.add(lLight);
        addColliderBox(new THREE.Box3().setFromObject(lamp), false);
      });
    });

    // 5. Timber Cottages & Medieval Mansions
    const houseConfigs = [
      { fbx: 'SM_BLD_body_v01_01.fbx', x: -28, z: 26, rot: 0.4 },
      { fbx: 'SM_BLD_body_v02_01.fbx', x: -30, z: -22, rot: -0.2 },
      { fbx: 'SM_BLD_body_v03_01.fbx', x: 28, z: 28, rot: -0.5 },
      { fbx: 'SM_BLD_body_add_v01_01.fbx', x: 28, z: -22, rot: 0.3 },
      { fbx: 'SM_BLD_body_v01_02.fbx', x: 0, z: 65, rot: 0 },
      { fbx: 'SM_BLD_body_v02_02.fbx', x: -38, z: 52, rot: 0.6 },
      { fbx: 'SM_BLD_body_v01_01.fbx', x: 42, z: -45, rot: -0.7 }
    ];
    houseConfigs.forEach(hc => {
      fbxLdr.load('/assets/maps/village/models/' + hc.fbx, (house) => {
        house.scale.setScalar(0.01);
        house.position.set(hc.x, 0, hc.z);
        house.rotation.y = hc.rot;
        house.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
        mapRoot.add(house);
        addColliderBox(new THREE.Box3().setFromObject(house), false);
      });
    });

    // 6. Watchtowers Guarding North and South Village Entrances
    fbxLdr.load('/assets/maps/village/models/SM_PROP_watchtower_wood_01.fbx', (tower) => {
      tower.scale.setScalar(0.01);
      tower.position.set(-42, 0, -42);
      tower.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
      mapRoot.add(tower);
      addColliderBox(new THREE.Box3().setFromObject(tower), false);
    });

    fbxLdr.load('/assets/maps/village/models/SM_PROP_watchtower_wood_02.fbx', (tower) => {
      tower.scale.setScalar(0.01);
      tower.position.set(42, 0, 72);
      tower.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
      mapRoot.add(tower);
      addColliderBox(new THREE.Box3().setFromObject(tower), false);
    });

    // 7. Scenic Wooden Bridge over Eastern Path
    fbxLdr.load('/assets/maps/village/models/SM_PROP_bridge_wood_01.fbx', (bridge) => {
      bridge.scale.setScalar(0.01);
      bridge.position.set(58, 0, 10);
      bridge.rotation.y = 1.57;
      bridge.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
      mapRoot.add(bridge);
      addColliderBox(new THREE.Box3().setFromObject(bridge), true);
    });

    // 8. Benches, Crates, Sacks, Barrels & Farmsteads
    const benchConfigs = [
      { x: -5, z: 12, rot: 1.57 },
      { x: 5, z: 12, rot: -1.57 }
    ];
    benchConfigs.forEach(bc => {
      fbxLdr.load('/assets/maps/village/models/SM_PROP_bench_01.fbx', (bench) => {
        bench.scale.setScalar(0.01);
        bench.position.set(bc.x, 0, bc.z);
        bench.rotation.y = bc.rot;
        mapRoot.add(bench);
      });
    });

    // Hay Bales & Wooden Carts
    fbxLdr.load('/assets/maps/village/models/SM_PROP_cart_02.fbx', (cart) => {
      cart.scale.setScalar(0.01);
      cart.position.set(22, 0, 8);
      cart.rotation.y = 0.5;
      cart.traverse(c => { if (c.isMesh) c.castShadow = true; });
      mapRoot.add(cart);
      addColliderBox(new THREE.Box3().setFromObject(cart), false);
    });

    fbxLdr.load('/assets/maps/village/models/SM_PROP_hay_06.fbx', (hay) => {
      hay.scale.setScalar(0.01);
      hay.position.set(26, 0, 6);
      hay.traverse(c => { if (c.isMesh) c.castShadow = true; });
      mapRoot.add(hay);
    });

    // Wooden Crates & Sacks Clusters
    const crateConfigs = [
      { fbx: 'SM_PROP_crate_01.fbx', x: -12, z: 20 },
      { fbx: 'SM_PROP_crate_02.fbx', x: -13, z: 19 },
      { fbx: 'SM_PROP_sack_08.fbx', x: 12, z: 20 },
      { fbx: 'SM_PROP_sack_09.fbx', x: 13, z: 19 },
      { fbx: 'SM_PROP_signpost_01.fbx', x: -4, z: -2 }
    ];
    crateConfigs.forEach(cc => {
      fbxLdr.load('/assets/maps/village/models/' + cc.fbx, (prop) => {
        prop.scale.setScalar(0.01);
        prop.position.set(cc.x, 0, cc.z);
        prop.traverse(c => { if (c.isMesh) c.castShadow = true; });
        mapRoot.add(prop);
      });
    });

    // Perimeter Fences
    for (let f = -3; f <= 3; f++) {
      if (f === 0) continue;
      fbxLdr.load('/assets/maps/village/models/SM_PROP_fence_v02_01.fbx', (fence) => {
        fence.scale.setScalar(0.01);
        fence.position.set(f * 9, 0, -28);
        fence.traverse(c => { if (c.isMesh) c.castShadow = true; });
        mapRoot.add(fence);
        addColliderBox(new THREE.Box3().setFromObject(fence), false);
      });
    }

    // Barrels along paths
    for (let i = -2; i <= 2; i++) {
      if (i === 0) continue;
      fbxLdr.load('/assets/maps/village/models/SM_PROP_barrel_05.fbx', (barrel) => {
        barrel.scale.setScalar(0.01);
        barrel.position.set(i * 7, 0, 14);
        barrel.traverse(c => { if (c.isMesh) c.castShadow = true; });
        mapRoot.add(barrel);
        addColliderBox(new THREE.Box3().setFromObject(barrel), false);
      });
    }

    // Village Crossroads Spawn Point
    STATE.player.pos.set(0, 0.4, -10);
    STATE.dummy.pos.set(0, 0, 22);

    // Populate Supplied Wildlife in Village Environment (Priority 2)
    spawnVillageWildlife();
    spawnBirdsFlock('village');
  }

  // ══════════════════════════════════════════════════════════
  //  MAP 3: ROMAN TRAINING COLOSSEUM
  // ══════════════════════════════════════════════════════════
  function buildColosseum() {
    scene.background.setHex(0x060812);
    scene.fog = new THREE.FogExp2(0x060812, 0.012);
    ambLight.color.setHex(0x1e293b);
    ambLight.intensity = 0.7;
    sunLight.color.setHex(0x93c5fd);
    sunLight.intensity = 1.2;
    sunLight.position.set(45, 80, 35);

    STATE.player.activeSurface = 'stone';

    const R = 54;
    const floorM = new THREE.MeshStandardMaterial({ color: 0x0f1523, roughness: 0.4, metalness: 0.8 });
    const floor = new THREE.Mesh(new THREE.CylinderGeometry(R, R, 2, 64), floorM);
    floor.position.y = -1;
    floor.receiveShadow = true;
    mapRoot.add(floor);

    // Perimeter boundary wall
    const wallM = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.7, metalness: 0.4, side: THREE.BackSide });
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(R, R, 9, 64, 1, true), wallM);
    wall.position.y = 4.5;
    mapRoot.add(wall);

    // Tactical platforms & columns
    const platMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.7, roughness: 0.35 });
    [
      { x: 18, z: 18, w: 9, h: 2.2, d: 9 },
      { x: -18, z: 18, w: 9, h: 2.2, d: 9 },
      { x: 18, z: -18, w: 9, h: 2.2, d: 9 },
      { x: -18, z: -18, w: 9, h: 2.2, d: 9 }
    ].forEach(c => {
      const b = new THREE.Mesh(new THREE.BoxGeometry(c.w, c.h, c.d), platMat);
      b.position.set(c.x, c.h / 2, c.z);
      b.castShadow = true; b.receiveShadow = true;
      mapRoot.add(b);
      addColliderBox(new THREE.Box3().setFromObject(b), false);
    });

    STATE.player.pos.set(0, 0.4, -18);
    STATE.dummy.pos.set(0, 0, 22);

    // Spawn sample wildlife in Colosseum for combat testing
    spawnColosseumWildlife();
    spawnBirdsFlock('colosseum');
  }
''')

print("Part 4 added.")

# PART 5: CHARACTERS, WILDLIFE SYSTEM & REWARD DROPS (Priority 2 & 3)
parts.append('''
  // ══════════════════════════════════════════════════════════
  //  5. HERO CHAMPIONS (Stone Golem, Shadow Rogue, Mech)
  // ══════════════════════════════════════════════════════════
  const playerGroup = new THREE.Group();
  playerGroup.position.copy(STATE.player.pos);
  scene.add(playerGroup);

  const golemGroup = new THREE.Group();
  const rogueGroup = new THREE.Group();
  const assassinGroup = new THREE.Group();
  const scifiGroup    = new THREE.Group();
  const mechGroup     = new THREE.Group();
  const customAvatarGroup = new THREE.Group();
  playerGroup.add(golemGroup, rogueGroup, assassinGroup, scifiGroup, mechGroup, customAvatarGroup);

  golemGroup.visible = true;
  rogueGroup.visible = false;
  assassinGroup.visible = false;
  scifiGroup.visible = false;
  mechGroup.visible  = false;
  customAvatarGroup.visible = false;

  let golemMixer = null;
  const golemAnims = {};
  let currentGolemAction = null;
  let currentGolemKey = '';

  let rogueMixer = null;
  const rogueAnims = {};
  let currentRogueAction = null;
  let currentRogueKey = '';

  let rogueHandR = null;
  let golemHandR = null;

  const fbxLdr0  = new THREE.FBXLoader();
  const texLdr00 = new THREE.TextureLoader();

  // PBR Textures for Armored Stone Golem
  const golemBodyAlbedo  = texLdr00.load('/assets/models/stone_golem/textures/T_StoneGolem_Body_Albedo_Skin1.png');
  const golemBodyNormal  = texLdr00.load('/assets/models/stone_golem/textures/T_StoneGolem_Body_Normal.png');
  const golemBodyMetal   = texLdr00.load('/assets/models/stone_golem/textures/T_StoneGolem_Body_Metallic+Gloss.png');
  const golemArmorAlbedo = texLdr00.load('/assets/models/stone_golem/textures/T_StoneGolem_Armor_Albedo_Skin1.png');
  const golemArmorNormal = texLdr00.load('/assets/models/stone_golem/textures/T_StoneGolem_Armor_Normal.png');
  const golemEmission    = texLdr00.load('/assets/models/stone_golem/textures/T_StoneGolem_Armor_Emission.png');

  let golemFbx = null;
  let rogueFbx = null;

  // Load Armored Stone Golem (2.40m fantasy automaton)
  fbxLdr0.load('/assets/models/stone_golem/Mesh/SKM_StoneGolem.fbx', (fbx) => {
    golemFbx = fbx;
    fbx.scale.setScalar(0.0125);
    fbx.position.set(0, 0, 0);

    fbx.traverse(c => {
      if (c.isMesh || c.isSkinnedMesh) {
        c.castShadow = true; c.receiveShadow = true;
        const n = (c.name || '').toLowerCase();
        if (n.includes('armor') || n.includes('belt') || n.includes('helm') || n.includes('greaves') || n.includes('bracer')) {
          c.material = new THREE.MeshStandardMaterial({
            map: golemArmorAlbedo, normalMap: golemArmorNormal, emissiveMap: golemEmission,
            emissive: new THREE.Color(0x331000), roughness: 0.48, metalness: 0.68, skinning: true
          });
        } else {
          c.material = new THREE.MeshStandardMaterial({
            map: golemBodyAlbedo, normalMap: golemBodyNormal, metalnessMap: golemBodyMetal,
            roughness: 0.55, metalness: 0.60, skinning: true
          });
        }
      }
      if (c.isBone) {
        const bn = (c.name || '').toLowerCase();
        if (bn === 'hand_r' || bn === 'weapon_r' || bn === 'lowerarm_twist_01_r') golemHandR = c;
      }
    });

    golemGroup.add(fbx);
    golemMixer = new THREE.AnimationMixer(fbx);
    window.golemMixer = golemMixer;
    window.golemAnims = golemAnims;

    // Load Stone Golem Animation Clips
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@idle1.fbx',   'idle');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@walkF.fbx',   'walkF');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@walkB.fbx',   'walkB');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@walkL.fbx',   'walkL');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@walkR.fbx',   'walkR');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@jogF.fbx',    'jogF');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@jogB.fbx',    'jogB');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@attack1.fbx', 'attack1');
    loadGolemClip('/assets/models/stone_golem/Animations/StoneGolem@gethit1.fbx', 'getHit');
  });

  function loadGolemClip(url, key) {
    fbxLdr0.load(url, (animFbx) => {
      if (!animFbx.animations || !animFbx.animations.length) return;
      const rawClip = animFbx.animations[0];
      const cleanTracks = [];
      rawClip.tracks.forEach(t => {
        if (!t.name.startsWith('.position') && t.name !== 'root.position' && !t.name.startsWith('Armature.position')) {
          cleanTracks.push(t);
        }
      });
      const sanitizedClip = new THREE.AnimationClip(rawClip.name, rawClip.duration, cleanTracks);
      const action = golemMixer.clipAction(sanitizedClip);
      golemAnims[key] = action;

      if (key === 'idle' && !currentGolemAction) playGolemAnim('idle', true);
    });
  }

  function playGolemAnim(key, loop = true, crossFade = 0.2) {
    if (!golemMixer) return;
    const action = golemAnims[key];
    if (!action || currentGolemKey === key) return;
    action.loop = loop ? THREE.LoopRepeat : THREE.LoopOnce;
    action.clampWhenFinished = !loop;
    action.reset();
    if (currentGolemAction && currentGolemAction !== action) {
      currentGolemAction.crossFadeTo(action, crossFade, true);
    }
    action.play();
    currentGolemAction = action;
    currentGolemKey = key;
  }

  // Load Shadow Rogue (1.83m authentic human scale)
  fbxLdr0.load('/assets/models/rogue/rogue_all.fbx', (fbx) => {
    rogueFbx = fbx;
    fbx.scale.setScalar(0.0100);
    fbx.position.set(0, 0, 0);

    fbx.traverse(c => {
      if (c.isMesh || c.isSkinnedMesh) {
        c.castShadow = true; c.receiveShadow = true;
        c.material = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.42, metalness: 0.70, skinning: true });
      }
      if (c.isBone) {
        const bn = (c.name || '').toLowerCase();
        if (bn === 'hand_r' || bn === 'weapon_r' || bn === 'wrist_inner_r') rogueHandR = c;
      }
    });

    rogueGroup.add(fbx);
    rogueMixer = new THREE.AnimationMixer(fbx);
    window.rogueMixer = rogueMixer;
    window.rogueAnims = rogueAnims;

    // Retarget golem clips onto Rogue humanoid skeleton
    Object.keys(golemAnims).forEach(k => {
      const gAct = golemAnims[k];
      if (gAct) retargetClipToRogue(gAct.getClip(), k);
    });
  });

  function retargetClipToRogue(clip, key) {
    if (!rogueMixer) return;
    const rogueTracks = [];
    clip.tracks.forEach(t => {
      if (t.name.endsWith('.quaternion')) {
        const rawBoneName = t.name.split('.')[0];
        const rogueBone = rogueFbx.getObjectByName(rawBoneName);
        if (rogueBone) {
          rogueTracks.push(new THREE.QuaternionKeyframeTrack(`${rawBoneName}.quaternion`, t.times, t.values));
        }
      }
    });
    if (rogueTracks.length > 0) {
      const rClip = new THREE.AnimationClip(`rogue_${key}`, clip.duration, rogueTracks);
      rogueAnims[key] = rogueMixer.clipAction(rClip);
      if (key === 'idle' && !currentRogueAction) playRogueAnim('idle', true);
    }
  }

  function playRogueAnim(key, loop = true, crossFade = 0.2) {
    if (!rogueMixer) return;
    const action = rogueAnims[key];
    if (!action || currentRogueKey === key) return;
    action.loop = loop ? THREE.LoopRepeat : THREE.LoopOnce;
    action.clampWhenFinished = !loop;
    action.reset();
    if (currentRogueAction && currentRogueAction !== action) {
      currentRogueAction.crossFadeTo(action, crossFade, true);
    }
    action.play();
    currentRogueAction = action;
    currentRogueKey = key;
  }

  // 3. Elemental Mech (High-Tech Vanguard Frame)
  const mechBody = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.1, 0.55), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.25, metalness: 0.9 }));
  mechBody.position.y = 1.35;
  mechGroup.add(mechBody);
  const mechArmR = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.85, 8), new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.8 }));
  mechArmR.position.set(0.65, 1.25, 0);
  mechGroup.add(mechArmR);

  // 4. Medieval Assassin Girl (User's Supplied GLTF Model)
  let assassinMesh = null;
  const gltfLdrAssassin = new THREE.GLTFLoader();
  gltfLdrAssassin.load('/assets/models/assassin_girl/scene.gltf', (gltf) => {
    assassinMesh = gltf.scene;
    assassinMesh.scale.setScalar(0.010);
    assassinMesh.position.set(0, 0, 0);
    assassinMesh.traverse(c => {
      if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; }
    });
    assassinGroup.add(assassinMesh);
  });

  // 5. Sci-Fi Trooper Man (User's Supplied FBX Model)
  let scifiMesh = null;
  const scifiTexLdr = new THREE.TextureLoader();
  const scifiTopA = scifiTexLdr.load('/assets/models/hightech_suit/Sci-FI_Trooper_Man_v.3/Textures/T_SciFiTrooperV3_top_a.png');
  const scifiTopN = scifiTexLdr.load('/assets/models/hightech_suit/Sci-FI_Trooper_Man_v.3/Textures/T_SciFiTrooperV3_top_n.png');
  const scifiTopE = scifiTexLdr.load('/assets/models/hightech_suit/Sci-FI_Trooper_Man_v.3/Textures/T_SciFiTrooperV3_top_emissive.png');
  const scifiBtmA = scifiTexLdr.load('/assets/models/hightech_suit/Sci-FI_Trooper_Man_v.3/Textures/T_SciFiTrooperV3_bottom_a.png');
  const scifiBtmN = scifiTexLdr.load('/assets/models/hightech_suit/Sci-FI_Trooper_Man_v.3/Textures/T_SciFiTrooperV3_bottom_n.png');
  const scifiBtmE = scifiTexLdr.load('/assets/models/hightech_suit/Sci-FI_Trooper_Man_v.3/Textures/T_SciFiTrooperV3_bottom_emissive.png');

  fbxLdr0.load('/assets/models/hightech_suit/Sci-FI_Trooper_Man_v.3/Meshes/SK_SciFiTrooperManV3.fbx', (fbx) => {
    scifiMesh = fbx;
    fbx.scale.setScalar(0.010);
    fbx.position.set(0, 0, 0);
    fbx.traverse(c => {
      if (c.isMesh || c.isSkinnedMesh) {
        c.castShadow = true; c.receiveShadow = true;
        const n = (c.name || '').toLowerCase();
        if (n.includes('top') || n.includes('head') || n.includes('chest') || n.includes('arm')) {
          c.material = new THREE.MeshStandardMaterial({
            map: scifiTopA, normalMap: scifiTopN, emissiveMap: scifiTopE,
            emissive: new THREE.Color(0x38bdf8), emissiveIntensity: 1.8,
            roughness: 0.45, metalness: 0.85, skinning: true
          });
        } else {
          c.material = new THREE.MeshStandardMaterial({
            map: scifiBtmA, normalMap: scifiBtmN, emissiveMap: scifiBtmE,
            emissive: new THREE.Color(0x38bdf8), emissiveIntensity: 1.8,
            roughness: 0.45, metalness: 0.85, skinning: true
          });
        }
      }
    });
    scifiGroup.add(fbx);
  });

  // 4. Custom 3D Avatar Chassis (for 3D Face Scan)
  const customAvatarMesh = new THREE.Group();
  const headMesh = new THREE.Mesh(new THREE.SphereGeometry(0.24, 16, 16), new THREE.MeshStandardMaterial({ color: 0xfbcfe8, roughness: 0.6 }));
  headMesh.position.y = 1.65;
  const torsoMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.2, 0.8, 8), new THREE.MeshStandardMaterial({ color: 0x3b82f6, roughness: 0.5 }));
  torsoMesh.position.y = 1.1;
  customAvatarMesh.add(headMesh, torsoMesh);
  customAvatarGroup.add(customAvatarMesh);

  function setChar(charId) {
    STATE.player.char = charId;
    golemGroup.visible = (charId === 'golem');
    rogueGroup.visible = (charId === 'rogue');
    assassinGroup.visible = (charId === 'assassin');
    scifiGroup.visible    = (charId === 'scifi');
    mechGroup.visible     = (charId === 'mech');
    customAvatarGroup.visible = (charId === 'custom');

    const nameEl = document.getElementById('player-char-name');
    const badgeEl = document.getElementById('char-avatar-badge');

    if (charId === 'golem') {
      nameEl.innerText = 'ARMORED STONE GOLEM';
      badgeEl.innerText = '🗿';
      STATE.player.height = 2.40; STATE.player.radius = 0.65; STATE.player.eyeHeight = 2.10;
      playGolemAnim('idle', true);
    } else if (charId === 'rogue') {
      nameEl.innerText = 'SHADOW ROGUE';
      badgeEl.innerText = '🗡️';
      STATE.player.height = 1.83; STATE.player.radius = 0.42; STATE.player.eyeHeight = 1.68;
      playRogueAnim('idle', true);
    } else if (charId === 'assassin') {
      nameEl.innerText = 'MEDIEVAL ASSASSIN';
      badgeEl.innerText = '🥷';
      STATE.player.height = 1.81; STATE.player.radius = 0.42; STATE.player.eyeHeight = 1.68;
      STATE.player.walkSpeed = 5.2; STATE.player.sprintSpeed = 10.2;
    } else if (charId === 'scifi') {
      nameEl.innerText = 'SCI-FI TROOPER';
      badgeEl.innerText = '🛡️';
      STATE.player.height = 1.82; STATE.player.radius = 0.50; STATE.player.eyeHeight = 1.70;
      STATE.player.walkSpeed = 4.8; STATE.player.sprintSpeed = 9.4;
    } else if (charId === 'mech') {
      nameEl.innerText = 'ELEMENTAL MECH';
      badgeEl.innerText = '🤖';
      STATE.player.height = 2.00; STATE.player.radius = 0.50; STATE.player.eyeHeight = 1.80;
    } else if (charId === 'custom') {
      nameEl.innerText = 'CUSTOM 3D AVATAR';
      badgeEl.innerText = '👤';
      STATE.player.height = 1.85; STATE.player.radius = 0.45; STATE.player.eyeHeight = 1.70;
    }

    log(`Champion switched to [${nameEl.innerText}]`, 'log-system');
    toast(`HERO: ${nameEl.innerText}`);
  }

  // ══════════════════════════════════════════════════════════
  //  6. WILDLIFE SYSTEM & HUNTING REWARDS (Priority 2 & 3)
  // ══════════════════════════════════════════════════════════
  const wildlife = [];
  const rewards = [];
  let nextWildlifeId = 1;

  function clearWildlife() {
    for (const w of wildlife) {
      scene.remove(w.mesh);
    }
    wildlife.length = 0;
  }

  function clearRewards() {
    for (const r of rewards) {
      scene.remove(r.mesh);
    }
    rewards.length = 0;
  }

  // ══════════════════════════════════════════════════════════
  //  FLYING BIRDS FLOCK SYSTEM (User's Birds GLTF)
  // ══════════════════════════════════════════════════════════
  const birdFlock = [];

  function clearBirdsFlock() {
    for (const b of birdFlock) {
      scene.remove(b.mesh);
    }
    birdFlock.length = 0;
  }

  function spawnBirdsFlock(mapId) {
    clearBirdsFlock();
    const gltfLdr = new THREE.GLTFLoader();
    gltfLdr.load('/assets/models/birds/scene.gltf', (gltf) => {
      const baseBird = gltf.scene;
      baseBird.scale.setScalar(1.2);
      const animClip = gltf.animations && gltf.animations.length ? gltf.animations[0] : null;

      const birdCount = 5;
      const center = (mapId === 'school') ? new THREE.Vector3(0, 30, 0) : new THREE.Vector3(0, 32, 10);
      const radius = 45;

      for (let i = 0; i < birdCount; i++) {
        const bClone = baseBird.clone();
        bClone.traverse(c => { if (c.isMesh) { c.castShadow = true; } });
        scene.add(bClone);

        let mixer = null;
        if (animClip) {
          mixer = new THREE.AnimationMixer(bClone);
          const act = mixer.clipAction(animClip);
          act.time = (i / birdCount) * animClip.duration;
          act.play();
        }

        birdFlock.push({
          mesh: bClone,
          mixer: mixer,
          center: center,
          angle: (i / birdCount) * Math.PI * 2,
          speed: 0.35 + (i * 0.04),
          radius: radius + (i * 4),
          height: center.y + (i * 2.5 - 5)
        });
      }
    });
  }

  // Animal Textures
  const extraTexLdr = new THREE.TextureLoader();
  const animalSharedTex = extraTexLdr.load('/assets/models/animals_fbx/Animals_FREE/Textures/Texture.png');
  const mBodyTex = extraTexLdr.load('/assets/models/monster/textures_png/Texture Monster/T_Monster_Body_Albedo_Skin1.PNG');
  const mArmorTex = extraTexLdr.load('/assets/models/monster/textures_png/Texture Monster/T_Monster_Armor_Albedo_Skin1.PNG');
  const mSwordTex = extraTexLdr.load('/assets/models/monster/textures_png/Texture Monster/T_Monster_sword_Albedo_Skin1.PNG');

  // Monkey Shared Materials & Loaded Animation Clips
  const monkeyTexLdr = new THREE.TextureLoader();
  const monkeyDiffuse = monkeyTexLdr.load('/assets/models/monkey/textures/Monkey_B1_diffuse.png');
  const monkeyNormal  = monkeyTexLdr.load('/assets/models/monkey/textures/Monkey_B1_normal.png');
  const monkeyRough   = monkeyTexLdr.load('/assets/models/monkey/textures/Monkey_B1_Roughness.png');

  let monkeyTemplateFbx = null;
  const monkeyAnimClips = {};

  // Pre-load Monkey Base Model & Motions
  fbxLdr0.load('/assets/models/monkey/Monkey_B1.Fbx', (fbx) => {
    monkeyTemplateFbx = fbx;
    fbx.traverse(c => {
      if (c.isMesh || c.isSkinnedMesh) {
        c.castShadow = true; c.receiveShadow = true;
        c.material = new THREE.MeshStandardMaterial({
          map: monkeyDiffuse, normalMap: monkeyNormal, roughnessMap: monkeyRough,
          roughness: 0.65, metalness: 0.1, skinning: true
        });
      }
    });

    // Load Monkey Motion FBX files
    const loadAnim = (url, key) => {
      fbxLdr0.load(url, (animFbx) => {
        if (animFbx.animations && animFbx.animations.length) {
          monkeyAnimClips[key] = animFbx.animations[0];
        }
      });
    };

    loadAnim('/assets/models/monkey/animations/Monkey_B1_Idle_Motion.Fbx', 'idle');
    loadAnim('/assets/models/monkey/animations/Monkey_B1_Run_Motion.Fbx',  'run');
    loadAnim('/assets/models/monkey/animations/Monkey_B1_Roar_Motion.Fbx', 'roar');
    loadAnim('/assets/models/monkey/animations/Monkey_B1_Die_Motion.Fbx',  'die');
  });

  // Spawn an Animal Instance
  function spawnAnimal(type, x, z, options = {}) {
    const id = nextWildlifeId++;
    const entity = {
      id,
      type,
      name: options.name || (type.toUpperCase()),
      pos: new THREE.Vector3(x, 0, z),
      spawnPos: new THREE.Vector3(x, 0, z),
      targetPos: new THREE.Vector3(x, 0, z),
      yaw: Math.random() * Math.PI * 2,
      hp: options.hp || 100,
      maxHp: options.hp || 100,
      speed: options.speed || 4.5,
      dead: false,
      state: 'idle',
      stateTimer: Math.random() * 3 + 2,
      alertRadius: options.alertRadius || 12,
      rewardType: options.rewardType || 'mana',
      rewardValue: options.rewardValue || 40,
      mesh: new THREE.Group(),
      mixer: null,
      actions: {},
      currentAction: null
    };

    entity.mesh.position.copy(entity.pos);
    scene.add(entity.mesh);

    if (type === 'monkey') {
      entity.rewardType = 'mana';
      entity.rewardValue = 40;
      entity.name = 'Jungle Monkey';

      const setupMonkeyMesh = (baseFbx) => {
        const monkeyClone = baseFbx.clone();
        monkeyClone.scale.setScalar(0.016); // ~1.15m height
        entity.mesh.add(monkeyClone);

        entity.mixer = new THREE.AnimationMixer(monkeyClone);
        ['idle', 'run', 'roar', 'die'].forEach(k => {
          if (monkeyAnimClips[k]) {
            const act = entity.mixer.clipAction(monkeyAnimClips[k]);
            entity.actions[k] = act;
          }
        });
        if (entity.actions['idle']) {
          entity.actions['idle'].play();
          entity.currentAction = entity.actions['idle'];
        }
      };

      if (monkeyTemplateFbx) {
        setupMonkeyMesh(monkeyTemplateFbx);
      } else {
        fbxLdr0.load('/assets/models/monkey/Monkey_B1.Fbx', setupMonkeyMesh);
      }
    } else if (type === 'deer') {
      entity.rewardType = 'hp';
      entity.rewardValue = 45;
      entity.hp = 75; entity.maxHp = 75;
      entity.speed = 7.5;
      entity.name = 'Wild Deer';

      const gltfLdr = new THREE.GLTFLoader();
      gltfLdr.load('/assets/models/wildlife/deer.glb', (gltf) => {
        gltf.scene.scale.setScalar(1.5);
        gltf.scene.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
        entity.mesh.add(gltf.scene);
      });
    } else if (type === 'tiger') {
      entity.rewardType = 'buff';
      entity.rewardValue = 25; // +25% spell damage
      entity.hp = 150; entity.maxHp = 150;
      entity.speed = 6.2;
      entity.name = 'Apex Tiger';

      const gltfLdr = new THREE.GLTFLoader();
      gltfLdr.load('/assets/models/wildlife/tiger.glb', (gltf) => {
        gltf.scene.scale.setScalar(1.4);
        gltf.scene.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
        entity.mesh.add(gltf.scene);
      });
    } else if (type === 'horse') {
      entity.rewardType = 'stam';
      entity.rewardValue = 50;
      entity.hp = 120; entity.maxHp = 120;
      entity.speed = 8.0;
      entity.name = 'Wild Horse';

      const gltfLdr = new THREE.GLTFLoader();
      gltfLdr.load('/assets/models/wildlife/horse.glb', (gltf) => {
        gltf.scene.scale.setScalar(1.6);
        gltf.scene.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } });
        entity.mesh.add(gltf.scene);
      });
    } else if (type === 'chicken') {
      entity.rewardType = 'stam';
      entity.rewardValue = 35;
      entity.hp = 40; entity.maxHp = 40;
      entity.speed = 3.5;
      entity.name = 'Village Chicken';
      fbxLdr0.load('/assets/models/animals_fbx/Animals_FREE/Meshes/Chicken_001.fbx', (fbx) => {
        fbx.scale.setScalar(1.0);
        fbx.traverse(c => {
          if (c.isMesh) { c.material = new THREE.MeshStandardMaterial({ map: animalSharedTex, roughness: 0.8 }); c.castShadow = true; }
        });
        entity.mesh.add(fbx);
      });
    } else if (type === 'dog') {
      entity.rewardType = 'hp';
      entity.rewardValue = 30;
      entity.hp = 90; entity.maxHp = 90;
      entity.speed = 5.8;
      entity.name = 'Watch Dog';
      fbxLdr0.load('/assets/models/animals_fbx/Animals_FREE/Meshes/Dog_001.fbx', (fbx) => {
        fbx.scale.setScalar(1.1);
        fbx.traverse(c => {
          if (c.isMesh) { c.material = new THREE.MeshStandardMaterial({ map: animalSharedTex, roughness: 0.8 }); c.castShadow = true; }
        });
        entity.mesh.add(fbx);
      });
    } else if (type === 'kitty') {
      entity.rewardType = 'mana';
      entity.rewardValue = 35;
      entity.hp = 45; entity.maxHp = 45;
      entity.speed = 4.8;
      entity.name = 'Feline Prowler';
      fbxLdr0.load('/assets/models/animals_fbx/Animals_FREE/Meshes/Kitty_001.fbx', (fbx) => {
        fbx.scale.setScalar(1.1);
        fbx.traverse(c => {
          if (c.isMesh) { c.material = new THREE.MeshStandardMaterial({ map: animalSharedTex, roughness: 0.8 }); c.castShadow = true; }
        });
        entity.mesh.add(fbx);
      });
    } else if (type === 'penguin') {
      entity.rewardType = 'mana';
      entity.rewardValue = 35;
      entity.hp = 50; entity.maxHp = 50;
      entity.speed = 3.2;
      entity.name = 'Frost Penguin';
      fbxLdr0.load('/assets/models/animals_fbx/Animals_FREE/Meshes/Pinguin_001.fbx', (fbx) => {
        fbx.scale.setScalar(1.0);
        fbx.traverse(c => {
          if (c.isMesh) { c.material = new THREE.MeshStandardMaterial({ map: animalSharedTex, roughness: 0.8 }); c.castShadow = true; }
        });
        entity.mesh.add(fbx);
      });
    } else if (type === 'boss_monster') {
      entity.rewardType = 'boss';
      entity.rewardValue = 80;
      entity.hp = options.hp || 400; entity.maxHp = options.hp || 400;
      entity.speed = options.speed || 4.2;
      entity.name = 'Infernal Dread Fiend';
      entity.alertRadius = 35;

      fbxLdr0.load('/assets/models/monster/Monster/Mesh/Monster%20Skin1.fbx', (fbx) => {
        fbx.scale.setScalar(0.015);
        fbx.traverse(c => {
          if (c.isMesh) {
            c.castShadow = true; c.receiveShadow = true;
            const n = (c.name || '').toLowerCase();
            if (n.includes('armor')) {
              c.material = new THREE.MeshStandardMaterial({ map: mArmorTex, roughness: 0.45, metalness: 0.8 });
            } else {
              c.material = new THREE.MeshStandardMaterial({ map: mBodyTex, roughness: 0.6, metalness: 0.4 });
            }
          }
        });
        entity.mesh.add(fbx);

        fbxLdr0.load('/assets/models/monster/Monster/Mesh/Sword%20Skin1.fbx', (sword) => {
          sword.scale.setScalar(0.015);
          sword.position.set(0.6, 1.4, 0.4);
          sword.rotation.set(0.4, 0, -0.6);
          sword.traverse(sc => {
            if (sc.isMesh) {
              sc.material = new THREE.MeshStandardMaterial({ map: mSwordTex, roughness: 0.35, metalness: 0.9 });
              sc.castShadow = true;
            }
          });
          entity.mesh.add(sword);
        });
      });
    }

    wildlife.push(entity);
    return entity;
  }

  // Populate Environments with Configured Wildlife
  function spawnSchoolWildlife() {
    spawnAnimal('monkey', -16, 12, { alertRadius: 10 });
    spawnAnimal('monkey', 18, -14, { alertRadius: 10 });
    spawnAnimal('deer', 42, 25, { alertRadius: 15 });
    spawnAnimal('deer', 48, -20, { alertRadius: 15 });
    spawnAnimal('dog', -25, 5, { alertRadius: 12 });
    spawnAnimal('chicken', -8, -10, { alertRadius: 7 });
    spawnAnimal('kitty', 12, 16, { alertRadius: 8 });
    spawnAnimal('tiger', -45, -60, { alertRadius: 16 });
    spawnAnimal('boss_monster', 0, 75, { hp: 400, speed: 4.2 });
  }

  function spawnVillageWildlife() {
    spawnAnimal('monkey', -8, 14, { alertRadius: 9 });
    spawnAnimal('monkey', 12, 10, { alertRadius: 9 });
    spawnAnimal('chicken', -3, 8, { alertRadius: 6 });
    spawnAnimal('chicken', 3, 14, { alertRadius: 6 });
    spawnAnimal('kitty', -15, 6, { alertRadius: 7 });
    spawnAnimal('dog', -6, -8, { alertRadius: 11 });
    spawnAnimal('deer', -45, -15, { alertRadius: 16 });
    spawnAnimal('deer', -50, 25, { alertRadius: 16 });
    spawnAnimal('horse', 32, 14, { alertRadius: 14 });
    spawnAnimal('tiger', 45, -45, { alertRadius: 18 });
    spawnAnimal('boss_monster', 0, 88, { hp: 400, speed: 4.2 });
  }

  function spawnColosseumWildlife() {
    spawnAnimal('monkey', -12, 12, { alertRadius: 10 });
    spawnAnimal('deer', 14, 14, { alertRadius: 12 });
    spawnAnimal('tiger', -18, -18, { alertRadius: 14 });
    spawnAnimal('penguin', 0, 16, { alertRadius: 8 });
    spawnAnimal('boss_monster', 0, 0, { hp: 400, speed: 4.5 });
  }

  // Play Wildlife Skeletal Animation
  function playAnimalAnim(entity, animKey, loop = true) {
    if (!entity.mixer || !entity.actions[animKey]) return;
    const nextAction = entity.actions[animKey];
    if (entity.currentAction === nextAction) return;
    nextAction.loop = loop ? THREE.LoopRepeat : THREE.LoopOnce;
    nextAction.clampWhenFinished = !loop;
    nextAction.reset();
    if (entity.currentAction) entity.currentAction.crossFadeTo(nextAction, 0.2, true);
    nextAction.play();
    entity.currentAction = nextAction;
  }

  // Wildlife Combat & Hunting Loop (Priority 3)
  function damageWildlife(entity, amount, elem = 'fire') {
    if (entity.dead) return;

    const isCrit = Math.random() < 0.25;
    // Check if player has Tiger Power Surge buff (+25% damage)
    const buffMultiplier = STATE.buffs.powerSurge > 0 ? 1.25 : 1.0;
    const finalDmg = Math.round((isCrit ? amount * 1.5 : amount) * buffMultiplier);

    entity.hp = Math.max(0, entity.hp - finalDmg);
    SFX.hit();
    flashHitMarker();

    // Damage Number Floating in 3D
    spawnDmgNum(finalDmg, entity.pos.clone().add(new THREE.Vector3(0, 1.8, 0)), elem, isCrit);

    // Hit Reaction: flash white and trigger vocalization
    entity.mesh.traverse(c => {
      if (c.isMesh && c.material) {
        const origColor = c.material.color.clone();
        c.material.color.setHex(0xffffff);
        setTimeout(() => { if (c.material) c.material.color.copy(origColor); }, 120);
      }
    });

    if (entity.type === 'monkey') {
      SFX.monkeyRoar();
      playAnimalAnim(entity, 'roar', false);
    } else {
      SFX.animalHit();
    }

    log(`Hit [${entity.name}] for ${finalDmg} ${elem.toUpperCase()} damage! (HP: ${entity.hp}/${entity.maxHp})`, 'log-damage');

    // Update target HUD to reflect animal stats
    document.getElementById('hud-target-name').innerText = entity.name.toUpperCase();
    document.getElementById('val-target-hp').innerText = entity.hp;
    document.getElementById('bar-target-hp').style.width = `${(entity.hp / entity.maxHp) * 100}%`;
    const dist = Math.round(playerGroup.position.distanceTo(entity.pos));
    document.getElementById('val-target-dist').innerText = `${dist}m`;
    document.getElementById('val-target-status').innerText = entity.hp > 0 ? 'ALERT' : 'DEFEATED';

    if (entity.hp <= 0) {
      killWildlife(entity);
    } else {
      // Retaliate or flee based on nature
      if (entity.type === 'deer' || entity.type === 'horse' || entity.hp < 30) {
        entity.state = 'flee';
      } else {
        entity.state = 'attack';
      }
    }
  }

  // Wildlife Death & Reward Spawn
  function killWildlife(entity) {
    if (entity.dead) return;
    entity.dead = true;
    entity.state = 'dead';

    log(`💥 [${entity.name}] DEFEATED! Collect the dropped reward.`, 'log-reward');
    toast(`DEFEATED: ${entity.name.toUpperCase()}`);

    if (entity.type === 'monkey' && entity.actions['die']) {
      playAnimalAnim(entity, 'die', false);
    } else {
      // Procedural collapse
      entity.mesh.rotation.z = Math.PI / 2;
      entity.mesh.position.y = 0.2;
    }

    // Spawn 3D Collectible Reward Drop (Priority 3)
    spawnReward(entity.rewardType, entity.pos.clone().add(new THREE.Vector3(0, 0.8, 0)), entity.rewardValue);

    // Fade out defeated animal mesh after 5 seconds
    setTimeout(() => {
      scene.remove(entity.mesh);
    }, 5000);
  }

  // 3D Collectible Reward Item
  function spawnReward(type, pos, val) {
    const rGroup = new THREE.Group();
    rGroup.position.copy(pos);

    // Glowing Fantasy Crystal Octahedron
    let color = 0x38bdf8;
    if (type === 'hp') color = 0x22c55e;
    else if (type === 'mana') color = 0xa855f7;
    else if (type === 'buff') color = 0xef4444;
    else if (type === 'stam') color = 0xfacc15;

    const gemMat = new THREE.MeshStandardMaterial({
      color: color, emissive: color, emissiveIntensity: 0.6,
      roughness: 0.2, metalness: 0.8
    });
    const gem = new THREE.Mesh(new THREE.OctahedronGeometry(0.45, 0), gemMat);
    gem.castShadow = true;
    rGroup.add(gem);

    // Pulsing Point Light & Ring
    const pLight = new THREE.PointLight(color, 1.5, 6);
    rGroup.add(pLight);

    const ring = new THREE.Mesh(
      new THREE.RingGeometry(0.55, 0.65, 24),
      new THREE.MeshBasicMaterial({ color: color, side: THREE.DoubleSide, transparent: true, opacity: 0.7 })
    );
    ring.rotation.x = Math.PI / 2;
    rGroup.add(ring);

    scene.add(rGroup);

    const reward = {
      type,
      val,
      pos: pos.clone(),
      mesh: rGroup,
      collected: false,
      pulseTime: 0
    };
    rewards.push(reward);
  }

  function collectReward(r) {
    if (r.collected) return;
    r.collected = true;

    SFX.rewardPickup();
    scene.remove(r.mesh);

    if (r.type === 'mana') {
      STATE.player.mana = Math.min(STATE.player.maxMana, STATE.player.mana + r.val);
      toast(`REWARD: +${r.val} MANA (Monkey Rune)`);
      log(`Collected Monkey Rune: Restored +${r.val} Mana!`, 'log-reward');
    } else if (r.type === 'hp') {
      STATE.player.hp = Math.min(STATE.player.maxHp, STATE.player.hp + r.val);
      toast(`REWARD: +${r.val} HEALTH (Vitality Venison)`);
      log(`Collected Vitality Venison: Restored +${r.val} Health!`, 'log-reward');
    } else if (r.type === 'buff') {
      STATE.buffs.powerSurge = 20.0; // 20s duration
      toast(`BUFF: +25% SPELL POWER (Apex Tiger Essence)`);
      log(`Empowered with Apex Tiger Essence: +25% Spell Damage for 20s!`, 'log-power');
    } else if (r.type === 'stam') {
      STATE.player.stam = Math.min(STATE.player.maxStam, STATE.player.stam + r.val);
      toast(`REWARD: +${r.val} STAMINA (Steed Essence)`);
      log(`Collected Steed Essence: Restored +${r.val} Stamina!`, 'log-reward');
    }

    updatePlayerHUD();
  }
''')

print("Part 5 added.")

# PART 6: SUPERNATURAL POWERS, SPELL COMMAND INTERFACE, GRIMOIRE & FACE SCAN
parts.append('''
  // ══════════════════════════════════════════════════════════
  //  7. SUPERNATURAL POWERS (Priority 4)
  // ══════════════════════════════════════════════════════════
  function activatePower(powerId) {
    SFX.init();
    const p = STATE.player;

    if (powerId === 'ultra-jump') {
      const pow = STATE.powers.ultraJump;
      if (pow.cd > 0) {
        log(`Ultra Jump cooling down (${pow.cd.toFixed(1)}s)`, 'log-system');
        return;
      }
      if (p.mana < 25) {
        log(`Insufficient mana for Ultra Jump (${Math.round(p.mana)}/25)`, 'log-system');
        return;
      }

      p.mana -= 25;
      pow.cd = pow.maxCd;
      p.vel.y = 22.0; // 22 m/s -> launches player 16m high into the air!
      p.grounded = false;
      p.moveState = 'jump';

      SFX.ultraJump();

      // Ground shockwave ring effect
      spawnShockwave(playerGroup.position.clone(), 'power');
      toast('SUPERNATURAL POWER: ULTRA JUMP!');
      log('Activated ULTRA JUMP! Vaulting 16m into the stratosphere.', 'log-power');

    } else if (powerId === 'ultra-speed') {
      const pow = STATE.powers.ultraSpeed;
      if (pow.cd > 0) {
        log(`Ultra Speed cooling down (${pow.cd.toFixed(1)}s)`, 'log-system');
        return;
      }
      if (p.mana < 30) {
        log(`Insufficient mana for Ultra Speed (${Math.round(p.mana)}/30)`, 'log-system');
        return;
      }

      p.mana -= 30;
      pow.active = true;
      pow.timer = pow.maxDur;
      pow.cd = pow.maxCd;

      SFX.ultraSpeed();
      document.getElementById('speed-lines-overlay').classList.add('active');

      toast('SUPERNATURAL POWER: ULTRA SPEED (8s)!');
      log('Activated ULTRA SPEED! Kinetic velocity multiplied by 240%.', 'log-power');

    } else if (powerId === 'super-vision') {
      const pow = STATE.powers.superVision;
      if (pow.cd > 0) {
        log(`Super Vision cooling down (${pow.cd.toFixed(1)}s)`, 'log-system');
        return;
      }
      if (p.mana < 20) {
        log(`Insufficient mana for Super Vision (${Math.round(p.mana)}/20)`, 'log-system');
        return;
      }

      p.mana -= 20;
      pow.active = true;
      pow.timer = pow.maxDur;
      pow.cd = pow.maxCd;

      SFX.superVision();
      document.getElementById('super-vision-overlay').classList.add('active');

      toast('SUPERNATURAL POWER: SUPER VISION (12s)!');
      log('Activated SUPER VISION! Clairvoyance radar tracking all entities.', 'log-power');
    }

    updatePlayerHUD();
  }

  // Visual Shockwave Ring
  function spawnShockwave(pos, type = 'power') {
    const geom = new THREE.RingGeometry(0.5, 1.2, 32);
    const col = (type === 'power') ? 0xfacc15 : 0x38bdf8;
    const mat = new THREE.MeshBasicMaterial({ color: col, side: THREE.DoubleSide, transparent: true, opacity: 0.9 });
    const ring = new THREE.Mesh(geom, mat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.copy(pos).add(new THREE.Vector3(0, 0.1, 0));
    scene.add(ring);

    particles.push({
      mesh: ring,
      isRing: true,
      scaleSpeed: 24,
      life: 0.6,
      maxLife: 0.6
    });
  }

  // ══════════════════════════════════════════════════════════
  //  8. SPELL COMMAND INTERFACE (Type to Cast - Priority 5)
  // ══════════════════════════════════════════════════════════
  const spellCmdContainer = document.getElementById('spell-cmd-container');
  const spellCmdInput = document.getElementById('spell-cmd-input');
  const spellCmdSuggestions = document.getElementById('spell-cmd-suggestions');
  let cmdOpen = false;
  let selectedSuggestionIdx = 0;
  let currentSuggestions = [];

  function openSpellCommand() {
    cmdOpen = true;
    spellCmdContainer.style.display = 'flex';
    spellCmdInput.value = '';
    selectedSuggestionIdx = 0;
    if (document.pointerLockElement) document.exitPointerLock();
    renderCommandSuggestions('');
    setTimeout(() => spellCmdInput.focus(), 50);
  }

  function closeSpellCommand() {
    cmdOpen = false;
    spellCmdContainer.style.display = 'none';
    spellCmdInput.value = '';
    spellCmdInput.blur();
  }

  document.getElementById('btn-spell-cmd').onclick = () => {
    if (cmdOpen) closeSpellCommand();
    else openSpellCommand();
  };
  document.getElementById('spell-cmd-close').onclick = closeSpellCommand;

  spellCmdInput.addEventListener('input', e => {
    renderCommandSuggestions(e.target.value);
  });

  spellCmdInput.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      e.preventDefault();
      closeSpellCommand();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (currentSuggestions.length > 0) {
        selectedSuggestionIdx = (selectedSuggestionIdx + 1) % currentSuggestions.length;
        highlightSuggestion();
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (currentSuggestions.length > 0) {
        selectedSuggestionIdx = (selectedSuggestionIdx - 1 + currentSuggestions.length) % currentSuggestions.length;
        highlightSuggestion();
      }
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (currentSuggestions.length > 0 && currentSuggestions[selectedSuggestionIdx]) {
        executeSpellCommand(currentSuggestions[selectedSuggestionIdx].command);
      } else {
        executeSpellCommand(spellCmdInput.value.trim());
      }
      closeSpellCommand();
    }
  });

  // Autocomplete Suggestions from Unified Catalogue
  function renderCommandSuggestions(query) {
    const q = query.toLowerCase().replace(/^(cast|use)\s+/, '').trim();
    // Search combined spells and powers
    const all = [...SPELLS.map(s => ({ ...s, isPower: false })), ...POWERS.map(p => ({ ...p, isPower: true }))];
    currentSuggestions = all.filter(item => {
      if (!q) return true;
      return item.name.toLowerCase().includes(q) ||
             item.command.toLowerCase().includes(q) ||
             item.elem.toLowerCase().includes(q);
    });

    selectedSuggestionIdx = 0;
    spellCmdSuggestions.innerHTML = '';

    if (currentSuggestions.length === 0) {
      spellCmdSuggestions.innerHTML = '<div style="padding:12px; font-size:12px; color:#94a3b8; font-style:italic;">No matching spells or powers found.</div>';
      return;
    }

    currentSuggestions.slice(0, 7).forEach((item, idx) => {
      const el = document.createElement('div');
      el.className = `cmd-item ${idx === 0 ? 'selected' : ''}`;
      el.innerHTML = `
        <div class="cmd-item-left">
          <span class="cmd-icon">${item.icon}</span>
          <div>
            <span class="cmd-name">${item.name}</span>
            <span class="cmd-elem-badge" style="background:${elemColor(item.elem)}22; color:${elemColor(item.elem)};">${item.elem}</span>
          </div>
        </div>
        <div class="cmd-meta">
          <span>${item.isPower ? 'POWER' : item.dmg + ' DMG'}</span>
          <span style="color:#c084fc;">${item.cost} MANA</span>
          <span style="color:#38bdf8;">${item.cd}s CD</span>
        </div>
      `;
      el.onclick = () => {
        executeSpellCommand(item.command);
        closeSpellCommand();
      };
      spellCmdSuggestions.appendChild(el);
    });
  }

  function highlightSuggestion() {
    const items = spellCmdSuggestions.querySelectorAll('.cmd-item');
    items.forEach((it, i) => {
      it.classList.toggle('selected', i === selectedSuggestionIdx);
    });
  }

  // Execute Real Spell or Supernatural Power from Command String
  function executeSpellCommand(rawCmd) {
    if (!rawCmd) return;
    const cmd = rawCmd.toLowerCase().replace(/^(cast|use)\s+/, '').trim();

    // Check Supernatural Powers
    const powerMatch = POWERS.find(p => p.command.toLowerCase() === cmd || p.name.toLowerCase() === cmd);
    if (powerMatch) {
      activatePower(powerMatch.id);
      return;
    }

    // Check Spell Catalog
    const spellMatch = SPELLS.find(s => s.command.toLowerCase() === cmd || s.name.toLowerCase() === cmd || s.id === cmd);
    if (spellMatch) {
      // Find slot index or cast directly
      let slotIdx = STATE.slots.indexOf(spellMatch.id);
      if (slotIdx >= 0) {
        castSlot(slotIdx);
      } else {
        // Cast directly even if not bound to hotbar
        castSpellDirect(spellMatch);
      }
      return;
    }

    log(`Unknown command: "${rawCmd}". Open Grimoire [G] for spell names.`, 'log-system');
    toast(`UNKNOWN: "${rawCmd}"`);
  }

  function castSpellDirect(spell) {
    if (STATE.player.mana < spell.cost) {
      log(`Insufficient mana for ${spell.name} (${Math.round(STATE.player.mana)}/${spell.cost})`, 'log-system');
      toast(`LOW MANA: ${spell.cost} REQUIRED`);
      return;
    }

    STATE.player.mana -= spell.cost;
    STATE.player.castTimer = 0.45;
    STATE.player.moveState = 'cast';

    if (STATE.player.char === 'golem') playGolemAnim('attack1', false, 0.1);
    else if (STATE.player.char === 'rogue') playRogueAnim('attack1', false, 0.1);

    const org = getCastOrigin();
    const dir = getAimDirection();

    if (spell.id === 'fireball')          mkFireball(org, dir);
    else if (spell.id === 'flame-burst')  castFlameBurst();
    else if (spell.id === 'inferno-wave') mkInfernoWave(org, dir);
    else if (spell.id === 'thunder-surge')mkThunder(org, dir);
    else if (spell.id === 'ice-shard')    mkIce(org, dir);
    else if (spell.id === 'arcane-bolt')  mkArcane(org, dir);
    else {
      // Generalized elemental burst for other grimoire spells
      mkFireball(org, dir);
    }

    log(`Typed Spell Cast: [${spell.name.toUpperCase()}]`, 'log-power');
    toast(`CAST: ${spell.name.toUpperCase()}`);
    updatePlayerHUD();
  }

  // ══════════════════════════════════════════════════════════
  //  9. MAGICAL GRIMOIRE INTERFACE (Priority 6)
  // ══════════════════════════════════════════════════════════
  let currentGrimoireTab = 'all';

  function switchGrimoireTab(tab) {
    currentGrimoireTab = tab;
    document.querySelectorAll('.spell-tabs .tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.innerText.toLowerCase().includes(tab) || (tab === 'all' && btn.innerText.includes('ALL')));
    });
    renderGrimoire();
  }

  function filterGrimoire() {
    renderGrimoire();
  }

  function renderGrimoire() {
    const grid = document.getElementById('grimoire-grid');
    grid.innerHTML = '';
    const q = (document.getElementById('grimoire-search').value || '').toLowerCase().trim();

    const items = (currentGrimoireTab === 'power')
      ? POWERS.map(p => ({ ...p, isPower: true }))
      : [...SPELLS.map(s => ({ ...s, isPower: false })), ...POWERS.map(p => ({ ...p, isPower: true }))];

    const filtered = items.filter(it => {
      if (currentGrimoireTab !== 'all' && currentGrimoireTab !== 'power' && it.elem !== currentGrimoireTab) return false;
      if (currentGrimoireTab === 'power' && !it.isPower) return false;
      if (!q) return true;
      return it.name.toLowerCase().includes(q) || it.desc.toLowerCase().includes(q) || it.elem.toLowerCase().includes(q);
    });

    filtered.forEach(it => {
      const card = document.createElement('div');
      card.className = `spell-card ${it.elem}`;
      card.innerHTML = `
        <div>
          <div class="sc-header">
            <span class="sc-title">${it.icon} ${it.name}</span>
            <span class="cbadge" style="background:${elemColor(it.elem)}22; border-color:${elemColor(it.elem)}; color:${elemColor(it.elem)};">${it.elem.toUpperCase()}</span>
          </div>
          <div class="sc-desc">${it.desc}</div>
          <div class="sc-stats">
            <span>COST: <strong style="color:#c084fc;">${it.cost} MP</strong></span>
            <span>CD: <strong style="color:#38bdf8;">${it.cd}s</strong></span>
            ${it.dmg ? `<span>DMG: <strong style="color:#f87171;">${it.dmg}</strong></span>` : ''}
          </div>
          <span class="sc-cmd-pill">Command: /${it.command}</span>
        </div>
        <div class="sc-footer">
          <button class="btn-primary" style="padding:6px 12px; font-size:9px;" onclick="executeSpellCommand('${it.command}'); toggleModal('spellbook-modal');">
            ${it.isPower ? 'ACTIVATE POWER' : 'CAST SPELL'}
          </button>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  // ══════════════════════════════════════════════════════════
  //  10. 3D FACE-SCANNING WORKFLOW (Priority 8)
  // ══════════════════════════════════════════════════════════
  let cameraStream = null;

  function switchLoadoutTab(tab) {
    document.getElementById('presets-container').style.display = (tab === 'presets' ? 'block' : 'none');
    document.getElementById('facescan-container').style.display = (tab === 'facescan' ? 'flex' : 'none');
    document.getElementById('tab-btn-presets').classList.toggle('active', tab === 'presets');
    document.getElementById('tab-btn-facescan').classList.toggle('active', tab === 'facescan');
  }

  async function startCamera() {
    try {
      const constraints = { video: { width: 640, height: 480, facingMode: 'user' } };
      cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
      const video = document.getElementById('webcam-video');
      video.srcObject = cameraStream;
      video.style.display = 'block';
      document.getElementById('photo-preview-img').style.display = 'none';
      document.getElementById('face-guide-oval').style.display = 'block';

      document.getElementById('btn-start-camera').style.display = 'none';
      document.getElementById('btn-capture-photo').style.display = 'inline-block';
      document.getElementById('btn-retake-photo').style.display = 'none';
      toast('CAMERA ENGAGED');
    } catch (err) {
      console.warn('Webcam permission / access error:', err);
      log('Webcam permission not granted or device unavailable. Use Upload Photo option.', 'log-system');
      alert('Camera permission denied or camera unavailable. You can use the "Upload Photo" option below.');
    }
  }

  function capturePhoto() {
    const video = document.getElementById('webcam-video');
    const canvas = document.getElementById('photo-canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    const img = document.getElementById('photo-preview-img');
    img.src = dataUrl;
    img.style.display = 'block';
    video.style.display = 'none';
    document.getElementById('face-guide-oval').style.display = 'none';

    document.getElementById('btn-capture-photo').style.display = 'none';
    document.getElementById('btn-retake-photo').style.display = 'inline-block';
    document.getElementById('btn-generate-avatar').style.display = 'inline-block';

    // Stop stream to release hardware
    if (cameraStream) {
      cameraStream.getTracks().forEach(t => t.stop());
      cameraStream = null;
    }
    toast('PHOTO CAPTURED');
  }

  function retakePhoto() {
    document.getElementById('btn-retake-photo').style.display = 'none';
    document.getElementById('btn-generate-avatar').style.display = 'none';
    startCamera();
  }

  function handlePhotoUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      const img = document.getElementById('photo-preview-img');
      img.src = ev.target.result;
      img.style.display = 'block';
      document.getElementById('webcam-video').style.display = 'none';
      document.getElementById('face-guide-oval').style.display = 'none';
      document.getElementById('btn-retake-photo').style.display = 'inline-block';
      document.getElementById('btn-generate-avatar').style.display = 'inline-block';
      toast('PHOTO UPLOADED');
    };
    reader.readAsDataURL(file);
  }

  function generateAvatarFromPhoto() {
    // Honest labeling notice (as required by Priority 8 & AVATAR_PIPELINE.md)
    log('Checking 3D avatar generation service...', 'log-system');
    const statusBox = document.getElementById('provider-box');
    statusBox.style.borderColor = '#ef4444';
    statusBox.innerHTML = `
      <strong>Provider Status: Not Configured</strong><br>
      <span style="color:#f87171;">Server environment variable <code>AVATAR_API_KEY</code> is missing.</span><br>
      <span>To generate custom 3D mesh avatars, connect a Ready Player Me or Tripo3D API key in <code>.env</code>. You can preview and equip the verified local humanoid avatar chassis immediately.</span>
    `;
    toast('AVATAR SERVICE REQUIRES API KEY');
  }

  function equipCustomAvatar() {
    setChar('custom');
    toggleModal('loadout-modal');
    toast('CUSTOM AVATAR EQUIPPED');
  }
''')

print("Part 6 added.")

# PART 7: SPELL PROJECTILES, COMBAT RESOLUTION, GAME LOOP, INPUT & LAUNCH
parts.append(r'''
  // ══════════════════════════════════════════════════════════
  //  11. SPELL PROJECTILE CREATION & KINEMATICS
  // ══════════════════════════════════════════════════════════
  const projectiles = [];
  const particles = [];

  function getAimDirection() {
    const dir = new THREE.Vector3(0, 0, -1);
    dir.applyAxisAngle(new THREE.Vector3(1, 0, 0), -STATE.player.pitch);
    dir.applyAxisAngle(new THREE.Vector3(0, 1, 0), STATE.player.yaw);
    return dir.normalize();
  }

  function getCastOrigin() {
    const ch = STATE.player.char;
    const origin = new THREE.Vector3();
    if (ch === 'golem' && golemHandR) {
      golemHandR.getWorldPosition(origin);
      if (origin.lengthSq() > 0.01) return origin;
    } else if (ch === 'rogue' && rogueHandR) {
      rogueHandR.getWorldPosition(origin);
      if (origin.lengthSq() > 0.01) return origin;
    }

    const fwd = getAimDirection();
    const right = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), fwd).normalize();
    const hOff = ch === 'golem' ? 0.75 : 0.45;
    const yOff = STATE.player.eyeHeight * 0.85;

    return playerGroup.position.clone()
      .add(new THREE.Vector3(0, yOff, 0))
      .addScaledVector(right, -hOff)
      .addScaledVector(fwd, 0.8);
  }

  function castSlot(i) {
    if (STATE.cds[i] > 0) {
      log(`Cooldown active (${STATE.cds[i].toFixed(1)}s)`, 'log-system');
      return;
    }
    const spell = SPELLS.find(s => s.id === STATE.slots[i]);
    if (!spell) return;
    if (STATE.player.mana < spell.cost) {
      log(`Insufficient mana (${Math.round(STATE.player.mana)}/${spell.cost})`, 'log-system');
      toast(`LOW MANA: ${spell.cost} REQUIRED`);
      return;
    }

    STATE.player.mana -= spell.cost;
    STATE.cds[i] = spell.cd;
    STATE.player.castTimer = 0.45;
    STATE.player.moveState = 'cast';

    document.getElementById('crosshair').classList.add('spread');
    setTimeout(() => document.getElementById('crosshair').classList.remove('spread'), 180);

    if (STATE.player.char === 'golem') playGolemAnim('attack1', false, 0.1);
    else if (STATE.player.char === 'rogue') playRogueAnim('attack1', false, 0.1);

    const org = getCastOrigin();
    const dir = getAimDirection();

    if (spell.id === 'fireball')          mkFireball(org, dir);
    else if (spell.id === 'flame-burst')  castFlameBurst();
    else if (spell.id === 'inferno-wave') mkInfernoWave(org, dir);
    else if (spell.id === 'thunder-surge')mkThunder(org, dir);
    else if (spell.id === 'ice-shard')    mkIce(org, dir);
    else if (spell.id === 'arcane-bolt')  mkArcane(org, dir);

    updatePlayerHUD();
  }

  // 1. Fireball
  function mkFireball(pos, dir) {
    if (!STATE.stats) STATE.stats = {};
    STATE.stats.spellsCast = (STATE.stats.spellsCast || 0) + 1;
    SFX.fireball();
    const grp = new THREE.Group();
    grp.position.copy(pos);
    const core = new THREE.Mesh(
      new THREE.SphereGeometry(0.35, 16, 16),
      new THREE.MeshStandardMaterial({ color: 0xffedd5, emissive: 0xf97316, emissiveIntensity: 2.5 })
    );
    grp.add(core);
    scene.add(grp);

    projectiles.push({
      group: grp,
      velocity: dir.clone().multiplyScalar(46),
      type: 'fire',
      dmg: 45,
      lifetime: 3.0,
      radius: 0.5,
      onHit: (p) => {
        SFX.flameBurst();
        spawnExplosion(p, 'fire');
      }
    });
  }

  // 2. Flame Burst
  function castFlameBurst() {
    SFX.flameBurst();
    spawnExplosion(playerGroup.position.clone().add(new THREE.Vector3(0, 1.2, 0)), 'fire', 8.0);
    // Radial damage check to dummy & wildlife within 8m
    if (playerGroup.position.distanceTo(STATE.dummy.pos) < 8.5) hitDummy(50, 'fire');
    for (const w of wildlife) {
      if (!w.dead && playerGroup.position.distanceTo(w.pos) < 8.5) {
        damageWildlife(w, 50, 'fire');
      }
    }
  }

  // 3. Inferno Wave
  function mkInfernoWave(pos, dir) {
    SFX.infernoWave();
    const grp = new THREE.Group();
    grp.position.copy(pos);
    const ring = new THREE.Mesh(
      new THREE.CylinderGeometry(1.6, 2.2, 0.6, 16, 1, true),
      new THREE.MeshBasicMaterial({ color: 0xf97316, wireframe: true })
    );
    grp.add(ring);
    scene.add(grp);

    projectiles.push({
      group: grp,
      velocity: dir.clone().multiplyScalar(32),
      type: 'fire',
      dmg: 38,
      lifetime: 2.2,
      radius: 1.8,
      onHit: (p) => spawnExplosion(p, 'fire', 4.5)
    });
  }

  // 4. Thunder Surge
  function mkThunder(pos, dir) {
    SFX.thunder();
    const grp = new THREE.Group();
    grp.position.copy(pos);
    const bolt = new THREE.Mesh(
      new THREE.CylinderGeometry(0.12, 0.22, 2.2, 8),
      new THREE.MeshStandardMaterial({ color: 0xe0f2fe, emissive: 0x38bdf8, emissiveIntensity: 3.5 })
    );
    bolt.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    grp.add(bolt);
    scene.add(grp);

    projectiles.push({
      group: grp,
      velocity: dir.clone().multiplyScalar(68),
      type: 'lightning',
      dmg: 65,
      lifetime: 2.0,
      radius: 0.6,
      onHit: (p) => spawnExplosion(p, 'lightning', 3.2)
    });
  }

  // 5. Ice Shard
  function mkIce(pos, dir) {
    SFX.ice();
    const grp = new THREE.Group();
    grp.position.copy(pos);
    const shard = new THREE.Mesh(
      new THREE.ConeGeometry(0.25, 1.4, 6),
      new THREE.MeshStandardMaterial({ color: 0x93c5fd, emissive: 0x38bdf8, roughness: 0.15, metalness: 0.85 })
    );
    shard.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    grp.add(shard);
    scene.add(grp);

    projectiles.push({
      group: grp,
      velocity: dir.clone().multiplyScalar(52),
      type: 'ice',
      dmg: 40,
      lifetime: 2.4,
      radius: 0.5,
      onHit: (p) => spawnExplosion(p, 'ice', 2.8)
    });
  }

  // 6. Arcane Bolt
  function mkArcane(pos, dir) {
    SFX.arcane();
    const grp = new THREE.Group();
    grp.position.copy(pos);
    const orb = new THREE.Mesh(
      new THREE.IcosahedronGeometry(0.38, 1),
      new THREE.MeshStandardMaterial({ color: 0xe9d5ff, emissive: 0xa855f7, emissiveIntensity: 2.8 })
    );
    grp.add(orb);
    scene.add(grp);

    projectiles.push({
      group: grp,
      velocity: dir.clone().multiplyScalar(48),
      type: 'arcane',
      dmg: 55,
      lifetime: 2.6,
      radius: 0.6,
      onHit: (p) => spawnExplosion(p, 'arcane', 3.5)
    });
  }

  // Explosions & Particles
  function spawnExplosion(pos, elem = 'fire', scale = 1.0) {
    const col = elemColor(elem);
    for (let i = 0; i < 18; i++) {
      const pMat = new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.9 });
      const p = new THREE.Mesh(new THREE.BoxGeometry(0.18 * scale, 0.18 * scale, 0.18 * scale), pMat);
      p.position.copy(pos);
      scene.add(p);
      particles.push({
        mesh: p,
        isRing: false,
        velocity: new THREE.Vector3((Math.random() - 0.5) * 16 * scale, Math.random() * 10 * scale + 2, (Math.random() - 0.5) * 16 * scale),
        life: 0.7,
        maxLife: 0.7,
        gravity: 20
      });
    }
  }

  function elemColor(e) {
    return { fire: '#fb923c', lightning: '#38bdf8', ice: '#93c5fd', arcane: '#c084fc', power: '#facc15' }[e] || '#fff';
  }

  // ── COMBAT RESOLUTION ON TRAINING AUTOMATON ─────────────────
  const dummyGroup = new THREE.Group();
  dummyGroup.position.copy(STATE.dummy.pos);
  scene.add(dummyGroup);

  const dTorso = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.4, 0.6), new THREE.MeshStandardMaterial({ color: 0x991b1b, metalness: 0.6, roughness: 0.4 }));
  dTorso.position.y = 1.8;
  const dHead = new THREE.Mesh(new THREE.SphereGeometry(0.35, 12, 12), new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.8 }));
  dHead.position.y = 2.8;
  dummyGroup.add(dTorso, dHead);

  function hitDummy(amount, type) {
    if (STATE.dummy.dead) return;
    const isCrit = Math.random() < 0.22;
    const dmg = isCrit ? Math.round(amount * 1.5) : amount;
    STATE.dummy.hp = Math.max(0, STATE.dummy.hp - dmg);
    SFX.hit();
    flashHitMarker();

    spawnDmgNum(dmg, STATE.dummy.pos.clone().add(new THREE.Vector3(0, 3.0, 0)), type, isCrit);

    dTorso.material.color.setHex(0xffffff);
    setTimeout(() => dTorso.material.color.setHex(0x991b1b), 100);
    updateTargetHUD();
    log(`Hit Automaton [${type.toUpperCase()}] for ${dmg}${isCrit ? ' CRIT' : ''}!`, 'log-damage');

    if (STATE.dummy.hp <= 0) killDummy();
  }

  function killDummy() {
    STATE.dummy.dead = true;
    dummyGroup.visible = false;
    spawnExplosion(STATE.dummy.pos.clone().add(new THREE.Vector3(0, 2, 0)), 'fire');
    log('💥 Automaton ELIMINATED! Rebuilding in 3.5s…', 'log-system');
    setTimeout(() => {
      STATE.dummy.hp = STATE.dummy.maxHp;
      STATE.dummy.dead = false;
      dummyGroup.visible = true;
      updateTargetHUD();
      log('Automaton reassembled.', 'log-system');
    }, 3500);
  }

  function flashHitMarker() {
    const hm = document.getElementById('hitmarker');
    hm.classList.add('active');
    setTimeout(() => hm.classList.remove('active'), 120);
  }

  function spawnDmgNum(val, wPos, type, crit) {
    const s = wPos.clone().project(camera);
    const x = (s.x * 0.5 + 0.5) * window.innerWidth;
    const y = (-s.y * 0.5 + 0.5) * window.innerHeight;
    const el = document.createElement('div');
    el.className = `fdmg ${type}${crit ? ' crit' : ''}`;
    el.innerText = crit ? `${val} CRIT!` : `${val}`;
    el.style.left = `${x}px`; el.style.top = `${y}px`;
    document.getElementById('dmg-layer').appendChild(el);
    setTimeout(() => el.remove(), 850);
  }

  function toast(msg) {
    const t = document.getElementById('toast');
    t.innerText = msg;
    t.classList.add('show');
    SFX.beep();
    setTimeout(() => t.classList.remove('show'), 1600);
  }

  function log(text, cls = '') {
    const l = document.getElementById('combat-log');
    const d = document.createElement('div');
    d.className = `log-line ${cls}`;
    d.innerText = text;
    l.appendChild(d);
    while (l.children.length > 5) l.removeChild(l.firstChild);
  }

  // ── HUD UPDATES ───────────────────────────────────────────
  function updatePlayerHUD() {
    const p = STATE.player;
    document.getElementById('val-hp').innerText = Math.round(p.hp);
    document.getElementById('bar-hp').style.width = `${(p.hp / p.maxHp) * 100}%`;
    document.getElementById('val-shield').innerText = Math.round(p.shield);
    document.getElementById('bar-shield').style.width = `${(p.shield / p.maxShield) * 100}%`;
    document.getElementById('val-mana').innerText = Math.round(p.mana);
    document.getElementById('bar-mana').style.width = `${(p.mana / p.maxMana) * 100}%`;
    document.getElementById('val-stam').innerText = Math.round(p.stam);
    document.getElementById('bar-stam').style.width = `${(p.stam / p.maxStam) * 100}%`;

    // Active buffs pills
    const buffRow = document.getElementById('buff-row');
    buffRow.innerHTML = '';
    if (STATE.powers.ultraSpeed.active) {
      buffRow.innerHTML += `<span class="buff-pill buff-speed">⚡ SPEED (${STATE.powers.ultraSpeed.timer.toFixed(1)}s)</span>`;
    }
    if (STATE.powers.superVision.active) {
      buffRow.innerHTML += `<span class="buff-pill buff-vision">👁️ VISION (${STATE.powers.superVision.timer.toFixed(1)}s)</span>`;
    }
    if (STATE.buffs.powerSurge > 0) {
      buffRow.innerHTML += `<span class="buff-pill buff-power">🔥 +25% SURGE (${STATE.buffs.powerSurge.toFixed(1)}s)</span>`;
    }

    // Power cooldown buttons text
    document.getElementById('pcd-jump').innerText = STATE.powers.ultraJump.cd > 0 ? `${STATE.powers.ultraJump.cd.toFixed(1)}s` : '';
    document.getElementById('pcd-speed').innerText = STATE.powers.ultraSpeed.cd > 0 ? `${STATE.powers.ultraSpeed.cd.toFixed(1)}s` : '';
    document.getElementById('pcd-vision').innerText = STATE.powers.superVision.cd > 0 ? `${STATE.powers.superVision.cd.toFixed(1)}s` : '';
  }

  function updateTargetHUD() {
    document.getElementById('val-target-hp').innerText = Math.round(STATE.dummy.hp);
    document.getElementById('bar-target-hp').style.width = `${(STATE.dummy.hp / STATE.dummy.maxHp) * 100}%`;
    const dist = Math.round(playerGroup.position.distanceTo(STATE.dummy.pos));
    document.getElementById('val-target-dist').innerText = `${dist}m`;
  }

  function updateCDs(dt) {
    for (let i = 0; i < 5; i++) {
      if (STATE.cds[i] > 0) {
        STATE.cds[i] = Math.max(0, STATE.cds[i] - dt);
        const spell = SPELLS.find(s => s.id === STATE.slots[i]);
        const pct = (STATE.cds[i] / (spell ? spell.cd : 1)) * 100;
        const cd = document.getElementById(`cd-${i}`);
        cd.style.height = `${pct}%`;
        cd.innerText = STATE.cds[i] > 0 ? STATE.cds[i].toFixed(1) : '';
      } else {
        document.getElementById(`cd-${i}`).style.height = '0%';
        document.getElementById(`cd-${i}`).innerText = '';
      }
    }

    // Update Supernatural Powers Durations & Cooldowns
    const uj = STATE.powers.ultraJump;
    if (uj.cd > 0) uj.cd = Math.max(0, uj.cd - dt);

    const us = STATE.powers.ultraSpeed;
    if (us.active) {
      us.timer -= dt;
      if (us.timer <= 0) {
        us.active = false;
        document.getElementById('speed-lines-overlay').classList.remove('active');
        log('Ultra Speed expired. Returning to standard pace.', 'log-system');
      }
    }
    if (us.cd > 0) us.cd = Math.max(0, us.cd - dt);

    const sv = STATE.powers.superVision;
    if (sv.active) {
      sv.timer -= dt;
      if (sv.timer <= 0) {
        sv.active = false;
        document.getElementById('super-vision-overlay').classList.remove('active');
        log('Super Vision expired.', 'log-system');
      }
    }
    if (sv.cd > 0) sv.cd = Math.max(0, sv.cd - dt);

    if (STATE.buffs.powerSurge > 0) {
      STATE.buffs.powerSurge = Math.max(0, STATE.buffs.powerSurge - dt);
    }
  }

  function updateHotbarUI() {
    for (let i = 0; i < 5; i++) {
      const spell = SPELLS.find(s => s.id === STATE.slots[i]);
      if (!spell) continue;
      document.getElementById(`si-${i}`).innerText = spell.icon;
      document.getElementById(`sn-${i}`).innerText = spell.name.split(' ')[0].toUpperCase();
      document.getElementById(`slot-${i}`).className = `aslot ${spell.elem}`;
    }
  }

  // ── MODALS (MAPS, LOADOUT, SPELLS, AUDIO) ───────────────────
  function toggleModal(id) {
    const m = document.getElementById(id);
    const isOpen = (m.style.display === 'flex');
    m.style.display = isOpen ? 'none' : 'flex';
    if (!isOpen && document.pointerLockElement) document.exitPointerLock();
    if (id === 'spellbook-modal' && !isOpen) renderGrimoire();
  }

  document.getElementById('btn-maps').onclick    = () => toggleModal('map-modal');
  document.getElementById('btn-spells').onclick  = () => toggleModal('spellbook-modal');
  document.getElementById('btn-loadout').onclick = () => toggleModal('loadout-modal');
  document.getElementById('btn-audio').onclick   = () => toggleModal('audio-modal');
  document.getElementById('close-maps').onclick  = () => toggleModal('map-modal');
  document.getElementById('close-spells').onclick= () => toggleModal('spellbook-modal');
  document.getElementById('close-loadout').onclick=() => toggleModal('loadout-modal');
  document.getElementById('close-audio').onclick = () => toggleModal('audio-modal');
  document.getElementById('btn-apply-loadout').onclick = () => toggleModal('loadout-modal');

  function updateVolumes() {
    const vm = parseFloat(document.getElementById('vol-master').value) / 100;
    const vs = parseFloat(document.getElementById('vol-sfx').value) / 100;
    const va = parseFloat(document.getElementById('vol-amb').value) / 100;

    document.getElementById('val-vol-master').innerText = Math.round(vm * 100) + '%';
    document.getElementById('val-vol-sfx').innerText = Math.round(vs * 100) + '%';
    document.getElementById('val-vol-amb').innerText = Math.round(va * 100) + '%';

    SFX.setMasterVol(vm);
    SFX.setSfxVol(vs);
    SFX.setAmbVol(va);
  }

  function selectChar(cId) {
    document.querySelectorAll('.char-card').forEach(c => c.classList.remove('selected'));
    const target = document.querySelector(`.char-card[data-char="${cId}"]`);
    if (target) target.classList.add('selected');
    setChar(cId);
  }

  // ══════════════════════════════════════════════════════════
  //  12. INPUT CONTROLS, LOCOMOTION & GAME LOOP
  // ══════════════════════════════════════════════════════════
  const keys = {};
  let pointerLocked = false;

  window.addEventListener('keydown', e => {
    SFX.init();

    // If typing in spell command terminal, do not trigger game movements
    if (cmdOpen) return;

    keys[e.code] = true;

    // Quick Slot Casting
    if (e.code === 'KeyQ') castSlot(1);
    if (e.code === 'KeyE') {
      // Check for reward pickup first
      checkInteractReward();
      castSlot(2);
    }
    if (e.code === 'KeyR') castSlot(3);
    if (e.code === 'KeyF') castSlot(4);

    // Supernatural Powers shortcuts (Priority 4)
    if (e.code === 'KeyV') activatePower('ultra-jump');
    if (e.code === 'KeyB') activatePower('ultra-speed');
    if (e.code === 'KeyX') activatePower('super-vision');

    // Spell command input toggle (Priority 5)
    if (e.code === 'Slash') {
      e.preventDefault();
      openSpellCommand();
    }

    // Modal navigation
    if (e.code === 'KeyM') { e.preventDefault(); toggleModal('map-modal'); }
    if (e.code === 'KeyG' || e.code === 'KeyK') { e.preventDefault(); toggleModal('spellbook-modal'); }
    if (e.code === 'Tab')  { e.preventDefault(); toggleModal('loadout-modal'); }
  });

  window.addEventListener('keyup', e => {
    if (!cmdOpen) keys[e.code] = false;
  });

  container.addEventListener('mousedown', e => {
    SFX.init();
    if (cmdOpen) return;
    if (!pointerLocked) {
      container.requestPointerLock();
      return;
    }
    if (e.button === 0) castSlot(0); // Primary spell
    if (e.button === 2) {
      STATE.player.ads = true;
      document.getElementById('crosshair').classList.add('ads');
    }
  });

  window.addEventListener('mouseup', e => {
    if (e.button === 2) {
      STATE.player.ads = false;
      document.getElementById('crosshair').classList.remove('ads');
    }
  });

  window.addEventListener('contextmenu', e => e.preventDefault());

  document.addEventListener('pointerlockchange', () => {
    pointerLocked = (document.pointerLockElement === container);
    document.getElementById('start-hint').style.opacity = pointerLocked ? '0' : '1';
  });

  document.addEventListener('mousemove', e => {
    if (!pointerLocked || cmdOpen) return;
    const sens = STATE.settings.sens * (STATE.player.ads ? 0.55 : 1.0);
    STATE.player.yaw   -= e.movementX * sens;
    STATE.player.pitch += e.movementY * sens;
    STATE.player.pitch = Math.max(-0.6, Math.min(0.85, STATE.player.pitch));
  });

  function checkInteractReward() {
    for (const r of rewards) {
      if (!r.collected && playerGroup.position.distanceTo(r.pos) < 3.2) {
        collectReward(r);
        break;
      }
    }
  }

  // Camera coordinates smoothing
  const camPos = new THREE.Vector3();
  const camTarget = new THREE.Vector3();

  // ── MAIN ANIMATION & SIMULATION LOOP ───────────────────────
  function animate() {
    requestAnimationFrame(animate);
    const dt = Math.min(clock.getDelta(), 0.08);
    const time = clock.getElapsedTime();
    const p = STATE.player;

    // 1. LOCOMOTION KINEMATICS
    const inputW = keys['KeyW'] || false;
    const inputS = keys['KeyS'] || false;
    const inputA = keys['KeyA'] || false;
    const inputD = keys['KeyD'] || false;
    const isMoving = (inputW || inputS || inputA || inputD) && !cmdOpen;

    p.sprinting = (keys['ShiftLeft'] || keys['ShiftRight'] || false) && !p.ads && isMoving;

    // Determine target speed with Ultra Speed boost
    let targetSpeed = 0;
    if (isMoving) {
      if (p.ads) targetSpeed = p.adsSpeed;
      else if (p.sprinting) targetSpeed = p.sprintSpeed;
      else targetSpeed = p.walkSpeed;

      // Apply Supernatural Ultra Speed multiplier (2.4x)
      if (STATE.powers.ultraSpeed.active) {
        targetSpeed *= 2.4;
      }
    }

    // Stamina depletion & regeneration
    if (p.sprinting && !STATE.powers.ultraSpeed.active) {
      p.stam = Math.max(0, p.stam - 18 * dt);
      if (p.stam <= 0) p.sprinting = false;
    } else {
      p.stam = Math.min(p.maxStam, p.stam + 25 * dt);
    }

    // Mana regeneration
    p.mana = Math.min(p.maxMana, p.mana + 8 * dt);

    // Direction vector in world space
    const moveDir = new THREE.Vector3(0, 0, 0);
    if (inputW) moveDir.z -= 1;
    if (inputS) moveDir.z += 1;
    if (inputA) moveDir.x -= 1;
    if (inputD) moveDir.x += 1;
    if (moveDir.lengthSq() > 0) {
      moveDir.normalize();
      moveDir.applyAxisAngle(new THREE.Vector3(0, 1, 0), p.yaw);
    }

    // Smooth horizontal acceleration
    const accel = p.grounded ? 26.0 : 8.0;
    p.vel.x += (moveDir.x * targetSpeed - p.vel.x) * Math.min(1, accel * dt);
    p.vel.z += (moveDir.z * targetSpeed - p.vel.z) * Math.min(1, accel * dt);

    const horizSpeed = Math.sqrt(p.vel.x * p.vel.x + p.vel.z * p.vel.z);
    p.currentSpeed = horizSpeed;
    document.getElementById('player-speed-val').innerText = horizSpeed.toFixed(1);

    // 2. WALL-SLIDING COLLISION DETECTION
    let desiredX = playerGroup.position.x + p.vel.x * dt;
    let desiredZ = playerGroup.position.z + p.vel.z * dt;
    const playerRadius = p.radius;
    const playerFeetY = playerGroup.position.y;
    const playerHeadY = playerFeetY + p.height;

    for (const col of colliders) {
      if (col.isStep) continue; // Steps handled by climbing
      if (playerHeadY > col.min.y && playerFeetY < col.max.y) {
        const qx = Math.max(col.min.x, Math.min(desiredX, col.max.x));
        const qz = Math.max(col.min.z, Math.min(desiredZ, col.max.z));
        const dx = desiredX - qx;
        const dz = desiredZ - qz;
        const distSq = dx * dx + dz * dz;

        if (distSq < playerRadius * playerRadius) {
          const dist = Math.sqrt(distSq);
          let nx = (dist > 0.0001) ? dx / dist : 0;
          let nz = (dist > 0.0001) ? dz / dist : 1;

          const penetration = playerRadius - dist;
          desiredX += nx * penetration;
          desiredZ += nz * penetration;

          const dot = p.vel.x * nx + p.vel.z * nz;
          if (dot < 0) {
            p.vel.x -= dot * nx;
            p.vel.z -= dot * nz;
          }
        }
      }
    }

    playerGroup.position.x = desiredX;
    playerGroup.position.z = desiredZ;

    // 3. GROUND HEIGHT, CURBS & VERTICAL KINEMATICS
    let groundY = 0;
    for (const col of colliders) {
      if (desiredX >= col.min.x - playerRadius && desiredX <= col.max.x + playerRadius &&
          desiredZ >= col.min.z - playerRadius && desiredZ <= col.max.z + playerRadius) {
        if (col.max.y <= playerFeetY + 0.45 && col.max.y > groundY) {
          groundY = col.max.y;
        }
      }
    }

    // Jump trigger
    if (keys['Space'] && p.grounded && p.moveState !== 'jump' && !cmdOpen) {
      p.vel.y = p.jumpForce;
      p.grounded = false;
      p.moveState = 'jump';
      SFX.jump();
    }

    // Apply gravity
    p.vel.y -= p.gravity * dt;
    playerGroup.position.y += p.vel.y * dt;

    if (playerGroup.position.y <= groundY) {
      const wasAir = !p.grounded;
      playerGroup.position.y = groundY;
      p.vel.y = 0;
      if (wasAir && p.moveState === 'jump') {
        p.moveState = 'land';
        SFX.land();
      }
      p.grounded = true;
    } else {
      p.grounded = false;
    }

    if (p.moveState === 'land') {
      setTimeout(() => { if (p.moveState === 'land') p.moveState = 'idle'; }, 240);
    }

    if (p.castTimer > 0) {
      p.castTimer -= dt;
      if (p.castTimer <= 0) p.moveState = isMoving ? (p.sprinting ? 'jog' : 'walk') : 'idle';
    }

    if (p.moveState !== 'cast' && p.moveState !== 'land' && p.moveState !== 'jump') {
      if (!p.grounded) p.moveState = 'fall';
      else if (!isMoving) p.moveState = 'idle';
      else p.moveState = p.sprinting ? 'jog' : 'walk';
    }

    // Footstep audio synchronization
    if (isMoving && p.grounded) {
      p.stepTimer -= dt;
      if (p.stepTimer <= 0) {
        const speedRatio = STATE.powers.ultraSpeed.active ? 1.6 : (p.sprinting ? 1.2 : 1.0);
        SFX.step(p.activeSurface, speedRatio);
        p.stepTimer = STATE.powers.ultraSpeed.active ? 0.18 : (p.sprinting ? 0.28 : 0.46);
      }
    }

    // Facing orientation
    if (p.ads) {
      let dy = p.yaw - playerGroup.rotation.y;
      while (dy > Math.PI)  dy -= Math.PI * 2;
      while (dy < -Math.PI) dy += Math.PI * 2;
      playerGroup.rotation.y += dy * Math.min(1, 16 * dt);
    } else if (isMoving) {
      const moveYaw = Math.atan2(p.vel.x, p.vel.z);
      let dy = moveYaw - playerGroup.rotation.y;
      while (dy > Math.PI)  dy -= Math.PI * 2;
      while (dy < -Math.PI) dy += Math.PI * 2;
      playerGroup.rotation.y += dy * Math.min(1, 14 * dt);
    }

    // Skeletal animation updates
    document.getElementById('anim-state-val').innerText = p.moveState.toUpperCase();
    let animKey = 'idle';
    if (p.moveState === 'cast') animKey = 'attack1';
    else if (p.moveState === 'jump' || p.moveState === 'fall') animKey = 'walkF';
    else if (p.moveState === 'jog') animKey = 'jogF';
    else if (p.moveState === 'walk') animKey = 'walkF';

    if (p.char === 'golem' && golemMixer) {
      playGolemAnim(animKey, animKey !== 'attack1', 0.2);
      if (currentGolemAction) {
        currentGolemAction.timeScale = STATE.powers.ultraSpeed.active ? 2.2 : (p.sprinting ? 1.45 : 1.0);
      }
      golemMixer.update(dt);
      if (golemFbx) golemFbx.position.set(0, 0, 0);
    }

    if (p.char === 'rogue' && rogueMixer) {
      playRogueAnim(animKey, animKey !== 'attack1', 0.2);
      if (currentRogueAction) {
        currentRogueAction.timeScale = STATE.powers.ultraSpeed.active ? 2.2 : (p.sprinting ? 1.45 : 1.0);
      }
      rogueMixer.update(dt);
      if (rogueFbx) rogueFbx.position.set(0, 0, 0);
    }

    // 4. THIRD-PERSON CAMERA
    const ch = p.char;
    const baseCamDist = p.ads ? (ch === 'golem' ? 2.8 : 2.2) : (ch === 'golem' ? 3.9 : 3.2);
    const shoulderOffset = p.ads ? 0.45 : 0.65;
    const camHeightOffset = STATE.player.eyeHeight * 0.95;

    const tgt = playerGroup.position.clone().add(new THREE.Vector3(0, camHeightOffset, 0));
    const cosP = Math.cos(p.pitch);
    const sinP = Math.sin(p.pitch);
    let camDist = baseCamDist;

    const rightVec = new THREE.Vector3(Math.cos(p.yaw), 0, -Math.sin(p.yaw)).multiplyScalar(shoulderOffset);
    const desiredCamPos = tgt.clone()
      .add(rightVec)
      .add(new THREE.Vector3(Math.sin(p.yaw) * cosP * camDist, sinP * camDist, Math.cos(p.yaw) * cosP * camDist));

    camPos.lerp(desiredCamPos, Math.min(1, 20 * dt));
    camTarget.lerp(tgt.clone().add(rightVec.clone().multiplyScalar(0.4)), Math.min(1, 22 * dt));

    camera.position.copy(camPos);
    camera.lookAt(camTarget);

    // Dynamic FOV widening during Ultra Speed
    const targetFov = STATE.powers.ultraSpeed.active ? 74 : (p.ads ? 48 : 60);
    camera.fov += (targetFov - camera.fov) * Math.min(1, 10 * dt);
    camera.updateProjectionMatrix();

    // Update Flying Birds Flock
    for (let i = 0; i < birdFlock.length; i++) {
      const b = birdFlock[i];
      if (b.mixer) b.mixer.update(dt);
      b.angle += b.speed * dt;
      const bx = b.center.x + Math.cos(b.angle) * b.radius;
      const bz = b.center.z + Math.sin(b.angle) * b.radius;
      const by = b.height + Math.sin(b.angle * 2) * 1.5;
      b.mesh.position.set(bx, by, bz);
      b.mesh.rotation.y = -b.angle + Math.PI / 2;
      b.mesh.rotation.z = Math.cos(b.angle) * 0.2;
    }

    // 5. WILDLIFE AI UPDATE & ANIMATIONS
    for (let i = 0; i < wildlife.length; i++) {
      const w = wildlife[i];
      if (w.dead) continue;

      if (w.mixer) w.mixer.update(dt);

      const distToPlayer = w.pos.distanceTo(playerGroup.position);

      w.stateTimer -= dt;
      if (w.stateTimer <= 0) {
        // AI State transition
        if (distToPlayer < w.alertRadius) {
          if (w.type === 'deer' || w.type === 'horse') {
            w.state = 'flee';
          } else if (w.type === 'tiger') {
            w.state = 'attack';
          } else if (w.type === 'monkey') {
            w.state = 'alert';
          }
        } else {
          // Wander / Idle alternation
          w.state = (Math.random() < 0.4) ? 'idle' : 'wander';
          if (w.state === 'wander') {
            // Pick random wander waypoint within 25m of spawn
            const ang = Math.random() * Math.PI * 2;
            const dist = Math.random() * 20;
            w.targetPos.set(w.spawnPos.x + Math.cos(ang) * dist, 0, w.spawnPos.z + Math.sin(ang) * dist);
          }
        }
        w.stateTimer = Math.random() * 3 + 2.5;
      }

      // Execute AI Behavior Movement
      if (w.state === 'flee') {
        // Run directly away from player
        const fleeDir = w.pos.clone().sub(playerGroup.position).normalize();
        w.pos.addScaledVector(fleeDir, w.speed * 1.35 * dt);
        w.yaw = Math.atan2(fleeDir.x, fleeDir.z);
        if (w.type === 'monkey') playAnimalAnim(w, 'run', true);
      } else if (w.state === 'attack') {
        // Charge toward player
        const chgDir = playerGroup.position.clone().sub(w.pos).normalize();
        w.pos.addScaledVector(chgDir, w.speed * dt);
        w.yaw = Math.atan2(chgDir.x, chgDir.z);
        if (w.type === 'monkey') playAnimalAnim(w, 'run', true);
      } else if (w.state === 'wander') {
        const toTarget = w.targetPos.clone().sub(w.pos);
        if (toTarget.length() > 0.8) {
          const wDir = toTarget.normalize();
          w.pos.addScaledVector(wDir, w.speed * 0.65 * dt);
          w.yaw = Math.atan2(wDir.x, wDir.z);
          if (w.type === 'monkey') playAnimalAnim(w, 'run', true);
        } else {
          w.state = 'idle';
          if (w.type === 'monkey') playAnimalAnim(w, 'idle', true);
        }
      } else {
        // Idle
        if (w.type === 'monkey') playAnimalAnim(w, 'idle', true);
      }

      w.mesh.position.copy(w.pos);
      w.mesh.rotation.y = w.yaw;
    }

    // 6. COLLECTIBLE REWARDS ANIMATION & PROXIMITY CHECK
    for (const r of rewards) {
      if (r.collected) continue;
      r.pulseTime += dt;
      r.mesh.rotation.y += 2.2 * dt;
      r.mesh.position.y = r.pos.y + Math.sin(r.pulseTime * 4) * 0.15;

      // Proximity Collection
      if (playerGroup.position.distanceTo(r.pos) < 2.5) {
        collectReward(r);
      }
    }

    // 7. SUPER VISION 3D-TO-2D SCREEN PROJECTION (Priority 4C)
    if (STATE.powers.superVision.active) {
      const markersContainer = document.getElementById('super-vision-markers');
      let html = '';

      // Project Wildlife onto screen
      for (const w of wildlife) {
        if (w.dead) continue;
        const dist = Math.round(playerGroup.position.distanceTo(w.pos));
        if (dist > 90) continue;

        const screenPos = w.pos.clone().add(new THREE.Vector3(0, 1.8, 0)).project(camera);
        if (screenPos.z > 1) continue; // Behind camera

        const sx = (screenPos.x * 0.5 + 0.5) * window.innerWidth;
        const sy = (-screenPos.y * 0.5 + 0.5) * window.innerHeight;

        const hpPct = Math.round((w.hp / w.maxHp) * 100);
        html += `
          <div class="sv-marker" style="left:${sx}px; top:${sy}px;">
            <div class="sv-box">
              <span class="sv-title">${w.name.toUpperCase()}</span>
              <span class="sv-dist">${dist}m &bull; ${w.hp}/${w.maxHp} HP</span>
              <div class="sv-hp"><div class="sv-hp-fill" style="width:${hpPct}%;"></div></div>
            </div>
            <div class="sv-pointer"></div>
          </div>
        `;
      }

      // Project Training Automaton
      if (!STATE.dummy.dead) {
        const dist = Math.round(playerGroup.position.distanceTo(STATE.dummy.pos));
        const screenPos = STATE.dummy.pos.clone().add(new THREE.Vector3(0, 3.0, 0)).project(camera);
        if (screenPos.z <= 1) {
          const sx = (screenPos.x * 0.5 + 0.5) * window.innerWidth;
          const sy = (-screenPos.y * 0.5 + 0.5) * window.innerHeight;
          const hpPct = Math.round((STATE.dummy.hp / STATE.dummy.maxHp) * 100);
          html += `
            <div class="sv-marker" style="left:${sx}px; top:${sy}px;">
              <div class="sv-box hostile">
                <span class="sv-title">AUTOMATON</span>
                <span class="sv-dist">${dist}m &bull; ${STATE.dummy.hp}/${STATE.dummy.maxHp} HP</span>
                <div class="sv-hp"><div class="sv-hp-fill" style="width:${hpPct}%; background:#ef4444;"></div></div>
              </div>
              <div class="sv-pointer"></div>
            </div>
          `;
        }
      }

      markersContainer.innerHTML = html;
    }

    // 8. PROJECTILE KINEMATICS & HIT RESOLUTION
    for (let i = projectiles.length - 1; i >= 0; i--) {
      const pr = projectiles[i];
      pr.group.position.addScaledVector(pr.velocity, dt);
      pr.lifetime -= dt;

      // Hit Training Automaton
      if (!STATE.dummy.dead && pr.group.position.distanceTo(STATE.dummy.pos.clone().add(new THREE.Vector3(0, 2.0, 0))) < 1.8) {
        hitDummy(pr.dmg, pr.type);
        pr.onHit(pr.group.position);
        scene.remove(pr.group);
        projectiles.splice(i, 1);
        continue;
      }

      // Hit Wildlife
      let hitAnimal = false;
      for (const w of wildlife) {
        if (!w.dead && pr.group.position.distanceTo(w.pos.clone().add(new THREE.Vector3(0, 0.8, 0))) < (pr.radius + 2.0)) {
          damageWildlife(w, pr.dmg, pr.type);
          pr.onHit(pr.group.position);
          scene.remove(pr.group);
          projectiles.splice(i, 1);
          hitAnimal = true;
          break;
        }
      }
      if (hitAnimal) continue;

      // Hit Map Solids
      let hitSolid = false;
      for (const col of colliders) {
        if (!col.isStep && col.box.containsPoint(pr.group.position)) {
          hitSolid = true;
          break;
        }
      }

      if (hitSolid || pr.group.position.y <= 0 || pr.lifetime <= 0) {
        pr.onHit(pr.group.position);
        scene.remove(pr.group);
        projectiles.splice(i, 1);
      }
    }

    // 9. PARTICLES UPDATE
    for (let i = particles.length - 1; i >= 0; i--) {
      const pt = particles[i];
      pt.life -= dt;
      if (pt.isRing) {
        pt.mesh.scale.addScalar(pt.scaleSpeed * dt);
        pt.mesh.material.opacity = pt.life / pt.maxLife;
      } else {
        pt.velocity.y -= (pt.gravity || 20) * dt;
        pt.mesh.position.addScaledVector(pt.velocity, dt);
        const sc = pt.life / pt.maxLife;
        pt.mesh.scale.set(sc, sc, sc);
      }
      if (pt.life <= 0) {
        scene.remove(pt.mesh);
        particles.splice(i, 1);
      }
    }

    // 10. HUD REFRESH
    updatePlayerHUD();
    updateCDs(dt);

    renderer.render(scene, camera);
  }

  // Expose on window for runtime automation and CDP test runners
  window.STATE = STATE;
  window.playerGroup = playerGroup;
  window.camera = camera;
  window.colliders = colliders;
  window.wildlife = wildlife;
  window.rewards = rewards;
  window.loadMap = loadMap;
  window.setChar = setChar;
  window.castSlot = castSlot;
  window.activatePower = activatePower;
  window.executeSpellCommand = executeSpellCommand;
  window.openSpellCommand = openSpellCommand;
  window.closeSpellCommand = closeSpellCommand;
  window.keys = keys;
  window.SFX = SFX;
  window.camera = camera;
  window.projectiles = projectiles;
  window.damageWildlife = damageWildlife;
  window.collectReward = collectReward;
  window.wildlife = wildlife;
  window.rewards = rewards;
  window.colliders = colliders;
  window.STATE = STATE;
  window.golemMixer = golemMixer;
  window.golemAnims = golemAnims;
  window.rogueMixer = rogueMixer;
  window.rogueAnims = rogueAnims;

  // ── LAUNCH GAME PROTOTYPE ──────────────────────────────────
  loadMap('school'); // Start in user's supplied School map!
  updateHotbarUI();
  updatePlayerHUD();
  updateTargetHUD();
  renderGrimoire();

  // Position initial camera
  camPos.set(0, 3.5, -6);
  camTarget.set(0, 2.1, 0);
  animate();

} catch(e) { console.error("FATAL ERROR:", e.message, e.stack); }
</script>
</body>
</html>
''')

# Write out full content
full_html = "".join(parts)
with open("public/prototype/index.html", "w") as f:
    f.write(full_html)

os.makedirs("game/prototype", exist_ok=True)
with open("game/prototype/index.html", "w") as f:
    f.write(full_html)

print(f"Generated public/prototype/index.html ({len(full_html)} bytes)")
print(f"Synchronized game/prototype/index.html ({len(full_html)} bytes)")

