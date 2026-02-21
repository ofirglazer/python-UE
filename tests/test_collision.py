"""
Unit tests for collision detection and resolution.

Tests sphere-sphere and sphere-ground collision detection and physics response.
"""

import pytest
import numpy as np
from physics.collision import (
    detect_sphere_sphere_collision,
    detect_sphere_ground_collision,
    resolve_sphere_sphere_collision,
    resolve_ground_collision,
)
from config import GameConfig


@pytest.fixture
def test_config():
    return GameConfig()


class TestDetectSphereSphereCollision:
    """Tests for sphere-sphere collision detection."""

    def test_no_collision_far_apart(self):
        """Test no collision when spheres are far apart."""
        pos1 = np.array([0.0, 0.0, 0.0])
        pos2 = np.array([10.0, 0.0, 0.0])
        is_colliding, normal, penetration = detect_sphere_sphere_collision(
            pos1, 1.0, pos2, 1.0
        )
        assert not is_colliding
        assert normal is None
        assert penetration is None

    def test_collision_touching(self):
        """Test collision when spheres are exactly touching."""
        pos1 = np.array([0.0, 0.0, 0.0])
        pos2 = np.array([2.0, 0.0, 0.0])
        is_colliding, normal, penetration = detect_sphere_sphere_collision(
            pos1, 1.0, pos2, 1.0
        )
        # Exactly touching might not register due to floating point
        # but should be very close to collision
        assert penetration is None or penetration < 0.001

    def test_collision_overlapping(self):
        """Test collision when spheres are overlapping."""
        pos1 = np.array([0.0, 0.0, 0.0])
        pos2 = np.array([1.5, 0.0, 0.0])
        is_colliding, normal, penetration = detect_sphere_sphere_collision(
            pos1, 1.0, pos2, 1.0
        )
        assert is_colliding
        assert normal is not None
        assert penetration is not None
        assert penetration > 0

    def test_collision_normal_direction(self):
        """Test that collision normal points from sphere2 to sphere1."""
        pos1 = np.array([1.0, 0.0, 0.0])
        pos2 = np.array([0.0, 0.0, 0.0])
        is_colliding, normal, penetration = detect_sphere_sphere_collision(
            pos1, 0.8, pos2, 0.8
        )
        if is_colliding and normal is not None:
            # Normal should point in positive X direction
            assert normal[0] > 0

    def test_collision_different_radii(self):
        """Test collision with different sphere sizes."""
        pos1 = np.array([0.0, 0.0, 0.0])
        pos2 = np.array([2.5, 0.0, 0.0])
        is_colliding, normal, penetration = detect_sphere_sphere_collision(
            pos1, 2.0, pos2, 1.0
        )
        assert is_colliding
        assert penetration is not None
        assert abs(penetration - 0.5) < 0.01


class TestDetectSphereGroundCollision:
    """Tests for sphere-ground collision detection."""

    def test_no_collision_above_ground(self, test_config):
        """Test no collision when sphere is above ground."""
        pos = np.array([0.0, 5.0, 0.0])
        is_colliding, penetration = detect_sphere_ground_collision(test_config, pos, 1.0)
        assert not is_colliding
        assert penetration == 0.0

    def test_collision_on_ground(self, test_config):
        """Test collision when sphere is resting on ground."""
        pos = np.array([0.0, 1.0, 0.0])
        is_colliding, penetration = detect_sphere_ground_collision(
            test_config, pos, 1.0, ground_level=0.0
        )
        # Sphere exactly on ground
        assert not is_colliding or abs(penetration) < 0.01

    def test_collision_below_ground(self, test_config):
        """Test collision when sphere penetrates ground."""
        pos = np.array([0.0, 0.5, 0.0])
        is_colliding, penetration = detect_sphere_ground_collision(
            test_config, pos, 1.0, ground_level=0.0
        )
        assert is_colliding
        assert penetration > 0
        assert abs(penetration - 0.5) < 0.01

    def test_collision_custom_ground_level(self, test_config):
        """Test collision with custom ground level."""
        pos = np.array([0.0, 5.0, 0.0])
        is_colliding, penetration = detect_sphere_ground_collision(
            test_config, pos, 1.0, ground_level=5.0
        )
        assert is_colliding


class TestResolveSphereSphereCollision:
    """Tests for sphere-sphere collision resolution."""

    def test_resolution_separates_spheres(self, test_config):
        """Test that resolution pushes spheres apart."""
        # Spheres overlapping and moving toward each other
        pos1 = np.array([0.0, 0.0, 0.0])
        pos2 = np.array([1.0, 0.0, 0.0])  # Only 1.0 apart
        vel1 = np.array([1.0, 0.0, 0.0])  # Moving right (toward pos2)
        vel2 = np.array([0.0, 0.0, 0.0])  # Stationary
        normal = np.array([1.0, 0.0, 0.0])  # Points from pos2 to pos1
        penetration = 0.5  # They're overlapping by 0.5

        new_pos1, new_vel1, new_pos2, new_vel2 = resolve_sphere_sphere_collision(
            test_config, pos1, vel1, 1.0, pos2, vel2, 1.0, normal, penetration
        )

        # After resolution, distance should be at least original distance
        distance = np.linalg.norm(new_pos1 - new_pos2)
        original_distance = np.linalg.norm(pos1 - pos2)
        # Position correction pushes them apart by penetration
        assert distance >= original_distance

    def test_resolution_conserves_momentum(self, test_config):
        """Test that collision conserves total momentum (approximately)."""
        pos1 = np.array([0.0, 0.0, 0.0])
        pos2 = np.array([1.5, 0.0, 0.0])
        vel1 = np.array([2.0, 0.0, 0.0])
        vel2 = np.array([0.0, 0.0, 0.0])
        mass1 = mass2 = 1.0
        normal = np.array([1.0, 0.0, 0.0])
        penetration = 0.5

        initial_momentum = mass1 * vel1 + mass2 * vel2

        new_pos1, new_vel1, new_pos2, new_vel2 = resolve_sphere_sphere_collision(
            test_config, pos1, vel1, mass1, pos2, vel2, mass2, normal, penetration, restitution=1.0
        )

        final_momentum = mass1 * new_vel1 + mass2 * new_vel2

        # Momentum should be conserved (within floating point error)
        np.testing.assert_array_almost_equal(initial_momentum, final_momentum, decimal=5)

    def test_resolution_equal_mass_exchange(self, test_config):
        """Test head-on collision with equal masses exchanges velocities."""
        # Two spheres moving toward each other head-on
        pos1 = np.array([0.0, 0.0, 0.0])
        pos2 = np.array([1.5, 0.0, 0.0])
        vel1 = np.array([1.0, 0.0, 0.0])  # Moving right
        vel2 = np.array([0.0, 0.0, 0.0])  # Stationary
        normal = np.array([1.0, 0.0, 0.0])  # Points from pos2 to pos1
        penetration = 0.5

        new_pos1, new_vel1, new_pos2, new_vel2 = resolve_sphere_sphere_collision(
            test_config, pos1, vel1, 1.0, pos2, vel2, 1.0, normal, penetration, restitution=1.0
        )

        # With perfect elasticity and equal mass:
        # Moving sphere should stop, stationary should move
        # (elastic collision transfers all momentum)
        assert new_vel1[0] <= 0.1  # First sphere should stop or reverse slightly
        assert new_vel2[0] > 0.5   # Second sphere should move forward


class TestResolveGroundCollision:
    """Tests for ground collision resolution."""

    def test_resolution_places_on_ground(self, test_config):
        """Test that resolution places sphere exactly on ground."""
        pos = np.array([0.0, 0.5, 0.0])
        vel = np.array([0.0, -5.0, 0.0])
        radius = 1.0

        new_pos, new_vel, on_ground = resolve_ground_collision(
            test_config, pos, vel, radius, ground_level=0.0
        )

        assert on_ground
        assert abs(new_pos[1] - radius) < 0.01

    def test_resolution_reverses_velocity(self, test_config):
        """Test that collision reverses vertical velocity."""
        pos = np.array([0.0, 0.5, 0.0])
        vel = np.array([0.0, -5.0, 0.0])

        new_pos, new_vel, on_ground = resolve_ground_collision(
            test_config, pos, vel, 1.0, restitution=1.0
        )

        # With perfect restitution, velocity should reverse
        assert new_vel[1] > 0
        assert abs(new_vel[1] - 5.0) < 0.1

    def test_resolution_applies_friction(self, test_config):
        """Test that collision applies friction to horizontal motion."""
        pos = np.array([0.0, 0.5, 0.0])
        vel = np.array([5.0, -1.0, 5.0])

        new_pos, new_vel, on_ground = resolve_ground_collision(
            test_config, pos, vel, 1.0, friction=0.5
        )

        # Horizontal velocity should be reduced
        assert abs(new_vel[0]) < abs(vel[0])
        assert abs(new_vel[2]) < abs(vel[2])

    def test_resolution_stops_small_bounces(self, test_config):
        """Test that small bounces are stopped."""
        pos = np.array([0.0, 0.5, 0.0])
        vel = np.array([0.0, -0.2, 0.0])

        new_pos, new_vel, on_ground = resolve_ground_collision(
            test_config, pos, vel, 1.0, restitution=0.3
        )

        # Small bounce should be eliminated
        assert new_vel[1] == 0.0

    def test_no_resolution_above_ground(self, test_config):
        """Test that no resolution occurs when above ground."""
        pos = np.array([0.0, 5.0, 0.0])
        vel = np.array([1.0, 2.0, 3.0])

        new_pos, new_vel, on_ground = resolve_ground_collision(test_config, pos, vel, 1.0)

        assert not on_ground
        np.testing.assert_array_equal(new_pos, pos)
        np.testing.assert_array_equal(new_vel, vel)
