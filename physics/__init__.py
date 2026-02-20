"""Physics simulation modules for the UE-inspired simulation."""

from .object import PhysicsObject
from .collision import (
    detect_sphere_sphere_collision,
    detect_sphere_ground_collision,
    resolve_sphere_sphere_collision,
    resolve_ground_collision,
)

__all__ = [
    'PhysicsObject',
    'detect_sphere_sphere_collision',
    'detect_sphere_ground_collision',
    'resolve_sphere_sphere_collision',
    'resolve_ground_collision',
]
