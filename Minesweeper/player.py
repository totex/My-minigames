import pygame

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 24)

class Player:
    def __init__(self):
        self.health = 5

    def sub_health(self):
        self.health -= 1

    def get_health(self):
        return self.health


class Stats:
    @staticmethod
    def draw(surface, label, pos):
        textsurface = myfont.render(label, False, (255, 255, 255))
        surface.blit(textsurface, (pos[0], pos[1]))
