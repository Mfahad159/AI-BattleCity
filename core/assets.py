import pygame
from constants import TILE_SIZE, CYAN, AMBER, MINT, PURPLE, BRICK, STEEL, WATER, FOREST, EAGLE, BG_PRIMARY

class AssetManager:
    def __init__(self):
        self.sprites = {}
        self._generate_all()

    def get_sprite(self, name, direction=(0, -1)):
        # Cache rotated versions
        key = (name, direction)
        if key in self.sprites:
            return self.sprites[key]
            
        base_sprite = self.sprites.get(name)
        if base_sprite:
            angle = self._dir_to_angle(direction)
            rotated = pygame.transform.rotate(base_sprite, angle)
            self.sprites[key] = rotated
            return rotated
        return None

    def _dir_to_angle(self, direction):
        if direction == (0, -1): return 0
        if direction == (0, 1): return 180
        if direction == (-1, 0): return 90
        if direction == (1, 0): return 270
        return 0

    def _generate_all(self):
        self.sprites['player'] = self._create_tank_sprite(CYAN)
        self.sprites['basic'] = self._create_tank_sprite(AMBER)
        self.sprites['fast'] = self._create_tank_sprite(MINT, sleek=True)
        self.sprites['armor'] = self._create_tank_sprite((180, 180, 200), heavy=True)
        self.sprites['boss'] = self._create_tank_sprite(PURPLE, boss=True)
        self.sprites['eagle'] = self._create_eagle_sprite()

    def _create_tank_sprite(self, color, sleek=False, heavy=False, boss=False):
        size = 24 if not boss else 28
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw tracks
        track_w = 4 if not heavy else 6
        pygame.draw.rect(surface, (40, 40, 40), (2, 4, track_w, size-8))
        pygame.draw.rect(surface, (40, 40, 40), (size-2-track_w, 4, track_w, size-8))
        
        # Draw body
        body_w = 14 if not sleek else 10
        body_h = 16
        body_rect = pygame.Rect(0, 0, body_w, body_h)
        body_rect.center = (size//2, size//2)
        pygame.draw.rect(surface, color, body_rect)
        
        # Draw turret
        turret_rect = pygame.Rect(size//2 - 4, size//2 - 4, 8, 8)
        pygame.draw.rect(surface, color, turret_rect)
        pygame.draw.rect(surface, (255, 255, 255, 100), turret_rect, 1) # Highlight
        
        # Draw barrel
        if boss:
            pygame.draw.rect(surface, color, (size//2 - 5, size//2 - 12, 3, 10))
            pygame.draw.rect(surface, color, (size//2 + 2, size//2 - 12, 3, 10))
        else:
            pygame.draw.rect(surface, color, (size//2 - 2, size//2 - 12, 4, 10))
            
        return surface

    def _create_eagle_sprite(self):
        surface = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Simple eagle silhouette
        pygame.draw.polygon(surface, AMBER, [
            (12, 4), (4, 12), (8, 12), (8, 20), (16, 20), (16, 12), (20, 12)
        ])
        # Add glow
        pygame.draw.circle(surface, (255, 185, 0, 50), (12, 12), 10)
        return surface

# Global instance
assets = AssetManager()
