# Combat System — GDevelop 3D

This system governs primary weapons, aiming, raycast hit detection, projectile spawning, and damage application.

## Weapon Archetypes & Behavior
1. **Pulse Repeater (Assault)**:
   - Firing mode: Rapid automatic / semi-burst.
   - Projectile speed: `120 m/s` (fast projectile with tracer).
   - Base damage: `20 HP`.
   - Recoil: Subtle upward camera pitch kick (`+0.008 rad` per shot).
2. **Volt Arc Caster (Energy)**:
   - Firing mode: Sustained electric raycast beam.
   - Range: `35 meters`.
   - Continuous damage: `38 HP/sec` + secondary arc to nearest enemy within 6m.
3. **Ember Fang (Close-Range)**:
   - Firing mode: Multi-pellet cone discharge (8 burning fragments).
   - Range: `15 meters` with damage falloff.
   - Max close damage: `75 HP` point-blank.

## Aiming & Crosshair
- Reticle sits fixed at viewport center `(WindowWidth() / 2, WindowHeight() / 2)`.
- Direction vector is derived directly from camera orientation.
- Raycast is performed forward `100 meters`:
  - If ray intersects enemy bounding cylinder / collider:
    - Reticle turns RED (Hit confirmation).
    - Plays audio hit-tick.
    - Spawns floating combat damage text at hit position.
