import random
from constants import ENEMY_SPAWNS, SPAWN_FAIRNESS_DISTANCE, MAX_ACTIVE_ENEMIES
from tanks.basic_tank import BasicTank
from tanks.fast_tank import FastTank
from tanks.armor_tank import ArmorTank

class Spawner:
    def __init__(self):
        self.spawn_points = ENEMY_SPAWNS
        self.spawn_index = 0
        self.spawn_cooldown = 120 # Ticks between spawns
        self.timer = 0

    def update(self, game):
        self.timer += 1
        if self.timer >= self.spawn_cooldown:
            if len(game.enemies) < MAX_ACTIVE_ENEMIES and game.enemies_spawned < game.total_enemies:
                self.spawn_enemy(game)
                self.timer = 0

    def spawn_enemy(self, game):
        # Rotate spawn points
        pos = self.spawn_points[self.spawn_index]
        self.spawn_index = (self.spawn_index + 1) % len(self.spawn_points)
        
        # Fairness check
        px, py = game.player.x, game.player.y
        dist = abs(pos[0] - px) + abs(pos[1] - py)
        if dist < SPAWN_FAIRNESS_DISTANCE:
            # Skip this spawn point or find another
            return
            
        # Determine tank type based on level and progress
        # Level 1: first 10 are Basic, then Fast
        if game.level == 1:
            if game.enemies_destroyed < 10:
                enemy = BasicTank(pos[0], pos[1])
            else:
                enemy = FastTank(pos[0], pos[1])
        elif game.level == 2:
            # Mix of Fast and Armor
            if random.random() < 0.3:
                enemy = ArmorTank(pos[0], pos[1])
            else:
                enemy = FastTank(pos[0], pos[1])
        else:
            enemy = BasicTank(pos[0], pos[1])
            
        game.enemies.append(enemy)
        game.enemies_spawned += 1
