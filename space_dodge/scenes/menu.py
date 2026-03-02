from __future__ import annotations

import pygame

from core.settings import GameSettings
from utils.ui import Button


class MenuScene:
    def __init__(self, settings: GameSettings, screen: pygame.Surface) -> None:
        self._settings = settings
        self._screen = screen
        self._font_large = pygame.font.Font(None, 64)
        self._font_medium = pygame.font.Font(None, 36)
        self._font_small = pygame.font.Font(None, 24)

        self.player_name = ""
        self.is_active = True
        self.should_start = False

        center_x = settings.screen.width // 2
        self._start_button = Button(
            center_x - 100,
            settings.screen.height // 2 + 50,
            200,
            50,
            "Start Game",
            self._font_medium,
        )

        self._input_rect = pygame.Rect(center_x - 150, settings.screen.height // 2 - 20, 300, 40)
        self._input_active = True

    def handle_event(self, event: pygame.event.Event) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self._start_button.update(mouse_pos)

        if self._start_button.is_clicked(event):
            if self.player_name.strip():
                self.should_start = True

        if event.type == pygame.KEYDOWN:
            if self._input_active:
                if event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        self.should_start = True
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 15:
                        self.player_name += event.unicode

    def handle_input(self, pressed: pygame.key.ScancodeWrapper, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self._screen.fill(self._settings.screen.background_color)

        # Title
        title_surf = self._font_large.render("SPACE DODGE", True, (100, 200, 255))
        title_rect = title_surf.get_rect(center=(self._settings.screen.width // 2, 100))
        self._screen.blit(title_surf, title_rect)

        # Name label
        label_surf = self._font_medium.render("Enter Your Name:", True, (255, 255, 255))
        label_rect = label_surf.get_rect(center=(self._settings.screen.width // 2, self._input_rect.top - 30))
        self._screen.blit(label_surf, label_rect)

        # Input box
        pygame.draw.rect(self._screen, (30, 30, 50), self._input_rect, border_radius=4)
        pygame.draw.rect(self._screen, (100, 100, 150), self._input_rect, width=2, border_radius=4)

        name_surf = self._font_medium.render(self.player_name, True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=self._input_rect.center)
        self._screen.blit(name_surf, name_rect)

        # Cursor
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = name_rect.right + 2 if self.player_name else self._input_rect.centerx
            pygame.draw.line(self._screen, (255, 255, 255), (cursor_x, self._input_rect.top + 8), (cursor_x, self._input_rect.bottom - 8), 2)

        self._start_button.draw(self._screen)

        # Instructions
        instr_surf = self._font_small.render("Controls: WASD to move, SPACE to shoot", True, (150, 150, 180))
        instr_rect = instr_surf.get_rect(center=(self._settings.screen.width // 2, self._settings.screen.height - 40))
        self._screen.blit(instr_surf, instr_rect)
