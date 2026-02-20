# UE-Inspired 3D Simulation

A Python-based 3D physics simulation inspired by Unreal Engine, featuring first-person controls, real-time physics, and OpenGL rendering.

## Features

- **First-Person Camera**: Mouse-look controls with smooth rotation
- **Physics Simulation**: Gravity, collision detection, and response
- **Dynamic Objects**: Spheres and boxes with realistic bouncing and friction
- **Interactive Controls**: Shoot spheres, spawn crates, jump and move
- **OpenGL Rendering**: Hardware-accelerated 3D graphics with lighting
- **Modular Architecture**: Clean separation of concerns with testable components

## Requirements

- Python 3.8+
- pygame >= 2.5.0
- PyOpenGL >= 3.1.7
- PyOpenGL-accelerate >= 3.1.7
- numpy >= 1.24.0

## Installation

```bash
# Clone or download the repository
cd ue_simulation

# Install dependencies
pip install -r requirements.txt
```

## Running the Simulation

```bash
python main.py
```

## Controls

| Key/Input | Action |
|-----------|--------|
| **W/A/S/D** | Move forward/left/backward/right |
| **Mouse** | Look around (FPS camera) |
| **SPACE** | Jump |
| **F** | Shoot physics sphere |
| **G** | Spawn crate at crosshair |
| **R** | Reset scene |
| **ESC** | Quit |

## Project Structure

```
ue_simulation/
├── config.py              # Configuration constants
├── main.py                # Entry point
├── core/                  # Core engine systems
│   ├── camera.py         # First-person camera
│   ├── player.py         # Player controller
│   ├── scene.py          # Static scene rendering
│   └── engine.py         # Main game loop
├── physics/               # Physics simulation
│   ├── object.py         # Physics object class
│   └── collision.py      # Collision detection/response
├── rendering/             # Rendering systems
│   ├── primitives.py     # 3D shape rendering
│   ├── lighting.py       # Lighting setup
│   └── hud.py            # HUD overlay
├── utils/                 # Utility functions
│   └── math_utils.py     # Vector math helpers
└── tests/                 # Test suite
    ├── test_math_utils.py
    ├── test_collision.py
    ├── test_physics.py
    ├── test_player.py
    └── test_integration.py
```

## Architecture

### Core Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Testability**: All components are unit-tested with high coverage
3. **PEP 8 Compliance**: Code follows Python style guidelines
4. **Type Hints**: Function signatures include type annotations
5. **Documentation**: Comprehensive docstrings for all public APIs

### System Overview

```
┌─────────────────────────────────────────────────┐
│             GameEngine (main loop)               │
│  - Event handling                                │
│  - Frame timing                                  │
│  - System coordination                           │
└──────────────┬──────────────────────────────────┘
               │
      ┌────────┼────────┬────────┬────────┐
      │        │        │        │        │
┌─────▼──┐ ┌──▼───┐ ┌──▼────┐ ┌─▼──────┐ │
│ Player │ │Scene │ │Physics│ │Renderer│ │
│        │ │      │ │Objects│ │        │ │
└────┬───┘ └──────┘ └───┬───┘ └────────┘ │
     │                  │                 │
┌────▼────┐      ┌──────▼──────┐    ┌────▼────┐
│ Camera  │      │  Collision  │    │   HUD   │
│         │      │  Detection  │    │         │
└─────────┘      └─────────────┘    └─────────┘
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_physics.py

# Run with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "collision"
```

## Configuration

All simulation parameters are centralized in `config.py`:

- **Display**: Window size, FOV, rendering distances
- **Physics**: Gravity, friction, restitution (bounciness)
- **Player**: Movement speed, jump height, camera sensitivity
- **Objects**: Size ranges, mass, lifetime limits
- **Rendering**: Colors, lighting parameters, FPS targets

Example configuration changes:

```python
# In config.py

# Make gravity stronger
GRAVITY = -25.0  # Default: -18.0

# Increase player jump height
JUMP_SPEED = 12.0  # Default: 8.0

# Make objects bouncier
RESTITUTION = 0.8  # Default: 0.45
```

## Physics System

### Collision Detection

- **Sphere-Sphere**: Efficient distance-based detection
- **Sphere-Ground**: Simple plane collision
- **Spatial Hashing**: Could be added for optimization with many objects

### Collision Response

- **Impulse-Based**: Physically accurate momentum transfer
- **Restitution**: Configurable bounciness (0 = no bounce, 1 = perfect bounce)
- **Friction**: Horizontal velocity dampening on ground contact

### Integration

- **Semi-Implicit Euler**: Velocity updated before position
- **Fixed Time Step Cap**: Prevents physics explosions on slow frames
- **Continuous Collision**: Objects can't tunnel through surfaces

## Rendering

### Graphics Pipeline

1. **Skybox**: Gradient background (rendered first, no depth)
2. **Camera Transform**: Apply player view matrix
3. **Static Scene**: Crates and pillars
4. **Dynamic Objects**: Physics spheres and boxes
5. **HUD Overlay**: 2D information display

### Lighting Model

- **Phong Shading**: Smooth per-fragment lighting
- **Two-Light Setup**:
  - Key light: Warm directional (sun)
  - Fill light: Cool directional (ambient)
- **Specular Highlights**: Shiny material properties

## Performance Optimization

### Current Optimizations

- Object culling after max count
- FPS-independent physics (delta time)
- Immediate mode OpenGL (simple but not fastest)

### Potential Improvements

- Vertex Buffer Objects (VBO) for geometry
- Instanced rendering for repeated objects
- Spatial partitioning (octree/grid) for collision
- GPU compute shaders for physics

## Extending the Simulation

### Adding New Object Types

```python
# In physics/object.py
class PhysicsObject:
    def __init__(self, ..., shape="sphere"):
        # Add new shape type
        if shape == "cylinder":
            # Initialize cylinder-specific properties
            pass
```

### Adding New Controls

```python
# In core/engine.py
def _handle_keydown(self, key):
    if key == K_e:
        # Custom action
        self._do_custom_action()
```

### Custom Physics Behaviors

```python
# In physics/object.py
def update(self, dt, other_objects):
    # Add custom forces
    if self.custom_behavior:
        self.vel += self.custom_force * dt
```

## Known Limitations

1. **No Multithreading**: Physics runs on single thread
2. **Simple Collision**: Only spheres collide with each other
3. **No Persistence**: Scene resets on restart
4. **Fixed Ground**: Only horizontal plane supported
5. **CPU Physics**: All calculations on CPU (not GPU)

## Troubleshooting

### Common Issues

**ImportError: No module named 'OpenGL'**
```bash
pip install PyOpenGL PyOpenGL-accelerate
```

**Black screen on startup**
- Check GPU drivers are up to date
- Verify OpenGL support: `glxinfo | grep "OpenGL version"`

**Low FPS**
- Reduce number of objects (config.MAX_OBJECTS)
- Lower resolution (config.WINDOW_WIDTH/HEIGHT)
- Disable lighting temporarily to test

**Objects fall through ground**
- Check GROUND_LEVEL in config
- Verify physics timestep isn't too large

## Contributing

When contributing, please:

1. Follow PEP 8 style guidelines
2. Add type hints to function signatures
3. Write unit tests for new features
4. Update documentation
5. Run `pytest` before submitting

## License

This project is for educational purposes demonstrating game engine concepts in Python.

## Acknowledgments

- Inspired by Unreal Engine's editor viewport
- Physics based on classical mechanics and game physics literature
- Rendering uses immediate mode OpenGL for educational clarity

## Contact

For questions or issues, please refer to the project documentation.
