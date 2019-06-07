import pygame
from board import Grid
from player import Player, Stats
from enum import Enum, auto

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,100)

surface = pygame.display.set_mode((1200, 900))
pygame.display.set_caption('Minesweeper')


class States(Enum):
    running = auto()
    game_over = auto()
    win = auto()

state = States.running

player = Player()
grid = Grid(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and state == States.running:
            if pygame.mouse.get_pressed()[0]: # check for the left mouse button
                pos = pygame.mouse.get_pos()
                grid.click(pos[0], pos[1])
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                grid.mark_mine(pos[0]//30, pos[1]//30)
            if grid.check_if_win():
                state = States.win
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (state == States.game_over or state == States.win):
                grid.reload()
                state = States.running
            if event.key == pygame.K_b:
                grid.show_mines()

    surface.fill((0,0,0))

    if player.get_health() == 0:
        state = States.game_over

    if state == States.game_over:
        Stats.draw(surface, 'Game over!', (970, 350))
        Stats.draw(surface, 'Press Space to restart', (920, 400))
    elif state == States.win:
        Stats.draw(surface, 'You win!', (1000, 350))
        Stats.draw(surface, 'Press Space to restart', (920, 400))

    grid.draw(surface)
    Stats.draw(surface, 'Lives remaining', (950, 100))
    Stats.draw(surface, str(player.get_health()), (1020, 200))
    Stats.draw(surface, 'RMB to mark mine', (950, 550))
    Stats.draw(surface, 'press b to show mines', (920, 650))

    pygame.display.flip()
