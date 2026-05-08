import pygame
from tanks.base_tank import BaseTank
from constants import PLAYER_HP, CYAN, PLAYER_SPAWN

class PlayerTank(BaseTank):
    def __init__(self):
        x, y = PLAYER_SPAWN
        super().__init__(x, y)
        self.hp = PLAYER_HP
        self.speed = 1 # Player moves every frame if key held?
        # Actually Spec says "one tile per tick". But player movement usually feels better if it has some rhythm.
        # Let's set speed to 2 (moves every 2 ticks) to match Fast tank or similar.
        self.speed = 2 
        self.fire_rate = 30 # Faster than enemies
        self.color = CYAN

    def handle_input(self, keys, grid):
        moved = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            moved = self.move(0, -1, grid)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            moved = self.move(0, 1, grid)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            moved = self.move(-1, 0, grid)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            moved = self.move(1, 0, grid)
            
        shooting = False
        if keys[pygame.K_SPACE]:
            shooting = self.shoot()
            
        return moved, shooting

    def render(self, surface):
        super().render(surface, self.color)
