import pygame
from core.grid import Grid
from core.bullet import Bullet
from tanks.player_tank import PlayerTank
from ui.hud import HUD
from ui.window_controls import WindowControls
from constants import BG_PRIMARY, BG_SECONDARY, WINDOW_WIDTH, WINDOW_HEIGHT, CYAN, TITLE_BAR_HEIGHT

from core.spawner import Spawner

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.window_controls = WindowControls()
        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TITLE_BAR_HEIGHT))
        
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
            
            # 6. COLLISION DETECT (Special check for Eagle)
            if bullet.grid_x == 12 and bullet.grid_y == 24: # Eagle Pos
                self.running = False # Game Over
            
        # 7. ANIMATIONS (Smooth movement)
        self.player.update_animation()
        for enemy in self.enemies:
            enemy.update_animation()

        # 8. STATE UPDATE
        self.bullets = [b for b in self.bullets if b.active]
        
        for e in self.enemies:
            if not e.active:
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
            # Special Boss Level
            self.total_enemies = 1
            from tanks.boss_tank import BossTank
            # Spawn boss in the center top
            self.enemies = [BossTank(12, 1)]
        else:
            self.total_enemies = 20
            self.enemies = []

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
