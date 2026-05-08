import pygame
from constants import CYAN, AMBER, MINT, PURPLE, TILE_SIZE

class AIOverlay:
    def __init__(self):
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled

    def render(self, surface, game):
        if not self.enabled:
            return
            
        # Draw paths for all enemies
        for enemy in game.enemies:
            if hasattr(enemy, 'path') and enemy.path:
                # Draw lines between path nodes
                points = [(p[0]*TILE_SIZE + TILE_SIZE//2, p[1]*TILE_SIZE + TILE_SIZE//2) for p in enemy.path]
                if len(points) > 1:
                    pygame.draw.lines(surface, enemy.color, False, points, 2)
            
            # Draw target info
            px, py = enemy.render_x, enemy.render_y
            font = pygame.font.SysFont("Arial", 12)
            state_text = f"AI: {type(enemy).__name__}"
            if hasattr(enemy, 'state'): state_text += f" [{enemy.state}]"
            
            txt = font.render(state_text, True, (255, 255, 255))
            surface.blit(txt, (px - 20, py - 30))

        # Draw Eagle Range
        ex, ey = 12*TILE_SIZE + TILE_SIZE//2, 24*TILE_SIZE + TILE_SIZE//2
        pygame.draw.circle(surface, AMBER, (ex, ey), 100, 1)
