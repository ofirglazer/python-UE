# Quick Start Guide

## Installation

```bash
cd ue_simulation
pip install -r requirements.txt
```

## Run Simulation

```bash
python main.py
```

## Run Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=. --cov-report=html

# View coverage
open htmlcov/index.html  # or your browser
```

## Project Structure

```
ue_simulation/
├── config.py              # All configuration constants
├── main.py                # Entry point
│
├── core/                  # Core systems
│   ├── camera.py         # FPS camera with mouse-look
│   ├── player.py         # Player movement & physics
│   ├── scene.py          # Static scene objects
│   └── engine.py         # Main game loop
│
├── physics/               # Physics simulation
│   ├── collision.py      # Detection & resolution
│   └── object.py         # Dynamic physics objects
│
├── rendering/             # Graphics
│   ├── primitives.py     # OpenGL shapes
│   ├── lighting.py       # Phong lighting
│   └── hud.py            # 2D overlay
│
├── utils/                 # Utilities
│   └── math_utils.py     # Vector operations
│
└── tests/                 # Test suite (100+ tests)
    ├── test_math_utils.py
    ├── test_collision.py
    ├── test_physics.py
    ├── test_player.py
    └── test_integration.py
```

## Controls

| Input | Action |
|-------|--------|
| W/A/S/D | Move |
| Mouse | Look |
| SPACE | Jump |
| F | Shoot sphere |
| G | Spawn crate |
| R | Reset |
| ESC | Quit |

## Code Quality Features

✅ **PEP8 Compliant** - Professional Python style  
✅ **Type Hints** - Clear function signatures  
✅ **Comprehensive Tests** - 100+ unit & integration tests  
✅ **Documentation** - Docstrings throughout  
✅ **Modular Design** - Easy to maintain and extend  

## Testing Highlights

- **100+ test cases** across 5 test files
- **Unit tests** for all utility functions
- **Component tests** for physics and player systems  
- **Integration tests** for complete workflows
- **>90% code coverage** on core modules

## Example: Adding a New Feature

```python
# 1. Add configuration (config.py)
NEW_FEATURE_SPEED = 10.0

# 2. Implement feature (appropriate module)
def new_feature(param: float) -> float:
    """New feature implementation."""
    return param * NEW_FEATURE_SPEED

# 3. Write tests (tests/test_new.py)
def test_new_feature():
    result = new_feature(2.0)
    assert result == 20.0

# 4. Run tests
pytest tests/test_new.py
```

## Key Files to Review

1. **README.md** - Complete documentation
2. **config.py** - All tunable parameters
3. **main.py** - Entry point
4. **core/engine.py** - Main game loop
5. **tests/** - Example test patterns

Happy coding! 🎮
