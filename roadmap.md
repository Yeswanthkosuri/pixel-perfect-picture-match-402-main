# ELEMENTAL ARENA — Roadmap

Spec source: user-uploaded ELEMENTAL_ARENA_pasted.md. Phase order from spec §18; scope agreed in chat: full foundation (Phases 1–4 core surfaces), honest labeling for anything not yet real.

## Done
- [x] Lovable Cloud enabled; email/password auth enabled
- [x] Schema: profiles (+signup trigger), avatars, loadouts, worlds with RLS + grants
- [x] Private buckets: avatar-photos (10MB), avatar-assets (50MB)

## In progress — Foundation build
- [ ] Design system (dark charcoal / electric blue / violet / cyan neon, gaming typography)
- [ ] Public: landing page (`/`), auth page (`/auth`), reset-password, world browse (`/worlds`), legal pages
- [ ] Authenticated: dashboard, avatar creator, character workshop (2 elements + 5 abilities + weapon + loadouts), world creation wizard + edit/delete/duplicate/publish/share, account settings
- [ ] Game launch page `/play` with "game build not yet integrated" state
- [ ] Integration contract doc for GDevelop (character + world config formats)

## Later (not this build)
- [ ] Phase 5: friends, invitations, match metadata (schema left extensible)
- [ ] Phase 6/7: GDevelop integration, real multiplayer
- [ ] Avatar-generation service selection + integration (UI built; generation clearly marked pending)
