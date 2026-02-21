"""
OpenGL primitive rendering functions.

This module provides functions for rendering basic 3D shapes used in the simulation.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Tuple

import config
from config import GameConfig


def draw_sphere(
    config: GameConfig,
    radius: float,
    slices: int | None = None,
    stacks: int | None = None
) -> None:
    """
    Draw a sphere using OpenGL quadrics.

    Args:
        radius: Sphere radius
        slices: Number of subdivisions around Z-axis
        stacks: Number of subdivisions along Z-axis
    """
    if slices is None:
        slices = config.SphereConfig.slices
    if stacks is None:
        stacks = config.SphereConfig.stacks

    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)


def draw_box(half_extent: float) -> None:
    """
    Draw a box centered at origin.

    Args:
        half_extent: Half the box size (distance from center to face)
    """
    s = half_extent

    # Define vertices for each face
    vertices = [
        # Front face
        [(-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)],
        # Back face
        [(s, -s, -s), (-s, -s, -s), (-s, s, -s), (s, s, -s)],
        # Left face
        [(-s, -s, -s), (-s, -s, s), (-s, s, s), (-s, s, -s)],
        # Right face
        [(s, -s, s), (s, -s, -s), (s, s, -s), (s, s, s)],
        # Top face
        [(-s, s, s), (s, s, s), (s, s, -s), (-s, s, -s)],
        # Bottom face
        [(-s, -s, -s), (s, -s, -s), (s, -s, s), (-s, -s, s)],
    ]

    # Normal vectors for each face
    normals = [
        (0, 0, 1),   # Front
        (0, 0, -1),  # Back
        (-1, 0, 0),  # Left
        (1, 0, 0),   # Right
        (0, 1, 0),   # Top
        (0, -1, 0),  # Bottom
    ]

    glBegin(GL_QUADS)
    for face_vertices, normal in zip(vertices, normals):
        glNormal3fv(normal)
        for vertex in face_vertices:
            glVertex3fv(vertex)
    glEnd()


def draw_cylinder(
    radius: float,
    height: float,
    slices: int = 12
) -> None:
    """
    Draw a cylinder along the Y-axis.

    Args:
        radius: Cylinder radius
        height: Cylinder height
        slices: Number of subdivisions around the axis
    """
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluCylinder(quadric, radius, radius, height, slices, 1)
    gluDeleteQuadric(quadric)


def draw_ground(
    config: GameConfig,
    size: int | None = None,
    grid_step: int | None = None,
    ground_color: Tuple[float, float, float] | None = None,
    grid_color: Tuple[float, float, float] | None = None
) -> None:
    """
    Draw ground plane with grid lines.

    Args:
        size: Half-size of ground plane (meters)
        grid_step: Spacing between grid lines (meters)
        ground_color: RGB color for ground surface
        grid_color: RGB color for grid lines
    """
    if size is None:
        size = config.world.ground_size
    if grid_step is None:
        grid_step = config.world.ground_grid_step
    if ground_color is None:
        ground_color = config.environment_colors.ground_color
    if grid_color is None:
        grid_color = config.environment_colors.grid_color


    ground_y = config.GROUND_LEVEL

    # Draw ground plane
    glDisable(GL_LIGHTING)
    glColor3f(*ground_color)
    glBegin(GL_QUADS)
    glVertex3f(-size, ground_y, -size)
    glVertex3f(size, ground_y, -size)
    glVertex3f(size, ground_y, size)
    glVertex3f(-size, ground_y, size)
    glEnd()

    # Draw grid lines
    glLineWidth(1.0)
    glColor3f(*grid_color)
    glBegin(GL_LINES)

    # Lines parallel to X-axis
    for i in range(-size, size + 1, grid_step):
        glVertex3f(i, ground_y + 0.01, -size)
        glVertex3f(i, ground_y + 0.01, size)

    # Lines parallel to Z-axis
    for i in range(-size, size + 1, grid_step):
        glVertex3f(-size, ground_y + 0.01, i)
        glVertex3f(size, ground_y + 0.01, i)

    glEnd()
    glEnable(GL_LIGHTING)


def draw_skybox(
    horizon_color: Tuple[float, float, float] | None = None,
    zenith_color: Tuple[float, float, float] | None = None
) -> None:
    """
    Draw a gradient skybox using a fullscreen quad.

    Args:
        horizon_color: RGB color at horizon
        zenith_color: RGB color at zenith (top of sky)
    """
    if horizon_color is None:
        horizon_color = config.EnvironmentColorConfig.sky_horizon_color
    if zenith_color is None:
        zenith_color = config.EnvironmentColorConfig.sky_zenith_color

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    # Save matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw gradient quad
    glBegin(GL_QUADS)
    # Bottom (horizon)
    glColor3f(*horizon_color)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    # Top (zenith)
    glColor3f(*zenith_color)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)
    glEnd()

    # Restore matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
