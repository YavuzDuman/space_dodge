from __future__ import annotations

import random

import pygame

from core.settings import EnemySettings, HealSettings, ScreenSettings, SpawnSettings
from entities.enemy import Enemy
from entities.heal_item import HealItem


class EnemySpawner:
    def __init__(
        self,
        settings: SpawnSettings,
        enemy_settings: EnemySettings,
        heal_settings: HealSettings,
        screen: ScreenSettings,
        enemy_surface: pygame.Surface,
        projectile_surface: pygame.Surface,
        projectile_speed: float,
        heal_surface: pygame.Surface,
    ) -> None:
        self._settings = settings
        self._enemy_settings = enemy_settings
        self._heal_settings = heal_settings
        self._screen = screen
        self._enemy_surface = enemy_surface
        self._projectile_surface = projectile_surface
        self._projectile_speed = projectile_speed
        self._heal_surface = heal_surface
        self._timer = 0.0
        self._next_spawn = self._random_interval()

    def update(
        self,
        dt: float,
        level: int,
    ) -> tuple[list[Enemy], list[HealItem]]:
        self._timer += dt
        enemies: list[Enemy] = []
        heals: list[HealItem] = []
        if self._timer >= self._next_spawn:
            self._timer = 0.0
            self._next_spawn = self._random_interval()
            enemies.append(self._create_enemy(level))
            if level == 2 and random.random() < self._heal_settings.spawn_chance:
                heals.append(self._create_heal())
        return enemies, heals

    def _random_interval(self) -> float:
        return random.uniform(self._settings.interval_min, self._settings.interval_max)

    def _create_enemy(self, level: int) -> Enemy:
        y_position = random.uniform(0, self._screen.height - self._enemy_surface.get_height())
        position = pygame.Vector2(self._screen.width + 20, y_position)
        speed = random.uniform(self._enemy_settings.speed_min, self._enemy_settings.speed_max)
        if level == 2:
            fire_rate = random.uniform(
                self._enemy_settings.level_two_fire_rate_min,
                self._enemy_settings.level_two_fire_rate_max,
            )
            vertical_speed = self._enemy_settings.level_two_vertical_speed
        else:
            fire_rate = random.uniform(
                self._enemy_settings.fire_rate_min, self._enemy_settings.fire_rate_max
            )
            vertical_speed = 0.0
        return Enemy(
            position,
            speed,
            self._enemy_surface,
            self._projectile_surface,
            self._projectile_speed,
            fire_rate,
            vertical_speed,
        )

    def _create_heal(self) -> HealItem:
        y_position = random.uniform(0, self._screen.height - self._heal_surface.get_height())
        position = pygame.Vector2(self._screen.width + 20, y_position)
        speed = random.uniform(self._heal_settings.speed_min, self._heal_settings.speed_max)
        return HealItem(position, speed, self._heal_surface)
