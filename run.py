"""
Example of Pymunk Physics Engine

Top-down
"""
import math
import random
import arcade
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine
from constants import *
from player import Player

class MyWindow(arcade.Window):
    """ Main Window """
    def __init__(self, width, height, title):
        """ Init """
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        self.player = Player()

        self.wall_list = None
        self.rock_list = None
        self.gem_list = None

        self.bullet_list = None
        self.physics_engine: Optional[PymunkPhysicsEngine] = None

    def setup(self):
        """ Set up everything """
        self.player.setup()

        # Create the sprite lists
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.gem_list = arcade.SpriteList()

        # Set up the walls
        for x in range(0, SCREEN_WIDTH + 1, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png",
                                 SPRITE_SCALING_PLAYER)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png",
                                 SPRITE_SCALING_PLAYER)
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT
            self.wall_list.append(wall)

        # Set up the walls
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png",
                                 SPRITE_SCALING_PLAYER)
            wall.center_x = 0
            wall.center_y = y
            self.wall_list.append(wall)

            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png",
                                 SPRITE_SCALING_PLAYER)
            wall.center_x = SCREEN_WIDTH
            wall.center_y = y
            self.wall_list.append(wall)

        # Add some movable rocks
        for x in range(SPRITE_SIZE * 2, SPRITE_SIZE * 13, SPRITE_SIZE):
            rock = random.randrange(4) + 1
            item = arcade.Sprite(f":resources:images/space_shooter/meteorGrey_big{rock}.png",
                                 SPRITE_SCALING_PLAYER)
            item.center_x = x
            item.center_y = 400
            self.rock_list.append(item)

        # Add some movable coins
        for x in range(SPRITE_SIZE * 2, SPRITE_SIZE * 13, SPRITE_SIZE):
            items = [":resources:images/items/gemBlue.png",
                     ":resources:images/items/gemRed.png",
                     ":resources:images/items/coinGold.png",
                     ":resources:images/items/keyBlue.png"]
            item_name = random.choice(items)
            item = arcade.Sprite(item_name,
                                 SPRITE_SCALING_PLAYER)
            item.center_x = x
            item.center_y = 300
            self.gem_list.append(item)

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = 0.7

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, 0)

        # Create the physics engine
        self.physics_engine = PymunkPhysicsEngine(damping=damping,
                                                  gravity=gravity)

        def rock_hit_handler(sprite_a, sprite_b, arbiter, space, data):
            """ Called for bullet/rock collision """
            bullet_shape = arbiter.shapes[0]
            bullet_sprite = self.physics_engine.get_sprite_for_shape(bullet_shape)
            bullet_sprite.remove_from_sprite_lists()
            print("Rock")

        def wall_hit_handler(sprite_a, sprite_b, arbiter, space, data):
            """ Called for bullet/rock collision """
            bullet_shape = arbiter.shapes[0]
            bullet_sprite = self.physics_engine.get_sprite_for_shape(bullet_shape)
            bullet_sprite.remove_from_sprite_lists()
            print("Wall")

        self.physics_engine.add_collision_handler("bullet", "rock", post_handler=rock_hit_handler)
        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player.player_sprite,
                                       friction=0.6,
                                       moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                       damping=0.01,
                                       collision_type="player",
                                       max_velocity=400)

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=0.6,
                                            collision_type="wall",
                                            body_type=PymunkPhysicsEngine.STATIC)

        # Create some boxes to push around.
        # Mass controls, well, the mass of an object. Defaults to 1.
        self.physics_engine.add_sprite_list(self.rock_list,
                                            mass=2,
                                            friction=0.8,
                                            damping=0.1,
                                            collision_type="rock")
        # Create some boxes to push around.
        # Mass controls, well, the mass of an object. Defaults to 1.
        self.physics_engine.add_sprite_list(self.gem_list,
                                            mass=0.5,
                                            friction=0.8,
                                            damping=0.4,
                                            collision_type="rock")

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        bullet = arcade.SpriteSolidColor(5, 5, arcade.color.RED)
        self.bullet_list.append(bullet)

        # Position the bullet at the player's current location
        start_x = self.player.player_sprite.center_x
        start_y = self.player.player_sprite.center_y
        bullet.position = self.player.player_sprite.position

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        force = [math.cos(angle), math.sin(angle)]
        size = max(self.player.player_sprite.width, self.player.player_sprite.height) / 2

        bullet.center_x += size * force[0]
        bullet.center_y += size * force[1]

        self.physics_engine.add_sprite(bullet,
                                       mass=0.1,
                                       damping=1.0,
                                       friction=0.6,
                                       collision_type="bullet",
                                       elasticity=0.9)

        # Taking into account the angle, calculate our force.
        force[0] *= BULLET_MOVE_FORCE
        force[1] *= BULLET_MOVE_FORCE

        self.physics_engine.apply_force(bullet, force)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        self.player.on_key_press(key, modifiers)

        if key == arcade.key.SPACE:
            bullet = arcade.SpriteSolidColor(9, 9, arcade.color.RED)
            bullet.position = self.player.player_sprite.position
            bullet.center_x += 30
            self.bullet_list.append(bullet)
            self.physics_engine.add_sprite(bullet,
                                           mass=0.2,
                                           damping=1.0,
                                           friction=0.6,
                                           collision_type="bullet")
            force = (3000, 0)
            self.physics_engine.apply_force(bullet, force)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        self.player.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.player.on_update(self.physics_engine, delta_time)

        # --- Move items in the physics engine
        self.physics_engine.step()

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.wall_list.draw()
        self.bullet_list.draw()
        self.rock_list.draw()
        self.gem_list.draw()
        self.player.on_draw()


def main():
    """ Main function """
    window = MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
