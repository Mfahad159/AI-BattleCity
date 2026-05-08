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
        # 1. Fixed Positions
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
        else:
            # If failed, try again (simple retry logic for CSP)
            return self.generate(level)

    def _apply_base_safety(self):
        ex, ey = EAGLE_POS
        # One ring of walls (Brick by default)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = ex + dx, ey + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if self.grid[ny][nx] == EMPTY:
                        self.grid[ny][nx] = BRICK

    def _fill_terrain(self, level):
        # Determine densities based on level
        wall_density = min(CSP_MAX_WALL_DENSITY, 0.2 + (level * 0.05))
        
        total_tiles = GRID_SIZE * GRID_SIZE
        max_walls = int(total_tiles * wall_density)
        wall_count = 0
        
        # Iterate and assign terrain using a simple backtracking-like approach
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != EMPTY:
                    continue
                
                # Forward checking: Avoid placing walls near spawns or player
                if self._is_near_spawn(x, y):
                    self.grid[y][x] = EMPTY
                    continue
                
                # Randomly assign based on domain and density
                if wall_count < max_walls and random.random() < wall_density:
                    # Domain: {BRICK, STEEL, WATER, FOREST}
                    choice = random.choices(
                        [BRICK, STEEL, WATER, FOREST], 
                        weights=[0.6, 0.1, 0.1, 0.2]
                    )[0]
                    self.grid[y][x] = choice
                    wall_count += 1
                else:
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
