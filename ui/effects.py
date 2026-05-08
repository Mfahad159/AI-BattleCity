import pygame
import random
from constants import RED_HOT, AMBER, CYAN

class Particle:
    def __init__(self, x, y, color, size=None):
        self.x = x
        self.y = y
        self.color = color
        self.size = size if size else random.randint(2, 5)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 1.0 # 1.0 to 0.0
        self.decay = random.uniform(0.02, 0.05)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        return self.life > 0

    def render(self, surface):
        alpha = int(self.life * 255)
        # Create a small surface for alpha blending
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        c = (*self.color, alpha)
        pygame.draw.circle(s, c, (self.size, self.size), self.size)
        surface.blit(s, (self.x - self.size, self.y - self.size))

class EffectManager:
    def __init__(self):
        self.particles = []

    def create_explosion(self, x, y, color=RED_HOT, count=20):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def create_trail(self, x, y, color=CYAN):
        self.particles.append(Particle(x, y, color, size=2))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def render(self, surface):
        for p in self.particles:
            p.render(surface)
