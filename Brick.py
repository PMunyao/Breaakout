import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# brick class
class Brick(Sprite):
    def __init__(self, x, y, width, height, color):
        Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y