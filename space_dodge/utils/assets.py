from __future__ import annotations

import pygame


def build_player_surface(size: tuple[int, int]) -> pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    width, height = size
    points = [
        (0, height / 2),
        (width * 0.6, 0),
        (width, height / 2),
        (width * 0.6, height),
    ]
    pygame.draw.polygon(surface, (80, 200, 255), points)
    pygame.draw.polygon(surface, (30, 100, 200), points, width=2)
    return surface


def build_enemy_surface(size: tuple[int, int]) -> pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    width, height = size
    pygame.draw.rect(surface, (255, 90, 90), (0, 0, width, height), border_radius=6)
    pygame.draw.rect(surface, (160, 30, 30), (2, 2, width - 4, height - 4), width=2, border_radius=6)
    return surface


def build_projectile_surface(size: tuple[int, int], color: tuple[int, int, int]) -> pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.ellipse(surface, color, (0, 0, *size))
    return surface


def build_heart_surface(size: int) -> pygame.Surface:
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    color = (255, 50, 80)
    # Simple heart shape using two circles and a polygon
    r = size // 2
    pygame.draw.circle(surface, color, (r // 2, r // 2), r // 2)
    pygame.draw.circle(surface, color, (size - r // 2, r // 2), r // 2)
    pygame.draw.polygon(surface, color, [(0, r), (size, r), (r, size)])
    return surface


def build_heal_surface(size: tuple[int, int]) -> pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surface, (50, 255, 100), (0, 0, *size), border_radius=4)
    # Draw a plus sign
    w, h = size
    pygame.draw.line(surface, (255, 255, 255), (w // 2, 4), (w // 2, h - 4), width=3)
    pygame.draw.line(surface, (255, 255, 255), (4, h // 2), (w - 4, h // 2), width=3)
    return surface
