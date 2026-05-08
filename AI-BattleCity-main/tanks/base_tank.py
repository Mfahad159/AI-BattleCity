from constants import TILE_SIZE
from core.assets import assets

class BaseTank:
    def __init__(self, x, y, direction=(0, -1), tank_type='basic', speed=80.0):
        # Grid coordinates (for AI compatibility)
        self.x = x  
        self.y = y  
        self.direction = direction  # (dx, dy)
        self.tank_type = tank_type
        
        # Continuous pixel coordinates (centered in tile)
        self.pos_x = float(x * TILE_SIZE + TILE_SIZE // 2)
        self.pos_y = float(y * TILE_SIZE + TILE_SIZE // 2)
        self.render_x = self.pos_x
        self.render_y = self.pos_y
        
        # Grid target for AI movement
        self.target_gx = x
        self.target_gy = y
        
        # Physics - Speed is pixels per second
        self.base_speed = speed 
        self.hp = 1
        self.active = True
        self.fire_cooldown = 0

    def update_animation(self):
        # Continuous movement: render pos follows physics pos directly
        self.render_x = self.pos_x
        self.render_y = self.pos_y

    def move_smooth(self, dx, dy, dt, grid):
        # AI version: Move towards target_gx/y
        target_px = self.target_gx * TILE_SIZE + TILE_SIZE // 2
        target_py = self.target_gy * TILE_SIZE + TILE_SIZE // 2
        
        # Calculate distance to target
        dist_x = target_px - self.pos_x
        dist_y = target_py - self.pos_y
        dist = (dist_x**2 + dist_y**2)**0.5
        
        if dist > 1:
            # Move towards target
            move_dist = self.base_speed * dt
            if move_dist > dist: move_dist = dist # Don't overshoot
            
            self.pos_x += (dist_x / dist) * move_dist
            self.pos_y += (dist_y / dist) * move_dist
            
            # Update current grid pos for AI
            self.x = int(self.pos_x // TILE_SIZE)
            self.y = int(self.pos_y // TILE_SIZE)
            return False # Not reached yet
        else:
            # Reached target
            self.pos_x = target_px
            self.pos_y = target_py
            self.x = self.target_gx
            self.y = self.target_gy
            return True # Reached!

    def move(self, dx, dy, grid):
        # AI calls this to set a new target tile
        new_gx = self.x + dx
        new_gy = self.y + dy
        
        if grid.is_passable(new_gx, new_gy):
            self.target_gx = new_gx
            self.target_gy = new_gy
            self.direction = (dx, dy)
            return True
        return False

    def move_manual(self, dx, dy, dt, grid):
        # Player version: Direct velocity control
        self.direction = (dx, dy)
        new_x = self.pos_x + dx * self.base_speed * dt
        new_y = self.pos_y + dy * self.base_speed * dt
        
        # Collision check
        margin = 4
        size = 20
        points = [
            (new_x - size//2 + margin, new_y - size//2 + margin),
            (new_x + size//2 - margin, new_y - size//2 + margin),
            (new_x - size//2 + margin, new_y + size//2 - margin),
            (new_x + size//2 - margin, new_y + size//2 - margin)
        ]
        
        can_move = True
        for px, py in points:
            gx, gy = int(px // TILE_SIZE), int(py // TILE_SIZE)
            if not grid.is_passable(gx, gy):
                can_move = False
                break
        
        if can_move:
            self.pos_x = new_x
            self.pos_y = new_y
            self.x = int(self.pos_x // TILE_SIZE)
            self.y = int(self.pos_y // TILE_SIZE)
            self.target_gx = self.x # Sync target
            self.target_gy = self.y
            return True
        return False

    def update_cooldowns(self, dt=0.016):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1 # Keep it simple for now or use dt

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
