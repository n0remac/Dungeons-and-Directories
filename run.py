import math
import arcade
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine
from constants.screen import WIDTH, HEIGHT, TITLE
from game_objects import Player
from game_objects import Level
from managers import Physics
from managers import MyWindow

def main():
    """Main function"""
    window = MyWindow(WIDTH, HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
