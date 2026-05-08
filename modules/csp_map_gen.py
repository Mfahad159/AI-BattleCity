import random
from ai.bfs import bfs
from constants import (
    GRID_SIZE, EMPTY, BRICK, STEEL, WATER, FOREST, EAGLE, 
    EAGLE_POS, ENEMY_SPAWNS, PLAYER_SPAWN,
    CSP_MAX_WALL_DENSITY, CSP_EAGLE_MIN_RING, CSP_FAIRNESS_DISTANCE
)

class CSPMapGenerator:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def generate(self, level=1):
        """
        Main entry point for map generation.
        """
        max_retries = 100
        for _ in range(max_retries):
            # 1. Clear grid
            self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            ex, ey = EAGLE_POS
            self.grid[ey][ex] = EAGLE
            
            # 2. Base Safety Constraint
            self._apply_base_safety()
            
            # 3. Fill terrain with constraints
            self._fill_terrain(level)
            
            # 4. Final Validation: Reachability
            if self._check_reachability():
                return self.grid
        
        # Fallback to a very simple map if CSP fails too many times
        return self._generate_fallback_map()

    def _apply_base_safety(self):
        ex, ey = EAGLE_POS
        # Classic protection: 3 bricks on top, 1 on each side
        # Positions relative to Eagle:
        # (-1, -1), (0, -1), (1, -1) -> Top
        # (-1, 0),          (1, 0)  -> Sides
        for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0)]:
            nx, ny = ex + dx, ey + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                self.grid[ny][nx] = BRICK

    def _fill_terrain(self, level):
        # Structured generation: Battle City uses vertical/horizontal strips
        # We'll use a grid-based probability to create blocks
        
        for y in range(2, GRID_SIZE - 2): # Avoid edges for better movement
            for x in range(2, GRID_SIZE - 2):
                if self.grid[y][x] != EMPTY:
                    continue
                
                # Near eagle safety zone (from ring safety)
                ex, ey = EAGLE_POS
                if abs(x - ex) <= 2 and abs(y - ey) <= 2:
                    continue

                # Near spawns
                if self._is_near_spawn(x, y):
                    continue
                
                # Use a pattern: Only place walls on certain columns/rows
                # Creates the classic 'corridor' look
                if x % 3 == 0 or y % 5 == 0: # Denser pattern
                    if random.random() < 0.75: # Higher density
                        choice = random.choices(
                            [BRICK, STEEL, WATER, FOREST], 
                            weights=[0.75, 0.1, 0.05, 0.1]
                        )[0]
                        self.grid[y][x] = choice
        
        # Post-process: Ensure main corridors are open
        for x in [6, 13, 20]:
            for y in range(GRID_SIZE):
                if self.grid[y][x] in [BRICK, STEEL]:
                    if random.random() < 0.8: # Clear 80% of blockages in these main lanes
                        self.grid[y][x] = EMPTY

    def _is_near_spawn(self, x, y):
        # Fairness constraint: No walls on spawn points
        spawns = ENEMY_SPAWNS + [PLAYER_SPAWN]
        for sx, sy in spawns:
            if abs(x - sx) + abs(y - sy) < 2:
                return True
        # Fairness constraint: No enemy spawns near player (handled in spawner, but map gen helps)
        return False

    def _check_reachability(self):
        """
        Check if Eagle is reachable from all enemy spawn points.
        """
        ex, ey = EAGLE_POS
        for sx, sy in ENEMY_SPAWNS:
            path = bfs(self.grid, (sx, sy), (ex, ey))
            if path is None:
                return False
        return True

    def _generate_fallback_map(self):
        # Very simple map: Eagle + safety wall, everything else empty
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        ex, ey = EAGLE_POS
        self.grid[ey][ex] = EAGLE
        self._apply_base_safety()
        return self.grid
