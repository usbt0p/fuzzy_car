from .entity import Entity
from .environment import Constants as const
from sensors import Sensors
from random import getrandbits
from fuzzyControl import control_movement
from fuzzy import FuzzyControl
import pygame as pg

class Car(Entity, Sensors):
    def __init__(self, image : pg.image , dims : tuple, coords : tuple, 
                 speed : int, controller : FuzzyControl):

        super().__init__(image, dims, coords, speed)
        self.front_x_coords : int = self.x + self.width//2
        self.controller : FuzzyControl = controller

    def move_left(self, times=1):
        if self.x > (const.SCREEN_WIDTH - const.ROAD_WIDTH) // 2:
            self.x -= self.speed * times
            self.front_x_coords -= self.speed * times

    def move_right(self, times=1):
        if self.x < (const.SCREEN_WIDTH + const.ROAD_WIDTH) // 2 - self.width:
            self.x += self.speed * times
            self.front_x_coords += self.speed * times

    def random_walk(self):
        direction = bool(getrandbits(1))
        if direction:
            self.move_left()
        else:
            self.move_right()
    
    def manual_control(car, amount):
        # legacy for manual car movement
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            car.move_left(amount)
        if keys[pg.K_RIGHT]:
            car.move_right(amount)

    def control_system(self, d_y, d_x_r, d_x_l):
        '''Provides the needed logic to connect the sensors
        to the fuzzy control system. These are tha steps:
        1. Get the distance from the sensors
        2. Pass the distance to the controller
        3. Get the output from the controller
        4. Move the car according to the output
        '''
        # TODO por ahora esta funcion recibe las distancias de los sensores
        # la idea es en el futuro abstraer esto y que directamente se llame a los
        # sensores desde aqui, con lo que la funcion recibirá la lista de obstáculos 
        # del entorno

        # take the side measurements from the sensors and pass the proper one to the controller
        move_right = True

        if d_x_r < d_x_l:
            move_right = True
            side_move = d_x_r
        else:
            move_right = False
            side_move = d_x_l

        move_amount = int(
            self.controller.side_controller(side_move, d_y, debug=False))

        if move_right:
            self.move_right(times=move_amount)
        else:
            self.move_left(times=move_amount)


# TODO pasar distancia de pg a metros
# TODO crear una función de nearest_point? para que no vaya al centro, si no
# al punto más cercano del obstáculo, como un sensor real...


if __name__ == '__main__':
    car = Car(None, (50, 100), (200, 200), 20)
    print(car.__dict__)
    # print(dir(car))
    method_list = [
        func for func in dir(car) if
        callable(getattr(car, func)) and not func.startswith("__")
    ]
    print(method_list)
