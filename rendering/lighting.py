"""
OpenGL lighting setup and configuration.

This module handles all lighting initialization for the scene,
implementing a two-light setup similar to Unreal Engine's default lighting.
"""

from OpenGL.GL import *
import config


def setup_lighting() -> None:
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
    glLightfv(GL_LIGHT0, GL_POSITION, config.LIGHT0_POSITION)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, config.LIGHT0_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_AMBIENT, config.LIGHT0_AMBIENT)
    glLightfv(GL_LIGHT0, GL_SPECULAR, config.LIGHT0_SPECULAR)

    # Configure fill light (cool)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, config.LIGHT1_POSITION)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, config.LIGHT1_DIFFUSE)
    glLightfv(GL_LIGHT1, GL_AMBIENT, config.LIGHT1_AMBIENT)

    # Configure material properties for specular highlights
    glMaterialfv(GL_FRONT, GL_SPECULAR, config.MATERIAL_SPECULAR)
    glMaterialf(GL_FRONT, GL_SHININESS, config.MATERIAL_SHININESS)


def disable_lighting() -> None:
    """Temporarily disable lighting (useful for HUD rendering)."""
    glDisable(GL_LIGHTING)


def enable_lighting() -> None:
    """Re-enable lighting after it was disabled."""
    glEnable(GL_LIGHTING)
