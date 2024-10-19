from .environment import Colors as clrs
import pygame as pg


class Entity:
    def __init__(self, image, dims, coords, speed):
        self.image = image
        self.width = dims[0]
        self.height = dims[1]
        self.x = coords[0]
        self.y = coords[1]
        self.speed = speed  # could vary between horizontal and vertical

    def draw(self, screen):
        if self.image is None:
            pg.draw.rect(
                screen, clrs.RED, (self.x, self.y, self.width, self.height))
        else:
            screen.blit(self.image, (self.x, self.y))
