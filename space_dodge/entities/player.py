from __future__ import annotations

import pygame

from core.settings import PlayerSettings, ScreenSettings
from entities.projectile import Projectile


class Player:
    def __init__(
        self,
        settings: PlayerSettings,
        screen_settings: ScreenSettings,
        surface: pygame.Surface,
        projectile_surface: pygame.Surface,
        projectile_speed: float,
    ) -> None:
        self._settings = settings
        self._screen = screen_settings
        self._surface = surface
        self._projectile_surface = projectile_surface
        self._projectile_speed = projectile_speed
        self.position = pygame.Vector2(
            settings.start_x,
            screen_settings.height / 2 - settings.size[1] / 2,
        )
        self.rect = pygame.Rect(0, 0, *settings.size)
        self._velocity = pygame.Vector2(0, 0)
        self._fire_timer = 0.0
        self.lives = settings.lives

    def handle_input(self, pressed: pygame.key.ScancodeWrapper, dt: float) -> list[Projectile]:
        velocity = pygame.Vector2(0, 0)
        if pressed[pygame.K_w]:
            velocity.y -= 1
        if pressed[pygame.K_s]:
            velocity.y += 1
        if pressed[pygame.K_a]:
            velocity.x -= 1
        if pressed[pygame.K_d]:
            velocity.x += 1
        if velocity.length_squared() > 0:
            velocity = velocity.normalize() * self._settings.speed
        self._velocity = velocity

        projectiles = []
        self._fire_timer += dt
        if pressed[pygame.K_SPACE] or pressed[pygame.K_j]:  # Added J as alternative fire
            if self._fire_timer >= self._settings.fire_rate:
                self._fire_timer = 0.0
                projectiles.append(self._fire())
        return projectiles

    def _fire(self) -> Projectile:
        pos = pygame.Vector2(self.rect.right, self.rect.centery - self._projectile_surface.get_height() / 2)
        return Projectile(pos, self._projectile_speed, self._projectile_surface, True)

    def update(self, dt: float) -> None:
        self.position += self._velocity * dt
        self.position.x = max(0, min(self.position.x, self._screen.width - self.rect.width))
        self.position.y = max(0, min(self.position.y, self._screen.height - self.rect.height))
        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self.rect)
