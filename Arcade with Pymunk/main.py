import pymunkoptions
pymunkoptions.options["debug"] = False

import pymunk
import arcade
from math import degrees

space = pymunk.Space()
space.gravity = 0, -1000

mass = 1
radius = 30

segment_shape1 = pymunk.Segment(space.static_body, (500,400), (1300,440), 2)
segment_shape1.elasticity = 0.8
segment_shape1.friction = 1.0
space.add(segment_shape1)

segment_shape2 = pymunk.Segment(space.static_body, (100,160), (900,100), 2)
segment_shape2.elasticity = 0.8
segment_shape2.friction = 1.0
space.add(segment_shape2)


class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK)

        self.sprites = arcade.SpriteList()


    def on_draw(self):
        arcade.start_render()
        arcade.draw_lines([segment_shape1.a, segment_shape1.b], arcade.color.RED, 4)
        arcade.draw_lines([segment_shape2.a, segment_shape2.b], arcade.color.RED, 4)

        self.sprites.draw()


    def on_update(self, delta_time):
        space.step(delta_time)
        for index, sprite in enumerate(self.sprites):
            sprite.angle = degrees(space.bodies[index].angle)
            sprite.set_position(space.bodies[index].position.x, space.bodies[index].position.y)
            for body in space.bodies:
                if body.position.y < -100:
                    self.sprites.remove(sprite)
                    space.remove(body, body.shapes)


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            circle_moment = pymunk.moment_for_circle(mass, 0, radius)
            circle_body = pymunk.Body(mass, circle_moment)
            circle_body.position = x, y
            circle_shape = pymunk.Circle(circle_body, radius)
            circle_shape.elasticity = 0.8
            circle_shape.friction = 1.0
            space.add(circle_body, circle_shape)
            self.sprites.append(arcade.Sprite("sprites/smile.png", center_x=circle_body.position.x, center_y=circle_body.position.y))



MyGameWindow(1280, 720, 'My game window')
arcade.run()
