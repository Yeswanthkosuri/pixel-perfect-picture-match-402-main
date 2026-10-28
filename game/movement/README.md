# Player Movement System — GDevelop 3D

This system handles 3D character translation, sprinting, jumping, air control, slope stepping, and collision bounding.

## Coordinate Space
- **X-axis**: Horizontal Left / Right
- **Y-axis**: Vertical Up (Positive) / Down (Gravity)
- **Z-axis**: Depth Forward / Backward

## Parameters
| Parameter | Default Value | Description |
|---|---|---|
| `WalkSpeed` | `14.0 m/s` | Base tactical movement speed |
| `SprintSpeed` | `24.0 m/s` | Accelerated speed when holding Shift (drains Stamina) |
| `JumpForce` | `16.0 m/s` | Upward impulse on Spacebar |
| `Gravity` | `36.0 m/s²` | Continuous downward acceleration |
| `AirControl` | `0.65` | Momentum steering multiplier while airborne |
| `RotationSpeed` | `12.0 rad/s` | Slerp interpolation speed turning toward movement angle |

## GDevelop Event Logic
1. **Camera-Relative Vector Transformation**:
   - `MoveX = (Key W - Key S) * -sin(Camera.Yaw) + (Key D - Key A) * cos(Camera.Yaw)`
   - `MoveZ = (Key W - Key S) * -cos(Camera.Yaw) + (Key D - Key A) * -sin(Camera.Yaw)`
2. **Stamina Depletion & Regeneration**:
   - Condition: `Key Shift is pressed` AND `PlayerStamina > 0` AND `Moving`
   - Action: `Subtract 25 * TimeDelta() from PlayerStamina`, `Set Speed = SprintSpeed`
   - Else: `Add 18 * TimeDelta() to PlayerStamina` (capped at 100), `Set Speed = WalkSpeed`
3. **Ground Collision**:
   - Raycast downward `Distance: 1.1m` from character origin.
   - If hit surface: `IsGrounded = true`, `VerticalVelocity = 0`.
   - If Space pressed and `IsGrounded`: `VerticalVelocity = JumpForce`, `IsGrounded = false`.
