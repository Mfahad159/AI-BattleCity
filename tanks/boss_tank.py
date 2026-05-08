import pygame
from tanks.base_tank import BaseTank
from ai.minimax import MinimaxSolver
from constants import PURPLE, HP_BOSS, BOSS_PHASES, SPEED_SLOW, FIRE_RATE_BASIC
from core.assets import assets

class BossTank(BaseTank):
    def __init__(self, x, y):
        super().__init__(x, y, tank_type='boss', speed=40.0)
        self.hp = HP_BOSS
        self.max_hp = HP_BOSS
        self.color = PURPLE
        self.solver = MinimaxSolver()
        self.phase = 1

    def update_phase(self):
        for p, config in BOSS_PHASES.items():
            low, high = config['hp_range']
            if low <= self.hp <= high:
                self.phase = p
                ticks = config['speed']
                # Pixels per second calculation: (60 / ticks) * 32
                self.base_speed = (60.0 / ticks) * 32.0
                self.fire_rate = config['fire_rate']
                break

    def decide(self, grid, player):
        self.update_phase()
        
        # Grid alignment check for smooth movement
        if self.x != self.target_gx or self.y != self.target_gy:
            return "wait"
        
        # Build current state for minimax
        state = {
            'grid': grid.matrix,
            'boss_pos': (self.x, self.y),
            'player_pos': (player.x, player.y),
            'boss_hp': self.hp,
            'boss_max_hp': self.max_hp,
            'player_hp': player.hp,
            'player_max_hp': 1, # Player is 1 hit normally
            'is_over': not player.active or self.hp <= 0
        }
        
        depth = BOSS_PHASES[self.phase]['depth']
        _, best_action = self.solver.minimax(state, depth, float('-inf'), float('inf'), True)
        
        if best_action == "shoot":
            if self.can_shoot(): return "shoot"
        elif best_action:
            dx, dy = best_action
            self.move(dx, dy, grid)
            return "move"
            
        return "wait"

    def render(self, surface, color=None):
        # Boss is larger as per design.md
        px, py = self.render_x, self.render_y
        sprite = assets.get_sprite(self.tank_type, self.direction)
        if sprite:
            rect = sprite.get_rect(center=(px, py))
            surface.blit(sprite, rect)
