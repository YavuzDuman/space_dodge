from __future__ import annotations

import pygame

from core.settings import GameSettings
from entities.enemy import Enemy
from entities.heal_item import HealItem
from entities.player import Player
from entities.projectile import Projectile
from systems.spawner import EnemySpawner
from utils.assets import (
    build_enemy_surface,
    build_heal_surface,
    build_heart_surface,
    build_player_surface,
    build_projectile_surface,
)
from utils.ui import Button, Modal


class GameplayScene:
    def __init__(self, settings: GameSettings, screen: pygame.Surface) -> None:
        self._settings = settings
        self._screen = screen
        self.player_name = "Player"
        self.should_exit_to_menu = False

        self._player_projectile_surface = build_projectile_surface(
            settings.projectile.size, settings.projectile.color_player
        )
        self._enemy_projectile_surface = build_projectile_surface(
            settings.projectile.size, settings.projectile.color_enemy
        )
        self._player = Player(
            settings.player,
            settings.screen,
            build_player_surface(settings.player.size),
            self._player_projectile_surface,
            settings.projectile.player_speed,
        )
        self._enemy_surface = build_enemy_surface(settings.enemy.size)
        self._heal_surface = build_heal_surface(settings.heal.size)
        self._spawner = EnemySpawner(
            settings.spawn,
            settings.enemy,
            settings.heal,
            settings.screen,
            self._enemy_surface,
            self._enemy_projectile_surface,
            settings.projectile.enemy_speed,
            self._heal_surface,
        )
        self._enemies: list[Enemy] = []
        self._heals: list[HealItem] = []
        self._projectiles: list[Projectile] = []
        self._font = pygame.font.Font(None, 26)
        self._font_bold = pygame.font.Font(None, 28)
        self._score = 0.0
        self._heart_surface = build_heart_surface(24)
        self.is_paused = False
        self.game_over = False
        self.level = 1
        self._level_timer = settings.level.duration_seconds
        self._congrats_modal = Modal(
            (settings.screen.width, settings.screen.height),
            "CONGRATULATIONS!",
            self._font,
            "MENU",
        )
        self._congrats_modal.button.text = "MENU"

        # UI Components
        right_ui_x = settings.screen.width - 120
        self._pause_button = Button(right_ui_x, 20, 100, 30, "Pause", self._font)
        self._restart_button = Button(right_ui_x, 60, 100, 30, "Restart", self._font)
        self._menu_button = Button(right_ui_x, 100, 100, 30, "Menu", self._font)
        self._game_over_modal = Modal(
            (settings.screen.width, settings.screen.height),
            "GAME OVER",
            self._font,
            "RESTART",
        )

    def handle_input(self, pressed: pygame.key.ScancodeWrapper, dt: float) -> None:
        if self.game_over or self.is_paused:
            return
        new_projectiles = self._player.handle_input(pressed, dt)
        self._projectiles.extend(new_projectiles)

    def handle_event(self, event: pygame.event.Event) -> None:
        mouse_pos = pygame.mouse.get_pos()

        if self._is_congrats_visible():
            self._congrats_modal.button.update(mouse_pos)
            if self._congrats_modal.button.is_clicked(event):
                self.should_exit_to_menu = True
                self.is_paused = False
            return

        self._pause_button.update(mouse_pos)
        self._restart_button.update(mouse_pos)
        self._menu_button.update(mouse_pos)

        if self._pause_button.is_clicked(event):
            self.is_paused = not self.is_paused
            self._pause_button.text = "Resume" if self.is_paused else "Pause"

        if self._restart_button.is_clicked(event):
            self.reset()

        if self._menu_button.is_clicked(event):
            self.should_exit_to_menu = True

        if self.game_over:
            self._game_over_modal.button.update(mouse_pos)
            if self._game_over_modal.button.is_clicked(event):
                self.reset()

    def update(self, dt: float) -> None:
        if self.game_over or self.is_paused or self._is_congrats_visible():
            return

        self._score += dt
        self._player.update(dt)
        self._advance_level_timer(dt)

        if not self._is_congrats_visible():
            new_enemies, new_heals = self._spawner.update(dt, self.level)
            self._enemies.extend(new_enemies)
            self._heals.extend(new_heals)

        # Update Enemies
        for enemy in list(self._enemies):
            new_enemy_projectiles = enemy.update(dt, self._settings.screen.height)
            self._projectiles.extend(new_enemy_projectiles)
            if enemy.is_offscreen():
                self._enemies.remove(enemy)
            elif enemy.rect.colliderect(self._player.rect):
                self._handle_player_hit()
                if enemy in self._enemies:
                    self._enemies.remove(enemy)

        # Update Heals
        for heal in list(self._heals):
            heal.update(dt)
            if heal.is_offscreen():
                self._heals.remove(heal)
            elif heal.rect.colliderect(self._player.rect):
                if self._player.lives < self._settings.player.lives:
                    self._player.lives += 1
                self._heals.remove(heal)

        # Update Projectiles
        for projectile in list(self._projectiles):
            projectile.update(dt)
            if projectile.is_offscreen(self._settings.screen.width):
                self._projectiles.remove(projectile)
                continue

            if projectile.is_player:
                for enemy in list(self._enemies):
                    if projectile.rect.colliderect(enemy.rect):
                        if projectile in self._projectiles:
                            self._projectiles.remove(projectile)
                        if enemy in self._enemies:
                            self._enemies.remove(enemy)
                        break
            else:
                if projectile.rect.colliderect(self._player.rect):
                    self._handle_player_hit()
                    if projectile in self._projectiles:
                        self._projectiles.remove(projectile)

    def _handle_player_hit(self) -> None:
        self._player.lives -= 1
        if self._player.lives <= 0:
            self.game_over = True

    def _advance_level_timer(self, dt: float) -> None:
        self._level_timer = max(0.0, self._level_timer - dt)
        if self._level_timer <= 0:
            if self.level == 1:
                self.level = 2
                self._level_timer = self._settings.level.duration_seconds
                self._clear_level_entities()
            else:
                # Level 2 complete
                self.is_paused = True

    def _clear_level_entities(self) -> None:
        self._enemies.clear()
        self._heals.clear()
        self._projectiles.clear()

    def _is_congrats_visible(self) -> bool:
        return self.level == 2 and self._level_timer <= 0

    def reset(self) -> None:
        self._clear_level_entities()
        self._score = 0.0
        self._player.lives = self._settings.player.lives
        self._player.position.y = self._settings.screen.height / 2 - self._player.rect.height / 2
        self._player.position.x = self._settings.player.start_x
        self._player.rect.topleft = (
            round(self._player.position.x),
            round(self._player.position.y),
        )
        self.game_over = False
        self.is_paused = False
        self._pause_button.text = "Pause"
        self.should_exit_to_menu = False
        self.level = 1
        self._level_timer = self._settings.level.duration_seconds

    def draw(self) -> None:
        background = (
            self._settings.screen.background_level_two
            if self.level == 2
            else self._settings.screen.background_color
        )
        self._screen.fill(background)
        self._player.draw(self._screen)
        for enemy in self._enemies:
            enemy.draw(self._screen)
        for heal in self._heals:
            heal.draw(self._screen)
        for projectile in self._projectiles:
            projectile.draw(self._screen)

        # Draw Lives (Hearts) and Name
        name_text = self._font_bold.render(f"{self.player_name}", True, (255, 255, 255))
        self._screen.blit(name_text, (20, 20))
        
        heart_start_x = 25 + name_text.get_width()
        for i in range(self._player.lives):
            self._screen.blit(self._heart_surface, (heart_start_x + i * 30, 18))

        level_text = self._font.render(f"Level {self.level}", True, (220, 220, 240))
        self._screen.blit(level_text, (self._settings.screen.width // 2 - 40, 20))

        minutes, seconds = divmod(int(self._level_timer), 60)
        timer_text = self._font.render(
            f"Time Left: {minutes:01d}:{seconds:02d}",
            True,
            (220, 220, 240),
        )
        self._screen.blit(timer_text, (20, 50))

        # UI
        self._pause_button.draw(self._screen)
        self._restart_button.draw(self._screen)
        self._menu_button.draw(self._screen)

        if self.game_over:
            self._game_over_modal.draw(self._screen)

        if self._is_congrats_visible():
            self._congrats_modal.draw(self._screen)
