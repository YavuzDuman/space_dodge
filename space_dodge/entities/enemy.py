from __future__ import annotations

import random

import pygame

from entities.projectile import Projectile


class Enemy:
    def __init__(
        self,
        position: pygame.Vector2,
        speed: float,
        surface: pygame.Surface,
        projectile_surface: pygame.Surface,
        projectile_speed: float,
        fire_rate: float,
        vertical_speed: float = 0.0,
    ) -> None:
        self.position = position
        self.speed = speed
        self._surface = surface
        self._projectile_surface = projectile_surface
        self._projectile_speed = projectile_speed
        self._fire_rate = fire_rate
        self._fire_timer = 0.0
        self._vertical_speed = vertical_speed
        self._vertical_direction = random.choice([-1, 1])
        self._direction_timer = random.uniform(0.6, 1.8)
        self._direction_elapsed = 0.0
        self.rect = pygame.Rect(
            round(position.x),
            round(position.y),
            surface.get_width(),
            surface.get_height(),
        )

    def update(self, dt: float, screen_height: int | None = None) -> list[Projectile]:
        self.position.x -= self.speed * dt

        if self._vertical_speed > 0 and screen_height is not None:
            self._direction_elapsed += dt
            if self._direction_elapsed >= self._direction_timer:
                self._direction_elapsed = 0.0
                self._direction_timer = random.uniform(0.6, 1.8)
                self._vertical_direction = random.choice([-1, 1])

            self.position.y += self._vertical_direction * self._vertical_speed * dt
            max_y = screen_height - self.rect.height
            if self.position.y < 0:
                self.position.y = 0
                self._vertical_direction = 1
            elif self.position.y > max_y:
                self.position.y = max_y
                self._vertical_direction = -1

        self.rect.topleft = (round(self.position.x), round(self.position.y))

        projectiles = []
        self._fire_timer += dt
        if self._fire_timer >= self._fire_rate:
            self._fire_timer = 0.0
            # Add some randomness to next fire
            self._fire_rate *= random.uniform(0.8, 1.2)
            projectiles.append(self._fire())
        return projectiles

    def _fire(self) -> Projectile:
        pos = pygame.Vector2(
            self.rect.left - self._projectile_surface.get_width(),
            self.rect.centery - self._projectile_surface.get_height() / 2,
        )
        return Projectile(pos, self._projectile_speed, self._projectile_surface, False)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self.rect)

    def is_offscreen(self) -> bool:
        return self.rect.right < 0
