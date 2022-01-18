import arcade
from arcade.pymunk_physics_engine import PymunkPhysicsEngine


class Physics(PymunkPhysicsEngine):
    def __init__(
        self, gravity=..., damping: float = 1, maximum_incline_on_ground: float = 0.708
    ):
        super().__init__(
            gravity=gravity,
            damping=damping,
            maximum_incline_on_ground=maximum_incline_on_ground,
        )

    def setup(self, player, wall_list, rock_list, gem_list):
        def rock_hit_handler(sprite_a, sprite_b, arbiter, space, data):
            """Called for bullet/rock collision"""
            bullet_shape = arbiter.shapes[0]
            bullet_sprite = self.get_sprite_for_shape(bullet_shape)
            bullet_sprite.remove_from_sprite_lists()
            print("Rock")

        def wall_hit_handler(sprite_a, sprite_b, arbiter, space, data):
            """Called for bullet/rock collision"""
            bullet_shape = arbiter.shapes[0]
            bullet_sprite = self.get_sprite_for_shape(bullet_shape)
            bullet_sprite.remove_from_sprite_lists()
            print("Wall")

        self.add_collision_handler("bullet", "rock", post_handler=rock_hit_handler)
        self.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

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
        self.add_sprite(
            player.player_sprite,
            friction=0.6,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.01,
            collision_type="player",
            max_velocity=400,
        )

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.add_sprite_list(
            wall_list,
            friction=0.6,
            collision_type="wall",
            body_type=PymunkPhysicsEngine.STATIC,
        )

        # Create some boxes to push around.
        # Mass controls, well, the mass of an object. Defaults to 1.
        self.add_sprite_list(
            rock_list, mass=2, friction=0.8, damping=0.1, collision_type="rock"
        )
        # Create some boxes to push around.
        # Mass controls, well, the mass of an object. Defaults to 1.
        self.add_sprite_list(
            gem_list, mass=0.5, friction=0.8, damping=0.4, collision_type="rock"
        )
