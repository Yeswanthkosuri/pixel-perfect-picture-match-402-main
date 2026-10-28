# ELEMENTAL ARENA — Development Workflow & Engine Guide

Welcome to the development workflow guide for **ELEMENTAL ARENA**. This guide is written in clear, step-by-step instructions specifically for beginners.

---

## 1. Project Directory Structure

We have established a clean separation between the **Lovable Web App** and the **GDevelop Game Engine**:

```
pixel-perfect-picture-match-402-main/
├── .git/                      <-- Version control repository (protects your project)
├── .env                       <-- Private Supabase / Lovable credentials (never committed)
├── src/                       <-- LOVABLE WEBSITE SOURCE CODE (Preserved untouched)
│   ├── routes/                <-- Web pages (landing, auth, dashboard, workshop)
│   ├── components/            <-- UI components (Radix UI, buttons, cards)
│   └── integrations/          <-- Supabase backend client & database types
├── drizzle/                   <-- Database migrations (profiles, loadouts, worlds, avatars)
├── public/                    <-- Static web assets
│   └── prototype/             <-- Web-accessible 3D game prototype
├── game/                      <-- GDEVELOP GAME SOURCE & ARCHITECTURE
│   ├── game.json              <-- Open this file directly in GDevelop 5
│   ├── prototype/             <-- Standalone 3D playable prototype (index.html)
│   ├── scenes/                <-- Colosseum and lobby layouts
│   ├── movement/              <-- 3D movement controller documentation
│   ├── camera/                <-- Orbital follow camera specifications
│   ├── combat/                <-- Weapon and raycast mechanics
│   ├── health_damage/         <-- Health, shield, and respawn logic
│   ├── elements/              <-- 12 Elemental affinities and combo reactions
│   ├── abilities/             <-- 5-slot loadout and ability catalogs
│   ├── character_config/      <-- Character configuration schema
│   ├── world_config/          <-- Map geometry and boundary definitions
│   ├── networking/            <-- Multiplayer WebRTC P2P specifications
│   ├── ui/                    <-- Combat HUD and reticle layout
│   ├── assets/                <-- Game models, textures, and sounds
│   ├── ASSET_INVENTORY.md     <-- Complete audit of all 3D models
│   ├── INTEGRATION_CONTRACT.md<-- Data interface between website and game
│   ├── MULTIPLAYER_ARCHITECTURE.md <-- Multiplayer plan
│   └── AVATAR_PIPELINE.md     <-- Photo-to-3D avatar pipeline
└── 3D Models /                <-- Raw collected 3D asset archives
```

---

## 2. How to Run & Play the 3D Prototype Right Now

You have two simple ways to play the prototype locally:

### Option A: Direct Browser Play (Easiest)
1. In macOS Finder, navigate to:
   `/Users/apple/Downloads/pixel-perfect-picture-match-402-main/game/prototype/`
2. Double-click `index.html`. It opens directly in Safari, Chrome, or any web browser!
3. Click the screen to lock cursor and start battling the Target Automaton!

### Option B: Local Web Server
1. In your terminal, run:
   ```bash
   python3 -m http.server 8085 --directory public
   ```
2. Open your browser to:
   `http://localhost:8085/prototype/index.html`

---

## 3. How to Open the Project in GDevelop 5

1. Open **GDevelop.app** on your Mac (located in `/Applications/GDevelop.app`).
2. Click **Open a project** (or `File -> Open`).
3. Navigate to:
   `/Users/apple/Downloads/pixel-perfect-picture-match-402-main/game/game.json`
4. Select `game.json` and click **Open**.
5. You can now visually edit the 3D scene, inspect the layers, objects, variables, and click **Preview** (play button) to run the game inside GDevelop!

---

## 4. Git Version Control & Safety Rules

- **Git is initialized**: Your workspace is now protected under Git.
- **Never force-push or rebase**: As connected to Lovable, always make clean, regular commits so your online project history remains in sync.
- **Backup before major changes**: Before importing large 3D models or modifying database schemas, run:
  ```bash
  git status
  git commit -am "checkpoint: description of changes"
  ```
- **No paid services required**: Everything we have established uses free, open-source tools (GDevelop 5, Three.js, Git, Supabase free tier).
