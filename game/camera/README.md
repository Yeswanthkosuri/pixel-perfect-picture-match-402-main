# Camera System — GDevelop 3D Orbital Follow Camera

This system implements a responsive third-person camera that follows the player smoothly while allowing full 360-degree orbital control and pitch limits.

## Configuration Parameters
- **Target Offset**: `(0, 2.2, 0)` meters above the player's root (chest/shoulder level).
- **Default Distance**: `8.0` meters.
- **Min / Max Distance (Zoom)**: `4.0m` to `14.0m`.
- **Mouse Sensitivity**: `0.0025` radians per pixel.
- **Pitch Clamps**: `-20°` (looking up) to `+70°` (looking straight down).
- **Smooth Factor (Damping)**: `0.15` per frame for camera translation.

## Mathematical Formulation
```
Camera.X = Player.X + sin(Yaw) * cos(Pitch) * Distance
Camera.Y = Player.Y + 2.2 + sin(Pitch) * Distance
Camera.Z = Player.Z + cos(Yaw) * cos(Pitch) * Distance
Camera.LookAt(Player.X, Player.Y + 2.2, Player.Z)
```

## Camera Occlusion / Collision
When obstacles or arena boundaries intervene between the player and the camera:
1. Cast ray from `Player.Center` to desired `Camera.Position`.
2. If hit detected with obstacle collider, adjust `Distance = HitPoint.Distance - 0.5m`.
3. Prevents camera clipping inside walls.
