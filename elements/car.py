from .entity import Entity
from .environment import Constants as const
from sensors import Sensors
from random import getrandbits
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
        to the fuzzy control system. These are the steps:
        1. Get the distance from the sensors
        2. Pass the distance to the controller
        3. Get the output from the controller
        4. Move the car according to the output
        '''
        # TODO por ahora esta funcion recibe las distancias de los sensores
        # la idea es en el futuro abstraer esto y que directamente se llame a los
        # sensores desde aqui, con lo que la funcion recibirá la lista de obstáculos 
        move_right = True 
        for y, r, l in zip(d_y, d_x_r, d_x_l):
            # take the side measurements from the sensors and pass the proper one to the controller
                           
            # a sensor will pass None if there is no obstacle in that direction
            if l is None:
                move_right = True
                side_move = r
            elif r is None:
                move_right = False
                side_move = l
            else:
                # this means the obstacle is exactly in front of the car
                # the order of the rules will determine what is done in this case
                # also the last movement, since move_right will've been set 
                side_move = 0
                print(f'Warning: object right in the middle! (Y: {y}, R: {r}, L: {l})')
                print('Movement will be determined by the last movement.')
                print('Last movement: move_right=', move_right)
                

            move_amount = int(
                self.controller.side_controller(side_move, y, debug=False))

            if move_right:
                self.move_right(times=move_amount)
            else:
                self.move_left(times=move_amount)

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
