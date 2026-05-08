import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BG_SECONDARY, TEXT_PRIMARY, TEXT_ACCENT, FONT_SIZE_HEADING, FONT_SIZE_BODY

class HUD:
    def __init__(self):
        self.font_heading = pygame.font.SysFont("Courier New", FONT_SIZE_HEADING, bold=True)
        self.font_body = pygame.font.SysFont("Courier New", FONT_SIZE_BODY)

    def render(self, surface, level, lives, score, enemies_remaining):
        hud_x = WINDOW_WIDTH - 150
        
        # Title
        title_surf = self.font_heading.render("BATTLE CITY", True, TEXT_ACCENT)
        surface.blit(title_surf, (hud_x, 20))
        
        # Level
        level_surf = self.font_body.render(f"LEVEL: {level:02d}", True, TEXT_PRIMARY)
        surface.blit(level_surf, (hud_x, 70))
        
        # Lives
        lives_surf = self.font_body.render(f"LIVES: {lives:02d}", True, TEXT_PRIMARY)
        surface.blit(lives_surf, (hud_x, 110))
        
        # Score
        score_label = self.font_body.render("SCORE:", True, TEXT_PRIMARY)
        surface.blit(score_label, (hud_x, 160))
        score_val = self.font_heading.render(f"{score:06d}", True, TEXT_ACCENT)
        surface.blit(score_val, (hud_x, 185))
        
        # Enemies
        enemy_surf = self.font_body.render(f"ENEMIES: {enemies_remaining:02d}", True, TEXT_PRIMARY)
        surface.blit(enemy_surf, (hud_x, 240))
