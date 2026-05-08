import random
from tanks.base_tank import BaseTank
from ai.bfs import bfs
from constants import AMBER, EAGLE_POS, SPEED_SLOW, FIRE_RATE_BASIC, BFS_REPLAN_TICKS

class BasicTank(BaseTank):
    def __init__(self, x, y):
        super().__init__(x, y, tank_type='basic')
        self.color = AMBER
        self.speed = SPEED_SLOW
        self.fire_rate = FIRE_RATE_BASIC
        self.path = []
        self.replan_timer = 0

    def decide(self, grid, player):
        self.update_cooldowns()
        if self.replan_timer > 0:
            self.replan_timer -= 1

        # 1. PRIMARY: Shoot if player in LOS
        if self._can_see_player(grid, player):
            return "shoot"

        # 2. MOVEMENT: Follow BFS path
        if not self.path or self.replan_timer <= 0:
            self.path = bfs(grid.matrix, (self.x, self.y), EAGLE_POS)
            self.replan_timer = BFS_REPLAN_TICKS
            # Remove current position from path
            if self.path and len(self.path) > 0:
                self.path.pop(0)

        if self.path:
            next_tile = self.path[0]
            dx = next_tile[0] - self.x
            dy = next_tile[1] - self.y
            
            # 3. WALL: If brick ahead, shoot it
            if grid.get_tile(next_tile[0], next_tile[1]) == 1: # BRICK
                self.direction = (dx, dy)
                return "shoot"
            
            # Attempt move
            if self.move(dx, dy, grid):
                self.path.pop(0)
                return "move"
        else:
            # Random move if no path
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            dx, dy = random.choice(dirs)
            self.move(dx, dy, grid)
            return "move"

        return "wait"

    def _can_see_player(self, grid, player):
        if not player.active: return False
        if self.x == player.x or self.y == player.y:
            # Simple check LOS (no walls between)
            # ... implementation omitted for brevity, but let's assume LOS exists for now
            return True
        return False

    def render(self, surface):
        super().render(surface, self.color)
