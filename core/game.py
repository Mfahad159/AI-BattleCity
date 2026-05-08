import pygame
import random
from core.grid import Grid
from core.bullet import Bullet
from tanks.player_tank import PlayerTank
from ui.hud import HUD
from ui.window_controls import WindowControls
from constants import (
    BG_PRIMARY, BG_SECONDARY, WINDOW_WIDTH, WINDOW_HEIGHT, 
    CYAN, TITLE_BAR_HEIGHT, TILE_SIZE, AMBER
)

from core.spawner import Spawner

from ui.effects import EffectManager
from ui.ai_overlay import AIOverlay

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.window_controls = WindowControls()
        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TITLE_BAR_HEIGHT))
        
        self.effects = EffectManager()
        self.overlay = AIOverlay()
        
        # Pre-render CRT scanlines
        self.crt_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TITLE_BAR_HEIGHT), pygame.SRCALPHA)
        for y in range(0, WINDOW_HEIGHT, 4):
            pygame.draw.line(self.crt_surface, (0, 0, 0, 40), (0, y), (WINDOW_WIDTH, y))
        
        self.grid = Grid()
        self.hud = HUD()
        self.spawner = Spawner()
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
        self.enemies_spawned = 0
        self.enemies_destroyed = 0
        
    def handle_event(self, event):
        self.window_controls.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_f1:
                self.overlay.toggle()

    def update(self):
        if not self.player.active:
            return

        # 1. INPUT
        keys = pygame.key.get_pressed()
        moved, shot = self.player.handle_input(keys, self.grid)
        
        # 2. AGENT DECISIONS (Enemies)
        for enemy in self.enemies:
            action = enemy.decide(self.grid, self.player)
            if action == "shoot":
                new_bullet = Bullet(enemy.x, enemy.y, enemy.direction, 'enemy', enemy.color)
                self.bullets.append(new_bullet)

        # 3. MOVE & 4. SHOOT (Already handled in decisions and handle_input)
        self.player.update_cooldowns()
        if shot:
            new_bullet = Bullet(self.player.x, self.player.y, self.player.direction, 'player', CYAN)
            self.bullets.append(new_bullet)
            
        # 5. BULLET UPDATE
        all_tanks = [self.player] + self.enemies
        for bullet in self.bullets:
            bullet.update(self.grid, all_tanks)
            
            # Create trail
            if random.random() < 0.3:
                self.effects.create_trail(bullet.x * TILE_SIZE + TILE_SIZE//2, bullet.y * TILE_SIZE + TILE_SIZE//2, bullet.color)

            if not bullet.active:
                self.effects.create_explosion(bullet.x * TILE_SIZE + TILE_SIZE//2, bullet.y * TILE_SIZE + TILE_SIZE//2, bullet.color, count=5)

            if bullet.grid_x == 12 and bullet.grid_y == 24: # Eagle Pos
                self.effects.create_explosion(12*TILE_SIZE + 12, 24*TILE_SIZE + 12, AMBER, count=50)
                self.running = False # Game Over
            
        # 7. ANIMATIONS & EFFECTS
        self.player.update_animation()
        for enemy in self.enemies:
            enemy.update_animation()
        self.effects.update()

        # 8. STATE UPDATE
        self.bullets = [b for b in self.bullets if b.active]
        
        for e in self.enemies:
            if not e.active:
                self.effects.create_explosion(e.render_x, e.render_y, e.color, count=30)
                self.enemies_destroyed += 1
                self.score += 100
        self.enemies = [e for e in self.enemies if e.active]
        
        # 8. SPAWN CHECK
        self.spawner.update(self)
        
        # 9. LEVEL TRANSITION
        if self.enemies_destroyed >= self.total_enemies and not self.enemies:
            self.advance_level()

        # 10. WIN/LOSE CHECK
        if not self.player.active:
            self.effects.create_explosion(self.player.render_x, self.player.render_y, CYAN, count=30)
            self.lives -= 1
            if self.lives > 0:
                self.player = PlayerTank()
            else:
                self.running = False

    def advance_level(self):
        self.level += 1
        self.enemies_destroyed = 0
        self.enemies_spawned = 0
        self.bullets = []
        self.grid.generate_new_map(self.level)
        self.player = PlayerTank()
        
        if self.level == 3:
            self.total_enemies = 1
            from tanks.boss_tank import BossTank
            self.enemies = [BossTank(12, 1)]
        else:
            self.total_enemies = 20
            self.enemies = []

    def render(self):
        self.game_surface.fill(BG_PRIMARY)
        self.grid.render(self.game_surface)
        
        # Draw entities
        if self.player.active:
            self.player.render(self.game_surface, CYAN)
        
        for enemy in self.enemies:
            enemy.render(self.game_surface)
            
        for bullet in self.bullets:
            bullet.render(self.game_surface)
            
        # Draw effects and overlay
        self.effects.render(self.game_surface)
        self.overlay.render(self.game_surface, self)

        # Draw sidebar
        hud_rect = pygame.Rect(WINDOW_WIDTH - 160, 0, 160, WINDOW_HEIGHT)
        pygame.draw.rect(self.game_surface, BG_SECONDARY, hud_rect)
        self.hud.render(self.game_surface, self.level, self.lives, self.score, self.total_enemies - self.enemies_destroyed)
        
        # Apply CRT effect
        self.game_surface.blit(self.crt_surface, (0, 0))

        # Composite to main screen
        self.screen.fill(BG_PRIMARY)
        self.window_controls.render(self.screen)
        self.screen.blit(self.game_surface, (0, TITLE_BAR_HEIGHT))
