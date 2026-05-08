import pygame
from tanks.base_tank import BaseTank
from constants import PLAYER_HP, CYAN, PLAYER_SPAWN, SPEED_PLAYER

class PlayerTank(BaseTank):
    def __init__(self, x=10, y=24):
        # Initial pos (usually near eagle)
        super().__init__(x, y, tank_type='player', speed=150.0)
        self.hp = PLAYER_HP
        self.speed = SPEED_PLAYER
        self.fire_rate = 30 # Faster than enemies
        self.color = CYAN

    def handle_input(self, keys, grid, dt):
        moved = False
        dx, dy = 0, 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
            
        if dx != 0 or dy != 0:
            moved = self.move_manual(dx, dy, dt, grid)
            
        shooting = keys[pygame.K_SPACE]
            
        return moved, shooting

    def render(self, surface, color=None):
        super().render(surface, color or self.color)
