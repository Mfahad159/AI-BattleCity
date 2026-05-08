import pygame
from constants import TILE_SIZE

class BaseTank:
    def __init__(self, x, y, direction=(0, -1)):
        self.x = x  # Grid coordinate
        self.y = y  # Grid coordinate
        self.direction = direction  # (dx, dy)
        
        # Attributes to be overridden by subclasses
        self.hp = 1
        self.speed = 4  # Ticks per move
        self.fire_rate = 60  # Ticks between shots
        
        # Internal state
        self.move_cooldown = 0
        self.fire_cooldown = 0
        self.active = True

    def move(self, dx, dy, grid):
        self.direction = (dx, dy)
        
        if self.move_cooldown > 0:
            return False
            
        new_x = self.x + dx
        new_y = self.y + dy
        
        if grid.is_passable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.move_cooldown = self.speed
            return True
        return False

    def update_cooldowns(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

    def can_shoot(self):
        return self.fire_cooldown <= 0

    def shoot(self):
        if self.can_shoot():
            self.fire_cooldown = self.fire_rate
            return True
        return False

    def take_damage(self, amount=1):
        self.hp -= amount
        if self.hp <= 0:
            self.active = False
            return True # Destroyed
        return False

    def get_pixel_pos(self):
        # Center in tile
        px = self.x * TILE_SIZE + TILE_SIZE // 2
        py = self.y * TILE_SIZE + TILE_SIZE // 2
        return px, py

    def render(self, surface, color):
        if not self.active:
            return
            
        px, py = self.get_pixel_pos()
        # Draw body (20x20 centered in 24x24 tile)
        rect = pygame.Rect(0, 0, 20, 20)
        rect.center = (px, py)
        pygame.draw.rect(surface, color, rect)
        
        # Draw turret (small rectangle indicating direction)
        turret_w = 4
        turret_h = 10
        tx = px + self.direction[0] * 8
        ty = py + self.direction[1] * 8
        
        turret_rect = pygame.Rect(0, 0, turret_w, turret_h)
        if self.direction[0] != 0: # Horizontal
            turret_rect = pygame.Rect(0, 0, turret_h, turret_w)
            
        turret_rect.center = (tx, ty)
        pygame.draw.rect(surface, color, turret_rect)
