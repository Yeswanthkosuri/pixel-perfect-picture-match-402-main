// ELEMENTAL ARENA — game design catalogs.
// These are design/data definitions for the website and the future GDevelop
// integration contract. Actual in-game behavior is implemented in GDevelop.

import mapEmberCitadel from "@/assets/map-ember-citadel.jpg";
import mapFrostfallValley from "@/assets/map-frostfall-valley.jpg";
import mapNeonDistrict from "@/assets/map-neon-district.jpg";
import mapVerdantRuins from "@/assets/map-verdant-ruins.jpg";

export interface ElementDef {
  id: string;
  name: string;
  icon: string; // lucide icon name
  description: string;
  offensiveRole: string;
  utilityRole: string;
  exampleAbility: string;
  cssVar: string; // --element-<id> defined in styles.css
}

export const ELEMENTS: ElementDef[] = [
  {
    id: "fire", name: "Fire", icon: "flame", cssVar: "--element-fire",
    description: "Raw combustion and heat. Aggressive, area-denying, unforgiving.",
    offensiveRole: "Burn damage over time, igniting terrain",
    utilityRole: "Smoke screens and heat distortion",
    exampleAbility: "Expanding Flame — fire pushed by wind spreads across open ground",
  },
  {
    id: "water", name: "Water", icon: "droplets", cssVar: "--element-water",
    description: "Flow and pressure. Adaptable, controlling, everywhere.",
    offensiveRole: "Pressure jets and knockback waves",
    utilityRole: "Terrain flooding, dousing fires",
    exampleAbility: "Electrified Water — charged with lightning, stuns on contact",
  },
  {
    id: "lightning", name: "Lightning", icon: "zap", cssVar: "--element-lightning",
    description: "Instant, blinding, precise. High burst, high risk.",
    offensiveRole: "Chain bolts and burst damage",
    utilityRole: "Powering gadgets, EMP interference",
    exampleAbility: "Chain Arc — a bolt jumps between clustered enemies",
  },
  {
    id: "earth", name: "Earth", icon: "mountain", cssVar: "--element-earth",
    description: "Stone, metal, endurance. Slow to move, harder to stop.",
    offensiveRole: "Boulder throws and ground spikes",
    utilityRole: "Walls, cover, terrain reshaping",
    exampleAbility: "Molten Terrain — fused with fire, lava pools form on the ground",
  },
  {
    id: "wind", name: "Wind", icon: "wind", cssVar: "--element-wind",
    description: "Motion itself. Mobility, misdirection, escape.",
    offensiveRole: "Razor gales and projectile deflection",
    utilityRole: "Dashes, glides, boosting allies",
    exampleAbility: "Freezing Gust — paired with ice, a chilling storm front",
  },
  {
    id: "ice", name: "Ice", icon: "snowflake", cssVar: "--element-ice",
    description: "Stillness and control. Freezes the fight in place.",
    offensiveRole: "Shatter strikes on frozen targets",
    utilityRole: "Ice bridges, freezing traps",
    exampleAbility: "Permafrost Field — the ground locks enemies in place",
  },
  {
    id: "light", name: "Light", icon: "sun", cssVar: "--element-light",
    description: "Revelation and radiance. Burns away shadow and deception.",
    offensiveRole: "Focused beams and blinding flashes",
    utilityRole: "Revealing cloaked enemies, healing light",
    exampleAbility: "Contrasting Energy — against darkness, twin beams annihilate",
  },
  {
    id: "darkness", name: "Darkness", icon: "moon", cssVar: "--element-darkness",
    description: "Absence and fear. Stealth, suppression, control.",
    offensiveRole: "Shadow spikes and draining tendrils",
    utilityRole: "Cloaking fields, vision denial",
    exampleAbility: "Void Lash — a silent strike from unlit ground",
  },
  {
    id: "nature", name: "Nature", icon: "sprout", cssVar: "--element-nature",
    description: "Growth and life. Patient, regenerating, ever-spreading.",
    offensiveRole: "Thorn volleys and strangling vines",
    utilityRole: "Regrowth, healing blooms, camo foliage",
    exampleAbility: "Root Snare — vines erupt and hold a target in place",
  },
  {
    id: "gravity", name: "Gravity", icon: "magnet", cssVar: "--element-gravity",
    description: "The unseen pull. Manipulates position and momentum.",
    offensiveRole: "Crushing wells and heavy slams",
    utilityRole: "Levitation, pulling enemies off ledges",
    exampleAbility: "Singularity Point — with cosmic, a space-distortion vortex",
  },
  {
    id: "cosmic", name: "Cosmic", icon: "orbit", cssVar: "--element-cosmic",
    description: "Starlight and the void between. Exotic, reality-bending.",
    offensiveRole: "Star fragments and micro-singularities",
    utilityRole: "Blink teleports, gravity-free zones",
    exampleAbility: "Starshard Rain — debris from a dying constellation",
  },
  {
    id: "sound", name: "Sound", icon: "audio-waveform", cssVar: "--element-sound",
    description: "Frequency as a weapon. Disorients, resonates, shatters.",
    offensiveRole: "Sonic blasts and resonance damage",
    utilityRole: "Echo-locating hidden enemies, silence fields",
    exampleAbility: "Resonance Break — shatters frozen and armored targets",
  },
];

export interface AbilityDef {
  id: string;
  name: string;
  icon: string;
  category: "Mobility" | "Defense" | "Offense" | "Support";
  activation: "Active" | "Passive" | "Toggle";
  description: string;
  cooldown: string;
  duration: string;
  role: string;
}

export const ABILITIES: AbilityDef[] = [
  { id: "super-sprint", name: "Super Sprint", icon: "footprints", category: "Mobility", activation: "Active", description: "A short burst of extreme running speed.", cooldown: "8s", duration: "3s", role: "Close gaps or escape pressure" },
  { id: "double-jump", name: "Double Jump", icon: "chevrons-up", category: "Mobility", activation: "Passive", description: "A second jump while airborne.", cooldown: "—", duration: "Passive", role: "Reach high ledges, dodge in air" },
  { id: "air-dash", name: "Air Dash", icon: "wind", category: "Mobility", activation: "Active", description: "A quick directional lunge mid-air.", cooldown: "6s", duration: "Instant", role: "Aerial repositioning" },
  { id: "grappling-hook", name: "Grappling Hook", icon: "anchor", category: "Mobility", activation: "Active", description: "Fire a hook and pull toward a surface.", cooldown: "10s", duration: "Until release", role: "Vertical play and swings" },
  { id: "super-strength", name: "Super Strength", icon: "dumbbell", category: "Offense", activation: "Toggle", description: "Melee hits and object throws hit far harder.", cooldown: "Toggle", duration: "While active, drains power", role: "Breakthrough melee pressure" },
  { id: "reinforced-armor", name: "Reinforced Armor", icon: "shield-check", category: "Defense", activation: "Passive", description: "Plating reduces incoming damage.", cooldown: "—", duration: "Passive", role: "Frontline durability" },
  { id: "regeneration", name: "Regeneration", icon: "heart-pulse", category: "Support", activation: "Passive", description: "Slowly restores health when out of combat.", cooldown: "—", duration: "Passive", role: "Sustain between fights" },
  { id: "temporary-shield", name: "Temporary Shield", icon: "shield", category: "Defense", activation: "Active", description: "Projects an absorbing barrier for a few seconds.", cooldown: "18s", duration: "4s", role: "Survive a focused burst" },
  { id: "shadow-cloak", name: "Shadow Cloak", icon: "eye-off", category: "Defense", activation: "Active", description: "Blend into darkness; harder to target.", cooldown: "22s", duration: "5s", role: "Ambush and disengage" },
  { id: "tactical-scan", name: "Tactical Scan", icon: "radar", category: "Support", activation: "Active", description: "Reveal nearby enemies through walls.", cooldown: "15s", duration: "3s", role: "Information advantage" },
  { id: "quick-reload", name: "Quick Reload", icon: "rotate-cw", category: "Support", activation: "Active", description: "Reload dramatically faster.", cooldown: "5s", duration: "Instant", role: "Keep the pressure on" },
  { id: "wall-climb", name: "Wall Climb", icon: "ladder", category: "Mobility", activation: "Toggle", description: "Scale vertical surfaces for a limited time.", cooldown: "12s", duration: "Up to 6s of climbing", role: "Unusual angles and routes" },
];

export interface WeaponDef {
  id: string;
  name: string;
  category: "Assault" | "Precision" | "Close-range" | "Energy" | "Melee";
  icon: string;
  description: string;
  cosmetics: string[];
}

export const WEAPONS: WeaponDef[] = [
  { id: "pulse-repeater", name: "Pulse Repeater", category: "Assault", icon: "crosshair", description: "Rapid magnetic slug bursts with a steady climb in recoil.", cosmetics: ["Standard", "Cyan tracer", "Violet tracer", "Ember tracer"] },
  { id: "storm-autogun", name: "Storm Autogun", category: "Assault", icon: "machine-gun" in {} ? "zap" : "target", description: "High-capacity autogun that arcs tiny lightning sparks between hits.", cosmetics: ["Standard", "Storm-blue coil", "Purple coil"] },
  { id: "ion-lance", name: "Ion Lance", category: "Precision", icon: "scan-line", description: "Charged single-shot rifle that punishes anyone standing still.", cosmetics: ["Standard", "Frost-blue beam", "Solar beam"] },
  { id: "prism-marksman", name: "Prism Marksman", category: "Precision", icon: "telescope", description: "Splits light into refracted bolts that curve slightly toward targets.", cosmetics: ["Standard", "Prismatic", "Obsidian"] },
  { id: "ember-fang", name: "Ember Fang", category: "Close-range", icon: "flame-kindling", description: "Shotgun-style cone of burning pellets for doorways and corners.", cosmetics: ["Standard", "Molten", "Cinder"] },
  { id: "scatter-coil", name: "Scatter Coil", category: "Close-range", icon: "zap", description: "Short-range arc discharge — devastating within a few meters.", cosmetics: ["Standard", "Blue arc", "Violet arc"] },
  { id: "volt-arc-caster", name: "Volt Arc Caster", category: "Energy", icon: "battery-charging", description: "Sustained lightning beam that chains to a second nearby target.", cosmetics: ["Standard", "Cyan arc", "Storm violet"] },
  { id: "aether-beam", name: "Aether Beam", category: "Energy", icon: "sun-medium", description: "Focused photon lance with infinite range and slow charge-up.", cosmetics: ["Standard", "Golden", "Glacial"] },
  { id: "rift-cleaver", name: "Rift Cleaver", category: "Melee", icon: "sword", description: "Gravity-edged greatblade that warps space on impact.", cosmetics: ["Standard", "Violet edge", "Cyan edge"] },
  { id: "tempest-gauntlets", name: "Tempest Gauntlets", category: "Melee", icon: "hand-fist", description: "Electrified fists — every third strike releases a shock ring.", cosmetics: ["Standard", "Storm", "Magma"] },
];

export interface MapDef {
  id: string;
  name: string;
  tagline: string;
  description: string;
  recommendedModes: string[];
  image: string;
}

export const MAPS: MapDef[] = [
  {
    id: "ember-citadel", name: "Ember Citadel", tagline: "Volcanic fortress",
    description: "Obsidian towers above rivers of molten rock. Tight bridges, punishing heights, and lava that redraws the map.",
    recommendedModes: ["Team Deathmatch", "Last Element Standing"],
    image: mapEmberCitadel,
  },
  {
    id: "frostfall-valley", name: "Frostfall Valley", tagline: "Frozen wilderness",
    description: "Glacier walls and a frozen waterfall. Long sightlines broken by ice crevasses — precision territory.",
    recommendedModes: ["Domination", "Free-For-All"],
    image: mapFrostfallValley,
  },
  {
    id: "neon-district", name: "Neon District", tagline: "Futuristic city",
    description: "Rain-slick streets under holographic billboards. Vertical rooftops, neon cover, and airborne dashes.",
    recommendedModes: ["Team Deathmatch", "Domination"],
    image: mapNeonDistrict,
  },
  {
    id: "verdant-ruins", name: "Verdant Ruins", tagline: "Ancient forest",
    description: "Overgrown arches swallowed by jungle. Foliage concealment, root snares, and ambush-heavy play.",
    recommendedModes: ["Free-For-All", "Last Element Standing"],
    image: mapVerdantRuins,
  },
];

export const GAME_MODES = [
  { id: "free_for_all", name: "Free-For-All", status: "planned" as const, description: "Every player for themselves." },
  { id: "team_deathmatch", name: "Team Deathmatch", status: "planned" as const, description: "Two teams, highest score wins." },
  { id: "domination", name: "Domination", status: "planned" as const, description: "Hold capture zones to score." },
  { id: "last_element_standing", name: "Last Element Standing", status: "planned" as const, description: "One life. Last fighter wins." },
];

export const mapById = (id: string) => MAPS.find((m) => m.id === id);
export const elementById = (id: string) => ELEMENTS.find((e) => e.id === id);
export const abilityById = (id: string) => ABILITIES.find((a) => a.id === id);
export const weaponById = (id: string) => WEAPONS.find((w) => w.id === id);
