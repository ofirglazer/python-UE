"""
Configuration module for UE-inspired simulation.

This module contains all configuration constants used throughout the application,
following PEP8 naming conventions and grouped by category.
"""

from dataclasses import dataclass
from typing import Tuple


# ============================================================================
# Display Settings
# ============================================================================

@dataclass(frozen=True)
class DisplayConfig:
    width: int = 1920
    height: int = 1080
    title: str = (
        "UE-Inspired 3D Simulation | WASD+Mouse | F=Shoot G=Crate ESC=Quit"
    )


# ============================================================================
# Camera Settings
# ============================================================================

@dataclass(frozen=True)
class CameraConfig:
    field_of_view: float = 46.7  # 75.0
    near_plane: float = 0.1
    far_plane: float = 500.0
    mouse_sensitivity: float = 0.15
    pitch_limit: float = 89.0  # Maximum pitch angle in degrees


# ============================================================================
# Physics Settings
# ============================================================================

@dataclass(frozen=True)
class PhysicsConfig:
    gravity: float = -9.81  # -18.0  # Acceleration due to gravity (m/s²)
    friction: float = 0.82  # Ground friction coefficient (0-1)
    restitution: float = 0.45  # Bounciness coefficient (0-1)
    max_physics_delta: float = 0.05  # Maximum physics timestep (seconds)


# ============================================================================
# Player Settings
# ============================================================================

@dataclass(frozen=True)
class PlayerConfig:
    speed: float = 8.0  # Movement speed (m/s)
    height: float = 1.75  # Eye height above ground (meters)
    radius: float = 0.4  # Collision radius (meters)
    jump_speed: float = 3.0  # 8.0  # Initial vertical velocity when jumping (m/s)


# ============================================================================
# World Settings
# ============================================================================

@dataclass(frozen=True)
class WorldConfig:
    ground_level: float = 0.0  # Y-coordinate of ground plane
    ground_size: int = 80  # Half-size of ground plane (meters)
    ground_grid_step: int = 2  # Grid line spacing (meters)


# ============================================================================
# Gameplay Settings
# ============================================================================

@dataclass(frozen=True)
class GameplayConfig:
    shoot_speed: float = 30.0  # Initial velocity of shot spheres (m/s)
    shoot_cooldown: float = 0.15  # Time between shots (seconds)
    max_objects: int = 200  # Maximum number of physics objects
    object_lifetime: float = 120.0  # Maximum age of objects (seconds)
    world_kill_depth: float = -60.0  # Y-coordinate where objects are destroyed


# ============================================================================
# Rendering Settings
# ============================================================================

@dataclass(frozen=True)
class RenderingConfig:
    target_fps: int = 120
    fps_sample_size: int = 20  # Number of frames to average for FPS display


# ============================================================================
# Sphere Settings
# ============================================================================

@dataclass(frozen=True)
class SphereConfig:
    default_radius: float = 0.25
    default_mass: float = 0.8
    slices: int = 16  # Tessellation detail
    stacks: int = 12  # Tessellation detail

    colors: Tuple[Tuple[float, float, float], ...] = (
        (0.95, 0.25, 0.18),  # Red
        (0.15, 0.75, 0.35),  # Green
        (0.15, 0.50, 0.95),  # Blue
        (0.95, 0.75, 0.10),  # Yellow
        (0.80, 0.20, 0.80),  # Magenta
        (0.10, 0.85, 0.90),  # Cyan
    )


# ============================================================================
# Crate Settings
# ============================================================================

@dataclass(frozen=True)
class CrateConfig:
    min_size: float = 0.3
    max_size: float = 0.6
    mass: float = 2.0
    spawn_distance: float = 5.0  # Distance from player to spawn crates

    colors: Tuple[Tuple[float, float, float], ...] = (
        (0.65, 0.48, 0.28),  # Wooden brown
        (0.50, 0.60, 0.35),  # Olive green
        (0.40, 0.40, 0.55),  # Blue-grey
    )


# ============================================================================
# Color Palettes (Ground & Sky)
# ============================================================================

@dataclass(frozen=True)
class EnvironmentColorConfig:
    ground_color: Tuple[float, float, float] = (0.12, 0.12, 0.12)
    grid_color: Tuple[float, float, float] = (0.22, 0.22, 0.22)

    sky_horizon_color: Tuple[float, float, float] = (0.05, 0.12, 0.22)
    sky_zenith_color: Tuple[float, float, float] = (0.01, 0.04, 0.15)


# ============================================================================
# Lighting Settings
# ============================================================================

@dataclass(frozen=True)
class LightingConfig:
    # Main directional light (sun)
    light0_position: Tuple[float, float, float, float] = (1.0, 3.0, 2.0, 0.0)
    light0_diffuse: Tuple[float, float, float, float] = (1.0, 0.95, 0.9, 1.0)
    light0_ambient: Tuple[float, float, float, float] = (0.18, 0.18, 0.22, 1.0)
    light0_specular: Tuple[float, float, float, float] = (0.6, 0.6, 0.6, 1.0)

    # Fill light (cool)
    light1_position: Tuple[float, float, float, float] = (-2.0, 1.5, -1.0, 0.0)
    light1_diffuse: Tuple[float, float, float, float] = (0.15, 0.2, 0.35, 1.0)
    light1_ambient: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)

    # Material properties
    material_specular: Tuple[float, float, float, float] = (0.4, 0.4, 0.4, 1.0)
    material_shininess: float = 32.0


# ============================================================================
# Static Scene Objects
# ============================================================================

@dataclass(frozen=True)
class StaticSceneConfig:
    objects: Tuple[
        Tuple[str, Tuple[float, float, float], float, Tuple[float, float, float]],
        ...
    ] = (
        # (type, position, size, color)
        ("box", (-6.0, 0.5, -10.0), 0.5, (0.6, 0.45, 0.25)),
        ("box", (-5.0, 1.5, -10.0), 0.5, (0.55, 0.40, 0.20)),
        ("box", (-4.0, 0.5, -10.0), 0.5, (0.65, 0.48, 0.28)),
        ("box", (6.0, 0.5, -8.0), 0.5, (0.5, 0.35, 0.18)),
        ("box", (7.0, 1.5, -8.0), 0.5, (0.55, 0.38, 0.20)),
        ("pillar", (0.0, 1.5, -15.0), 0.8, (0.35, 0.35, 0.38)),
        ("pillar", (8.0, 1.5, -15.0), 0.8, (0.35, 0.35, 0.38)),
        ("pillar", (-8.0, 1.5, -15.0), 0.8, (0.35, 0.35, 0.38)),
    )


# ============================================================================
# HUD Settings
# ============================================================================

@dataclass(frozen=True)
class HUDConfig:
    crosshair_size: int = 12
    crosshair_gap: int = 4
    crosshair_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    crosshair_width: float = 1.5

    text_offset_x: int = 12
    text_offset_y: int = 12
    text_spacing: int = 2

    font_big_size: int = 20
    font_small_size: int = 14
    font_name: str = "consolas"


# ============================================================================
# Master Game Configuration
# ============================================================================

@dataclass(frozen=True)
class GameConfig:
    display: DisplayConfig = DisplayConfig()
    camera: CameraConfig = CameraConfig()
    physics: PhysicsConfig = PhysicsConfig()
    player: PlayerConfig = PlayerConfig()
    world: WorldConfig = WorldConfig()
    gameplay: GameplayConfig = GameplayConfig()
    rendering: RenderingConfig = RenderingConfig()
    sphere: SphereConfig = SphereConfig()
    crate: CrateConfig = CrateConfig()
    environment_colors: EnvironmentColorConfig = EnvironmentColorConfig()
    lighting: LightingConfig = LightingConfig()
    static_scene: StaticSceneConfig = StaticSceneConfig()
    hud: HUDConfig = HUDConfig()