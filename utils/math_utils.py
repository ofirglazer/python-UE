"""
Mathematical utility functions for the simulation.

This module provides vector operations and mathematical helpers used throughout
the physics and rendering systems.
"""

import numpy as np
from typing import Union


def normalize(vector: np.ndarray) -> np.ndarray:
    """
    Normalize a vector to unit length.

    Args:
        vector: Input vector (any dimension)

    Returns:
        Normalized vector (unit length), or zero vector if input is zero
    """
    norm = np.linalg.norm(vector)
    if norm > 1e-8:
        return vector / norm
    return vector


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between minimum and maximum bounds.

    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Clamped value
    """
    return max(min_value, min(max_value, value))


def vector_length(vector: np.ndarray) -> float:
    """
    Calculate the length (magnitude) of a vector.

    Args:
        vector: Input vector

    Returns:
        Length of the vector
    """
    return float(np.linalg.norm(vector))


def vector_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        vec1: First position vector
        vec2: Second position vector

    Returns:
        Distance between the two points
    """
    return vector_length(vec1 - vec2)


def lerp(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        t: Interpolation factor (0-1)

    Returns:
        Interpolated value
    """
    return start + (end - start) * t


def dot_product(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate dot product of two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Dot product (scalar)
    """
    return float(np.dot(vec1, vec2))


def safe_divide(numerator: Union[float, np.ndarray],
                denominator: Union[float, np.ndarray],
                default: Union[float, np.ndarray] = 0.0) -> Union[float, np.ndarray]:
    """
    Safely divide two numbers, returning default if denominator is zero.

    Args:
        numerator: Numerator value(s)
        denominator: Denominator value(s)
        default: Value to return if division by zero occurs

    Returns:
        Result of division, or default value
    """
    if isinstance(denominator, np.ndarray):
        mask = np.abs(denominator) > 1e-10
        result = np.where(mask, numerator / denominator, default)
        return result
    else:
        if abs(denominator) > 1e-10:
            return numerator / denominator
        return default
