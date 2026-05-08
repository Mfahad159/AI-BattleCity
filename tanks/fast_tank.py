from tanks.base_tank import BaseTank
from ai.greedy import greedy_step
from constants import MINT, EAGLE_POS, SPEED_FAST, FIRE_RATE_FAST

class FastTank(BaseTank):
    def __init__(self, x, y):
        super().__init__(x, y, tank_type='fast', speed=90.0)
        self.color = MINT
        self.speed = SPEED_FAST
        self.fire_rate = FIRE_RATE_FAST

    def decide(self, grid, player):
        # Grid alignment check for smooth movement
        if self.x != self.target_gx or self.y != self.target_gy:
            return "wait"
        
        # Fast Tank ONLY cares about Eagle
        move_dir = greedy_step(grid.matrix, (self.x, self.y), EAGLE_POS)
        if move_dir:
            dx, dy = move_dir
            nx, ny = self.x + dx, self.y + dy
            
            # If next tile is Brick, shoot it
            if grid.get_tile(nx, ny) == 1: # BRICK
                self.direction = (dx, dy)
                if self.can_shoot():
                    return "shoot"
            
            # Attempt move
            self.move(dx, dy, grid)
            return "move"
            
        return "wait"

    def render(self, surface, color=None):
        super().render(surface, color or self.color)
        # TODO: Add motion trail as per design.md
