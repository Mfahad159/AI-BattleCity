import pygame
from constants import GRID_SIZE, TILE_SIZE, TERRAIN_COLORS, EMPTY, BRICK, STEEL, WATER, FOREST, EAGLE
from modules.csp_map_gen import CSPMapGenerator

class Grid:
    def __init__(self):
        self.generator = CSPMapGenerator()
        self.matrix = self.generator.generate(level=1)
        self.eagle_alive = True

    def generate_new_map(self, level=1):
        self.matrix = self.generator.generate(level)
        self.eagle_alive = True

    def get_tile(self, x, y):
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            return self.matrix[y][x]
        return STEEL  # Treat out of bounds as indestructible steel

    def set_tile(self, x, y, value):
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            self.matrix[y][x] = value

    def is_passable(self, x, y):
        tile = self.get_tile(x, y)
        # Tanks can pass through EMPTY and FOREST
        return tile in [EMPTY, FOREST]

    def is_bullet_passable(self, x, y):
        tile = self.get_tile(x, y)
        # Bullets pass through EMPTY, WATER, and FOREST
        return tile in [EMPTY, WATER, FOREST]

    def destroy_wall(self, x, y):
        tile = self.get_tile(x, y)
        if tile == BRICK:
            self.set_tile(x, y, EMPTY)
            return True
        elif tile == EAGLE:
            self.set_tile(x, y, EMPTY)
            self.eagle_alive = False
            return True
        return False

    def render(self, surface):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                tile_type = self.matrix[y][x]
                color = TERRAIN_COLORS.get(tile_type, (0, 0, 0))
                
                # Basic rectangle rendering for now
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile_type != EMPTY:
                    from core.assets import assets
                    if tile_type == EAGLE:
                        sprite = assets.get_sprite('eagle')
                    elif tile_type == BRICK:
                        sprite = assets.get_sprite('brick_3d')
                    elif tile_type == STEEL:
                        sprite = assets.get_sprite('steel_3d')
                    else:
                        sprite = None

                    if sprite:
                        # 3D walls are taller, so we need to shift them UP by the depth difference
                        depth = sprite.get_height() - TILE_SIZE
                        surface.blit(sprite, (rect.x, rect.y - depth))
                        continue
                        
                    pygame.draw.rect(surface, color, rect)
                    
                    # Add subtle detail to tiles based on design.md
                    if tile_type == BRICK:
                        # Draw mini brick pattern
                        self._draw_brick_pattern(surface, rect)
                    elif tile_type == STEEL:
                        # Draw steel pattern
                        self._draw_steel_pattern(surface, rect)

    def _draw_brick_pattern(self, surface, rect):
        # Brick pattern logic from design.md
        # mortar color is 20% darker
        brick_color = TERRAIN_COLORS[BRICK]
        mortar_color = (int(brick_color[0]*0.8), int(brick_color[1]*0.8), int(brick_color[2]*0.8))
        
        # Draw 3 rows of bricks
        row_h = rect.height // 3
        for i in range(3):
            y = rect.y + i * row_h
            # Draw mortar line
            pygame.draw.line(surface, mortar_color, (rect.x, y), (rect.x + rect.width, y))
            
    def _draw_steel_pattern(self, surface, rect):
        # Steel panel logic from design.md
        base_color = TERRAIN_COLORS[STEEL]
        seam_color = (80, 88, 100)
        
        # 1px lines at tile thirds
        third_w = rect.width // 3
        third_h = rect.height // 3
        pygame.draw.line(surface, seam_color, (rect.x + third_w, rect.y), (rect.x + third_w, rect.y + rect.height))
        pygame.draw.line(surface, seam_color, (rect.x + 2 * third_w, rect.y), (rect.x + 2 * third_w, rect.y + rect.height))
        pygame.draw.line(surface, seam_color, (rect.x, rect.y + third_h), (rect.x + rect.width, rect.y + third_h))
        pygame.draw.line(surface, seam_color, (rect.x, rect.y + 2 * third_h), (rect.x + rect.width, rect.y + 2 * third_h))
