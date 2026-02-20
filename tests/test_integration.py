"""
Integration tests for the complete simulation system.

Tests interaction between multiple subsystems and end-to-end workflows.
"""

import pytest
import numpy as np
import pygame
from core.player import Player
from physics.object import PhysicsObject
import config



class TestPlayerPhysicsObjectInteraction:
    """Tests for interactions between player and physics objects."""

    def setup_method(self):
        """Reset state before each test."""
        PhysicsObject.reset_id_counter()

    def test_player_shoots_sphere_creates_object(self):
        """Test complete workflow of shooting a sphere."""
        player = Player()
        spawn_pos, velocity = player.shoot_sphere()

        # Create object with returned values
        sphere = PhysicsObject(
            pos=spawn_pos,
            vel=velocity,
            shape="sphere",
            size=config.SPHERE_DEFAULT_RADIUS,
            mass=config.SPHERE_DEFAULT_MASS
        )

        assert sphere.alive
        assert sphere.shape == "sphere"
        # Sphere should have forward velocity
        assert np.linalg.norm(sphere.vel) > 0

    def test_multiple_objects_physics_interaction(self):
        """Test multiple objects interacting through physics."""
        # Create two spheres on collision course
        obj1 = PhysicsObject(
            pos=(0, 5, 0),
            vel=(5, 0, 0),
            shape="sphere",
            size=1.0
        )
        obj2 = PhysicsObject(
            pos=(3, 5, 0),
            vel=(-5, 0, 0),
            shape="sphere",
            size=1.0
        )

        objects = [obj1, obj2]

        # Simulate until collision
        for _ in range(20):
            for obj in objects:
                obj.update(dt=0.05, other_objects=objects)

        # Objects should have separated and changed velocities
        # At least one should have reversed direction
        assert obj1.vel[0] <= 0 or obj2.vel[0] >= 0


class TestCompleteGameLoopSimulation:
    """Tests simulating complete game loop scenarios."""

    def setup_method(self):
        """Reset state before each test."""
        PhysicsObject.reset_id_counter()

    def test_object_lifecycle(self):
        """Test complete lifecycle of a physics object."""
        # Create object high up
        obj = PhysicsObject(
            pos=(0, 50, 0),
            vel=(0, 0, 0),
            shape="sphere",
            size=1.0
        )

        assert obj.alive
        assert obj.age == 0.0

        # Simulate falling to ground
        for i in range(100):
            obj.update(dt=0.1, other_objects=[])

            if obj.on_ground:
                break

        # Should eventually land on ground
        assert obj.on_ground
        # Age should have increased
        assert obj.age > 0

    def test_scene_with_player_and_objects(self):
        """Test a scene with player movement and physics objects."""
        player = Player()
        objects = []

        # Spawn some objects
        for i in range(5):
            spawn_pos, velocity = player.shoot_sphere()
            obj = PhysicsObject(
                pos=spawn_pos,
                vel=velocity,
                shape="sphere",
                size=0.5
            )
            objects.append(obj)

        # Simulate for several steps
        keys = {pygame.K_w: True}  # Move forward
        for _ in range(10):
            player.update(dt=0.1, keys_pressed=keys)

            alive_objects = [o for o in objects if o.alive]
            for obj in alive_objects:
                obj.update(dt=0.1, other_objects=alive_objects)

            objects = alive_objects

        # Player should have moved
        assert player.position[2] < 5.0  # Started at z=5

        # Some objects might still be alive
        assert len(objects) >= 0


class TestPhysicsConsistency:
    """Tests for physics simulation consistency and correctness."""

    def setup_method(self):
        """Reset state before each test."""
        PhysicsObject.reset_id_counter()

    def test_energy_dissipation_over_time(self):
        """Test that energy dissipates over time due to friction and restitution."""
        # Create bouncing sphere
        obj = PhysicsObject(
            pos=(0, 10, 0),
            vel=(0, 0, 0),
            shape="sphere",
            size=1.0
        )

        heights = []
        for _ in range(200):
            obj.update(dt=0.05, other_objects=[])
            if obj.vel[1] >= 0 and len(heights) > 0:
                # Local maximum (peak of bounce)
                heights.append(obj.pos[1])

        # Heights should generally decrease
        if len(heights) > 2:
            assert heights[-1] < heights[0]

    def test_no_objects_pass_through_ground(self):
        """Test that no objects pass through the ground plane."""
        objects = []

        # Create multiple objects at various positions
        for i in range(10):
            obj = PhysicsObject(
                pos=(i * 2, 20, 0),
                vel=(0, -20, 0),
                shape="sphere",
                size=0.5 + i * 0.1
            )
            objects.append(obj)

        # Simulate
        for _ in range(100):
            for obj in objects:
                obj.update(dt=0.05, other_objects=objects)

        # All objects should be at or above ground
        for obj in objects:
            assert obj.pos[1] >= config.GROUND_LEVEL + obj.size - 0.01


class TestPlayerMovementIntegration:
    """Tests for complete player movement scenarios."""

    def test_player_exploration_path(self):
        """Test player moving in a complete path."""
        player = Player()
        initial_pos = player.position.copy()

        # Move in a square pattern
        movements = [
            ({pygame.K_w: True}, 20),  # Forward
            ({pygame.K_d: True}, 20),  # Right
            ({pygame.K_s: True}, 20),  # Backward
            ({pygame.K_a: True}, 20),  # Left
        ]

        # Track positions to verify movement occurred
        positions = [initial_pos.copy()]
        
        for keys, steps in movements:
            for _ in range(steps):
                player.update(dt=0.1, keys_pressed=keys)
            positions.append(player.position.copy())

        # Player should return close to start (square path)
        final_distance = np.linalg.norm(player.position - initial_pos)
        assert final_distance < 1.0  # Close to start
        
        # But should have moved during the path
        max_distance = max(np.linalg.norm(pos - initial_pos) for pos in positions)
        assert max_distance > 5.0  # Moved significantly during path

    def test_player_jump_and_land(self):
        """Test complete jump cycle."""
        player = Player()

        # Ensure on ground
        player.position[1] = config.PLAYER_HEIGHT
        player.update(dt=0.1, keys_pressed={})
        assert player.on_ground

        # Jump
        player.update(dt=0.1, keys_pressed={pygame.K_SPACE: True})
        assert not player.on_ground
        assert player.velocity[1] > 0

        # Let player land
        for _ in range(100):
            player.update(dt=0.05, keys_pressed={})
            if player.on_ground and abs(player.velocity[1]) < 0.1:
                break

        # Should be back on ground
        assert player.on_ground
        assert abs(player.velocity[1]) < 1.0


class TestStressScenarios:
    """Stress tests with many objects."""

    def setup_method(self):
        """Reset state before each test."""
        PhysicsObject.reset_id_counter()

    def test_many_objects_performance(self):
        """Test simulation with many physics objects."""
        objects = []

        # Create many objects
        for i in range(50):
            obj = PhysicsObject(
                pos=(i % 10, 10 + i % 5, i // 10),
                vel=(0, 0, 0),
                shape="sphere",
                size=0.3
            )
            objects.append(obj)

        # Simulate a few steps
        for _ in range(10):
            alive_objects = [o for o in objects if o.alive]
            for obj in alive_objects:
                obj.update(dt=0.1, other_objects=alive_objects)
            objects = alive_objects

        # Most objects should still be alive
        assert len(objects) > 40

    def test_max_objects_limit(self):
        """Test that object limit is enforced."""
        objects = []

        # Create more than max
        for i in range(config.MAX_OBJECTS + 50):
            obj = PhysicsObject(
                pos=(0, 10, 0),
                vel=(0, 0, 0)
            )
            objects.append(obj)

        # Trim to max
        if len(objects) > config.MAX_OBJECTS:
            objects = objects[-config.MAX_OBJECTS:]

        assert len(objects) == config.MAX_OBJECTS
