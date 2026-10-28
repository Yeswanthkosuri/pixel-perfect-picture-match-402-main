# Health & Damage System — GDevelop 3D

This system manages health pools, rechargeable shields, damage mitigation, death states, and arena respawning.

## Vital Statistics
- **Max Health**: `100.0`
- **Max Shield**: `50.0` (Absorbs damage first; begins regenerating after 5 seconds of not taking damage at `15 Shield/sec`).
- **Invulnerability Period**: `2.5 seconds` upon respawn (indicated by a cyan energy mesh aura).

## Damage Formula
```
Incoming Damage -> Shield Absorber
If (Damage <= Shield) {
    Shield -= Damage;
    ResidualDamage = 0;
} Else {
    ResidualDamage = Damage - Shield;
    Shield = 0;
    Health -= ResidualDamage;
}
```

## Death & Respawn Sequence
1. When `Health <= 0`:
   - Set player state to `DEAD`.
   - Disable movement and input controllers.
   - Detonate player chassis into particle emitters matching equipped primary element.
   - Display HUD overlay: `RE-MATERIALIZING COMBAT CHASSIS...` with 2.5s timer.
2. At timer expiration:
   - Reposition player at active spawn beacon `(0, 1.0, -20)`.
   - Reset `Health = 100`, `Shield = 50`, `Stamina = 100`.
   - Activate 2.5s invulnerability shield.
   - Re-enable input and play respawn sound.
