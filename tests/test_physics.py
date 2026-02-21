"""
Unit tests for PhysicsObject class.

Tests object initialization, physics updates, and collision handling.
"""

import pytest
import numpy as np
from physics.object import PhysicsObject
from config import GameConfig

@pytest.fixture
def test_config():
    return GameConfig()


class TestPhysicsObjectInitialization:
    """Tests for PhysicsObject initialization."""

    def setup_method(self):
        """Reset ID counter before each test."""
        PhysicsObject.reset_id_counter()

    def test_default_initialization(self, test_config):
        """Test creating object with default parameters."""
        obj = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0))
        assert obj.id == 1
        assert obj.shape == "sphere"
        assert obj.size == 0.4
        assert obj.mass == 1.0
        assert obj.alive is True
        assert obj.age == 0.0

    def test_custom_initialization(self, test_config):
        """Test creating object with custom parameters."""
        obj = PhysicsObject(
            test_config,
            pos=(1, 2, 3),
            vel=(4, 5, 6),
            shape="box",
            size=0.8,
            color=(1.0, 0.0, 0.0),
            mass=2.5
        )
        np.testing.assert_array_equal(obj.pos, [1, 2, 3])
        np.testing.assert_array_equal(obj.vel, [4, 5, 6])
        assert obj.shape == "box"
        assert obj.size == 0.8
        assert obj.mass == 2.5

    def test_unique_ids(self, test_config):
        """Test that objects get unique IDs."""
        obj1 = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0))
        obj2 = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0))
        obj3 = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0))
        assert obj1.id != obj2.id
        assert obj2.id != obj3.id
        assert obj1.id < obj2.id < obj3.id

    def test_box_rotation_initialized(self, test_config):
        """Test that boxes get rotation angles initialized."""
        obj = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0), shape="box")
        assert obj.rot is not None
        assert len(obj.rot) == 3
        assert obj.rot_vel is not None
        assert len(obj.rot_vel) == 3


class TestPhysicsObjectUpdate:
    """Tests for PhysicsObject update method."""

    def setup_method(self):
        """Reset ID counter before each test."""
        PhysicsObject.reset_id_counter()

    def test_update_applies_gravity(self, test_config):
        """Test that update applies gravity to velocity."""
        obj = PhysicsObject(test_config, pos=(0, 10, 0), vel=(0, 0, 0))
        initial_vel_y = obj.vel[1]
        obj.update(dt=0.1, other_objects=[])
        # Velocity should decrease (gravity is negative)
        assert obj.vel[1] < initial_vel_y

    def test_update_moves_object(self, test_config):
        """Test that update changes position based on velocity."""
        obj = PhysicsObject(test_config, pos=(0, 10, 0), vel=(5, 0, 0))
        initial_pos = obj.pos.copy()
        obj.update(dt=0.1, other_objects=[])
        # Position should have changed
        assert not np.array_equal(obj.pos, initial_pos)
        assert obj.pos[0] > initial_pos[0]

    def test_update_increments_age(self, test_config):
        """Test that update increments object age."""
        obj = PhysicsObject(test_config, pos=(0, 10, 0), vel=(0, 0, 0))
        assert obj.age == 0.0
        obj.update(dt=0.5, other_objects=[])
        assert obj.age == 0.5
        obj.update(dt=0.3, other_objects=[])
        assert abs(obj.age - 0.8) < 1e-7

    def test_update_ground_collision(self, test_config):
        """Test that objects collide with ground."""
        obj = PhysicsObject(test_config, pos=(0, 0.5, 0), vel=(0, -5, 0), size=1.0)
        obj.update(dt=0.1, other_objects=[])
        # Object should be on ground
        assert obj.on_ground
        # Position should be at ground level + radius
        assert abs(obj.pos[1] - (test_config.world.ground_level + obj.size)) < 0.01

    def test_update_kills_fallen_objects(self, test_config):
        """Test that objects below kill depth are marked as dead."""
        obj = PhysicsObject(test_config, pos=(0, -100, 0), vel=(0, 0, 0))
        obj.update(dt=0.1, other_objects=[])
        assert not obj.alive

    def test_update_kills_old_objects(self, test_config):
        """Test that very old objects are marked as dead."""
        obj = PhysicsObject(test_config, pos=(0, 10, 0), vel=(0, 0, 0))
        obj.age = test_config.gameplay.object_lifetime + 1
        obj.update(dt=0.1, other_objects=[])
        assert not obj.alive

    def test_box_rotation_updates(self, test_config):
        """Test that box rotation changes over time."""
        obj = PhysicsObject(test_config, pos=(0, 10, 0), vel=(0, 0, 0), shape="box")
        initial_rot = obj.rot.copy()
        obj.update(dt=0.1, other_objects=[])
        # Rotation should have changed
        assert not np.array_equal(obj.rot, initial_rot)

    def test_box_rotation_dampens_on_ground(self, test_config):
        """Test that box rotation velocity dampens when on ground."""
        obj = PhysicsObject(test_config, pos=(0, 1, 0), vel=(0, 0, 0), shape="box", size=1.0)
        # Force object to ground
        obj.pos[1] = obj.size
        obj.on_ground = True
        initial_rot_vel = obj.rot_vel.copy()

        # Update multiple times
        for _ in range(5):
            obj.update(dt=0.1, other_objects=[])

        # Rotation velocity should decrease
        assert np.linalg.norm(obj.rot_vel) < np.linalg.norm(initial_rot_vel)


class TestPhysicsObjectCollisions:
    """Tests for sphere-sphere collision handling."""

    def setup_method(self):
        """Reset ID counter before each test."""
        PhysicsObject.reset_id_counter()

    def test_sphere_sphere_collision_detection(self, test_config):
        """Test that sphere-sphere collisions are detected."""
        obj1 = PhysicsObject(test_config, pos=(0, 5, 0), vel=(1, 0, 0), shape="sphere", size=1.0)
        obj2 = PhysicsObject(test_config, pos=(1.5, 5, 0), vel=(-1, 0, 0), shape="sphere", size=1.0)

        initial_pos1 = obj1.pos.copy()
        initial_pos2 = obj2.pos.copy()

        obj1.update(dt=0.1, other_objects=[obj2])

        # Positions should have changed due to collision
        distance_before = np.linalg.norm(initial_pos1 - initial_pos2)
        distance_after = np.linalg.norm(obj1.pos - obj2.pos)

        # Objects should be pushed apart
        assert distance_after > distance_before

    def test_sphere_box_no_collision(self, test_config):
        """Test that spheres don't collide with boxes."""
        sphere = PhysicsObject(test_config, pos=(0, 5, 0), vel=(0, 0, 0), shape="sphere")
        box = PhysicsObject(test_config, pos=(0, 5, 0), vel=(0, 0, 0), shape="box")

        initial_pos = sphere.pos.copy()
        sphere.update(dt=0.1, other_objects=[box])

        # Position shouldn't change due to box (no sphere-box collision)
        # (only gravity and initial velocity)
        assert sphere.pos[1] < initial_pos[1]  # Gravity pulls down
        assert sphere.pos[0] == initial_pos[0]  # No horizontal change

    def test_sphere_ignores_self_collision(self, test_config):
        """Test that object doesn't collide with itself."""
        obj = PhysicsObject(test_config, pos=(0, 5, 0), vel=(0, 0, 0))
        initial_pos = obj.pos.copy()

        # Try to make it collide with itself
        obj.update(dt=0.1, other_objects=[obj])

        # Should only move due to gravity, not collision
        assert obj.pos[1] < initial_pos[1]


class TestPhysicsObjectRepr:
    """Tests for string representation."""

    def setup_method(self):
        """Reset ID counter before each test."""
        PhysicsObject.reset_id_counter()

    def test_repr_contains_key_info(self, test_config):
        """Test that repr contains essential object information."""
        obj = PhysicsObject(test_config, pos=(1, 2, 3), vel=(4, 5, 6), shape="box")
        repr_str = repr(obj)

        assert "PhysicsObject" in repr_str
        assert "box" in repr_str
        assert str(obj.id) in repr_str


class TestPhysicsObjectResetCounter:
    """Tests for ID counter reset functionality."""

    def setup_method(self):
        """Reset ID counter before each test."""
        PhysicsObject.reset_id_counter()

    def test_reset_counter_resets_ids(self, test_config):
        """Test that resetting counter starts IDs from 1 again."""
        obj1 = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0))
        assert obj1.id == 1

        obj2 = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0))
        assert obj2.id == 2

        PhysicsObject.reset_id_counter()

        obj3 = PhysicsObject(test_config, pos=(0, 0, 0), vel=(0, 0, 0))
        assert obj3.id == 1
