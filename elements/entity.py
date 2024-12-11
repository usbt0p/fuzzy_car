from .environment import Colors as clrs
from .environment import Constants as const
import pygame as pg


class Entity:

    _hitbox = False  

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
                screen, 
                clrs.RED, 
                # upper left corner 
                (self.x + const.ROAD_ORIGIN_X, 
                 self.y + const.ROAD_ORIGIN_Y, 
                 self.width, 
                 self.height) # lower right corner
            )
        else:
            screen.blit(self.image, 
                (self.x + const.ROAD_ORIGIN_X, 
                self.y + const.ROAD_ORIGIN_Y)
                )

        if Entity._hitbox:
            pg.draw.rect(
                    screen, 
                    clrs.GREEN, 
                    (self.x + const.ROAD_ORIGIN_X, 
                     self.y + const.ROAD_ORIGIN_Y, 
                    self.width, 
                    self.height), 
                    1)
            

if __name__ == '__main__':

    def test_hitbox_change():
        pass

            


