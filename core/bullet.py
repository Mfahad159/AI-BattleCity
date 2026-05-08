import pygame
from constants import TILE_SIZE, BULLET_SPEED_MULTIPLIER, GRID_SIZE

class Bullet:
    def __init__(self, x, y, direction, owner_type, color):
        self.x = x  # Grid float coordinate for smoother movement if needed, but Spec says grid aligned.
        # Actually Spec says "advance one tile".
        self.grid_x = x
        self.grid_y = y
        self.dx, self.dy = direction
        self.owner_type = owner_type # 'player' or 'enemy'
        self.color = color
        self.active = True
        
        # Speed: bullets move twice as fast as tanks.
        # If tank moves 1 tile/tick (max), bullet moves 2 tiles/tick?
        # Spec says: "Bullet speed = 2x tank movement speed".
        # Let's assume this means it updates more frequently or moves more distance.
        self.step_count = 2 

    def update(self, grid, tanks):
        for _ in range(self.step_count):
            self.grid_x += self.dx
            self.grid_y += self.dy
            
            # Boundary check
            if not (0 <= self.grid_x < GRID_SIZE and 0 <= self.grid_y < GRID_SIZE):
                self.active = False
                return
                
            # Collision with walls
            tile = grid.get_tile(self.grid_x, self.grid_y)
            if tile == 1: # BRICK
                grid.destroy_wall(self.grid_x, self.grid_y)
                self.active = False
                return
            elif tile == 2: # STEEL
                self.active = False
                return
            elif tile == 5: # EAGLE
                # Game Over logic handled in Game class, but mark bullet inactive
                self.active = False
                return
                
            # Collision with tanks
            for tank in tanks:
                if tank.active and tank.x == self.grid_x and tank.y == self.grid_y:
                    # Don't hit self
                    # (Need to check if owner is player/enemy and don't hit same type maybe? 
                    # Actually Spec says "bullet hits a tank... takes 1 hit of damage")
                    tank.take_damage(1)
                    self.active = False
                    return

    def render(self, surface):
        px = self.grid_x * TILE_SIZE + TILE_SIZE // 2
        py = self.grid_y * TILE_SIZE + TILE_SIZE // 2
        
        # Draw bullet head
        pygame.draw.rect(surface, self.color, (px-2, py-2, 4, 4))
        
        # Draw simple trail
        for i in range(1, 4):
            tx = px - self.dx * i * 6
            ty = py - self.dy * i * 6
            alpha = 255 - i * 60
            # Trail color with alpha (requires surface with SRCALPHA)
            # For now just draw smaller/dimmer dots
            pygame.draw.circle(surface, self.color, (int(tx), int(ty)), 2 - i//2)
