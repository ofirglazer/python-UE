"""
UE-Inspired 3D Simulation

A Python-based 3D physics simulation inspired by Unreal Engine,
featuring first-person controls, physics objects, and real-time rendering.
"""

__version__ = "1.0.0"
__author__ = "Ofir Glazer"

from core import Camera, Player, SceneRenderer
from physics import PhysicsObject
from rendering import HUD

__all__ = [
    'Camera',
    'Player',
    'SceneRenderer',
    'PhysicsObject',
    'HUD',
]
