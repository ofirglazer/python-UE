"""
Main entry point for the UE-inspired simulation.

Run this file to start the simulation:
    python main.py
"""

from core.engine import GameEngine
from config import GameConfig


def main() -> None:
    """Initialize and run the game engine."""
    config = GameConfig()
    engine = GameEngine(config)
    engine.initialize()
    engine.run()


if __name__ == "__main__":
    main()
