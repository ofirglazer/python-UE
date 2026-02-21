"""
Collision detection and response system.

This module handles all collision detection between physics objects,
including sphere-sphere, sphere-ground, and collision response.
"""

import numpy as np
from typing import Tuple, Optional

from utils.math_utils import vector_distance, normalize, dot_product
from config import GameConfig


def detect_sphere_sphere_collision(
    pos1: np.ndarray,
    radius1: float,
    pos2: np.ndarray,
    radius2: float
) -> Tuple[bool, Optional[np.ndarray], Optional[float]]:
    """
    Detect collision between two spheres.

    Args:
        pos1: Position of first sphere
        radius1: Radius of first sphere
        pos2: Position of second sphere
        radius2: Radius of second sphere

    Returns:
        Tuple of (is_colliding, collision_normal, penetration_depth)
        Returns (False, None, None) if no collision
    """
    diff = pos1 - pos2
    distance = np.linalg.norm(diff)
    min_distance = radius1 + radius2

    if distance < min_distance and distance > 1e-6:
        normal = diff / distance
        penetration = min_distance - distance
        return True, normal, penetration

    return False, None, None


def detect_sphere_ground_collision(
    pos: np.ndarray,
    radius: float,
    ground_level: float | None = None
) -> Tuple[bool, float]:
    """
    Detect collision between a sphere and the ground plane.

    Args:
        pos: Position of sphere center
        radius: Radius of sphere
        ground_level: Y-coordinate of ground plane

    Returns:
        Tuple of (is_colliding, penetration_depth)
    """
    if ground_level is None:
        ground_level = config.WorldConfig.ground_level

    bottom = pos[1] - radius
    if bottom <= ground_level:
        penetration = ground_level - bottom
        return True, penetration
    return False, 0.0


def resolve_sphere_sphere_collision(
    pos1: np.ndarray,
    vel1: np.ndarray,
    mass1: float,
    pos2: np.ndarray,
    vel2: np.ndarray,
    mass2: float,
    normal: np.ndarray,
    penetration: float,
    restitution: float | None = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Resolve collision between two spheres using impulse-based physics.

    Args:
        pos1: Position of first sphere
        vel1: Velocity of first sphere
        mass1: Mass of first sphere
        pos2: Position of second sphere
        vel2: Velocity of second sphere
        mass2: Mass of second sphere
        normal: Collision normal (from sphere2 to sphere1)
        penetration: Overlap distance
        restitution: Bounciness coefficient (0-1)

    Returns:
        Tuple of (new_pos1, new_vel1, new_pos2, new_vel2)
    """
    if restitution is None:
        restitution = config.PhysicsConfig.restitution

    # Separate objects
    new_pos1 = pos1 + normal * penetration * 0.5
    new_pos2 = pos2 - normal * penetration * 0.5

    # Calculate relative velocity
    relative_velocity = vel1 - vel2
    velocity_along_normal = dot_product(relative_velocity, normal)

    # Only resolve if objects are moving towards each other
    if velocity_along_normal < 0:
        # Calculate impulse
        impulse_magnitude = -(1 + restitution) * velocity_along_normal
        impulse_magnitude /= (1 / mass1 + 1 / mass2)

        impulse = impulse_magnitude * normal

        # Apply impulse
        new_vel1 = vel1 + (impulse / mass1)
        new_vel2 = vel2 - (impulse / mass2)
    else:
        new_vel1 = vel1.copy()
        new_vel2 = vel2.copy()

    return new_pos1, new_vel1, new_pos2, new_vel2


def resolve_ground_collision(
    pos: np.ndarray,
    vel: np.ndarray,
    radius: float,
    ground_level: float | None = None,
    restitution: float | None = None,
    friction: float | None = None
) -> Tuple[np.ndarray, np.ndarray, bool]:
    """
    Resolve collision with ground plane.

    Args:
        pos: Position of sphere center
        vel: Velocity vector
        radius: Sphere radius
        ground_level: Y-coordinate of ground plane
        restitution: Bounciness coefficient
        friction: Friction coefficient

    Returns:
        Tuple of (new_position, new_velocity, is_on_ground)
    """
    if ground_level is None:
        ground_level = config.WorldConfig.ground_level
    if restitution is None:
        restitution = config.PhysicsConfig.restitution
    if friction is None:
        friction = config.PhysicsConfig.friction

    new_pos = pos.copy()
    new_vel = vel.copy()
    is_on_ground = False

    floor = ground_level + radius

    if pos[1] <= floor:
        # Position correction
        new_pos[1] = floor

        # Bounce
        new_vel[1] = -vel[1] * restitution

        # Apply friction to horizontal movement
        new_vel[0] *= friction
        new_vel[2] *= friction

        is_on_ground = True

        # Stop small bounces
        if abs(new_vel[1]) < 0.3:
            new_vel[1] = 0.0

    return new_pos, new_vel, is_on_ground
