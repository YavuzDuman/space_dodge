from __future__ import annotations

import pygame

from core.settings import GameSettings
from scenes.gameplay import GameplayScene
from scenes.menu import MenuScene


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._settings = GameSettings()
        self._screen = pygame.display.set_mode(
            (self._settings.screen.width, self._settings.screen.height)
        )
        pygame.display.set_caption(self._settings.screen.title)
        self._clock = pygame.time.Clock()
        
        self._menu_scene = MenuScene(self._settings, self._screen)
        self._gameplay_scene = GameplayScene(self._settings, self._screen)
        self._scene = self._menu_scene
        
        self._running = True

    def run(self) -> None:
        while self._running:
            dt = self._clock.tick(self._settings.screen.fps) / 1000.0
            self._handle_events()
            
            if self._scene == self._menu_scene:
                if self._menu_scene.should_start:
                    self._gameplay_scene.player_name = self._menu_scene.player_name
                    self._gameplay_scene.reset()
                    self._scene = self._gameplay_scene
                    self._menu_scene.should_start = False
            elif self._scene == self._gameplay_scene:
                if self._gameplay_scene.should_exit_to_menu:
                    self._scene = self._menu_scene
                    self._gameplay_scene.should_exit_to_menu = False

            self._scene.handle_input(pygame.key.get_pressed(), dt)
            self._scene.update(dt)
            self._scene.draw()
            pygame.display.flip()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            self._scene.handle_event(event)
