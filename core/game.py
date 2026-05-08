import pygame
from core.grid import Grid
from tanks.player_tank import PlayerTank
from core.bullet import Bullet
from constants import BG_PRIMARY, BG_SECONDARY, WINDOW_WIDTH, WINDOW_HEIGHT, CYAN

from ui.hud import HUD

class Game:
    def __init__(self, screen):
        self.screen = screen
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        if not self.player.active:
            return

        # 1. INPUT
        keys = pygame.key.get_pressed()
        moved, shot = self.player.handle_input(keys, self.grid)
        
        # 2. AGENT DECISIONS (Enemies)
        for enemy in self.enemies:
            # enemy.decide(self.grid, self.player)
            pass

        # 3. MOVE & 4. SHOOT
        self.player.update_cooldowns()
        if shot:
            new_bullet = Bullet(self.player.x, self.player.y, self.player.direction, 'player', CYAN)
            self.bullets.append(new_bullet)
            
        for enemy in self.enemies:
            enemy.update_cooldowns()
            # if enemy.should_shoot(): ...

        # 5. BULLET UPDATE
        all_tanks = [self.player] + self.enemies
        for bullet in self.bullets:
            bullet.update(self.grid, all_tanks)
            
        # 7. STATE UPDATE (Remove inactive bullets/enemies)
        self.bullets = [b for b in self.bullets if b.active]
        self.enemies = [e for e in self.enemies if e.active]
        
        # 10. WIN/LOSE CHECK
        if not self.player.active:
            # Handle game over
            pass

    def render(self):
        # Step 9: RENDER
        self.screen.fill(BG_PRIMARY)
        self.grid.render(self.screen)
        
        # Draw sidebar
        hud_rect = pygame.Rect(WINDOW_WIDTH - 160, 0, 160, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, BG_SECONDARY, hud_rect)
        self.hud.render(self.screen, self.level, self.lives, self.score, self.total_enemies - self.enemies_destroyed)
        
        # Draw entities
        if self.player.active:
            self.player.render(self.screen)
        
        for enemy in self.enemies:
            enemy.render(self.screen)
            
        for bullet in self.bullets:
            bullet.render(self.screen)
