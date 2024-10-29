from .entity import Entity
from .environment import Constants as const
from sensors import Sensors
from random import getrandbits
from fuzzyControl import control_movement


class Car(Entity, Sensors):
    def __init__(self, image, dims, coords, speed):
        super().__init__(image, dims, coords, speed)
        self.front_x_coords = self.x + self.width//2

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

    def controller(self, d_y, d_x_r, d_x_l):
        
        '''# FIXME esta mierda
        print(d_y, d_x_r, d_x_l)
        if None in d_y:
            d_y = [25 if x is None else x for x in d_y] 
        elif None in d_x_r:
            d_x_r = [10 if x is None else x for x in d_x_r] 
        elif None in d_x_l:
            d_x_l = [10 if x is None else x for x in d_x_l] '''
        print(d_y, d_x_r, d_x_l)
        move = control_movement(d_y, d_x_r, d_x_l)
        int_move = int(move)
        print(int_move)

        if int_move > 0:
            self.move_right(times=abs(int_move))
        elif int_move < 0:
            self.move_left(times=abs(int_move))
            #print('right')


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
