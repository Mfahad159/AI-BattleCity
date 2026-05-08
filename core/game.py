import pygame
from core.grid import Grid
from constants import BG_PRIMARY, BG_SECONDARY, WINDOW_WIDTH, WINDOW_HEIGHT

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.grid = Grid()
        self.running = True
        
        # Lists for entities
        self.player = None
        self.enemies = []
        self.bullets = []
        
        # Game state
        self.level = 1
        self.lives = 10
        self.score = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        # 1. INPUT (handled in handle_event and player update)
        # 2. AGENT DECISIONS
        # 3. MOVE
        # 4. SHOOT
        # 5. BULLET UPDATE
        # 6. COLLISION DETECT
        # 7. STATE UPDATE
        # 8. SPAWN CHECK
        # 10. WIN/LOSE CHECK
        pass

    def render(self):
        # Step 9: RENDER
        
        # Clear screen
        self.screen.fill(BG_PRIMARY)
        
        # Draw grid
        self.grid.render(self.screen)
        
        # Draw HUD area (sidebar)
        hud_rect = pygame.Rect(WINDOW_WIDTH - 160, 0, 160, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, BG_SECONDARY, hud_rect)
        
        # Draw entities (to be implemented)
        # self.player.render(self.screen)
        # for enemy in self.enemies:
        #     enemy.render(self.screen)
        # for bullet in self.bullets:
        #     bullet.render(self.screen)
