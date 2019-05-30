import os
from random import randint


class Grid:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT  = HEIGHT
        self.grid = self.create()
        self.p_x = self.WIDTH // 2
        self.p_y = self.HEIGHT - 2
        self.set_player_pos(self.p_x, self.p_y)
        self.timer = 2
        self.catched = 0
        self.lost = 0

    def create(self):
        brd = []
        for h in range(self.HEIGHT):
            brd.append([])
            for w in range(self.WIDTH):
                if w < 1 or w == self.WIDTH-1:
                    brd[h].append('x')
                elif h == self.HEIGHT-1:
                    brd[h].append('x')
                else:
                    brd[h].append('.')
        return brd

    def draw(self):
        self.clear()
        for row in self.grid:
            for character in row:
                print(character, end='')
            print()
        print("Eggs catched: " + str(self.catched) + "    " + "Eggs lost: " + str(self.lost))

    def update(self):
        self.timer -= 0.5
        if self.timer < 0:
            self.add_egg(randint(1, self.WIDTH-2), 1)
            self.timer = randint(1, 5)

        self.move_eggs()

    def clear(self):
        os.system('cls') # only works with CMD and Powershell, doesn't work with Git-Bash

    def set_player_pos(self, x, y):
        self.p_x, self.p_y = x, y

    def get_player_pos(self):
        return self.p_x, self.p_y

    def set_cell(self, x, y, chr):
        self.grid[y][x] = chr

    def get_cell(self, x, y):
        return self.grid[y][x]

    def check_Hbounds(self, x):
        return x > 0 and x < self.WIDTH-1

    def check_Vbounds(self, y):
        return y >= 0 and y < self.HEIGHT-2

    def add_egg(self, x, y):
        self.grid[y][x] = 'o'

    def move_eggs(self):
        for y in range(len(self.grid)-1, 0, -1):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) == 'o' and self.check_Vbounds(y):
                    self.set_cell(x, y, '.')
                    self.set_cell(x, y+1, 'o')
                    if self.get_cell(x, y+2) == 'U':
                        self.catched += 1
                elif self.get_cell(x, y) == 'o':
                    self.set_cell(x, y, '.')
                    self.lost += 1

    