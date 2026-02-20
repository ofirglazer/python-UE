"""
Main game engine implementation.

This module contains the core game loop and engine initialization,
coordinating all subsystems (rendering, physics, input).
"""

import pygame
import time
import random
from typing import List
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from core import Player, SceneRenderer
from physics import PhysicsObject
from rendering import (
    draw_sphere,
    draw_box,
    draw_ground,
    draw_skybox,
    setup_lighting,
    HUD,
)
import config


class GameEngine:
    """
    Main game engine coordinating all systems.

    Attributes:
        running: Whether the engine is running
        clock: Pygame clock for timing
        player: Player instance
        physics_objects: List of active physics objects
        scene_renderer: Static scene renderer
        hud: HUD renderer
        shoot_cooldown: Time until next shot allowed
        fps_accumulator: Accumulated FPS for averaging
        fps_count: Number of FPS samples
        fps_display: Current displayed FPS value
    """

    def __init__(self):
        """Initialize the game engine and all subsystems."""
        self.running: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.last_time: float = 0.0

        # Core systems
        self.player: Player = Player()
        self.physics_objects: List[PhysicsObject] = []
        self.scene_renderer: SceneRenderer = SceneRenderer()
        self.hud: None  # Don't create yet

        # Timing
        self.shoot_cooldown: float = 0.0
        self.fps_accumulator: float = 0.0
        self.fps_count: int = 0
        self.fps_display: float = 0.0

    def initialize(self) -> None:
        """Initialize Pygame, OpenGL, and all subsystems."""
        # Initialize Pygame
        pygame.init()
        self.hud = HUD()  # Now pygame is ready
        pygame.display.set_caption(config.WINDOW_TITLE)
        pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
            DOUBLEBUF | OPENGL
        )

        # Hide cursor and grab mouse for FPS controls
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        # Initialize OpenGL
        self._init_opengl()

        # Set initial time
        self.last_time = time.time()

    def _init_opengl(self) -> None:
        """Configure OpenGL rendering state."""
        # Viewport
        glViewport(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # Projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(
            config.FIELD_OF_VIEW,
            config.WINDOW_WIDTH / config.WINDOW_HEIGHT,
            config.NEAR_PLANE,
            config.FAR_PLANE
        )
        glMatrixMode(GL_MODELVIEW)

        # Depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        # Normals
        glEnable(GL_NORMALIZE)

        # Lighting
        setup_lighting()

    def run(self) -> None:
        """Main game loop."""
        self.running = True

        while self.running:
            # Calculate time delta
            current_time = time.time()
            dt = min(current_time - self.last_time, config.MAX_PHYSICS_DELTA)
            self.last_time = current_time

            # Update FPS counter
            self._update_fps(dt)

            # Update cooldowns
            self.shoot_cooldown = max(0.0, self.shoot_cooldown - dt)

            # Process input
            self._process_events()

            # Update game state
            self._update(dt)

            # Render frame
            self._render()

            # Frame rate limiting
            self.clock.tick(config.TARGET_FPS)

        # Cleanup
        pygame.quit()

    def _update_fps(self, dt: float) -> None:
        """
        Update FPS counter with exponential averaging.

        Args:
            dt: Frame time delta
        """
        if dt > 0:
            self.fps_accumulator += 1.0 / dt
            self.fps_count += 1

        if self.fps_count >= config.FPS_SAMPLE_SIZE:
            self.fps_display = self.fps_accumulator / self.fps_count
            self.fps_accumulator = 0.0
            self.fps_count = 0

    def _process_events(self) -> None:
        """Process pygame events and input."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                self._handle_keydown(event.key)

            elif event.type == MOUSEMOTION:
                self.player.handle_mouse_motion(*event.rel)

    def _handle_keydown(self, key: int) -> None:
        """
        Handle keyboard key press events.

        Args:
            key: Pygame key constant
        """
        if key == K_ESCAPE:
            self.running = False

        elif key == K_r:
            self._reset_scene()

        elif key == K_f and self.shoot_cooldown == 0:
            self._shoot_sphere()

        elif key == K_g:
            self._spawn_crate()

    def _reset_scene(self) -> None:
        """Reset the scene to initial state."""
        self.physics_objects.clear()
        self.player.reset()
        PhysicsObject.reset_id_counter()

    def _shoot_sphere(self) -> None:
        """Shoot a physics sphere from player position."""
        spawn_pos, velocity = self.player.shoot_sphere()
        color = random.choice(config.SPHERE_COLORS)

        sphere = PhysicsObject(
            pos=spawn_pos,
            vel=velocity,
            shape="sphere",
            size=config.SPHERE_DEFAULT_RADIUS,
            color=color,
            mass=config.SPHERE_DEFAULT_MASS
        )
        self.physics_objects.append(sphere)
        self.shoot_cooldown = config.SHOOT_COOLDOWN

    def _spawn_crate(self) -> None:
        """Spawn a physics crate at crosshair location."""
        target_pos = self.player.get_crosshair_target()
        color = random.choice(config.CRATE_COLORS)
        size = random.uniform(config.CRATE_MIN_SIZE, config.CRATE_MAX_SIZE)

        crate = PhysicsObject(
            pos=target_pos,
            vel=[
                random.uniform(-2, 2),
                random.uniform(2, 6),
                random.uniform(-2, 2)
            ],
            shape="box",
            size=size,
            color=color,
            mass=config.CRATE_MASS
        )
        self.physics_objects.append(crate)

    def _update(self, dt: float) -> None:
        """
        Update all game systems.

        Args:
            dt: Time delta in seconds
        """
        # Get current key states
        keys_pressed = pygame.key.get_pressed()

        # Update player
        self.player.update(dt, keys_pressed)

        # Update physics objects
        alive_objects = [obj for obj in self.physics_objects if obj.alive]
        for obj in alive_objects:
            obj.update(dt, alive_objects)

        # Remove dead objects
        self.physics_objects = [obj for obj in alive_objects if obj.alive]

        # Limit total objects
        if len(self.physics_objects) > config.MAX_OBJECTS:
            self.physics_objects = self.physics_objects[-config.MAX_OBJECTS:]

    def _render(self) -> None:
        """Render the current frame."""
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Render skybox (before camera transform)
        draw_skybox()

        # Apply camera transformation
        self.player.camera.apply_to_opengl()

        # Render ground
        draw_ground()

        # Render static scene
        self.scene_renderer.render()

        # Render physics objects
        self._render_physics_objects()

        # Render HUD
        self.hud.render(
            config.WINDOW_WIDTH,
            config.WINDOW_HEIGHT,
            self.fps_display,
            len(self.physics_objects),
            self.player.position
        )

        # Swap buffers
        pygame.display.flip()

    def _render_physics_objects(self) -> None:
        """Render all active physics objects."""
        for obj in self.physics_objects:
            glPushMatrix()
            glTranslatef(*obj.pos)
            glColor3fv(obj.color)

            if obj.shape == "sphere":
                draw_sphere(obj.size)
            else:  # box
                glRotatef(obj.rot[0], 1, 0, 0)
                glRotatef(obj.rot[1], 0, 1, 0)
                glRotatef(obj.rot[2], 0, 0, 1)
                draw_box(obj.size)

            glPopMatrix()
