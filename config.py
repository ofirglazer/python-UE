"""
Configuration module for UE-inspired simulation.

This module contains all configuration constants used throughout the application,
following PEP8 naming conventions and grouped by category.
"""

from typing import Tuple


# ============================================================================
# Display Settings
# ============================================================================
WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 1280
WINDOW_TITLE: str = "UE-Inspired 3D Simulation | WASD+Mouse | F=Shoot G=Crate ESC=Quit"


# ============================================================================
# Camera Settings
# ============================================================================
FIELD_OF_VIEW: float = 75.0
NEAR_PLANE: float = 0.1
FAR_PLANE: float = 500.0
MOUSE_SENSITIVITY: float = 0.15
PITCH_LIMIT: float = 89.0  # Maximum pitch angle in degrees


# ============================================================================
# Physics Settings
# ============================================================================
GRAVITY: float = -18.0  # Acceleration due to gravity (m/s²)
FRICTION: float = 0.82  # Ground friction coefficient (0-1)
RESTITUTION: float = 0.45  # Bounciness coefficient (0-1)
MAX_PHYSICS_DELTA: float = 0.05  # Maximum physics timestep (seconds)


# ============================================================================
# Player Settings
# ============================================================================
PLAYER_SPEED: float = 8.0  # Movement speed (m/s)
PLAYER_HEIGHT: float = 1.75  # Eye height above ground (meters)
PLAYER_RADIUS: float = 0.4  # Collision radius (meters)
JUMP_SPEED: float = 8.0  # Initial vertical velocity when jumping (m/s)


# ============================================================================
# World Settings
# ============================================================================
GROUND_LEVEL: float = 0.0  # Y-coordinate of ground plane
GROUND_SIZE: int = 80  # Half-size of ground plane (meters)
GROUND_GRID_STEP: int = 2  # Grid line spacing (meters)


# ============================================================================
# Gameplay Settings
# ============================================================================
SHOOT_SPEED: float = 30.0  # Initial velocity of shot spheres (m/s)
SHOOT_COOLDOWN: float = 0.15  # Time between shots (seconds)
MAX_OBJECTS: int = 200  # Maximum number of physics objects
OBJECT_LIFETIME: float = 120.0  # Maximum age of objects (seconds)
WORLD_KILL_DEPTH: float = -60.0  # Y-coordinate where objects are destroyed


# ============================================================================
# Rendering Settings
# ============================================================================
TARGET_FPS: int = 120
FPS_SAMPLE_SIZE: int = 20  # Number of frames to average for FPS display


# ============================================================================
# Sphere Settings
# ============================================================================
SPHERE_DEFAULT_RADIUS: float = 0.25
SPHERE_DEFAULT_MASS: float = 0.8
SPHERE_SLICES: int = 16  # Tessellation detail
SPHERE_STACKS: int = 12  # Tessellation detail


# ============================================================================
# Crate Settings
# ============================================================================
CRATE_MIN_SIZE: float = 0.3
CRATE_MAX_SIZE: float = 0.6
CRATE_MASS: float = 2.0
CRATE_SPAWN_DISTANCE: float = 5.0  # Distance from player to spawn crates


# ============================================================================
# Color Palettes
# ============================================================================
SPHERE_COLORS: Tuple[Tuple[float, float, float], ...] = (
    (0.95, 0.25, 0.18),  # Red
    (0.15, 0.75, 0.35),  # Green
    (0.15, 0.50, 0.95),  # Blue
    (0.95, 0.75, 0.10),  # Yellow
    (0.80, 0.20, 0.80),  # Magenta
    (0.10, 0.85, 0.90),  # Cyan
)

CRATE_COLORS: Tuple[Tuple[float, float, float], ...] = (
    (0.65, 0.48, 0.28),  # Wooden brown
    (0.50, 0.60, 0.35),  # Olive green
    (0.40, 0.40, 0.55),  # Blue-grey
)

# Ground colors
GROUND_COLOR: Tuple[float, float, float] = (0.12, 0.12, 0.12)
GRID_COLOR: Tuple[float, float, float] = (0.22, 0.22, 0.22)

# Sky colors
SKY_HORIZON_COLOR: Tuple[float, float, float] = (0.05, 0.12, 0.22)
SKY_ZENITH_COLOR: Tuple[float, float, float] = (0.01, 0.04, 0.15)


# ============================================================================
# Lighting Settings
# ============================================================================
# Main directional light (sun)
LIGHT0_POSITION: Tuple[float, float, float, float] = (1.0, 3.0, 2.0, 0.0)
LIGHT0_DIFFUSE: Tuple[float, float, float, float] = (1.0, 0.95, 0.9, 1.0)
LIGHT0_AMBIENT: Tuple[float, float, float, float] = (0.18, 0.18, 0.22, 1.0)
LIGHT0_SPECULAR: Tuple[float, float, float, float] = (0.6, 0.6, 0.6, 1.0)

# Fill light (cool)
LIGHT1_POSITION: Tuple[float, float, float, float] = (-2.0, 1.5, -1.0, 0.0)
LIGHT1_DIFFUSE: Tuple[float, float, float, float] = (0.15, 0.2, 0.35, 1.0)
LIGHT1_AMBIENT: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)

# Material properties
MATERIAL_SPECULAR: Tuple[float, float, float, float] = (0.4, 0.4, 0.4, 1.0)
MATERIAL_SHININESS: float = 32.0


# ============================================================================
# Static Scene Objects
# ============================================================================
STATIC_OBJECTS: Tuple[Tuple[str, Tuple[float, float, float], float, Tuple[float, float, float]], ...] = (
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
HUD_CROSSHAIR_SIZE: int = 12
HUD_CROSSHAIR_GAP: int = 4
HUD_CROSSHAIR_COLOR: Tuple[float, float, float] = (1.0, 1.0, 1.0)
HUD_CROSSHAIR_WIDTH: float = 1.5

HUD_TEXT_OFFSET_X: int = 12
HUD_TEXT_OFFSET_Y: int = 12
HUD_TEXT_SPACING: int = 2

HUD_FONT_BIG_SIZE: int = 20
HUD_FONT_SMALL_SIZE: int = 14
HUD_FONT_NAME: str = "consolas"
