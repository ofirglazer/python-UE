"""
Unit tests for Player class.

Tests player movement, camera control, and interaction mechanics.
"""

import pytest
import numpy as np
import pygame
from core.player import Player
from config import GameConfig


@pytest.fixture
def test_config():
    return GameConfig()


class TestPlayerInitialization:
    """Tests for Player initialization."""

    def test_default_initialization(self, test_config):
        """Test creating player with default parameters."""
        player = Player(test_config)
        assert player.camera is not None
        assert len(player.velocity) == 3
        assert not player.on_ground

    def test_custom_initialization(self, test_config):
        """Test creating player with custom position and yaw."""
        player = Player(test_config, position=(10, 20, 30), yaw=45.0)
        np.testing.assert_array_almost_equal(player.position, [10, 20, 30])
        assert player.camera.yaw == 45.0

    def test_initial_velocity_zero(self, test_config):
        """Test that player starts with zero velocity."""
        player = Player(test_config)
        np.testing.assert_array_equal(player.velocity, [0, 0, 0])


class TestPlayerMouseMotion:
    """Tests for mouse-based camera control."""

    def test_mouse_motion_changes_yaw(self, test_config):
        """Test that horizontal mouse motion changes yaw."""
        player = Player(test_config)
        initial_yaw = player.camera.yaw
        player.handle_mouse_motion(dx=100, dy=0)
        assert player.camera.yaw != initial_yaw

    def test_mouse_motion_changes_pitch(self, test_config):
        """Test that vertical mouse motion changes pitch."""
        player = Player(test_config)
        initial_pitch = player.camera.pitch
        player.handle_mouse_motion(dx=0, dy=100)
        assert player.camera.pitch != initial_pitch

    def test_mouse_motion_both_axes(self, test_config):
        """Test mouse motion affecting both yaw and pitch."""
        player = Player(test_config)
        initial_yaw = player.camera.yaw
        initial_pitch = player.camera.pitch
        player.handle_mouse_motion(dx=50, dy=50)
        assert player.camera.yaw != initial_yaw
        assert player.camera.pitch != initial_pitch

    def test_pitch_clamping(self, test_config):
        """Test that pitch is clamped to valid range."""
        player = Player(test_config)
        # Try to pitch way up
        player.handle_mouse_motion(dx=0, dy=10000)
        assert player.camera.pitch <= test_config.camera.pitch_limit
        assert player.camera.pitch >= -test_config.camera.pitch_limit


class TestPlayerMovement:
    """Tests for keyboard-based player movement."""

    def test_forward_movement(self, test_config):
        """Test moving forward with W key."""
        player = Player(test_config)
        keys = {pygame.K_w: True}
        player.update(dt=0.1, keys_pressed=keys)
        # Should have moved (velocity applied)
        assert player.velocity[0] != 0 or player.velocity[2] != 0

    def test_backward_movement(self, test_config):
        """Test moving backward with S key."""
        player = Player(test_config)
        player.camera.yaw = 0  # Face forward
        keys_forward = {pygame.K_w: True}
        player.update(dt=0.1, keys_pressed=keys_forward)
        pos_forward = player.position.copy()

        player2 = Player(test_config)
        player2.camera.yaw = 0
        keys_backward = {pygame.K_s: True}
        player2.update(dt=0.1, keys_pressed=keys_backward)
        pos_backward = player2.position.copy()

        # Movement directions should be opposite (roughly)
        assert pos_forward[2] < pos_backward[2]

    def test_strafe_movement(self, test_config):
        """Test strafing with A/D keys."""
        player = Player(test_config)
        keys = {pygame.K_d: True}
        initial_pos = player.position.copy()
        player.update(dt=0.1, keys_pressed=keys)
        # Should have moved sideways
        assert not np.array_equal(player.position, initial_pos)

    def test_diagonal_movement_normalized(self, test_config):
        """Test that diagonal movement is normalized to prevent faster speed."""
        player1 = Player(test_config)
        player2 = Player(test_config)

        # Move forward only
        keys_forward = {pygame.K_w: True}
        player1.update(dt=0.1, keys_pressed=keys_forward)
        forward_speed = np.linalg.norm(player1.velocity[:3])

        # Move diagonally (forward + right)
        keys_diagonal = {pygame.K_w: True, pygame.K_d: True}
        player2.update(dt=0.1, keys_pressed=keys_diagonal)
        diagonal_speed = np.linalg.norm(player2.velocity[:3])

        # Speeds should be roughly equal (normalized movement)
        assert abs(forward_speed - diagonal_speed) < 0.1

    def test_no_movement_no_keys(self, test_config):
        """Test that player doesn't move horizontally without input."""
        player = Player(test_config)
        player.position[1] = 100  # High up to avoid ground collision
        keys = {}
        initial_x = player.position[0]
        initial_z = player.position[2]
        player.update(dt=0.1, keys_pressed=keys)
        # X and Z shouldn't change (Y will due to gravity)
        assert abs(player.position[0] - initial_x) < 0.01
        assert abs(player.position[2] - initial_z) < 0.01


class TestPlayerJump:
    """Tests for jumping mechanics."""

    def test_jump_when_on_ground(self, test_config):
        """Test that player can jump when on ground."""
        player = Player(test_config)
        player.position[1] = test_config.player.height
        player.on_ground = True
        keys = {pygame.K_SPACE: True}

        initial_vel_y = player.velocity[1]
        player.update(dt=0.01, keys_pressed=keys)

        # Velocity should have increased upward
        assert player.velocity[1] > initial_vel_y

    def test_no_jump_in_air(self, test_config):
        """Test that player cannot jump while in air."""
        player = Player(test_config)
        player.position[1] = 100
        player.on_ground = False
        keys = {pygame.K_SPACE: True}

        initial_vel_y = player.velocity[1]
        player.update(dt=0.01, keys_pressed=keys)

        # Velocity shouldn't jump (only gravity applied)
        assert player.velocity[1] <= initial_vel_y


class TestPlayerGravity:
    """Tests for gravity effects on player."""

    def test_gravity_pulls_down(self, test_config):
        """Test that gravity decreases vertical velocity."""
        player = Player(test_config)
        player.position[1] = 100  # High up
        initial_vel_y = player.velocity[1]
        player.update(dt=0.1, keys_pressed={})
        # Velocity should decrease (become more negative)
        assert player.velocity[1] < initial_vel_y

    def test_falls_when_in_air(self, test_config):
        """Test that player falls when not on ground."""
        player = Player(test_config)
        player.position[1] = 100
        initial_y = player.position[1]
        player.update(dt=0.1, keys_pressed={})
        # Should have fallen
        assert player.position[1] < initial_y


class TestPlayerGroundCollision:
    """Tests for ground collision."""

    def test_stops_at_ground(self, test_config):
        """Test that player stops at ground level."""
        player = Player(test_config)
        player.position[1] = test_config.player.height - 0.5
        player.velocity[1] = -10

        # Update multiple times to ensure settling
        for _ in range(10):
            player.update(dt=0.1, keys_pressed={})

        # Should be exactly at ground level
        expected_height = test_config.world.ground_level + test_config.player.height
        assert abs(player.position[1] - expected_height) < 0.01

    def test_on_ground_flag_set(self, test_config):
        """Test that on_ground flag is set correctly."""
        player = Player(test_config)
        player.position[1] = test_config.player.height
        player.update(dt=0.1, keys_pressed={})
        assert player.on_ground

    def test_on_ground_flag_unset_in_air(self, test_config):
        """Test that on_ground flag is false when in air."""
        player = Player(test_config)
        player.position[1] = 100
        player.update(dt=0.1, keys_pressed={})
        assert not player.on_ground


class TestPlayerActions:
    """Tests for player action methods."""

    def test_shoot_sphere_returns_valid_data(self, test_config):
        """Test that shoot_sphere returns position and velocity."""
        player = Player(test_config)
        spawn_pos, velocity = player.shoot_sphere()

        assert len(spawn_pos) == 3
        assert len(velocity) == 3
        assert np.linalg.norm(velocity) > 0

    def test_shoot_sphere_spawns_ahead(self, test_config):
        """Test that sphere spawns ahead of player."""
        player = Player(test_config)
        player.camera.yaw = 0  # Face forward (negative Z)
        spawn_pos, velocity = player.shoot_sphere()

        # Spawn position should be ahead of player
        assert spawn_pos[2] < player.position[2]

    def test_get_crosshair_target_returns_position(self, test_config):
        """Test that get_crosshair_target returns a position."""
        player = Player(test_config)
        target = player.get_crosshair_target()

        assert len(target) == 3
        assert isinstance(target, np.ndarray)

    def test_crosshair_target_distance(self, test_config):
        """Test that crosshair target is at specified distance."""
        player = Player(test_config)
        distance = 10.0
        target = player.get_crosshair_target(distance=distance)

        # Calculate distance (ignoring Y for ground clamping)
        horizontal_dist = np.sqrt(
            (target[0] - player.position[0])**2 +
            (target[2] - player.position[2])**2
        )
        # Should be approximately the requested distance
        assert abs(horizontal_dist - distance) < 1.0


class TestPlayerReset:
    """Tests for player reset functionality."""

    def test_reset_position(self, test_config):
        """Test that reset returns player to start position."""
        player = Player(test_config)
        player.position[:] = [100, 200, 300]
        player.reset()

        assert player.position[0] == 0.0
        assert player.position[1] == test_config.player.height
        assert player.position[2] == 5.0

    def test_reset_velocity(self, test_config):
        """Test that reset zeros velocity."""
        player = Player(test_config)
        player.velocity[:] = [10, 20, 30]
        player.reset()

        np.testing.assert_array_equal(player.velocity, [0, 0, 0])

    def test_reset_camera(self, test_config):
        """Test that reset resets camera orientation."""
        player = Player(test_config)
        player.camera.yaw = 180
        player.camera.pitch = 45
        player.reset()

        assert player.camera.yaw == 0.0
        assert player.camera.pitch == 0.0

    def test_reset_flags(self, test_config):
        """Test that reset clears state flags."""
        player = Player(test_config)
        player.on_ground = True
        player.reset()

        assert not player.on_ground


class TestPlayerRepr:
    """Tests for string representation."""

    def test_repr_contains_key_info(self, test_config):
        """Test that repr contains player state information."""
        player = Player(test_config)
        repr_str = repr(player)

        assert "Player" in repr_str
        assert "pos=" in repr_str
        assert "vel=" in repr_str
