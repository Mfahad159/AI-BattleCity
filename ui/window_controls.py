import pygame
from constants import WINDOW_WIDTH, CYAN, RED_HOT, MINT, BG_SECONDARY, TEXT_PRIMARY

class WindowControls:
    def __init__(self):
        self.height = 30
        self.rect = pygame.Rect(0, 0, WINDOW_WIDTH, self.height)
        
        # Buttons
        self.close_rect = pygame.Rect(WINDOW_WIDTH - 30, 5, 20, 20)
        self.max_rect = pygame.Rect(WINDOW_WIDTH - 60, 5, 20, 20)
        self.min_rect = pygame.Rect(WINDOW_WIDTH - 90, 5, 20, 20)
        
        self.dragging = False
        self.drag_offset = (0, 0)

    def render(self, surface):
        # Draw title bar background
        pygame.draw.rect(surface, BG_SECONDARY, self.rect)
        pygame.draw.line(surface, CYAN, (0, self.height - 1), (WINDOW_WIDTH, self.height - 1), 1)
        
        # Draw buttons with neon style
        # Close (X)
        pygame.draw.rect(surface, RED_HOT, self.close_rect, 1)
        pygame.draw.line(surface, RED_HOT, (self.close_rect.x + 5, self.close_rect.y + 5), 
                         (self.close_rect.x + 15, self.close_rect.y + 15), 2)
        pygame.draw.line(surface, RED_HOT, (self.close_rect.x + 15, self.close_rect.y + 5), 
                         (self.close_rect.x + 5, self.close_rect.y + 15), 2)
        
        # Maximize (Square)
        pygame.draw.rect(surface, MINT, self.max_rect, 1)
        pygame.draw.rect(surface, MINT, (self.max_rect.x + 5, self.max_rect.y + 5, 10, 10), 1)
        
        # Minimize (_)
        pygame.draw.rect(surface, CYAN, self.min_rect, 1)
        pygame.draw.line(surface, CYAN, (self.min_rect.x + 5, self.min_rect.y + 15), 
                         (self.min_rect.x + 15, self.min_rect.y + 15), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_rect.collidepoint(event.pos):
                pygame.quit()
                import sys
                sys.exit()
            elif self.min_rect.collidepoint(event.pos):
                pygame.display.iconify()
            elif self.max_rect.collidepoint(event.pos):
                # Toggle fullscreen or similar
                pygame.display.toggle_fullscreen()
            elif self.rect.collidepoint(event.pos):
                self.dragging = True
                # Get current window position
                # Note: Pygame doesn't easily expose window pos without SDL hints or complex calls
                # For now, we'll just handle clicks.
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
