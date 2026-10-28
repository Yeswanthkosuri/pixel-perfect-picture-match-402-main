# ELEMENTAL ARENA — Asset Inventory & Compatibility Audit

This inventory audits all 3D models and media collected in the `3D Models ` directory, detailing their current import status, format validity, and exact pipeline required for GDevelop 5.

## Current Asset Registry

| Asset Name | Current File Format | Intended Use | Scale & Orientation | Animations Included | Rig Compatibility | Texture Requirements | Current Import Status | GDevelop 5 Compatibility | Action Required |
|---|---|---|---|---|---|---|---|---|---|
| **College Raimon Environment** | `.glb` (inside `collegeraimon.zip`, 449.8 MB) | Colosseum / School Arena Environment | Standard Y-Up, ~1:1 scale | Static environment (None) | Static Mesh (No rig) | Embedded PBR materials | Archived in zip | **Native (.glb)** — File is too large (450MB) for web performance | Unzip, decimate/LOD mesh in Blender to reduce from 450MB to <35MB |
| **Birds Flock Pack** | `.gltf` + `.bin` (inside `birds_gltf.zip`, 201 KB) | Ambient arena wildlife / skybox effects | Standard Y-Up, scale 0.1 | Flight cycles included | Standard skeletal rig | Embedded textures | Ready for test | **Native (.gltf)** — 100% compatible | Can be imported directly into GDevelop 3D scene |
| **Armored Stone Golem** | `.fbx` (1.8MB), `.obj`, Maya `.mb`, Unity `.unitypackage` (801MB) | Earth Element Boss / Heavy Automaton | Standard Y-Up, Height ~3.5m | Yes (in `animations.zip`) | Humanoid/Monster biped rig | Requires diffuse, normal, roughness maps | Unpacked FBX & OBJ | **Incompatible as-is** (FBX/OBJ/Unitypackage not loaded directly) | Convert `SKM_StoneGolem.fbx` + animations to single `.glb` file |
| **Rogue Character** | `.fbx` (`rogue_all.fbx`, 4.2 MB) | Shadow/Void Assassin Character | Standard Y-Up, Height ~1.8m | Multiple animations combined in FBX | Standard Humanoid rig | Embedded textures in FBX | Standalone FBX | **Incompatible as-is** | Open in Blender / FBX2glTF converter to export as `.glb` with NLA tracks |
| **Animals Free Pack** | `.obj`, `.blend` (3.1MB), `.c4d`, `.unitypackage` | Nature / Summoned beasts | Standard Y-Up | Static pose in OBJ | Requires rigging | Texture atlas in `textures.zip` | Archive | **Incompatible as-is** | Export desired animal from `.blend` as `.glb` with UV textures |
| **Monster Pack** | Maya `.ma` / `.mb` (4.4MB), `.unitypackage` | Elemental Minions | Maya Y-Up | Maya animation clips | Custom monster rig | Texture zip is 0 bytes | Incomplete | **Incompatible** | Requires Maya/Blender to export mesh; textures currently missing |
| **Sci-Fi Trooper** | `.unitypackage` (`scifitroopermanv3.unitypackage`, 71 MB) | High-Tech Suit Avatar | Unknown (Unity package) | Unknown | Unity Mecanim humanoid | Embedded in Unity assets | Packaged | **Incompatible** | Extract mesh & textures in Unity Editor, export as `.glb` |
| **FANTASTIC Village** | `.blend` (59MB), `.crdownload` (321MB) | Fantasy / Ancient Map assets | Blender Z-Up | Static props | Static | Textures in incomplete download | Incomplete / Interrupted | **Incompatible as-is** | Re-download complete archive; export static props as `.glb` |
| **Medieval Assassin Girl** | `.crdownload` (101MB), empty zip | Female Assassin Avatar | Unknown | Unknown | Unknown | Unknown | **Corrupted / Interrupted Download** | **Unusable** | Re-download from original asset source |
| **Monkey Pack** | 5x `.crdownload` files, 0-byte zips | Custom Avatar / Companion | Unknown | Unknown | Unknown | Unknown | **Corrupted / Interrupted Download** | **Unusable** | Re-download from original asset source |

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
