"""
Head-Up Display (HUD) rendering system.

This module handles all 2D overlay rendering including crosshair,
FPS counter, and control hints.
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List, Tuple
import config


class HUD:
    """
    HUD rendering system for displaying overlay information.

    Attributes:
        font_big: Large font for primary information
        font_small: Small font for secondary information
    """

    def __init__(self):
        """Initialize HUD with fonts."""
        self.font_big = pygame.font.SysFont(
            config.HUD_FONT_NAME,
            config.HUD_FONT_BIG_SIZE,
            bold=True
        )
        self.font_small = pygame.font.SysFont(
            config.HUD_FONT_NAME,
            config.HUD_FONT_SMALL_SIZE
        )

    def render(
        self,
        screen_width: int,
        screen_height: int,
        fps: float,
        object_count: int,
        player_pos: np.ndarray
    ) -> None:
        """
        Render complete HUD overlay.

        Args:
            screen_width: Window width in pixels
            screen_height: Window height in pixels
            fps: Current frames per second
            object_count: Number of physics objects
            player_pos: Player position [x, y, z]
        """
        self._render_crosshair(screen_width, screen_height)
        self._render_text_overlay(
            screen_width,
            screen_height,
            fps,
            object_count,
            player_pos
        )

    def _render_crosshair(self, width: int, height: int) -> None:
        """
        Render crosshair at screen center.

        Args:
            width: Screen width
            height: Screen height
        """
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        # Set up 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw crosshair lines
        cx, cy = width // 2, height // 2
        glColor3f(*config.HUD_CROSSHAIR_COLOR)
        glLineWidth(config.HUD_CROSSHAIR_WIDTH)

        glBegin(GL_LINES)
        # Horizontal lines
        glVertex2f(cx - config.HUD_CROSSHAIR_SIZE, cy)
        glVertex2f(cx - config.HUD_CROSSHAIR_GAP, cy)
        glVertex2f(cx + config.HUD_CROSSHAIR_GAP, cy)
        glVertex2f(cx + config.HUD_CROSSHAIR_SIZE, cy)

        # Vertical lines
        glVertex2f(cx, cy - config.HUD_CROSSHAIR_SIZE)
        glVertex2f(cx, cy - config.HUD_CROSSHAIR_GAP)
        glVertex2f(cx, cy + config.HUD_CROSSHAIR_GAP)
        glVertex2f(cx, cy + config.HUD_CROSSHAIR_SIZE)
        glEnd()

        # Restore matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def _render_text_overlay(
        self,
        width: int,
        height: int,
        fps: float,
        object_count: int,
        player_pos: np.ndarray
    ) -> None:
        """
        Render text information overlay.

        Args:
            width: Screen width
            height: Screen height
            fps: Current FPS
            object_count: Number of objects
            player_pos: Player position
        """
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        # Set up 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Define text lines
        lines: List[Tuple[pygame.font.Font, str, Tuple[int, int, int]]] = [
            (self.font_big, f"FPS: {fps:.0f}", (200, 220, 200)),
            (self.font_small, f"Objects: {object_count}", (180, 200, 180)),
            (self.font_small,
             f"Pos: {player_pos[0]:.1f} {player_pos[1]:.1f} {player_pos[2]:.1f}",
             (160, 180, 200)),
            (self.font_small, "", (0, 0, 0)),  # Spacer
            (self.font_small, "WASD  Move", (200, 200, 160)),
            (self.font_small, "Mouse  Look", (200, 200, 160)),
            (self.font_small, "SPACE  Jump", (200, 200, 160)),
            (self.font_small, "F  Shoot sphere", (200, 200, 160)),
            (self.font_small, "G  Spawn crate", (200, 200, 160)),
            (self.font_small, "R  Reset   ESC  Quit", (200, 200, 160)),
        ]

        # Render each line
        y_offset = config.HUD_TEXT_OFFSET_Y
        for font, text, color in lines:
            if text:
                surface = font.render(text, True, color)
                self._draw_text_surface(
                    surface,
                    config.HUD_TEXT_OFFSET_X,
                    y_offset,
                    height
                )
            y_offset += font.get_height() + config.HUD_TEXT_SPACING

        # Restore matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    @staticmethod
    def _draw_text_surface(
        surface: pygame.Surface,
        x: int,
        y: int,
        screen_height: int
    ) -> None:
        """
        Draw a pygame surface as an OpenGL texture.

        Args:
            surface: Pygame text surface
            x: X position
            y: Y position (from top)
            screen_height: Total screen height
        """
        text_width, text_height = surface.get_size()
        text_data = pygame.image.tostring(surface, "RGBA", True)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glRasterPos2f(x, screen_height - y - text_height)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glDisable(GL_BLEND)
