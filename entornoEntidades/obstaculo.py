from .entorno import Constants as const
from .entidad import Entidad


class Obstaculo(Entidad):
    def __init__(self, image, dims, coords, speed):
        super().__init__(image, dims, coords, speed)
        self.front_x_coords = self.x + self.width // 2

    def move(self):
        self.y += self.speed

    def is_off_screen(self):
        return self.y > const.SCREEN_HEIGHT

    def check_collision(self, car):
        if self.y + self.height > car.y and self.y < car.y + car.height:
            if self.x + self.width > car.x and self.x < car.x + car.width:
                return True
        return False
