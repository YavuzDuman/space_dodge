from __future__ import annotations

import pygame


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int] = (60, 60, 80),
        hover_color: tuple[int, int, int] = (80, 80, 110),
        text_color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, width=1, border_radius=4)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered


class Modal:
    def __init__(
        self,
        screen_size: tuple[int, int],
        title: str,
        font: pygame.font.Font,
        button_text: str,
    ) -> None:
        self.width, self.height = 300, 200
        self.rect = pygame.Rect(
            (screen_size[0] - self.width) // 2,
            (screen_size[1] - self.height) // 2,
            self.width,
            self.height,
        )
        self.title = title
        self.font = font
        self.button = Button(
            self.rect.centerx - 60,
            self.rect.bottom - 60,
            120,
            40,
            button_text,
            font,
        )

    def draw(self, surface: pygame.Surface) -> None:
        # Dim background
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # Modal box
        pygame.draw.rect(surface, (40, 40, 50), self.rect, border_radius=8)
        pygame.draw.rect(surface, (180, 180, 200), self.rect, width=2, border_radius=8)

        # Title
        title_surf = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.rect.centerx, self.rect.top + 50))
        surface.blit(title_surf, title_rect)

        self.button.draw(surface)
