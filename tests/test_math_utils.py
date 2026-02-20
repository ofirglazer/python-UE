"""
Unit tests for mathematical utility functions.

Tests vector operations and mathematical helpers used throughout the simulation.
"""

import pytest
import numpy as np
from utils.math_utils import (
    normalize,
    clamp,
    vector_length,
    vector_distance,
    lerp,
    dot_product,
    safe_divide,
)


class TestNormalize:
    """Tests for the normalize function."""

    def test_normalize_unit_vector(self):
        """Test normalizing an already unit vector."""
        vec = np.array([1.0, 0.0, 0.0])
        result = normalize(vec)
        np.testing.assert_array_almost_equal(result, vec)

    def test_normalize_non_unit_vector(self):
        """Test normalizing a non-unit vector."""
        vec = np.array([3.0, 4.0, 0.0])
        result = normalize(vec)
        expected = np.array([0.6, 0.8, 0.0])
        np.testing.assert_array_almost_equal(result, expected)

    def test_normalize_zero_vector(self):
        """Test normalizing a zero vector returns zero vector."""
        vec = np.array([0.0, 0.0, 0.0])
        result = normalize(vec)
        np.testing.assert_array_almost_equal(result, vec)

    def test_normalize_negative_values(self):
        """Test normalizing a vector with negative components."""
        vec = np.array([-1.0, -1.0, 0.0])
        result = normalize(vec)
        expected_length = np.linalg.norm(result)
        assert abs(expected_length - 1.0) < 1e-7


class TestClamp:
    """Tests for the clamp function."""

    def test_clamp_within_range(self):
        """Test clamping a value already within range."""
        assert clamp(5.0, 0.0, 10.0) == 5.0

    def test_clamp_below_minimum(self):
        """Test clamping a value below minimum."""
        assert clamp(-5.0, 0.0, 10.0) == 0.0

    def test_clamp_above_maximum(self):
        """Test clamping a value above maximum."""
        assert clamp(15.0, 0.0, 10.0) == 10.0

    def test_clamp_at_boundaries(self):
        """Test clamping at exact boundaries."""
        assert clamp(0.0, 0.0, 10.0) == 0.0
        assert clamp(10.0, 0.0, 10.0) == 10.0

    def test_clamp_negative_range(self):
        """Test clamping with negative range."""
        assert clamp(-5.0, -10.0, -1.0) == -5.0
        assert clamp(-15.0, -10.0, -1.0) == -10.0


class TestVectorLength:
    """Tests for the vector_length function."""

    def test_length_unit_vector(self):
        """Test length of a unit vector."""
        vec = np.array([1.0, 0.0, 0.0])
        assert abs(vector_length(vec) - 1.0) < 1e-7

    def test_length_zero_vector(self):
        """Test length of a zero vector."""
        vec = np.array([0.0, 0.0, 0.0])
        assert vector_length(vec) == 0.0

    def test_length_3_4_5_triangle(self):
        """Test length using 3-4-5 triangle."""
        vec = np.array([3.0, 4.0, 0.0])
        assert abs(vector_length(vec) - 5.0) < 1e-7

    def test_length_negative_components(self):
        """Test length with negative components."""
        vec = np.array([-3.0, -4.0, 0.0])
        assert abs(vector_length(vec) - 5.0) < 1e-7


class TestVectorDistance:
    """Tests for the vector_distance function."""

    def test_distance_same_point(self):
        """Test distance between identical points."""
        vec1 = np.array([1.0, 2.0, 3.0])
        vec2 = np.array([1.0, 2.0, 3.0])
        assert vector_distance(vec1, vec2) == 0.0

    def test_distance_unit_apart(self):
        """Test distance of one unit."""
        vec1 = np.array([0.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])
        assert abs(vector_distance(vec1, vec2) - 1.0) < 1e-7

    def test_distance_3d(self):
        """Test distance in 3D space."""
        vec1 = np.array([0.0, 0.0, 0.0])
        vec2 = np.array([1.0, 1.0, 1.0])
        expected = np.sqrt(3.0)
        assert abs(vector_distance(vec1, vec2) - expected) < 1e-7


class TestLerp:
    """Tests for the lerp (linear interpolation) function."""

    def test_lerp_start(self):
        """Test lerp at start (t=0)."""
        assert lerp(0.0, 10.0, 0.0) == 0.0

    def test_lerp_end(self):
        """Test lerp at end (t=1)."""
        assert lerp(0.0, 10.0, 1.0) == 10.0

    def test_lerp_middle(self):
        """Test lerp at middle (t=0.5)."""
        assert lerp(0.0, 10.0, 0.5) == 5.0

    def test_lerp_negative_range(self):
        """Test lerp with negative range."""
        assert lerp(-10.0, 10.0, 0.5) == 0.0

    def test_lerp_extrapolate(self):
        """Test lerp with t outside [0,1]."""
        assert lerp(0.0, 10.0, 1.5) == 15.0


class TestDotProduct:
    """Tests for the dot_product function."""

    def test_dot_orthogonal_vectors(self):
        """Test dot product of orthogonal vectors."""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([0.0, 1.0, 0.0])
        assert abs(dot_product(vec1, vec2)) < 1e-7

    def test_dot_parallel_vectors(self):
        """Test dot product of parallel vectors."""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([2.0, 0.0, 0.0])
        assert abs(dot_product(vec1, vec2) - 2.0) < 1e-7

    def test_dot_opposite_vectors(self):
        """Test dot product of opposite vectors."""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([-1.0, 0.0, 0.0])
        assert abs(dot_product(vec1, vec2) + 1.0) < 1e-7


class TestSafeDivide:
    """Tests for the safe_divide function."""

    def test_safe_divide_normal(self):
        """Test safe division with non-zero denominator."""
        assert safe_divide(10.0, 2.0) == 5.0

    def test_safe_divide_by_zero(self):
        """Test safe division by zero returns default."""
        assert safe_divide(10.0, 0.0, default=0.0) == 0.0

    def test_safe_divide_custom_default(self):
        """Test safe division with custom default."""
        assert safe_divide(10.0, 0.0, default=99.0) == 99.0

    def test_safe_divide_array(self):
        """Test safe division with numpy arrays."""
        numerator = np.array([10.0, 20.0, 30.0])
        denominator = np.array([2.0, 0.0, 5.0])
        result = safe_divide(numerator, denominator, default=0.0)
        expected = np.array([5.0, 0.0, 6.0])
        np.testing.assert_array_almost_equal(result, expected)

    def test_safe_divide_very_small_denominator(self):
        """Test safe division with very small denominator."""
        result = safe_divide(10.0, 1e-12, default=0.0)
        assert result == 0.0
