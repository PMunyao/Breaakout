import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# paddle class
class Paddle(Sprite):
    def __init__(self, x, y, width, height, color, speed):
        Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    # function to register paddle movement
    def move(self, direction):
        if direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed