import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_SECONDARY, TEXT_PRIMARY, TEXT_ACCENT, 
    FONT_SIZE_HEADING, FONT_SIZE_BODY, GRID_SIZE, TILE_SIZE, TITLE_BAR_HEIGHT
)

class HUD:
    def __init__(self):
        self.font_heading = pygame.font.SysFont("Courier New", FONT_SIZE_HEADING, bold=True)
        self.font_body = pygame.font.SysFont("Courier New", FONT_SIZE_BODY)

    def render(self, surface, level, lives, score, enemies_remaining, debug_enabled):
        # Calculate hud_x to be exactly after the grid area
        grid_w = GRID_SIZE * TILE_SIZE
        hud_x = grid_w + 20
        hud_w = 210 # Safe width for sidebar content
        
        # 1. SCORE & STATUS
        font_title = pygame.font.SysFont("Impact", 36)
        title_surf = font_title.render("BATTLE CITY", True, TEXT_ACCENT)
        surface.blit(title_surf, (hud_x, TITLE_BAR_HEIGHT + 10))
        
        info_y = TITLE_BAR_HEIGHT + 60
        stats = [
            (f"LEVEL:", f"{level:02d}"),
            (f"LIVES:", f"{lives:02d}"),
            (f"SCORE:", f"{score:06d}"),
            (f"LEFT:",  f"{enemies_remaining:02d}")
        ]
        
        font_stats = pygame.font.SysFont("Verdana", 16, bold=True)
        for label, val in stats:
            l_surf = font_stats.render(label, True, TEXT_PRIMARY)
            v_surf = font_stats.render(val, True, TEXT_ACCENT)
            surface.blit(l_surf, (hud_x, info_y))
            surface.blit(v_surf, (hud_x + 80, info_y))
            info_y += 25

        # 2. NES CONTROLLER (Stylized)
        ctrl_y = info_y + 20
        pygame.draw.rect(surface, (180, 180, 180), (hud_x, ctrl_y, hud_w, 90), border_radius=10) # Body
        pygame.draw.rect(surface, (40, 40, 40), (hud_x + 10, ctrl_y + 10, hud_w - 20, 70), border_radius=5) # Inset
        # Buttons
        pygame.draw.circle(surface, (200, 0, 0), (hud_x + 150, ctrl_y + 45), 10) # A
        pygame.draw.circle(surface, (200, 0, 0), (hud_x + 180, ctrl_y + 45), 10) # B
        # D-Pad
        dp_x, dp_y = hud_x + 40, ctrl_y + 45
        pygame.draw.rect(surface, (20, 20, 20), (dp_x - 12, dp_y - 4, 24, 8))
        pygame.draw.rect(surface, (20, 20, 20), (dp_x - 4, dp_y - 12, 8, 24))

        # 3. CONTROL TABLE
        table_y = ctrl_y + 110
        font_header = pygame.font.SysFont("Impact", 20)
        header = font_header.render("GAMEPAD CONTROL:", True, (255, 255, 0)) # Yellow
        surface.blit(header, (hud_x, table_y))
        
        table_y += 30
        rows = [
            ("MOVE", "WASD / ARROWS"),
            ("SHOOT", "SPACE"),
            ("ESC", "QUIT")
        ]
        
        # Table Grid
        pygame.draw.rect(surface, (100, 100, 100), (hud_x, table_y, hud_w, 100), width=1)
        font_keys = pygame.font.SysFont("Verdana", 13, bold=True)
        for i, (action, key) in enumerate(rows):
            row_y = table_y + i * 32
            # Horizontal lines
            pygame.draw.line(surface, (100, 100, 100), (hud_x, row_y), (hud_x + hud_w, row_y))
            
            a_surf = font_stats.render(action, True, TEXT_PRIMARY)
            k_surf = font_keys.render(key, True, TEXT_ACCENT)
            surface.blit(a_surf, (hud_x + 5, row_y + 5))
            surface.blit(k_surf, (hud_x + 75, row_y + 7))

        # 4. 3D AI DEBUG BUTTON
        btn_y = WINDOW_HEIGHT - 120
        btn_rect = pygame.Rect(hud_x, btn_y, hud_w, 40)
        mx, my = pygame.mouse.get_pos()
        is_hover = btn_rect.collidepoint(mx, my)
        
        # 3D Shading
        base_color = (60, 140, 240) if is_hover else (40, 110, 200)
        pygame.draw.rect(surface, (20, 60, 120), (hud_x, btn_y + 4, hud_w, 40), border_radius=5) # Shadow
        pygame.draw.rect(surface, base_color, (hud_x, btn_y, hud_w, 40), border_radius=5) # Surface
        pygame.draw.rect(surface, (100, 180, 255), (hud_x, btn_y, hud_w, 40), width=2, border_radius=5) # Highlight
        
        status = "ON" if debug_enabled else "OFF"
        font_btn = pygame.font.SysFont("Impact", 18)
        b_surf = font_btn.render(f"AI DEBUGGER: {status}", True, (255, 255, 255))
        surface.blit(b_surf, b_surf.get_rect(center=btn_rect.center))

        # 5. FOOTER
        footer_y = btn_y + 50
        footer_text = [
            "If game is slow,",
            "disable AI Debug (F1)",
            "or use a better GPU."
        ]
        for i, line in enumerate(footer_text):
            f_surf = pygame.font.SysFont("Arial", 13).render(line, True, (150, 150, 150))
            surface.blit(f_surf, (hud_x, footer_y + i*18))
