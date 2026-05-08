import pygame
from constants import TILE_SIZE, BULLET_SPEED_MULTIPLIER, GRID_SIZE

class Bullet:
    def __init__(self, x, y, direction, owner, color):
        # Initial grid position (centered in tile)
        self.grid_x = x
        self.grid_y = y
        self.pos_x = float(x * TILE_SIZE + TILE_SIZE // 2)
        self.pos_y = float(y * TILE_SIZE + TILE_SIZE // 2)
        
        self.dx, self.dy = direction
        self.owner = owner # Reference to the tank that fired this
        self.owner_type = owner.tank_type if hasattr(owner, 'tank_type') else 'player'
        self.color = color
        self.active = True
        
        # Bullet speed (Pixels per second)
        self.speed = 300.0 

    def update(self, grid, tanks, dt):
        # Move bullet based on velocity
        self.pos_x += self.dx * self.speed * dt
        self.pos_y += self.dy * self.speed * dt
        
        # Current grid position
        self.grid_x = int(self.pos_x // TILE_SIZE)
        self.grid_y = int(self.pos_y // TILE_SIZE)
        
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
            grid.destroy_wall(self.grid_x, self.grid_y)
            self.active = False
            return
            
        # Collision with tanks
        for tank in tanks:
            if tank.active and tank != self.owner:
                # Friendly fire off: Enemies don't hit each other, Player doesn't hit self
                if self.owner_type != 'player' and tank.tank_type != 'player':
                    continue
                
                # Check pixel distance for better feel
                dist = ((self.pos_x - tank.pos_x)**2 + (self.pos_y - tank.pos_y)**2)**0.5
                if dist < 12: # Bullet radius + Tank radius
                    tank.take_damage(1)
                    self.active = False
                    return
        
        # Destroy bullet if it hits another bullet
        # (Optional, but helps with clarity)

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
