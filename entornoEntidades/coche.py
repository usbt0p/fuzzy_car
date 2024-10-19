from .entidad import Entidad
from .entorno import Constants as const
from sensores import Sensores


class Coche(Entidad, Sensores):
    def __init__(self, image, dims, coords, speed):
        super().__init__(image, dims, coords, speed)
        self.front_x_coords = self.x + self.width//2

    def move_left(self):
        if self.x > (const.SCREEN_WIDTH - const.ROAD_WIDTH) // 2:
            self.x -= self.speed
            self.front_x_coords -= self.speed

    def move_right(self):
        if self.x < (const.SCREEN_WIDTH + const.ROAD_WIDTH) // 2 - self.width:
            self.x += self.speed
            self.front_x_coords += self.speed

# TODO pasar distancia de pg a metros
# TODO crear una función de nearest_point? para que no vaya al centro, si no
# al punto más cercano del obstáculo, como un sensor real...


if __name__ == '__main__':
    car = Coche(None, (50, 100), (200, 200), 20)
    print(car.__dict__)
    # print(dir(car))
    method_list = [
        func for func in dir(car) if
        callable(getattr(car, func)) and not func.startswith("__")
    ]
    print(method_list)
