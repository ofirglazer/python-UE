"""
Camera system for first-person view.

This module implements a first-person camera with mouse-look controls,
similar to Unreal Engine's viewport camera.
"""

import numpy as np
import math
from OpenGL.GL import glRotatef, glTranslatef
from utils.math_utils import clamp
from config import GameConfig


class Camera:
    """
    First-person camera with mouse-look controls.

    Attributes:
        position: Camera position in world space [x, y, z]
        yaw: Horizontal rotation in degrees
        pitch: Vertical rotation in degrees
    """

    def __init__(
        self,
        config: GameConfig,
        position: tuple[float, float, float] = (0.0, 0.0, 0.0),
        yaw: float = 0.0,
        pitch: float = 0.0
    ):
        """
        Initialize the camera.

        Args:
            position: Initial camera position
            yaw: Initial horizontal rotation (degrees)
            pitch: Initial vertical rotation (degrees)
        """
        self.config = config
        self.position: np.ndarray = np.array(position, dtype=float)
        self.yaw: float = yaw
        self.pitch: float = pitch

    @property
    def forward(self) -> np.ndarray:
        """
        Calculate the forward direction vector.

        Returns:
            Normalized forward vector [x, y, z]
        """
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        return np.array([
            math.sin(yaw_rad) * math.cos(pitch_rad),
            -math.sin(pitch_rad),
            -math.cos(yaw_rad) * math.cos(pitch_rad)
        ])

    @property
    def right(self) -> np.ndarray:
        """
        Calculate the right direction vector (perpendicular to forward).

        Returns:
            Normalized right vector [x, y, z]
        """
        yaw_rad = math.radians(self.yaw)
        return np.array([
            math.cos(yaw_rad),
            0.0,
            math.sin(yaw_rad)
        ])

    @property
    def up(self) -> np.ndarray:
        """
        Calculate the up direction vector.

        Returns:
            Up vector [x, y, z]
        """
        return np.array([0.0, 1.0, 0.0])

    def rotate(self, delta_yaw: float, delta_pitch: float) -> None:
        """
        Rotate the camera by the given deltas.

        Args:
            delta_yaw: Change in horizontal rotation (degrees)
            delta_pitch: Change in vertical rotation (degrees)
        """
        self.yaw += delta_yaw
        self.pitch = clamp(
            self.pitch + delta_pitch,
            -self.config.camera.pitch_limit,
            self.config.camera.pitch_limit
        )

    def apply_to_opengl(self) -> None:
        """
        Apply camera transformation to OpenGL modelview matrix.

        This should be called after setting up the projection matrix
        and before rendering the scene.
        """
        glRotatef(-self.pitch, 1, 0, 0)  # Pitch around X-axis
        glRotatef(-self.yaw, 0, 1, 0)    # Yaw around Y-axis
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Camera(position={self.position}, "
                f"yaw={self.yaw:.1f}°, pitch={self.pitch:.1f}°)")
