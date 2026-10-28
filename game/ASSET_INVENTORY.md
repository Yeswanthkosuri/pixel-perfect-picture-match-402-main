# ELEMENTAL ARENA — Asset Inventory & Compatibility Audit

This inventory audits all 3D models and media collected in the `3D Models ` directory, detailing their current import status, format validity, and exact pipeline required for GDevelop 5.

## Phase 2 Upgraded Asset Registry

| Asset Name | Source Archive & Formats | Extracted Location | Intended Use | Scale & Metrics | Textures & Materials | Integration Status in Engine |
|---|---|---|---|---|---|---|
| **School Campus (College Raimon)** | `collegeraimon.zip` (429 MB `.glb`) | `game/assets/maps/school/CollegeRaimon.glb` & `public/...` | Academic campus arena | 12,471 nodes, 790 meshes, 479 materials. 1:1 scale | Japanese high school academic building, sports fields, fences, courtyards | **Integrated (Phase 2)** — Playable via Map Selector `[M]`. Hybrid architecture with immediate playable courtyard + GLTF streaming |
| **Fantastic Medieval Village** | `Unconfirmed 516336.crdownload` (321 MB valid ZIP) | `game/assets/maps/village/` & `public/...` | Medieval RPG village | 85 building FBXs, 339 prop FBXs, terrain textures | 5x PBR textures converted to 1024x1024 PNG (Cobblestone, Grass, Stone, Farmfield, Skybox) | **Integrated (Phase 2)** — Playable via Map Selector `[M]`. Village houses, timber beams, cobblestone streets, market stalls, perimeter fences |
| **Colosseum Arena** | Procedural 3D Roman Coliseum | Core Engine | Ancient gladiatorial arena | 60m radius, 12m stone columns, perimeter battlements | Roman sandstone, bronze braziers, sand ground | **Integrated** — Fully playable, optimized 60fps WebGL 2.0 |
| **Armored Stone Golem** | `SKM_StoneGolem.fbx` + `armored_stone_golem_unity.unitypackage` (801MB) | `game/assets/models/stone_golem/` & `public/...` | Heavy Earth Automaton / Tank | 0.015 Three.js scale (~3.2m height), Camera offset 2.5m | All 27 PBR textures extracted and converted from 4K TGA to web PNGs (Albedo, Normal, Metallic, Occlusion, Emission) | **Integrated (Phase 2)** — Playable in Loadout `[TAB]`. Heavy footsteps, stone armor, right-fist cast socket `(0.8, 1.8, 0.6)` |
| **Shadow Rogue** | `rogue_all.fbx` (4.2 MB) | `game/assets/models/` & `public/...` | Agile Shadow/Void Assassin | 0.018 Three.js scale (~1.85m height), Camera offset 1.8m | Skeletal humanoid rig with dual daggers | **Integrated (Phase 2)** — Playable in Loadout `[TAB]`. High agility, dagger cast socket `(0.4, 1.4, 0.5)` |
| **Elemental Mech** | Procedural High-Tech Combat Frame | Core Engine | Arcane Tech Vanguard | 2.0m height, floating shoulder cannons | Cybernetic plating with elemental plasma emissive core | **Integrated (Phase 2)** — Playable in Loadout `[TAB]`. Chest core casting socket |
| **Map Preview Thumbnails** | JPG renders (16:9) | `public/assets/maps/previews/` | Map Selection UI `[M]` | 400x225px web optimized | Colosseum, School Campus, Fantastic Village | **Active in UI** — Instant card previews with environment badges |
| **Web 3D Libraries** | Offline Three.js r128, FBXLoader, GLTFLoader, fflate | `public/assets/libs/` & `game/assets/libs/` | Standalone offline 3D runtime | Standalone JS bundles | Zero external CDN dependency | **Active** — Enables 100% offline local gameplay |


---

## Supported Formats in GDevelop 5 (3D Engine)

### 1. Natively Supported Formats
- **`.glb` (glTF 2.0 Binary - Strongly Recommended)**:
  - Single self-contained binary file containing mesh geometry, skeleton bones, animation keyframes, and PBR textures.
  - Loads fastest in GDevelop and Three.js runtime with minimal memory footprint.
- **`.gltf` (glTF 2.0 JSON + `.bin` + image textures)**:
  - Supported, but multiple files must be placed in the same asset directory.

### 2. Formats NOT Directly Supported by GDevelop
- **`.unitypackage`**: Proprietary Unity format. Cannot be read by GDevelop or web browsers. Must be extracted inside Unity and exported to GLTF.
- **`.fbx`**: Proprietary Autodesk format. GDevelop's web runtime does not bundle heavy FBX parsers.
- **`.obj`**: Wavefront OBJ lacks skeletal bone animation support and separate material `.mtl` linking is fragile in web builds.
- **`.blend` / `.c4d` / `.mb` / `.ma`**: Native project files from Blender, Cinema 4D, and Maya. Must be exported to `.glb`.
- **`.crdownload`**: Incomplete Chrome browser downloads. These are broken and will corrupt if renamed.

---

## Asset Conversion Pipeline to GLB

To convert any FBX, OBJ, or Blend model into a production-ready GDevelop `.glb`:
1. **Download Blender** (Free, open-source).
2. **Import Model**: `File -> Import -> FBX` (or OBJ).
3. **Verify Scale and Rotation**:
   - Apply transforms: `Ctrl + A -> All Transforms`.
   - Ensure character height is between `1.7m` and `2.0m`.
   - Forward facing along **-Z axis** with **+Y up**.
4. **Animation Check**:
   - Ensure animation clips are pushed to the **NLA (Non-Linear Animation) Stash**.
   - Common naming convention: `Idle`, `Walk`, `Run`, `Jump`, `Attack_Primary`, `Attack_Fire`, `Attack_Lightning`, `Hit_React`, `Death`.
5. **Texture Optimization**:
   - Ensure texture resolutions do not exceed `2048x2048` (use 1024x1024 for web performance).
   - Use PNG or JPEG.
6. **Export**:
   - `File -> Export -> glTF 2.0 (.glb)`.
   - Under *Include*: check `Limit to Selected Objects`.
   - Under *Animation*: check `Group by NLA Track` and `Export Deformation Bones Only`.
