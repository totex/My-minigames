import arcade


class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK)

        self.ground_list = None

        self.setup()

    def setup(self):
        my_map = arcade.read_tiled_map("my-map.tmx", 0.5)

        # self.ground_list = arcade.generate_sprites(my_map, "ground", 1)

    def on_draw(self):
        arcade.start_render()
        # self.ground_list.draw()

    def on_update(self, delta_time):
        pass


MyGameWindow(640, 640, 'Platfomer template')
arcade.run()
