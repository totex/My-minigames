import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from random import randint, choice


window = pyglet.window.Window(width=1200, height=900, caption="Space Invaders", resizable=False)
window.set_location(400, 100)
fps_display = FPSDisplay(window)
fps_display.label.font_size = 50

main_batch = pyglet.graphics.Batch()

def load_high_score(file):
    with open(file, 'r') as f:
        score = f.read()
    return score

def save_high_score(file, scr):
    with open(file, 'w') as f:
        f.write(str(scr))

# region Sprites, Labels and Animations
# loading static images
space = pyglet.image.load('res/sprites/space.jpg')
player_image = pyglet.image.load('res/sprites/PlayerShip.png') # space_ship.png
player_laser = pyglet.image.load('res/sprites/laser.png')
enemy_laser = pyglet.image.load('res/sprites/enemy_laser.png')
stats_bg_image = pyglet.image.load('res/sprites/stats_bg_white.png')

# loading sprite sheet animations for the ufo_head
ufo_head = pyglet.image.load('res/sprites/ufoHead_Sh.png')
ufo_head_seq = pyglet.image.ImageGrid(ufo_head, 1, 8, item_width=100, item_height=100)
ufo_head_texture = pyglet.image.TextureGrid(ufo_head_seq)
ufo_head_anim = pyglet.image.Animation.from_image_sequence(ufo_head_texture[0:], 0.1, loop=True)

# loading sprite sheet animations for the enemy space ship
enemy_ship = pyglet.image.load('res/sprites/enemyShip_Sh01.png')
enemy_ship_seq = pyglet.image.ImageGrid(enemy_ship, 1, 15, item_width=100, item_height=100)
enemy_ship_texture = pyglet.image.TextureGrid(enemy_ship_seq)
enemy_ship_anim = pyglet.image.Animation.from_image_sequence(enemy_ship_texture[0:], 0.1, loop=True)

# loading sprite sheet animations for explosion
xplosion_image = pyglet.image.load('res/sprites/explosion.png')
xplosion_seq = pyglet.image.ImageGrid(xplosion_image, 4, 5, item_width=96, item_height=96)
xplosion_textures = pyglet.image.TextureGrid(xplosion_seq)
xplosion_anim = pyglet.image.Animation.from_image_sequence(xplosion_textures[0:], 0.05, loop=True)

# creating a label called "enemies destroyed"
text1 = pyglet.text.Label("enemies destroyed", x=1000 , y=850, batch=main_batch)
text1.italic = True
text1.bold = True
text1.font_size = 16

# creating a label called "score"
text2 = pyglet.text.Label("score", x=1000 , y=750, batch=main_batch)
text2.italic = True
text2.bold = True
text2.font_size = 16

# creating a label called "player health"
text3 = pyglet.text.Label("player health", x=1000 , y=650, batch=main_batch)
text3.italic = True
text3.bold = True
text3.font_size = 16

# creating a label for high score text
high_score_text = pyglet.text.Label("high score", x=1000 , y=450, batch=main_batch)
high_score_text.italic = True
high_score_text.bold = True
high_score_text.font_size = 20

# label for displaying the high score value
high_score = load_high_score("res/score.txt")
high_score_value = pyglet.text.Label(high_score, x=1100, y=400, batch=main_batch)
high_score_value.color = (120, 200, 150, 255)
high_score_value.font_size = 24

# creating a label to display the number of destroyed enemies
num_enemies_destroyed = pyglet.text.Label(str(0), x=1100, y=800, batch=main_batch)
num_enemies_destroyed.color = (120, 200, 150, 255)
num_enemies_destroyed.font_size = 22

# creating a label to display the score
num_score = pyglet.text.Label(str(0), x=1100, y=700, batch=main_batch)
num_score.color = (220, 100, 150, 255)
num_score.font_size = 22

# creating a label to display the player's health
numb_player_health = pyglet.text.Label(str(5), x=1100, y=600, batch=main_batch)
numb_player_health.color = (0, 100, 50, 255)
numb_player_health.font_size = 22

game_over_text = pyglet.text.Label("game over", x=600 , y=500)
game_over_text.anchor_x = "center"
game_over_text.anchor_y = "center"
game_over_text.italic = True
game_over_text.bold = True
game_over_text.font_size = 60

reload_text = pyglet.text.Label("press r to reload", x=600 , y=350)
reload_text.anchor_x = "center"
reload_text.anchor_y = "center"
reload_text.italic = True
reload_text.bold = True
reload_text.font_size = 40

intro_text = pyglet.text.Label("press space to start", x=600 , y=450)
intro_text.anchor_x = "center"
intro_text.anchor_y = "center"
intro_text.italic = True
intro_text.bold = True
intro_text.font_size = 40

player = pyglet.sprite.Sprite(player_image, x=500, y=100, batch=main_batch)
stats_bg = pyglet.sprite.Sprite(stats_bg_image, x=980, y=300, batch=main_batch)
stats_bg.opacity = 10
# endregion

#explosion = pyglet.media.StaticSource(pyglet.media.load('../res/sounds/exp_01.wav', streaming=False))
explosion = pyglet.media.load('res/sounds/exp_01.wav', streaming=False)
player_gun_sound = pyglet.media.load('res/sounds/player_gun.wav', streaming=False)

player_laser_list = []
enemy_laser_list = []
enemy_list = []
bg_list = []
explosion_list = []

# when creating a new enemy, it will choose a random direction from the list below
directions = [1, -1]

player_speed = 300
left = False
right = False
destroyed_enemies = 0 # this for only stats
next_wave = 0
score = 0
fire = False
player_fire_rate = 0
enemy_fire_rate = 0
ufo_head_spawner = 0
enemy_ship_spawner = 0
ufo_head_spawner_count = 1
enemy_ship_spawner_count = 5
preloaded =  False
player_health = 5
player_is_alive = True
explode_time = 2
enemy_explode = False
shake_time = 0
game = False
flash_time = 1
player_flash = False

@window.event
def on_draw():
    window.clear()
    if not preloaded:
        preload()
    for bg in bg_list:
        bg.draw()
    if game:
        main_batch.draw()
    else:
        intro_text.draw()
    if not player_is_alive:
        game_over_text.draw()
        reload_text.draw()
    fps_display.draw()

def reload():
    global player_is_alive, next_wave, score, destroyed_enemies, player_fire_rate, enemy_fire_rate, explode_time
    global ufo_head_spawner, enemy_ship_spawner, ufo_head_spawner_count, enemy_ship_spawner_count, player_health
    global enemy_explode, shake_time, high_score
    next_wave = 0
    score = 0
    player_health = 5
    player_fire_rate = 0
    enemy_fire_rate = 0
    ufo_head_spawner = 0
    enemy_ship_spawner = 0
    ufo_head_spawner_count = 1
    enemy_ship_spawner_count = 5
    explode_time = 2
    enemy_explode = False
    shake_time = 0
    destroyed_enemies = 0
    player_is_alive = True
    player.x, player.y = 500, 100
    player.batch = main_batch

    # reload the score from the score text file
    high_score = load_high_score("res/score.txt")
    high_score_value.text = high_score

    num_enemies_destroyed.text = str(destroyed_enemies)
    num_score.text = str(score)
    numb_player_health.text = str(player_health)

    for obj in enemy_list:
        obj.batch = None
    for obj in enemy_laser_list:
        obj.batch = None
    enemy_list.clear()
    enemy_laser_list.clear()

@window.event
def on_key_press(symbol, modifiers):
    global  right, left, fire, game
    if symbol == key.RIGHT:
        right = True
    if symbol == key.LEFT:
        left = True
    if symbol == key.SPACE:
        fire = True
        if not game:
            game = True
            fire = False # to prevent firing when the game starts
    if symbol == key.R:
        reload()

@window.event
def on_key_release(symbol, modifiers):
    global right, left, fire
    if symbol == key.RIGHT:
        right = False
    if symbol == key.LEFT:
        left = False
    if symbol == key.SPACE:
        fire = False

def player_move(entity, dt):
    if right and entity.x < 1000:
        entity.x += player_speed * dt
    if left and entity.x > 100:
        entity.x -= player_speed * dt

# this function runs only once, it loads two background images at the start
def preload():
    global preloaded
    for i in range(2):
        bg_list.append(pyglet.sprite.Sprite(space, x=0, y=i*1200))
    preloaded = True

def bg_move(dt):
    for bg in bg_list:
        bg.y -= 50*dt
        if bg.y <= -1300:
            bg_list.remove(bg)
            bg_list.append(pyglet.sprite.Sprite(space, x=0, y=1100))

def enemy_move(enemies, yspeed, dt):
    global score
    for enemy in enemies:
        if enemy.x >= 1000:
            enemy.x = 1000
            enemy.speed *= -1
        if enemy.x <= 100:
            enemy.x = 100
            enemy.speed *= -1
        enemy.y -= yspeed*dt
        enemy.x += enemy.speed * dt
        if enemy.y <= 450 and enemy.y >= 449.4 and player_is_alive:
            score -= 1
            num_score.text = str(score)
        if enemy.y <= -100:
            enemies.remove(enemy)

def enemy_spawn(dt):
    global ufo_head_spawner, enemy_ship_spawner, player_is_alive, ufo_head_spawner_count, enemy_ship_spawner_count
    global next_wave
    ufo_head_spawner -= dt
    enemy_ship_spawner -= dt
    if player_is_alive:
        if ufo_head_spawner <= 0:
            enemy_list.append(pyglet.sprite.Sprite(ufo_head_anim, x=600, y=950, batch=main_batch))
            enemy_list[-1].speed = randint(100, 300) * choice(directions) # last spawned entity in entity list
            enemy_list[-1].hit_count = 0
            enemy_list[-1].MAX_HIT = 2
            ufo_head_spawner += ufo_head_spawner_count
        if enemy_ship_spawner <= 0:
            enemy_list.append(pyglet.sprite.Sprite(enemy_ship_anim, x=600, y=950, batch=main_batch))
            enemy_list[-1].speed = randint(100, 300) * choice(directions)  # last spawned entity in entity list
            enemy_list[-1].hit_count = 0
            enemy_list[-1].MAX_HIT = 8
            enemy_ship_spawner += enemy_ship_spawner_count
    if next_wave >= 20:
        ufo_head_spawner_count -= 0.05
        enemy_ship_spawner_count -= 0.2
        next_wave = 0

def enemy_shoot(dt):
    global enemy_fire_rate
    enemy_fire_rate -= dt
    if enemy_fire_rate <= 0:
        for enemy in enemy_list:
            if randint(0, 10) >= 5:
                enemy_laser_list.append(pyglet.sprite.Sprite(enemy_laser, enemy.x + 50, enemy.y, batch=main_batch))
        enemy_fire_rate += 5

def update_enemy_shoot(dt):
    for lsr in enemy_laser_list:
        lsr.y -= 400 * dt
        if lsr.y < -50: # if the lasers y position is belov -100 it gets removed from the laser list
            enemy_laser_list.remove(lsr)

def player_shoot(dt):
    global player_fire_rate
    player_fire_rate -= dt
    if player_fire_rate <= 0:
        player_laser_list.append(pyglet.sprite.Sprite(player_laser, player.x + 32, player.y + 96, batch=main_batch))
        player_fire_rate += 0.2
        if player_is_alive:
            player_gun_sound.play()

def update_player_shoot(dt):
    for lsr in player_laser_list:
        lsr.y += 400 * dt
        if lsr.y > 950: # if the lasers y position is above 950 it gets removed from the laser list
            player_laser_list.remove(lsr)

def screen_shake():
    global shake_time, enemy_explode
    shake_time -= 0.1
    x = randint(-10, 10)
    if shake_time <= 0:
        bg_list[0].x = x
        bg_list[1].x = x
        shake_time += 0.11
    elif shake_time >= 0:
        bg_list[0].x = 0
        bg_list[1].x = 0
        enemy_explode = False

def enemy_hit(entity):
    global destroyed_enemies, score, next_wave, enemy_explode
    entity.hit_count += 1
    if entity.hit_count >= entity.MAX_HIT and player_is_alive:
        enemy_explode = True
        explosion_list.append(pyglet.sprite.Sprite(xplosion_anim, x=entity.x, y=entity.y, batch=main_batch))
        enemy_list.remove(entity)  # remove the enemy from enemy list when gets shot two times
        #entity.batch = None # remove the enemy from the main batch
        entity.delete() # here it works,  but in test_02_batcher_tester.py often gives error???
        explosion.play()
        destroyed_enemies += 1 # this only for displaying the stats
        next_wave += 1
        score += 1
        num_enemies_destroyed.text = str(destroyed_enemies)
        num_score.text = str(score)

def player_hit():
    global player_health, numb_player_health, player_flash
    player_health -= 1
    numb_player_health.text = str(player_health)
    player_flash = True
    if player_health <= 0:
        player.batch = None
        game_over()

def update_flash():
    global flash_time, player_flash
    flash_time -= 0.2
    player.color = (255, 0, 0)
    if flash_time <= 0:
        player.color = (255, 255, 255)
        flash_time = 1
        player_flash = False

def update_explosion():
    global explode_time
    explode_time -= 0.1
    if explode_time <= 0:
        for exp in explosion_list:
            explosion_list.remove(exp)
            exp.delete()
        explode_time += 2

def game_over():
    global player_is_alive
    player_is_alive = False
    if score > int(high_score):
        save_high_score('res/score.txt', score)

def bullet_collision(entity, bullet_list):
    for lsr in bullet_list:
        if lsr.x < entity.x + entity.width and lsr.x + lsr.width > entity.x \
                and lsr.y < entity.y + entity.height and lsr.height + lsr.y > entity.y:
            bullet_list.remove(lsr)  # remove the laser from laser list when colliding with an enemy
            return True

def update(dt):
    if game:
        player_move(player, dt)
        enemy_move(enemy_list, 30, dt)
        if fire:
            player_shoot(dt)
        update_player_shoot(dt)
        enemy_shoot(dt)
        update_enemy_shoot(dt)
        for entity in enemy_list:
            if bullet_collision(entity, player_laser_list):
                enemy_hit(entity)
        if bullet_collision(player, enemy_laser_list) and player_is_alive:
            player_hit()
        if player_flash:
            update_flash()
        update_explosion()
        enemy_spawn(dt)
        if enemy_explode:
            screen_shake()
    bg_move(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
