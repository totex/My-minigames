import arcade

# Physics
MOVEMENT_SPEED = 8
JUMP_SPEED = 28
GRAVITY = 1.1

# Map
MAP_WIDTH = 40 * 128
MAP_HEIGHT = 7 * 128
TILE_WIDTH = 128

# Window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 896
WINDOW_HALF_WIDTH = WINDOW_WIDTH // 2


class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 100)

        arcade.set_background_color(arcade.color.BLACK)

        self.ground_list = None
        self.coins_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.collected_coins = 0

        self.setup()

    def setup(self):
        my_map = arcade.read_tiled_map("maps/my-map1.tmx", 1)
        self.ground_list = arcade.generate_sprites(my_map, "ground", 1)
        self.coins_list = arcade.generate_sprites(my_map, "coins", 1)

        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("images/character.png", 1)
        self.player_sprite.center_x = 640
        self.player_sprite.center_y = 350
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.ground_list, gravity_constant=GRAVITY)


    def on_draw(self):
        arcade.start_render()
        self.ground_list.draw()
        self.player_list.draw()
        self.coins_list.draw()
        arcade.draw_text(f"collected coins: {self.collected_coins}", arcade.get_viewport()[0] + 10, arcade.get_viewport()[2] + 866, arcade.color.GOLD, font_size=20)

    def clamp(self, value, mini, maxi):
        return max(min(value, maxi), mini)

    def on_update(self, delta_time):
        self.physics_engine.update()

        self.player_sprite.center_x = self.clamp(self.player_sprite.center_x, 0, MAP_WIDTH)

        if self.player_sprite.center_x > WINDOW_HALF_WIDTH and self.player_sprite.center_x < MAP_WIDTH - TILE_WIDTH - WINDOW_HALF_WIDTH:
            change_view = True
        else:
            change_view = False

        if change_view:
            arcade.set_viewport(self.player_sprite.center_x - WINDOW_HALF_WIDTH, self.player_sprite.center_x + WINDOW_HALF_WIDTH, 0, WINDOW_HEIGHT)

        coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coins_list)
        for coin in coins_hit:
            self.collected_coins += 1
            coin.kill()


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        if symbol == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


MyGameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, 'Simple Platformer template')
arcade.run()
