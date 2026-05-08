import pygame
from core.grid import Grid
from core.bullet import Bullet
from tanks.player_tank import PlayerTank
from ui.hud import HUD
from ui.window_controls import WindowControls
from constants import BG_PRIMARY, BG_SECONDARY, WINDOW_WIDTH, WINDOW_HEIGHT, CYAN, TITLE_BAR_HEIGHT

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.window_controls = WindowControls()
        # Surface for the actual game (excluding title bar)
        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TITLE_BAR_HEIGHT))
        
        self.grid = Grid()
        self.hud = HUD()
        self.running = True
        
        # Entities
        self.player = PlayerTank()
        self.enemies = []
        self.bullets = []
        
        # Game state
        self.level = 1
        self.lives = 10
        self.score = 0
        self.total_enemies = 20
        self.enemies_destroyed = 0
        
    def handle_event(self, event):
        self.window_controls.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        # ... (rest of update remains same)
        if not self.player.active:
            return

        keys = pygame.key.get_pressed()
        moved, shot = self.player.handle_input(keys, self.grid)
        
        self.player.update_cooldowns()
        if shot:
            new_bullet = Bullet(self.player.x, self.player.y, self.player.direction, 'player', CYAN)
            self.bullets.append(new_bullet)
            
        for enemy in self.enemies:
            enemy.update_cooldowns()

        all_tanks = [self.player] + self.enemies
        for bullet in self.bullets:
            bullet.update(self.grid, all_tanks)
            
        self.bullets = [b for b in self.bullets if b.active]
        self.enemies = [e for e in self.enemies if e.active]

    def render(self):
        # Render Game to its own surface
        self.game_surface.fill(BG_PRIMARY)
        self.grid.render(self.game_surface)
        
        # Draw sidebar
        hud_rect = pygame.Rect(WINDOW_WIDTH - 160, 0, 160, WINDOW_HEIGHT)
        pygame.draw.rect(self.game_surface, BG_SECONDARY, hud_rect)
        self.hud.render(self.game_surface, self.level, self.lives, self.score, self.total_enemies - self.enemies_destroyed)
        
        # Draw entities
        if self.player.active:
            self.player.render(self.game_surface)
        
        for enemy in self.enemies:
            enemy.render(self.game_surface)
            
        for bullet in self.bullets:
            bullet.render(self.game_surface)
            
        # Composite to main screen
        self.screen.fill(BG_PRIMARY)
        self.window_controls.render(self.screen)
        self.screen.blit(self.game_surface, (0, TITLE_BAR_HEIGHT))
