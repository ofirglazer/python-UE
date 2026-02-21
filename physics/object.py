"""
Physics object representation and simulation.

This module defines the PhysicsObject class which represents dynamic objects
in the simulation with position, velocity, shape, and physical properties.
"""

import numpy as np
import random
from typing import List, Tuple, Literal
from physics.collision import (
    detect_sphere_sphere_collision,
    detect_sphere_ground_collision,
    resolve_sphere_sphere_collision,
    resolve_ground_collision,
)
from config import GameConfig


ShapeType = Literal["sphere", "box"]


class PhysicsObject:
    """
    Represents a dynamic physics object in the simulation.

    Attributes:
        id: Unique identifier for this object
        pos: Position vector [x, y, z]
        vel: Velocity vector [x, y, z]
        shape: Object shape ("sphere" or "box")
        size: Radius (sphere) or half-extent (box)
        color: RGB color tuple
        mass: Mass in kilograms
        on_ground: Whether object is resting on ground
        alive: Whether object should continue existing
        age: Time since creation in seconds
        rot: Rotation angles for boxes [x, y, z] in degrees
        rot_vel: Angular velocity for boxes [x, y, z] in deg/s
    """

    _uid_counter: int = 0

    def __init__(
        self,
        config: GameConfig,
        pos: Tuple[float, float, float],
        vel: Tuple[float, float, float],
        shape: ShapeType = "sphere",
        size: float = 0.4,
        color: Tuple[float, float, float] = (0.9, 0.3, 0.2),
        mass: float = 1.0
    ):
        """
        Initialize a physics object.

        Args:
            pos: Initial position [x, y, z]
            vel: Initial velocity [x, y, z]
            shape: Object shape type
            size: Radius or half-extent
            color: RGB color (0-1 range)
            mass: Mass in kilograms
        """
        PhysicsObject._uid_counter += 1
        self.config = config
        self.id: int = PhysicsObject._uid_counter
        self.pos: np.ndarray = np.array(pos, dtype=float)
        self.vel: np.ndarray = np.array(vel, dtype=float)
        self.shape: ShapeType = shape
        self.size: float = size
        self.color: Tuple[float, float, float] = color
        self.mass: float = mass
        self.on_ground: bool = False
        self.alive: bool = True
        self.age: float = 0.0

        # Rotation for boxes
        self.rot: np.ndarray = np.array([
            random.uniform(0, 360),
            random.uniform(0, 360),
            random.uniform(0, 360)
        ], dtype=float)

        self.rot_vel: np.ndarray = np.array([
            random.uniform(-90, 90),
            random.uniform(-90, 90),
            random.uniform(-90, 90)
        ], dtype=float)

    def update(self, dt: float, other_objects: List['PhysicsObject']) -> None:
        """
        Update object physics for one timestep.

        Args:
            dt: Time delta in seconds
            other_objects: List of other physics objects for collision detection
        """
        self.age += dt

        # Destroy objects that are too old or fell off the world
        if self.pos[1] < self.config.gameplay.world_kill_depth or self.age > self.config.gameplay.object_lifetime:
            self.alive = False
            return

        # Apply gravity
        self.vel[1] += self.config.physics.gravity * dt

        # Update position
        self.pos += self.vel * dt

        # Update rotation for boxes
        if self.shape == "box":
            self.rot += self.rot_vel * dt

            # Dampen rotation when on ground
            if self.on_ground:
                self.rot_vel *= 0.92

        # Ground collision
        self.pos, self.vel, self.on_ground = resolve_ground_collision(
            self.config, self.pos, self.vel, self.size
        )

        # Sphere-sphere collisions
        if self.shape == "sphere":
            self._handle_sphere_collisions(other_objects)

    def _handle_sphere_collisions(self, other_objects: List['PhysicsObject']) -> None:
        """
        Handle collisions with other sphere objects.

        Args:
            other_objects: List of other physics objects
        """
        for other in other_objects:
            # Skip self and non-spheres
            if other.id == self.id or other.shape != "sphere":
                continue

            # Detect collision
            is_colliding, normal, penetration = detect_sphere_sphere_collision(
                self.pos, self.size, other.pos, other.size
            )

            if is_colliding and normal is not None and penetration is not None:
                # Resolve collision
                new_pos1, new_vel1, new_pos2, new_vel2 = resolve_sphere_sphere_collision(
                    self.config, self.pos, self.vel, self.mass,
                    other.pos, other.vel, other.mass,
                    normal, penetration
                )

                # Update both objects
                self.pos = new_pos1
                self.vel = new_vel1
                other.pos = new_pos2
                other.vel = new_vel2

    @classmethod
    def reset_id_counter(cls) -> None:
        """Reset the unique ID counter (useful for testing)."""
        cls._uid_counter = 0

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"PhysicsObject(id={self.id}, shape={self.shape}, "
                f"pos={self.pos}, vel={self.vel})")
