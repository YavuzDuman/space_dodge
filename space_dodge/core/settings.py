from dataclasses import dataclass


@dataclass(frozen=True)
class ScreenSettings:
    width: int = 960
    height: int = 540
    fps: int = 60
    title: str = "Space Dodge"
    background_color: tuple[int, int, int] = (10, 10, 30)
    background_level_two: tuple[int, int, int] = (10, 40, 20)


@dataclass(frozen=True)
class PlayerSettings:
    speed: float = 280.0
    size: tuple[int, int] = (40, 28)
    start_x: int = 80
    lives: int = 3
    fire_rate: float = 0.3


@dataclass(frozen=True)
class EnemySettings:
    speed_min: float = 140.0
    speed_max: float = 320.0
    size: tuple[int, int] = (36, 24)
    fire_rate_min: float = 1.0
    fire_rate_max: float = 3.5
    level_two_fire_rate_min: float = 0.6
    level_two_fire_rate_max: float = 2.0
    level_two_vertical_speed: float = 90.0


@dataclass(frozen=True)
class SpawnSettings:
    interval_min: float = 0.6
    interval_max: float = 1.4


@dataclass(frozen=True)
class ProjectileSettings:
    player_speed: float = 550.0
    enemy_speed: float = -380.0
    size: tuple[int, int] = (12, 6)
    color_player: tuple[int, int, int] = (100, 255, 150)
    color_enemy: tuple[int, int, int] = (255, 100, 100)


@dataclass(frozen=True)
class HealSettings:
    speed_min: float = 120.0
    speed_max: float = 240.0
    size: tuple[int, int] = (24, 24)
    spawn_chance: float = 0.2  # 20% chance whenever an enemy spawns


@dataclass(frozen=True)
class LevelSettings:
    duration_seconds: float = 60.0


@dataclass(frozen=True)
class GameSettings:
    screen: ScreenSettings = ScreenSettings()
    player: PlayerSettings = PlayerSettings()
    enemy: EnemySettings = EnemySettings()
    spawn: SpawnSettings = SpawnSettings()
    projectile: ProjectileSettings = ProjectileSettings()
    heal: HealSettings = HealSettings()
    level: LevelSettings = LevelSettings()
