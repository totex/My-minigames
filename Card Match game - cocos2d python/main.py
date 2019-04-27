import cocos
from cocos.director import director
from pyglet.window import mouse
from cocos.scenes import *
from random import randint, shuffle
import pyglet

# This needs to be on the top, otherwise the SceneManager won't work
director.init(width=1024, height=576, caption="Match the Shapes!")
director.window.pop_handlers()
director.window.set_location(400, 200)


def load_score(file):
    with open(file, 'r') as f:
        score = f.read()
    return score


def save_score(file, scr):
    with open(file, 'w') as f:
        f.write(str(scr))


def calculate_score(score):
    current_time = score
    loaded_time = load_score("res/score.txt")

    current_minutes = current_time.split(":")[0]
    current_seconds = current_time.split(":")[1]

    loaded_minutes = loaded_time.split(":")[0]
    loaded_seconds = loaded_time.split(":")[1]

    time1 = int(current_minutes) * 60 + int(current_seconds)
    time2 = int(loaded_minutes) * 60 + int(loaded_seconds)

    if time1 < time2:
        return True
    return False


""" ALL THE GAME RELATED LAYERS """
class CardLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self, image_path):
        super().__init__()
        self.clicked = False
        self.spr = cocos.sprite.Sprite(image_path, anchor=(0, 0))
        self.name = image_path.split("/")[2].split(".")[0]

        self.back = cocos.sprite.Sprite('res/sprites/back.png', anchor=(0, 0))

        self.add(self.spr)
        self.add(self.back)

    def card_clicked(self, x, y):
        return x < self.spr.x + self.spr.width and x > self.spr.x and y < self.spr.y + self.spr.height and y > self.spr.y

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if self.card_clicked(x, y) and len(CardManager.cards_clicked) < 2:
                self.clicked = True
                self.back.visible = False
            else:
                self.clicked = False
        if self.clicked and self not in CardManager.cards_clicked:
            CardManager.cards_clicked.append(self)
            CardManager.check_cards()


class CardManager():

    cards_clicked = []
    pairs = 0

    def __init__(self):
        """
           6  x=3, y=2
          12  x=4, y=3
          20  x=5, y=4
          24  x=6, y=4
        """
        self.level1 = 6 # number of cards at the start of the game
        self.level2 = 12
        self.level3 = 20
        self.level4 = 24

        self.current_level = self.level4

        path = "res/sprites/"
        files = [path + "circle_blue.png", path + "circle_green.png", path + "circle_red.png",
                 path + "penta_blue.png", path + "penta_green.png", path + "penta_red.png",
                 path + "rect_blue.png", path + "rect_green.png", path + "rect_red.png",
                 path + "star_blue.png", path + "star_green.png", path + "star_red.png"]

        random_list = []

        for i in range(self.current_level // 2):
            r = randint(0, len(files) - 1)
            if files[r] not in random_list:
                random_list.append(files[r])
                random_list.append(files[r])
            else:
                while files[r] in random_list:
                    r = randint(0, len(files) - 1)
                random_list.append(files[r])
                random_list.append(files[r])

        shuffle(random_list)

        positions = self.calc_positions()

        for i, file in enumerate(random_list):
            card = CardLayer(file)
            card.spr.image_anchor_x = 0
            card.spr.image_anchor_y = 0
            card.spr.position = positions[i]
            card.back.position = card.spr.position
            SceneManager.game_scene.add(card)

    def calc_positions(self):
        xx, yy = 0, 0
        if self.current_level == self.level1:
            xx, yy = 3, 2
        elif self.current_level == self.level2:
            xx, yy = 4, 3
        elif self.current_level == self.level3:
            xx, yy = 5, 4
        elif self.current_level == self.level4:
            xx, yy = 6, 4
        positions = []
        x_offset = 50
        y_offset = 50
        for x in range(xx):
            for y in range(yy):
                positions.append((x_offset, y_offset))
                y_offset += 120
            x_offset += 120
            y_offset = 50

        return positions

    @staticmethod
    def flip_cards_back(dt):
        for card in CardManager.cards_clicked:
            card.back.visible = True
        CardManager.cards_clicked = []  # need to set this here also

    @staticmethod
    def remove_cards(dt):
        SceneManager.game_scene.remove(CardManager.cards_clicked[0])
        SceneManager.game_scene.remove(CardManager.cards_clicked[1])
        CardManager.cards_clicked = [] # need to set this here also

    @staticmethod
    def check_cards():
        if len(CardManager.cards_clicked) == 2:
            if CardManager.cards_clicked[0].name == CardManager.cards_clicked[1].name:
                CardManager.pairs += 1
                pyglet.clock.schedule_once(CardManager.remove_cards, 0.5)
            else:
                pyglet.clock.schedule_once(CardManager.flip_cards_back, 1.0)
        if CardManager.pairs == 12:
            CardManager.pairs = 0
            GameScene.game_finished = True
            SceneManager.change_scene(SceneManager.wining_scene)


""" ALL THE MENU RELATED LAYERS """
class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super().__init__('CARD MATCH!')

        items = []

        items.append(cocos.menu.MenuItem('New Game', self.on_new_game))
        items.append(cocos.menu.MenuItem('Best Time', self.on_best_time))
        items.append(cocos.menu.MenuItem('Quit', self.on_quit))

        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_new_game(self):
        SceneManager.change_scene(SceneManager.game_scene)

    def on_best_time(self):
        SceneManager.change_scene(SceneManager.best_time_scene)

    def on_quit(self):
        director.window.close()


# Back to main button
class Button(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self, pos):
        super().__init__()
        self.spr = cocos.sprite.Sprite('res/sprites/back_to_main.png')

        self.spr.position = pos

        self.add(self.spr)

    def button_clicked(self, x, y):
        return x > self.spr.x - (self.spr.width//2) and x < self.spr.x + (self.spr.width // 2) and \
               y > self.spr.y - (self.spr.height//2) and y < self.spr.y + (self.spr.height // 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            if self.button_clicked(x, y):
                SceneManager.change_scene(SceneManager.start_scene)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.button_clicked(x, y):
            self.spr.scale = 1.2
        else:
            self.spr.scale = 1


# The Timer
class Timer(cocos.layer.Layer):

    current_time = ""
    time_start = None
    time_stop = None

    def __init__(self):
        super().__init__()
        self.label = cocos.text.Label("", font_name="Times New Roman", font_size=26,
                                 anchor_x="center", anchor_y="center")
        self.start_time = 0

        self.label.position = 874, 276
        self.add(self.label)

        Timer.time_start = self.run_scheduler
        Timer.time_stop = self.stop_scheduler

    def timer(self, dt):
        if GameScene.game_finished:
            self.stop_scheduler()
            self.start_time = 0
            GameScene.game_finished = False
        else:
            mins, secs = divmod(self.start_time, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            Timer.current_time = time_format
            self.label.element.text = time_format
            self.start_time += 1

    def run_scheduler(self):
        self.schedule_interval(self.timer, 1.0)

    def stop_scheduler(self):
        self.unschedule(self.timer)


""" ALL THE SCENES """
class StartScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()

        menu = MainMenu()

        self.add(cocos.layer.ColorLayer(50, 50, 50, 180))
        self.add(menu)


class GameScene(cocos.scene.Scene):

    game_finished = False

    def __init__(self):
        super().__init__()

        self.add(cocos.layer.ColorLayer(50, 50, 50, 180))
        self.add(Button(pos=(874, 376)))
        self.add(Timer())


    # def on_enter(self):
    #     super().on_enter()
    #
    # def on_exit(self):
    #     super().on_exit()


class BestTimeScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()

        self.add(cocos.layer.ColorLayer(50, 50, 50, 180))
        self.add(Button(pos=(512, 156)))

        self.label = cocos.text.Label("", font_name="Times New Roman", font_size=26,
                                      anchor_x="center", anchor_y="center", position=(512, 300))



        self.add(self.label)

    def on_enter(self):
        super().on_enter()
        self.label.element.text = load_score("res/score.txt")

    def on_exit(self):
        super().on_exit()


class WinningScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()

        self.add(cocos.layer.ColorLayer(50, 50, 50, 180))
        self.add(Button(pos=(512, 156)))

        self.add(cocos.text.Label("Your time was:", font_name="Times New Roman", font_size=26,
                                      anchor_x="center", anchor_y="center", position=(512,300)))

        self.score = cocos.text.Label("", font_name="Times New Roman", font_size=22,
                                     anchor_x="center", anchor_y="center", position=(512, 220))

        self.add(self.score)



    def on_enter(self):
        super().on_enter()
        self.score.element.text = Timer.current_time
        if calculate_score(Timer.current_time):
            save_score("res/score.txt", Timer.current_time)

    def on_exit(self):
        super().on_exit()


""" THE SCENE MANAGER """
class SceneManager:

    start_scene = StartScene()
    best_time_scene = BestTimeScene()
    game_scene = GameScene()
    wining_scene = WinningScene()

    active_scene = start_scene

    @staticmethod
    def change_scene(scene):
        SceneManager.active_scene = scene
        if SceneManager.active_scene == SceneManager.game_scene:
            CardManager()
            Timer.time_start()
        elif SceneManager.active_scene == SceneManager.start_scene:
            for child in SceneManager.game_scene.get_children():
                if hasattr(child, 'name'):
                    child.kill()
        director.replace(FlipX3DTransition(SceneManager.active_scene, duration=2))


if __name__ == "__main__":
    director.run(SceneManager.active_scene)