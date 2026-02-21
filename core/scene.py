"""
Scene rendering and management.

This module handles rendering of static scene objects like crates and pillars.
"""

from OpenGL.GL import *
from typing import Tuple
from rendering.primitives import draw_box, draw_cylinder
from config import GameConfig


class SceneRenderer:
    """
    Renderer for static scene objects.

    This class manages rendering of non-physics objects that are
    part of the static scene environment.
    """

    def __init__(self, config: GameConfig) -> None:
        """Initialize scene renderer with static objects."""
        self.config = config
        self.static_objects = self.config.static_scene.objects

    def render(self) -> None:
        """Render all static scene objects."""
        for obj_type, position, size, color in self.static_objects:
            self._render_object(obj_type, position, size, color)

    def _render_object(
        self,
        obj_type: str,
        position: Tuple[float, float, float],
        size: float,
        color: Tuple[float, float, float]
    ) -> None:
        """
        Render a single static object.

        Args:
            obj_type: Type of object ("box" or "pillar")
            position: Object position [x, y, z]
            size: Object size (half-extent for box, radius for pillar)
            color: RGB color tuple
        """
        glPushMatrix()
        glTranslatef(*position)
        glColor3fv(color)

        if obj_type == "box":
            draw_box(size)
        elif obj_type == "pillar":
            # Pillars are cylinders along Y-axis
            glTranslatef(0, -size, 0)
            draw_cylinder(size * 0.4, size * 2, slices=12)

        glPopMatrix()
