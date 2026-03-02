from __future__ import annotations

import pygame


class Projectile:
    def __init__(
        self,
        position: pygame.Vector2,
        speed: float,
        surface: pygame.Surface,
        is_player: bool,
    ) -> None:
        self.position = position
        self.speed = speed
        self._surface = surface
        self.is_player = is_player
        self.rect = pygame.Rect(
            round(position.x),
            round(position.y),
            surface.get_width(),
            surface.get_height(),
        )

    def update(self, dt: float) -> None:
        self.position.x += self.speed * dt
        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self.rect)

    def is_offscreen(self, screen_width: int) -> bool:
        return self.rect.right < 0 or self.rect.left > screen_width
