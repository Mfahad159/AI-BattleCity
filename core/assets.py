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
        # Create base tank sprites
        self.sprites['player'] = self._create_stacked_tank(CYAN)
        self.sprites['basic'] = self._create_stacked_tank(AMBER)
        self.sprites['fast'] = self._create_stacked_tank(MINT, sleek=True)
        self.sprites['armor'] = self._create_stacked_tank((180, 180, 200), heavy=True)
        self.sprites['boss'] = self._create_stacked_tank(PURPLE, boss=True)
        self.sprites['eagle'] = self._create_eagle_sprite()
        
        # Create 3D wall sprites
        self.sprites['brick_3d'] = self._create_stacked_wall(BRICK, depth=4)
        self.sprites['steel_3d'] = self._create_stacked_wall(STEEL, depth=6)

    def _create_stacked_tank(self, color, sleek=False, heavy=False, boss=False):
        size = 32 if boss else 28
        surface = pygame.Surface((size, size + 10), pygame.SRCALPHA)
        
        # Layers (Bottom to Top)
        layers = 4 if not heavy else 6
        for i in range(layers):
            layer_color = [max(0, c - (layers-i)*10) for c in color] # Darker bottom
            y_off = layers - i
            
            # Tracks
            track_w = 4 if not heavy else 6
            pygame.draw.rect(surface, (20, 20, 20), (2, 4 + y_off, track_w, size-8))
            pygame.draw.rect(surface, (20, 20, 20), (size-2-track_w, 4 + y_off, track_w, size-8))
            
            # Body
            body_w = 14 if not sleek else 10
            pygame.draw.rect(surface, layer_color, (size//2 - body_w//2, size//2 - 8 + y_off, body_w, 16))
            
            # Turret (Top layers only)
            if i > layers // 2:
                pygame.draw.rect(surface, layer_color, (size//2 - 4, size//2 - 4 + y_off, 8, 8))
                # Barrel
                if boss:
                    pygame.draw.rect(surface, layer_color, (size//2 - 5, size//2 - 12 + y_off, 3, 10))
                    pygame.draw.rect(surface, layer_color, (size//2 + 2, size//2 - 12 + y_off, 3, 10))
                else:
                    pygame.draw.rect(surface, layer_color, (size//2 - 2, size//2 - 12 + y_off, 4, 10))
                
        return surface

    def _create_stacked_wall(self, color, depth=5):
        surface = pygame.Surface((24, 24 + depth), pygame.SRCALPHA)
        # Side walls (Darker)
        side_color = [max(0, c - 40) for c in color]
        pygame.draw.rect(surface, side_color, (0, 0, 24, 24 + depth))
        # Top face
        pygame.draw.rect(surface, color, (0, 0, 24, 24))
        # Bevel / Highlight
        pygame.draw.rect(surface, (255, 255, 255, 50), (0, 0, 24, 24), 1)
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
