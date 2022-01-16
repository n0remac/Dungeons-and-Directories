import arcade
import random
from constants import *


class Level:
    def __init__(self) -> None:
        self.wall_list = None
        self.rock_list = None
        self.gem_list = None
        self.level_list = [self.wall_list, self.rock_list, self.gem_list]

    def setup(self) -> None:
        # TODO replace all this with a Tiled map
        # Create the sprite lists
        self.wall_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.gem_list = arcade.SpriteList()

        # Set up the walls
        for x in range(0, SCREEN_WIDTH + 1, SPRITE_SIZE):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassCenter.png", SPRITE_SCALING_PLAYER
            )
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

            wall = arcade.Sprite(
                ":resources:images/tiles/grassCenter.png", SPRITE_SCALING_PLAYER
            )
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT
            self.wall_list.append(wall)

        # Set up the walls
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT, SPRITE_SIZE):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassCenter.png", SPRITE_SCALING_PLAYER
            )
            wall.center_x = 0
            wall.center_y = y
            self.wall_list.append(wall)

            wall = arcade.Sprite(
                ":resources:images/tiles/grassCenter.png", SPRITE_SCALING_PLAYER
            )
            wall.center_x = SCREEN_WIDTH
            wall.center_y = y
            self.wall_list.append(wall)

        # Add some movable rocks
        for x in range(SPRITE_SIZE * 2, SPRITE_SIZE * 13, SPRITE_SIZE):
            rock = random.randrange(4) + 1
            item = arcade.Sprite(
                f":resources:images/space_shooter/meteorGrey_big{rock}.png",
                SPRITE_SCALING_PLAYER,
            )
            item.center_x = x
            item.center_y = 400
            self.rock_list.append(item)

        # Add some movable coins
        for x in range(SPRITE_SIZE * 2, SPRITE_SIZE * 13, SPRITE_SIZE):
            items = [
                ":resources:images/items/gemBlue.png",
                ":resources:images/items/gemRed.png",
                ":resources:images/items/coinGold.png",
                ":resources:images/items/keyBlue.png",
            ]
            item_name = random.choice(items)
            item = arcade.Sprite(item_name, SPRITE_SCALING_PLAYER)
            item.center_x = x
            item.center_y = 300
            self.gem_list.append(item)

    def on_draw(self):
        self.wall_list.draw()
        self.rock_list.draw()
        self.gem_list.draw()
