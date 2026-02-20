"""
Player controller and movement system.

This module handles player physics, movement, and input processing.
"""

import numpy as np
import pygame
from core.camera import Camera
from utils.math_utils import normalize
import config


class Player:
    """
    Player character with first-person movement and camera control.

    Attributes:
        camera: Camera instance for view control
        velocity: Current velocity vector [x, y, z]
        on_ground: Whether player is standing on ground
    """

    def __init__(
        self,
        position: tuple[float, float, float] = (0.0, config.PLAYER_HEIGHT, 5.0),
        yaw: float = 0.0
    ):
        """
        Initialize the player.

        Args:
            position: Starting position [x, y, z]
            yaw: Starting horizontal rotation (degrees)
        """
        self.camera: Camera = Camera(position=position, yaw=yaw, pitch=0.0)
        self.velocity: np.ndarray = np.zeros(3, dtype=float)
        self.on_ground: bool = False

    @property
    def position(self) -> np.ndarray:
        """Get player position (alias for camera position)."""
        return self.camera.position

    @position.setter
    def position(self, value: np.ndarray) -> None:
        """Set player position."""
        self.camera.position = value

    def handle_mouse_motion(self, dx: int, dy: int) -> None:
        """
        Process mouse motion for camera rotation.

        Args:
            dx: Mouse X movement in pixels
            dy: Mouse Y movement in pixels
        """
        self.camera.rotate(
            dx * config.MOUSE_SENSITIVITY,
            dy * config.MOUSE_SENSITIVITY
        )

    def update(self, dt: float, keys_pressed) -> None:
        """
        Update player physics and movement.

        Args:
            dt: Time delta in seconds
            keys_pressed: Pygame key state array or dict with key states
        """
        # Calculate movement direction from input
        movement = self._calculate_movement_input(keys_pressed)

        # Apply horizontal movement (ignore Y component for now)
        self.velocity[0] = movement[0]
        self.velocity[2] = movement[2]

        # Apply gravity
        self.velocity[1] += config.GRAVITY * dt

        # Handle jump - support both dict and array
        jump_pressed = self._get_key_state(keys_pressed, pygame.K_SPACE)
        if jump_pressed and self.on_ground:
            self.velocity[1] = config.JUMP_SPEED
            self.on_ground = False

        # Update position
        self.position += self.velocity * dt

        # Ground collision
        self._handle_ground_collision()

    def _get_key_state(self, keys_pressed, key):
        """
        Safely get key state from either dict or array.
        
        Args:
            keys_pressed: Key state dict or array
            key: Key to check
            
        Returns:
            Boolean indicating if key is pressed
        """
        try:
            # Try dict-style access
            return keys_pressed.get(key, False)
        except AttributeError:
            # Fall back to array indexing
            try:
                return bool(keys_pressed[key])
            except (IndexError, KeyError):
                return False

    def _calculate_movement_input(self, keys_pressed) -> np.ndarray:
        """
        Calculate movement vector from keyboard input.

        Args:
            keys_pressed: Pygame key state array or dict with key states

        Returns:
            Movement vector [x, y, z]
        """
        movement = np.zeros(3)

        # Get camera direction vectors (flatten Y for ground movement)
        forward = self.camera.forward.copy()
        forward[1] = 0.0
        right = self.camera.right.copy()

        # WASD movement - works with both dict and array
        if self._get_key_state(keys_pressed, pygame.K_w):
            movement += forward
        if self._get_key_state(keys_pressed, pygame.K_s):
            movement -= forward
        if self._get_key_state(keys_pressed, pygame.K_d):
            movement += right
        if self._get_key_state(keys_pressed, pygame.K_a):
            movement -= right

        # Normalize and scale
        if np.linalg.norm(movement) > 0:
            movement = normalize(movement) * config.PLAYER_SPEED

        return movement

    def _handle_ground_collision(self) -> None:
        """Handle collision with ground plane."""
        floor_level = config.GROUND_LEVEL + config.PLAYER_HEIGHT

        if self.position[1] <= floor_level:
            self.position[1] = floor_level
            if self.velocity[1] < 0:
                self.velocity[1] = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

    def shoot_sphere(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculate spawn position and velocity for shooting a sphere.

        Returns:
            Tuple of (spawn_position, initial_velocity)
        """
        forward = self.camera.forward
        spawn_pos = self.position + forward * 1.2
        velocity = forward * config.SHOOT_SPEED
        return spawn_pos, velocity

    def get_crosshair_target(self, distance: float = config.CRATE_SPAWN_DISTANCE) -> np.ndarray:
        """
        Calculate target position at crosshair.

        Args:
            distance: Distance from player to target

        Returns:
            Target position [x, y, z]
        """
        forward = self.camera.forward
        target = self.position + forward * distance
        # Clamp to ground level minimum
        target[1] = max(target[1], config.GROUND_LEVEL + 0.5)
        return target

    def reset(self) -> None:
        """Reset player to starting position and state."""
        self.position[:] = [0.0, config.PLAYER_HEIGHT, 5.0]
        self.velocity[:] = 0.0
        self.camera.yaw = 0.0
        self.camera.pitch = 0.0
        self.on_ground = False

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Player(pos={self.position}, vel={self.velocity}, "
                f"on_ground={self.on_ground})")
