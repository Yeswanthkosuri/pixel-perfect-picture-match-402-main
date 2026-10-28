# ELEMENTAL ARENA — Face-to-Avatar Character Pipeline

> [!WARNING]
> **Honest Labeling Notice**: The current build does NOT generate live 3D avatars from user photographs. The database tables (`public.avatars`) and private storage buckets (`avatar-photos`, `avatar-assets`) are pre-configured to receive generated avatars once a third-party generation provider is integrated. Until then, standard game chassis avatars are used.

---

## 1. Candidate Avatar-Generation Providers Evaluated

| Provider | Model Quality | Skeleton / Rig Format | Output Format | Integration API | Cost Tier | Verdict |
|---|---|---|---|---|---|---|
| **Ready Player Me** | Stylized Cyberpunk / Humanoid | Standard Humanoid (Mixamo compatible) | `.glb` directly | Mature REST API & Web SDK | Free tier + Paid enterprise | **Strongest Candidate** — Guaranteed bone compatibility & web-optimized GLB |
| **Tripo3D** | Photorealistic & Stylized 3D | Optional auto-rigging | `.glb` / `.obj` | REST API | Token / Subscription | High quality meshes, but rigging requires verification |
| **Meshy.ai** | AI 3D Mesh Generation | Auto-biped rig | `.glb` | REST API | Subscription | Good texture quality; polycount often high (needs LOD) |
| **Hyper3D / Rodin** | Ultra-high detail meshes | Custom bones | `.glb` | Enterprise API | Paid | High fidelity; requires heavy mesh decimation for web 3D |

---

## 2. Technical Rig & Mesh Requirements for GDevelop 3D

For any generated avatar to seamlessly play combat animations (Run, Jump, Cast Fire, Cast Lightning, Melee Slash):

1. **Standardized Humanoid Bone Hierarchy**:
   - Must follow standard Mixamo / Unity Humanoid naming:
     ```
     Hips
       ├── Spine -> Spine1 -> Spine2 -> Neck -> Head
       ├── LeftUpLeg -> LeftLeg -> LeftFoot -> LeftToeBase
       ├── RightUpLeg -> RightLeg -> RightFoot -> RightToeBase
       ├── LeftShoulder -> LeftArm -> LeftForeArm -> LeftHand
       └── RightShoulder -> RightArm -> RightForeArm -> RightHand
     ```
2. **Animation Retargeting**:
   - GDevelop does not feature runtime animation retargeting.
   - Therefore, the generated `.glb` avatar must either:
     - Share the identical bone binding matrix and rest pose (T-Pose) as the base combat animations, OR
     - Have the standard animation clips embedded into the `.glb` file before upload.
3. **Mesh Polycount & LODs**:
   - Maximum polygon budget: **15,000 to 25,000 triangles** for browser performance.
   - Raw AI outputs (often 200,000+ triangles) must pass through automatic decimation before storage.
4. **Texture Optimization**:
   - Textures must be packed into a single PBR texture atlas (Albedo, Normal, Roughness/Metallic).
   - Maximum resolution: **1024x1024** (or 2048x2048 max). Format: PNG / WebP or KTX2.
5. **Character Scale & Orientation**:
   - Bounding height: **1.75m to 1.95m**.
   - Pivot point: Bottom center of feet `(0, 0, 0)`.
   - Forward facing: **-Z axis** with **+Y up**.

---

## 3. Privacy, Player Consent & Storage Architecture

In accordance with GDPR, CCPA, and COPPA privacy standards:

1. **Explicit Consent Gate**:
   - Before uploading any facial photograph, the player must accept the Avatar Generation Terms:
     - Field: `consent_version` (e.g. `"v1.0"`) and `consent_accepted_at` (timestamp) saved in `public.avatars`.
2. **Zero Permanent Photo Retention**:
   - Facial photographs uploaded to the `avatar-photos` private Supabase bucket are stored with strict Row-Level Security (RLS) accessible ONLY by the authenticated owner.
   - Once the 3D model is generated, the raw photograph SHOULD be purged automatically or retained only if the user explicitly opts in for re-generation.
3. **Secure Asset Storage**:
   - Generated `.glb` models are stored in the `avatar-assets` bucket under folder `/{userId}/{avatarId}.glb`.
   - Accessible only by the authenticated owner, preventing unauthorized scraping of player likenesses.
