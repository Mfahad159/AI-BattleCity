# =============================================================================
# BATTLE CITY (TANK 1990) — AL2002 AI LAB PROJECT | SPRING 2026
# =============================================================================
# TECH STACK:  Python 3.11+ | Pygame 2.x
# INSTALL:     pip install pygame
# RUN:         python main.py
# =============================================================================
#
# ─── AI AGENT INSTRUCTIONS ───────────────────────────────────────────────────
#
# Hey AI Agent (Claude Code / Cursor / Copilot / Aider etc.) —
# This is the ROOT file of a Battle City (Tank 1990) clone built in Python +
# Pygame. The FULL game specification lives in: SPEC.md (read it first before
# doing anything). Below is the folder structure, module map, and task list.
# Always refer to SPEC.md for exact values (costs, HP, speeds, heuristics).
# Never hardcode magic numbers — use the constants defined in constants.py.
#
# ─── FOLDER STRUCTURE ────────────────────────────────────────────────────────
#
# battle_city/
# ├── main.py                   ← YOU ARE HERE. Entry point & game loop.
# ├── SPEC.md                   ← Full project specification (READ FIRST)
# ├── constants.py              ← ALL magic numbers, grid size, speeds, costs
# ├── settings.py               ← Per-level config (density, enemy pool, etc.)
# │
# ├── core/
# │   ├── game.py               ← Game class: orchestrates the 10-step game loop
# │   ├── grid.py               ← 26x26 tile grid, terrain types, map rendering
# │   ├── spawner.py            ← Enemy spawn logic + fairness constraint check
# │   └── bullet.py             ← Bullet movement, collision detection
# │
# ├── tanks/
# │   ├── base_tank.py          ← Abstract Tank class (HP, speed, fire rate, move)
# │   ├── player_tank.py        ← Player tank (keyboard input)
# │   ├── basic_tank.py         ← Simple Reflex Agent + BFS
# │   ├── fast_tank.py          ← Goal-Based Agent + Greedy Best-First
# │   ├── armor_tank.py         ← Model-Based Reflex Agent + A*
# │   └── boss_tank.py          ← Adversarial Agent + Minimax + Alpha-Beta
# │
# ├── ai/
# │   ├── bfs.py                ← BFS pathfinding (Basic Tank)
# │   ├── greedy.py             ← Greedy Best-First (Fast Tank)
# │   ├── astar.py              ← A* Search (Armor Tank)
# │   └── minimax.py            ← Minimax + Alpha-Beta Pruning (Boss Tank)
# │
# ├── modules/
# │   ├── csp_map_gen.py        ← Module A: CSP Map Generator (backtracking)
# │   ├── search_demo.py        ← Module B: Search algorithm visual demo
# │   └── boss_battle.py        ← Module C: Boss level adversarial setup
# │
# ├── levels/
# │   ├── level1.py             ← Level 1 config: Brick Maze
# │   ├── level2.py             ← Level 2 config: Steel Fortress
# │   └── boss_level.py         ← Boss Level: 12x12 arena config
# │
# ├── ui/
# │   ├── hud.py                ← HUD: lives, enemy count, level display
# │   ├── menu.py               ← Main menu screen
# │   └── game_over.py          ← Win/Lose screen
# │
# └── assets/
#     ├── sprites/              ← Tank sprites, bullet sprites, terrain tiles
#     └── sounds/               ← Shoot, explosion, game over sounds (optional)
#
# ─── MODULE RESPONSIBILITIES (for AI agent) ──────────────────────────────────
#
# constants.py   → Define: GRID_SIZE=26, TILE_SIZE=24, FPS=60, terrain cost
#                  dict, tank speeds, fire rates, HP values, spawn points,
#                  Eagle position, Boss heuristic weights.
#
# grid.py        → 26x26 int matrix. Methods: get_tile(), set_tile(),
#                  is_passable(), destroy_wall(), render(). Fires a
#                  WALL_DESTROYED event when a brick tile becomes empty.
#
# bfs.py         → bfs(grid, start, goal) → list of (x,y) tiles (path).
#                  Treats Empty+Forest as cost 1. Ignores brick cost.
#                  Re-triggered at spawn, path block, every 5 seconds.
#
# greedy.py      → greedy_step(grid, current, goal) → single (x,y) next tile.
#                  h(n) = Manhattan distance to Eagle. Recomputed every tick.
#                  No full path — just one step. No caching.
#
# astar.py       → astar(grid, start, goal) → list of (x,y) tiles (path).
#                  g costs: Empty=1, Forest=1, Brick=3, Steel=inf, Water=inf.
#                  h(n) = Manhattan distance (admissible).
#                  Re-triggered at spawn, retreat, and on WALL_DESTROYED event.
#
# minimax.py     → minimax(state, depth, alpha, beta, maximizing) → best_action.
#                  MAX=Boss, MIN=Player. Depth varies by Boss phase (2/3/4).
#                  MUST track and expose: nodes_without_pruning,
#                  nodes_with_pruning, speedup_ratio (required in report).
#
# csp_map_gen.py → generate_map(level_config) → 26x26 int grid.
#                  Uses backtracking search + forward checking.
#                  Enforces all 5 constraints (see SPEC.md Section 12).
#                  Final step: BFS reachability check — reject if Eagle
#                  unreachable from any spawn point.
#
# basic_tank.py  → SimpleReflexAgent. NO state variables. Pure IF/THEN rules.
#                  Uses bfs.py. Re-runs BFS every 5s or on path block.
#
# fast_tank.py   → GoalBasedAgent. Goal = destroy Eagle. NEVER targets player.
#                  Uses greedy.py. Single-step decision every tick.
#                  Shoots brick in path — never detours.
#
# armor_tank.py  → ModelBasedReflexAgent. Maintains self.hit_count (0-3).
#                  Uses astar.py. On hit_count==3 → BFS to nearest steel tile
#                  → retreat → wait 2s → recompute A* → resume.
#
# boss_tank.py   → AdversarialAgent. Uses minimax.py.
#                  Implements 3-phase system based on remaining HP.
#                  Phase 1 (10-7HP): depth=2. Phase 2 (6-3HP): depth=3.
#                  Phase 3 (2-1HP): depth=4.
#
# =============================================================================

import pygame
import sys
from core.game import Game
from constants import FPS, WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    game = Game(screen)

    # ── MAIN GAME LOOP ──────────────────────────────────────────────────────
    # The game loop follows the 10-step sequence defined in SPEC.md Section 6.
    # Each step is delegated to game.update() and game.render().
    # DO NOT put game logic here — keep main.py as a thin entry point only.
    # ────────────────────────────────────────────────────────────────────────
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update()          # Steps 1–8 of the game loop (see SPEC.md)
        game.render()          # Step 9: Draw everything to screen
        pygame.display.flip()
        clock.tick(FPS)        # Lock to FPS (60). Each tick = 1 game step.


if __name__ == "__main__":
    main()
