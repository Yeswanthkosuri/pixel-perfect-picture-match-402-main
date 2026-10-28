# ELEMENTAL ARENA — Website to Game Integration Contract

This document defines the interface and data contract between the **Lovable Web Application** (Dashboard, Authentication, Loadout Workshop, World Builder) and the **GDevelop Game Engine**.

---

## Architecture Overview

```
+-------------------------------------------------------------+
|                     LOVABLE WEB APP                         |
|  - User Auth (Supabase)       - World Creation Wizard       |
|  - Character Workshop         - Matchmaking / Session Init  |
+-------------------------------------------------------------+
                              |
                     window.postMessage
          (Structured Event Bridge / Zero Credentials)
                              |
                              v
+-------------------------------------------------------------+
|                   GDEVELOP GAME RUNNER                      |
|               (Embedded Iframe / Web Build)                 |
|  - Local Standalone Fallback  - Real-time 3D Three.js Engine|
|  - Loadout Ingestion          - Combat Loop & Visuals       |
+-------------------------------------------------------------+
                              ^
                              |
                       WebRTC / WebSocket
                    (Low-latency Combat Sync)
                              |
                              v
+-------------------------------------------------------------+
|             REAL-TIME MULTIPLAYER SERVICE / P2P             |
+-------------------------------------------------------------+
```

---

## Security Directives
1. **No Tokens in URLs**: Authentication tokens, refresh tokens, and database service keys MUST NEVER be passed in URL query parameters or hash fragments.
2. **PostMessage Handshake**: The game iframe and parent website communicate via `window.postMessage` with strict origin verification (`event.origin === window.location.origin`).
3. **No HTTP for Real-Time Combat**: Traditional HTTP REST requests are strictly for out-of-game data (saving world configs, querying profiles, storing loadout presets). In-game combat is synchronized via WebRTC data channels or low-latency WebSockets.

---

## 1. Handshake & Initialization Sequence

1. The parent website renders the game iframe:
   ```html
   <iframe id="game-viewport" src="/play/engine/index.html" allow="pointer-lock; autoplay"></iframe>
   ```
2. When the game engine finishes loading its assets, it sends a ready signal to parent:
   ```javascript
   window.parent.postMessage({ type: "ELEMENTAL_ARENA_GAME_READY" }, "*");
   ```
3. The Lovable web app responds with the verified player session and loadout payload:
   ```javascript
   iframe.contentWindow.postMessage({
     type: "ELEMENTAL_ARENA_INIT_SESSION",
     payload: sessionPayload
   }, window.location.origin);
   ```

---

## 2. Ingest Payload Schema (`INIT_SESSION`)

```typescript
interface ElementalArenaSessionPayload {
  // 1. Player Identity
  player: {
    userId: string;             // UUID from public.profiles
    username: string;           // Display handle
    avatarModelUrl?: string;    // Custom .glb avatar URL from Supabase storage (optional)
    rigId?: string;             // Humanoid rig standard
  };

  // 2. Character Loadout
  loadout: {
    name: string;
    elements: [string, string]; // Exactly 2 elements (e.g. ["fire", "lightning"])
    abilities: [string, string, string, string, string]; // Exactly 5 abilities
    weaponId: string;           // e.g. "pulse-repeater", "volt-arc-caster", "ember-fang"
    appearance: {
      colorTheme?: string;
      glowIntensity?: number;
    };
  };

  // 3. Match & World Configuration
  match: {
    worldId: string;            // UUID from public.worlds (or "default_arena")
    mapId: string;              // "ember-citadel" | "frostfall-valley" | "neon-district" | "verdant-ruins"
    gameMode: "free_for_all" | "team_deathmatch" | "domination" | "last_element_standing";
    maxPlayers: number;         // e.g. 8
    durationMinutes: number;    // e.g. 10
    respawnRule: "instant" | "timed_5s" | "none";
    friendlyFire: boolean;
    sessionId?: string;         // Matchmaking room ID
    isHost?: boolean;           // Host status for P2P coordination
  };
}
```

---

## 3. Game-to-Website Telemetry Events

During and after the match, the game posts status events back to the parent website:

### `MATCH_START`
```javascript
{
  type: "ELEMENTAL_ARENA_MATCH_START",
  timestamp: 1729864200000,
  mapId: "ember-citadel"
}
```

### `PLAYER_ELIMINATED`
```javascript
{
  type: "ELEMENTAL_ARENA_PLAYER_ELIMINATED",
  victimId: "user-uuid-1",
  killerId: "user-uuid-2",
  elementUsed: "fire",
  weaponUsed: "pulse-repeater"
}
```

### `MATCH_CONCLUDED`
```javascript
{
  type: "ELEMENTAL_ARENA_MATCH_CONCLUDED",
  matchDuration: 542, // seconds
  winnerUserId: "user-uuid-2",
  leaderboard: [
    { userId: "user-uuid-2", kills: 12, deaths: 3, score: 2400 },
    { userId: "user-uuid-1", kills: 5, deaths: 8, score: 1100 }
  ]
}
```

---

## 4. Standalone Local Fallback Mode

During local development or when the game is launched directly outside the Lovable website (`game/prototype/index.html` or in GDevelop preview):
- The game checks `window.parent === window`.
- If running standalone, it automatically initializes default offline values:
  - `username = "Fighter_Local"`
  - `elements = ["fire", "lightning"]`
  - `abilities = ["super-sprint", "inferno-orb", "thunder-surge", "double-jump", "temporary-shield"]`
  - `weaponId = "pulse-repeater"`
  - `mapId = "default-arena"`
- This guarantees the game remains 100% playable and testable locally at all times without requiring a live website or server connection.
