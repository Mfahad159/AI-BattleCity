# =============================================================================
# constants.py — Single source of truth for ALL magic numbers.
# AI Agent: import from here. NEVER hardcode these values anywhere else.
# All values are taken directly from SPEC.md.
# =============================================================================

# ── WINDOW & GRID ─────────────────────────────────────────────────────────────
GRID_SIZE      = 26          # 26x26 tile grid
TILE_SIZE      = 24          # pixels per tile (adjust for screen fit)
TITLE_BAR_HEIGHT = 30
WINDOW_WIDTH   = GRID_SIZE * TILE_SIZE + 160   # +160 for HUD sidebar
WINDOW_HEIGHT  = GRID_SIZE * TILE_SIZE + TITLE_BAR_HEIGHT
WINDOW_TITLE   = "Battle City"
FPS            = 60          # 1 game tick = 1 frame

# ── TERRAIN TILE VALUES ───────────────────────────────────────────────────────
EMPTY   = 0
BRICK   = 1
STEEL   = 2
WATER   = 3
FOREST  = 4
EAGLE   = 5

# ── A* TILE COSTS ─────────────────────────────────────────────────────────────
INF = float('inf')
ASTAR_COST = {
    EMPTY:  1,
    FOREST: 1,
    BRICK:  3,      # Shoot + wait penalty
    STEEL:  INF,    # Absolute barrier
    WATER:  INF,    # Tanks cannot cross
    EAGLE:  0,      # Goal tile
}

# ── FIXED POSITIONS ───────────────────────────────────────────────────────────
EAGLE_POS        = (12, 24)
PLAYER_SPAWN     = (4, 24)
ENEMY_SPAWNS     = [(0, 0), (12, 0), (24, 0)]  # TL, TC, TR

# ── PLAYER ────────────────────────────────────────────────────────────────────
PLAYER_LIVES     = 10
PLAYER_HP        = 1         # 1 hit to destroy

# ── SPAWN SYSTEM ──────────────────────────────────────────────────────────────
MAX_ACTIVE_ENEMIES      = 3         # Level 1 & 2
TOTAL_ENEMY_POOL        = 20        # Per level
SPAWN_FAIRNESS_DISTANCE = 10        # Min Manhattan distance from player

# ── TANK SPEEDS (ticks per tile move) ─────────────────────────────────────────
# Lower number = faster (moves every N ticks)
SPEED_SLOW   = 4   # Basic Tank
SPEED_MEDIUM = 3   # Armor Tank
SPEED_FAST   = 2   # Fast Tank

# ── BULLET SPEED ──────────────────────────────────────────────────────────────
BULLET_SPEED_MULTIPLIER = 2   # Bullets move 2x tank speed

# ── FIRE RATES (ticks between shots) ──────────────────────────────────────────
# At 60 FPS: 1s = 60 ticks, 1.5s = 90 ticks, 2s = 120 ticks, 3s = 180 ticks
FIRE_RATE_BASIC  = 180   # 1 bullet every 3 seconds
FIRE_RATE_FAST   = 90    # 1 bullet every 1.5 seconds
FIRE_RATE_ARMOR  = 120   # 1 bullet every 2 seconds

# ── TANK HP ───────────────────────────────────────────────────────────────────
HP_BASIC  = 1
HP_FAST   = 1
HP_ARMOR  = 4
HP_BOSS   = 10

# ── BFS REPLAN INTERVAL ───────────────────────────────────────────────────────
BFS_REPLAN_TICKS = 5 * FPS   # Re-run BFS every 5 seconds

# ── ARMOR TANK RETREAT WAIT ───────────────────────────────────────────────────
ARMOR_RETREAT_WAIT_TICKS = 2 * FPS   # Wait 2 seconds behind cover before resuming

# ── BOSS TANK — PHASE CONFIG ──────────────────────────────────────────────────
BOSS_PHASES = {
    1: {
        "hp_range":   (7, 10),
        "speed":      SPEED_SLOW,
        "fire_rate":  2 * FPS,     # 1 bullet per 2 seconds
        "depth":      2,
        "behavior":   "aggressive_push",
    },
    2: {
        "hp_range":   (3, 6),
        "speed":      SPEED_MEDIUM,
        "fire_rate":  int(1.5 * FPS),
        "depth":      3,
        "behavior":   "balanced_cover",
    },
    3: {
        "hp_range":   (1, 2),
        "speed":      SPEED_FAST,
        "fire_rate":  int(0.8 * FPS),
        "depth":      4,
        "behavior":   "desperate_rush",
    },
}

# ── BOSS EVALUATION HEURISTIC WEIGHTS ────────────────────────────────────────
BOSS_HEURISTIC = {
    "player_within_3_tiles":     +60,
    "player_in_line_of_sight":   +50,
    "boss_adjacent_to_steel":    +30,
    "player_hp_missing_per_hp":  +20,
    "boss_hp_missing_per_hp":    -40,
    "player_in_forest":          -20,
}

# ── BOSS ARENA (Boss Level only) ─────────────────────────────────────────────
BOSS_ARENA_SIZE = 12   # 12x12 tile arena

# ── CSP MAP GENERATOR CONSTRAINTS ────────────────────────────────────────────
CSP_MAX_WALL_DENSITY   = 0.40   # Max 40% of tiles can be walls
CSP_EAGLE_MIN_RING     = 1      # Min 1 ring of Brick/Steel around Eagle
CSP_FAIRNESS_DISTANCE  = 10     # No spawn within 10 tiles of player start

# ── LEVEL 1 SPECIFIC ──────────────────────────────────────────────────────────
LVL1_FAST_TANK_UNLOCK_KILLS = 10   # Fast tanks spawn only after 10 kills
LVL1_EAGLE_BRICK_LAYERS     = 2    # Eagle must have 2 brick layers at start

# ── COLORS & AESTHETICS (from design.md) ───────────────────────────────────────
# Primary Surface Colors
BG_PRIMARY        = (8,   10,  22)     # Main game canvas (deep navy)
BG_SECONDARY      = (14,  17,  35)     # HUD / sidebar background
BG_SURFACE        = (20,  24,  46)     # Card surfaces, menus
BG_ELEVATED       = (28,  33,  60)     # Hover states, active cells

# Grid overlay (RGBA — very subtle)
GRID_LINE_COLOR   = (255, 255, 255, 12)

# Neon Accents
CYAN              = (0,   240, 255)    # Player, UI highlights
CYAN_DIM          = (0,   150, 160)
AMBER             = (255, 185, 0)      # Enemy tanks, warnings
AMBER_DIM         = (160, 110, 0)
RED_HOT           = (255, 55,  55)     # Boss, destruction, game over
RED_DIM           = (140, 25,  25)
MINT              = (0,   255, 160)    # Power-ups, success
MINT_DIM          = (0,   140, 85)
PURPLE            = (180, 80,  255)    # Boss phase accent
PURPLE_DIM        = (90,  35,  130)

# Terrain Colors
TERRAIN_COLORS = {
    EMPTY:  BG_PRIMARY,
    BRICK:  (160, 82,  45),     # Warm terracotta
    STEEL:  (110, 120, 135),    # Metallic gray
    WATER:  (20,  60,  120),    # Deep ocean blue
    FOREST: (30,  75,  40),     # Dark woodland green
    EAGLE:  AMBER,              # Glowing amber
}

# UI Text Colors
TEXT_PRIMARY      = (230, 235, 255)    # Off-white blue tint
TEXT_SECONDARY    = (120, 130, 165)    # Muted
TEXT_ACCENT       = CYAN
TEXT_DANGER       = RED_HOT
TEXT_SUCCESS      = MINT
TEXT_DISABLED     = (55,  60,  85)

# Effects
BRICK_HIT_FLASH   = (255, 140, 60)
BRICK_CRUMBLE     = (100, 50,  20)

# ── TYPOGRAPHY ────────────────────────────────────────────────────────────────
FONT_SIZE_TITLE   = 36
FONT_SIZE_HEADING = 22
FONT_SIZE_BODY    = 16
FONT_SIZE_SMALL   = 12
FONT_SIZE_TINY    = 10
FONT_FAMILY       = ["Courier New", "Consolas", "monospace"]
