import pymunkoptions
pymunkoptions.options["debug"] = False
import pyglet
from pyglet.window import FPSDisplay, key
import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk.vec2d import Vec2d
import random

collision_types = {
    "ball":1,
    "brick":2,
    "bottom":3,
    "player":4
}

class Bricks:
    def __init__(self, space):
        for x in range(10):
            for y in range(10):
                body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                body.position = x*110+90, y*30+500
                shape = pymunk.Segment(body, (0,0), (100,0), 8)
                shape.elasticity = 0.98
                shape.collision_type = collision_types["brick"]
                space.add(body, shape)

        handler = space.add_collision_handler(collision_types["brick"], collision_types["ball"])
        handler.separate = self.remove_brick

    def remove_brick(self, arbiter, space, data):
        brick_shape = arbiter.shapes[0]
        space.remove(brick_shape, brick_shape.body)





class Walls:
    def __init__(self, space):
        left = pymunk.Segment(space.static_body, (50,110), (50,800), 2)
        top = pymunk.Segment(space.static_body, (50,800), (1230,800), 2)
        right = pymunk.Segment(space.static_body, (1230,800), (1230,110), 2)

        left.elasticity = 0.98
        top.elasticity = 0.98
        right.elasticity = 0.98

        bottom = pymunk.Segment(space.static_body, (50,50), (1230,50), 2)
        bottom.sensor = True
        bottom.collision_type = collision_types["bottom"]

        handler = space.add_collision_handler(collision_types["ball"], collision_types["bottom"])
        handler.begin = self.reset_game

        space.add(left, top, right, bottom)

    def reset_game(self, arbiter, space, data):
        window.reset_game()
        return True



class Ball(pymunk.Body):
    def __init__(self, space, position):
        super().__init__(1, pymunk.inf)
        self.position = position.x, position.y+18
        shape = pymunk.Circle(self, 10)
        shape.elasticity = 0.98
        shape.collision_type = collision_types["ball"]
        self.spc = space
        self.on_paddle = True
        self.velocity_func = self.constant_velocity

        self.joint = pymunk.GrooveJoint(space.static_body, self, (100,118), (1180,118), (0,0))

        space.add(self, shape, self.joint)

    def shoot(self):
        self.on_paddle = False
        self.spc.remove(self.joint)
        direction = Vec2d(random.choice([(50,500), (-50,500)]))
        self.apply_impulse_at_local_point(direction)

    def constant_velocity(self, body, gravity, damping, dt):
        body.velocity = body.velocity.normalized()*600

    def update(self):
        if self.position.x < 50 or self.position.x > 1230 or self.position.y > 800:
            self.velocity *= -1



class Player(pymunk.Body):
    def __init__(self, space):
        super().__init__(10, pymunk.inf)
        self.position = 640, 100
        shape = pymunk.Segment(self, (-50,0), (50,0), 8)
        shape.elasticity = 0.98
        shape.collision_type = collision_types["player"]

        joint = pymunk.GrooveJoint(space.static_body, self, (100,100), (1180,100), (0,0))

        space.add(self, shape, joint)


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(300, 50)
        self.fps = FPSDisplay(self)

        self.space = pymunk.Space()
        self.options = DrawOptions()

        self.player = Player(self.space)
        self.ball = Ball(self.space, self.player.position)
        self.walls = Walls(self.space)
        self.bricks = Bricks(self.space)

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options)
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.player.velocity = 600, 0
            if self.ball.on_paddle:
                self.ball.velocity = self.player.velocity
        if symbol == key.LEFT:
            self.player.velocity = -600, 0
            if self.ball.on_paddle:
                self.ball.velocity = self.player.velocity
        if symbol == key.SPACE:
            if self.ball.on_paddle:
                self.ball.shoot()
        if symbol == key.R:
            self.reset_game()

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.RIGHT, key.LEFT):
            self.player.velocity = 0, 0
            if self.ball.on_paddle:
                self.ball.velocity = 0, 0

    def reset_game(self):
        for shape in self.space.shapes:
            if shape.body != self.space.static_body and shape.body.body_type != pymunk.Body.KINEMATIC:
                self.space.remove(shape.body, shape)
        for constraint in self.space.constraints:
            self.space.remove(constraint)
        self.player = Player(self.space)
        self.ball = Ball(self.space, self.player.position)

    def update(self, dt):
        self.space.step(dt)
        self.ball.update()




if __name__ == "__main__":
    window = GameWindow(1280, 900, "Breakout game", resizable=False)
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()