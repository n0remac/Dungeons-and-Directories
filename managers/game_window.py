import arcade

class MyWindow(arcade.Window):
    """Main Window"""

    def __init__(self, width, height, title):
        """Init"""
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        self.player = Player()
        self.level = Level()

        self.bullet_list = None
        self.physics_engine: Optional[Physics] = None

    def setup(self):
        """Set up everything"""
        self.player.setup()
        self.level.setup()

        self.bullet_list = arcade.SpriteList()

        self.physics_engine = Physics(damping=0.7, gravity=(0, 0))
        self.physics_engine.setup(
            self.player, self.level.wall_list, self.level.rock_list, self.level.gem_list
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Called whenever the mouse button is clicked."""

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
        size = (
            max(self.player.player_sprite.width, self.player.player_sprite.height) / 2
        )

        bullet.center_x += size * force[0]
        bullet.center_y += size * force[1]

        self.physics_engine.add_sprite(
            bullet,
            mass=0.1,
            damping=1.0,
            friction=0.6,
            collision_type="bullet",
            elasticity=0.9,
        )

        # Taking into account the angle, calculate our force.
        force[0] *= BULLET_MOVE_FORCE
        force[1] *= BULLET_MOVE_FORCE

        self.physics_engine.apply_force(bullet, force)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        self.player.on_key_press(key, modifiers)

        if key == arcade.key.SPACE:
            bullet = arcade.SpriteSolidColor(9, 9, arcade.color.RED)
            bullet.position = self.player.player_sprite.position
            bullet.center_x += 30
            self.bullet_list.append(bullet)
            self.physics_engine.add_sprite(
                bullet, mass=0.2, damping=1.0, friction=0.6, collision_type="bullet"
            )
            force = (3000, 0)
            self.physics_engine.apply_force(bullet, force)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        self.player.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        """Movement and game logic"""

        self.player.on_update(self.physics_engine, delta_time)

        # --- Move items in the physics engine
        self.physics_engine.step()

    def on_draw(self):
        """Draw everything"""
        arcade.start_render()
        self.bullet_list.draw()
        self.level.on_draw()
        self.player.on_draw()
