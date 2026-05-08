import pygame
from tanks.base_tank import BaseTank
from ai.astar import astar
from ai.bfs import bfs
from constants import EAGLE_POS, SPEED_MEDIUM, FIRE_RATE_ARMOR, HP_ARMOR, ARMOR_RETREAT_WAIT_TICKS, EMPTY

class ArmorTank(BaseTank):
    def __init__(self, x, y):
        super().__init__(x, y, tank_type='armor', speed=50.0)
        self.hp = HP_ARMOR
        self.hit_count = 0
        self.color = (180, 180, 200) # Base armor color
        self.speed = SPEED_MEDIUM
        self.fire_rate = FIRE_RATE_ARMOR
        self.path = []
        self.state = "attacking" # "attacking", "retreating", "recovering"
        self.wait_timer = 0

    def take_damage(self, amount=1):
        self.hit_count += amount
        return super().take_damage(amount)

    def decide(self, grid, player):
        # Grid alignment check for smooth movement
        if self.x != self.target_gx or self.y != self.target_gy:
            return "wait"
        
        if self.state == "recovering":
            self.wait_timer -= 1
            if self.wait_timer <= 0:
                self.state = "attacking"
                self.path = []
            return "wait"

        if self.hit_count >= 3 and self.state == "attacking":
            self.state = "retreating"
            self.path = self._find_cover(grid)

        if not self.path:
            if self.state == "attacking":
                self.path = astar(grid.matrix, (self.x, self.y), EAGLE_POS)
            else: # retreating
                self.path = self._find_cover(grid)
            
            if self.path: self.path.pop(0)

        if self.path:
            next_tile = self.path[0]
            dx = next_tile[0] - self.x
            dy = next_tile[1] - self.y
            
            if self.state == "retreating" and self.x == next_tile[0] and self.y == next_tile[1]:
                self.state = "recovering"
                self.wait_timer = ARMOR_RETREAT_WAIT_TICKS
                return "wait"

            # If brick ahead and attacking, shoot it
            if self.state == "attacking" and grid.get_tile(next_tile[0], next_tile[1]) == 1:
                self.direction = (dx, dy)
                if self.can_shoot(): return "shoot"
            
            if self.move(dx, dy, grid):
                self.path.pop(0)
                return "move"
        
        return "wait"

    def _find_cover(self, grid):
        # BFS to nearest STEEL tile neighbor
        # For simplicity, just find nearest STEEL tile and get an EMPTY tile next to it
        # Real implementation would be more complex
        return [] # Placeholder

    def render(self, surface, color=None):
        # Color changes based on hit_count as per design.md
        colors = [(180, 180, 200), (160, 100, 80), (200, 60, 60), (255, 55, 55)]
        current_color = colors[min(self.hit_count, 3)]
        super().render(surface, color or current_color)
