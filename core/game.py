import pygame
import random
import math
from core.grid import Grid
from core.bullet import Bullet
from tanks.player_tank import PlayerTank
from ui.hud import HUD
from ui.window_controls import WindowControls
from constants import (
    BG_PRIMARY, BG_SECONDARY, WINDOW_WIDTH, WINDOW_HEIGHT, 
    CYAN, TITLE_BAR_HEIGHT, TILE_SIZE, AMBER, PLAYER_LIVES, GRID_SIZE
)

from core.spawner import Spawner

from ui.effects import EffectManager
from ui.ai_overlay import AIOverlay

from core.sounds import sounds

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.window_controls = WindowControls()
        grid_w = GRID_SIZE * TILE_SIZE
        self.game_surface = pygame.Surface((grid_w, WINDOW_HEIGHT - TITLE_BAR_HEIGHT))
        
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
        self.last_tick = pygame.time.get_ticks()
        sounds.play_bg()
        sounds.play('level_start')
        
        self.game_over = False
        self.game_over_timer = 0
        
        # Level Transition state
        self.transition_timer = 4.0 # 4 seconds for intro
        self.showing_transition = True
        
    def handle_event(self, event):
        self.window_controls.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_F1:
                self.overlay.toggle()
        
        if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Rects for buttons
            if pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50, 200, 50).collidepoint(mx, my):
                self.reset()
            elif pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 120, 200, 50).collidepoint(mx, my):
                import sys
                pygame.quit()
                sys.exit()

    def reset(self):
        # Full game reset
        self.level = 1
        self.score = 0
        self.lives = PLAYER_LIVES
        self.grid.generate_new_map(level=1)
        self.player = PlayerTank()
        self.enemies = []
        self.enemies_spawned = 0
        self.enemies_destroyed = 0
        self.bullets = []
        self.game_over = False
        self.game_over_timer = 0
        self.showing_transition = True
        self.transition_timer = 4.0
        sounds.play_bg()
        sounds.play('level_start')

    def update(self):
        # Delta time calculation (seconds)
        now = pygame.time.get_ticks()
        dt = (now - self.last_tick) / 1000.0
        self.last_tick = now
        if dt > 0.1: dt = 0.016 # Prevent jumping on lag

        if self.showing_transition:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.showing_transition = False
            return

        if self.game_over:
            self.game_over_timer += dt
            return
            
        if not self.player.active:
            # Respawn logic already handled below
            pass
            
        # 1. INPUT
        keys = pygame.key.get_pressed()
        moved, shot = self.player.handle_input(keys, self.grid, dt)
        if shot and self.player.shoot():
            sounds.play('shoot')
            new_bullet = Bullet(self.player.x, self.player.y, self.player.direction, self.player, CYAN)
            self.bullets.append(new_bullet)
        
        # 2. AGENT DECISIONS (Enemies)
        for enemy in self.enemies:
            action = enemy.decide(self.grid, self.player)
            if action == "shoot" and enemy.shoot():
                sounds.play('shoot')
                new_bullet = Bullet(enemy.x, enemy.y, enemy.direction, enemy, enemy.color)
                self.bullets.append(new_bullet)
            
            # Smooth enemy movement
            edx, edy = enemy.direction
            enemy.move_smooth(edx, edy, dt, self.grid)

        # 3. MOVE & 4. SHOOT
        self.player.update_cooldowns(dt)
        for enemy in self.enemies:
            enemy.update_cooldowns(dt)
            
        # 5. BULLET UPDATE
        all_tanks = [self.player] + self.enemies
        for bullet in self.bullets:
            bullet.update(self.grid, all_tanks, dt)
            
            # Create trail
            if random.random() < 0.3:
                self.effects.create_trail(bullet.grid_x * TILE_SIZE + TILE_SIZE//2, bullet.grid_y * TILE_SIZE + TILE_SIZE//2, bullet.color)

            if not bullet.active:
                sounds.play('explosion')
                self.effects.create_explosion(bullet.grid_x * TILE_SIZE + TILE_SIZE//2, bullet.grid_y * TILE_SIZE + TILE_SIZE//2, bullet.color, count=5)

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
                self.game_over = True
                sounds.play('lose')
                # Stop BG music
                if 'bg_music' in sounds.sounds:
                    sounds.sounds['bg_music'].stop()

        if not self.grid.eagle_alive:
            self.game_over = True
            sounds.play('lose')
            if 'bg_music' in sounds.sounds:
                sounds.sounds['bg_music'].stop()

    def advance_level(self):
        self.level += 1
        self.showing_transition = True
        self.transition_timer = 4.0
        sounds.play('level_start')
        
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
        # Update surface if screen resized
        curr_w, curr_h = self.screen.get_size()
        if self.game_surface.get_width() != curr_w or self.game_surface.get_height() != curr_h - TITLE_BAR_HEIGHT:
            self.game_surface = pygame.Surface((curr_w, curr_h - TITLE_BAR_HEIGHT))
            self.crt_surface = pygame.Surface((curr_w, curr_h - TITLE_BAR_HEIGHT), pygame.SRCALPHA)
            for y in range(0, curr_h, 4):
                pygame.draw.line(self.crt_surface, (0, 0, 0, 40), (0, y), (curr_w, y))

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

        # Apply CRT effect
        self.game_surface.blit(self.crt_surface, (0, 0))

        # Composite to main screen
        self.screen.fill(BG_PRIMARY)
        self.window_controls.render(self.screen)
        
        # Draw game area background with rounded corners
        grid_w = GRID_SIZE * TILE_SIZE
        game_rect = pygame.Rect(0, TITLE_BAR_HEIGHT, grid_w, WINDOW_HEIGHT - TITLE_BAR_HEIGHT)
        pygame.draw.rect(self.screen, BG_SECONDARY, game_rect, border_radius=6)
        
        # Blit game surface
        self.screen.blit(self.game_surface, (0, TITLE_BAR_HEIGHT))
        
        # Draw border outline
        pygame.draw.rect(self.screen, (60, 70, 100), game_rect, width=2, border_radius=6)

        # 2. RENDER SIDEBAR TO MAIN SCREEN
        # Draw Sidebar Background
        sidebar_rect = pygame.Rect(grid_w, TITLE_BAR_HEIGHT, 240, WINDOW_HEIGHT - TITLE_BAR_HEIGHT)
        pygame.draw.rect(self.screen, BG_SECONDARY, sidebar_rect)
        
        # Render HUD elements
        self.hud.render(self.screen, self.level, self.lives, self.score, self.total_enemies - self.enemies_destroyed)

        # Game Over Overlay
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            
            font = pygame.font.SysFont('Arial', 64, bold=True)
            # Pulsing effect
            pulse = math.sin(self.game_over_timer * 5) * 10
            text = font.render("YOU LOSE", True, (255, 50, 50))
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40 + pulse))
            overlay.blit(text, text_rect)
            
            # Buttons
            mx, my = pygame.mouse.get_pos()
            btn_font = pygame.font.SysFont('Arial', 24, bold=True)
            
            # Play Again
            btn1_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50, 200, 50)
            color1 = (40, 180, 100) if btn1_rect.collidepoint(mx, my) else (30, 140, 80)
            pygame.draw.rect(overlay, color1, btn1_rect, border_radius=8)
            t1 = btn_font.render("PLAY AGAIN", True, (255, 255, 255))
            overlay.blit(t1, t1.get_rect(center=btn1_rect.center))
            
            # Quit
            btn2_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 120, 200, 50)
            color2 = (220, 60, 60) if btn2_rect.collidepoint(mx, my) else (180, 50, 50)
            pygame.draw.rect(overlay, color2, btn2_rect, border_radius=8)
            t2 = btn_font.render("QUIT", True, (255, 255, 255))
            overlay.blit(t2, t2.get_rect(center=btn2_rect.center))
            
            self.screen.blit(overlay, (0, 0))

        # Level Transition Overlay
        if self.showing_transition:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            # Dark fade based on timer
            alpha = min(255, int(self.transition_timer * 100)) if self.transition_timer < 1.0 else 220
            overlay.fill((0, 0, 0, alpha))
            
            font_title = pygame.font.SysFont('Arial', 80, bold=True)
            font_info = pygame.font.SysFont('Arial', 32)
            
            # Title
            title_str = f"LEVEL {self.level}" if self.level < 3 else "BOSS BATTLE"
            title = font_title.render(title_str, True, (255, 215, 0)) # Gold
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60))
            overlay.blit(title, title_rect)
            
            # Dynamic Instructions
            instructions = [
                f"LIVES: {self.lives}",
                f"ENEMIES: {self.total_enemies}"
            ]
            if self.level == 3:
                instructions = ["OBJECTIVE: DESTROY THE BOSS", "CAUTION: SHIELDS ENABLED"]
            
            for i, line in enumerate(instructions):
                text = font_info.render(line, True, (200, 200, 200))
                rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20 + i*40))
                overlay.blit(text, rect)
            
            self.screen.blit(overlay, (0, 0))
