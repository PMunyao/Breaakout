import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# ball class
class Ball(Sprite):
    def __init__(self, x, y, width, height, color, speed, direction):
        Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = direction

    # function to move the ball
    def move(self):
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

    # function to bounce th eball off a surface after collision has occured
    def bounce(self, direction):
        if direction == 'x':
            self.direction = (self.direction[0] * -1, self.direction[1])
        elif direction == 'y':
            self.direction = (self.direction[0], self.direction[1] * -1)
        elif direction == 'xy':
            self.direction = (self.direction[0] * -1, self.direction[1] * -1)