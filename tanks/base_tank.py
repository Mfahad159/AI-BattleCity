from constants import TILE_SIZE
from core.assets import assets

class BaseTank:
    def __init__(self, x, y, direction=(0, -1), tank_type='basic'):
        self.x = x  # Grid coordinate
        self.y = y  # Grid coordinate
        self.direction = direction  # (dx, dy)
        self.tank_type = tank_type
        
        # Continuous rendering coordinates
        self.render_x = x * TILE_SIZE + TILE_SIZE // 2
        self.render_y = y * TILE_SIZE + TILE_SIZE // 2
        self.lerp_speed = 0.2 # Accelerator feeling
        
        # Attributes to be overridden by subclasses
        self.hp = 1
        self.speed = 30  # Ticks per move
        self.fire_rate = 60  # Ticks between shots
        
        # Internal state
        self.move_cooldown = 0
        self.fire_cooldown = 0
        self.active = True

    def update_animation(self):
        target_x = self.x * TILE_SIZE + TILE_SIZE // 2
        target_y = self.y * TILE_SIZE + TILE_SIZE // 2
        
        # Smoothly interpolate render position towards target
        self.render_x += (target_x - self.render_x) * self.lerp_speed
        self.render_y += (target_y - self.render_y) * self.lerp_speed

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
            
        sprite = assets.get_sprite(self.tank_type, self.direction)
        if sprite:
            depth = sprite.get_height() - 24 # Standard height
            rect = sprite.get_rect(center=(self.render_x, self.render_y - depth // 2))
            surface.blit(sprite, rect)
