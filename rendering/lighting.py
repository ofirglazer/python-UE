"""
OpenGL lighting setup and configuration.

This module handles all lighting initialization for the scene,
implementing a two-light setup similar to Unreal Engine's default lighting.
"""

from OpenGL.GL import *
from config import GameConfig


def setup_lighting(config: GameConfig) -> None:
    """
    Configure OpenGL lighting system.

    Sets up a two-light system:
    - LIGHT0: Warm directional key light (sun)
    - LIGHT1: Cool directional fill light

    This creates a natural-looking lighting environment similar to
    Unreal Engine's default lighting setup.
    """
    # Enable lighting system
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

    # Configure main directional light (key light)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, config.lighting.light0_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, config.lighting.light0_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, config.lighting.light0_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, config.lighting.light0_specular)

    # Configure fill light (cool)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, config.lighting.light1_position)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, config.lighting.light1_diffuse)
    glLightfv(GL_LIGHT1, GL_AMBIENT, config.lighting.light1_ambient)

    # Configure material properties for specular highlights
    glMaterialfv(GL_FRONT, GL_SPECULAR, config.lighting.material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, config.lighting.material_shininess)


def disable_lighting() -> None:
    """Temporarily disable lighting (useful for HUD rendering)."""
    glDisable(GL_LIGHTING)


def enable_lighting() -> None:
    """Re-enable lighting after it was disabled."""
    glEnable(GL_LIGHTING)
