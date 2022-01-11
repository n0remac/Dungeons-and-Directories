import arcade
from game_object import GameObject
from constants import *

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player_sprite = None
        self.player_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/"
                                           "femalePerson_idle.png",
                                           SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 250
        self.player_sprite.center_y = 250

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        
    def on_key_press(self, key, modifiers, physics_engine):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            bullet = arcade.SpriteSolidColor(9, 9, arcade.color.RED)
            bullet.position = self.player_sprite.position
            bullet.center_x += 30
            self.bullet_list.append(bullet)
            physics_engine.add_sprite(bullet,
                                           mass=0.2,
                                           damping=1.0,
                                           friction=0.6,
                                           collision_type="bullet")
            force = (3000, 0)
            physics_engine.apply_force(bullet, force)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, physics_engine, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            force = (0, PLAYER_MOVE_FORCE)
            physics_engine.apply_force(self.player_sprite, force)
        elif self.down_pressed and not self.up_pressed:
            force = (0, -PLAYER_MOVE_FORCE)
            physics_engine.apply_force(self.player_sprite, force)
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
            force = (-PLAYER_MOVE_FORCE, 0)
            physics_engine.apply_force(self.player_sprite, force)
        elif self.right_pressed and not self.left_pressed:
            force = (PLAYER_MOVE_FORCE, 0)
            physics_engine.apply_force(self.player_sprite, force)

        # --- Move items in the physics engine
        physics_engine.step()
    
    def on_draw(self):
        """ Draw everything """
        self.player_list.draw()