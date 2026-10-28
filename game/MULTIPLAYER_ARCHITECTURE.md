# ELEMENTAL ARENA — Multiplayer Networking Architecture

> [!IMPORTANT]
> **Status**: Local single-player prototype complete. Multiplayer architecture is defined below and will be implemented in sequential phases. No multiplayer implementation is marked complete until verified across two distinct client instances.

---

## 1. GDevelop Multiplayer Options Evaluated

We investigated two core networking options available for GDevelop 5:

### Option A: GDevelop Native P2P / WebRTC (Built-in Extension)
- **Mechanism**: WebRTC DataChannels connecting players peer-to-peer. Uses GDevelop's public broker server (or custom PeerJS/broker server) solely for initial SDP signaling.
- **Latency**: Direct peer-to-peer (minimal latency between nearby players).
- **Hosting Cost**: Free / very low (no dedicated servers required).
- **Topology**: Host-Client model (one player acts as session host and authoritative arbiter).
- **Recommendation for Phase 1**: **Recommended for early 1v1 and small 2-to-4 player testing.**

### Option B: Authoritative WebSockets (Colyseus or Supabase Realtime Broadcast)
- **Mechanism**: Dedicated stateful node server or Supabase Realtime broadcast channels.
- **Latency**: ~30-60ms depending on region.
- **Topology**: Dedicated authoritative server.
- **Recommendation for Phase 2**: Ideal for 8-player competitive matches, preventing host advantage and desync.

---

## 2. Session Joining & Matchmaking Flow (P2P Model)

```
[Player 1: Host]                                 [Player 2: Client]
       |                                                 |
       |--- 1. Creates Room (e.g., Code "ELEM-492") --->|
       |    Registers ID on Broker Signaling Server     |
       |                                                 |
       |<-- 2. Enters Code & Initiates WebRTC SDP Connect-|
       |                                                 |
       |=== 3. Direct WebRTC P2P DataChannel Established =|
       |                                                 |
       |--- 4. Host Sends Room Snapshot (Map, Rules) --->|
       |                                                 |
       |<-- 5. Client Acknowledges & Spawns Character ---|
```

1. **Host Session Creation**:
   - Host generates a 6-character room code (e.g., `ELEM-982`).
   - Host opens WebRTC signaling channel via broker.
2. **Client Joining**:
   - Client enters room code on Lovable web UI or in-game lobby.
   - Broker exchanges ICE candidates and establishes encrypted P2P data connection.
3. **Session Validation**:
   - Host validates that the client's version matches host version.
   - Host validates that selected elements and abilities conform to world restrictions (from `public.worlds.allowed_elements`).

---

## 3. Movement Synchronization (Client-Side Prediction & Interpolation)

In real-time 3D combat, sending every mouse movement over the network causes lag spikes. We use an **interpolated state snapshot model**:

### Packet Format (`PLAYER_TRANSFORM`):
```json
{
  "type": "TRANSFORM",
  "playerId": "user-uuid",
  "tick": 4921,
  "posX": 12.45,
  "posY": 0.0,
  "posZ": -18.2,
  "yaw": 1.57,
  "velX": 14.0,
  "velZ": 0.0,
  "isSprinting": true,
  "isJumping": false
}
```

### Transmission Rate:
- Broadcasted at **20 Hz** (every 50ms) via unreliable WebRTC data channel (`ordered: false, maxRetransmits: 0`) to avoid head-of-line blocking.

### Remote Client Handling:
- The remote client receives position packets into a small circular buffer (100ms jitter buffer).
- Performs linear interpolation (Lerp) between previous position and current position:
  $$\text{RenderPos} = \text{Lerp}(\text{Pos}_{t-1}, \text{Pos}_t, \alpha)$$
- Performs dead reckoning if a packet drops.

---

## 4. Combat State Synchronization (Host-Authoritative Hit Registration)

To eliminate desync and hit disputes:

1. **Cast Action (Client to Host)**:
   - When Player 2 presses `Q` (Inferno Orb), Player 2 instantly displays local cast animation and sends a reliable packet to Host:
     ```json
     {
       "type": "ABILITY_CAST",
       "casterId": "player-2",
       "ability": "inferno-orb",
       "origin": [12.4, 1.8, -18.2],
       "direction": [0.0, 0.1, 1.0],
       "clientTimestamp": 1729864205120
     }
     ```
2. **Host Verification & Broadcast**:
   - Host receives the cast packet, verifies cooldown validity, and replicates projectile spawn to all clients.
3. **Hit Resolution**:
   - Host calculates collision between projectile and player bounding boxes.
   - If hit: Host calculates damage, deducts Shield/Health, and broadcasts authoritative `DAMAGE_EVENT`:
     ```json
     {
       "type": "APPLY_DAMAGE",
       "targetId": "player-1",
       "damage": 45,
       "newHealth": 55,
       "newShield": 0,
       "knockback": [0, 4, 12]
     }
     ```
   - All clients apply damage and play hit react animations simultaneously.

---

## 5. External Services Required

| Feature | Requirement | Service Provider | Cost Status |
|---|---|---|---|
| **WebRTC Signaling / Broker** | Required for initial handshake between clients | GDevelop Default Broker or Free Public PeerJS Cloud | Free |
| **STUN Server** | Required to resolve public IP addresses behind NAT | Google Free STUN (`stun.l.google.com:19302`) | Free |
| **TURN Relay Server** | Required ONLY when both players are behind strict symmetric NATs / corporate firewalls | Metered.ca (Free 50GB/mo tier) or Coturn | Free tier available |
| **Player Loadout Persistence** | Storing selected elements, weapons, and stats | Lovable Cloud / Supabase Database | Existing setup |

---

## 6. Two-Client Local Testing Plan (Next Phase)

To test multiplayer before deploying publicly:
1. Export GDevelop HTML5 build to `public/game/`.
2. Open Browser Window 1: Host match at `http://localhost:5173/play?host=true`.
3. Open Browser Window 2 (Incognito): Join match using generated room code.
4. Verify:
   - Both characters render in the 3D colosseum.
   - Movement from Window 1 updates Window 2 smoothly.
   - Casting `Q` (Inferno Orb) from Window 1 inflicts damage and updates health on Window 2.
   - Respawn triggers correctly on Window 2 when health reaches zero.
