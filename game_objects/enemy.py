import arcade
from .game_object import GameObject
from constants.base import SPRITE_SCALING_PLAYER, PLAYER_MOVE_FORCE, MOVEMENT_SPEED


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enemy_sprite = None

    def setup(self):
        self.enemy_sprite = arcade.Sprite("resources/enemy.png", SPRITE_SCALING_PLAYER * 10)