from .entity import Entity
from .environment import Constants as const
from sensors import Sensors
from fuzzy import FuzzyControl
import pygame as pg
from scipy.spatial.distance import cdist

class Car(Entity, Sensors):
    def __init__(self, image : pg.image , dims : tuple, coords : tuple, 
                 speed : int, controller : FuzzyControl):

        super().__init__(image, dims, coords, speed)
        self.front_x_coords : int = self.x + self.width//2
        self.controller : FuzzyControl = controller
        # car will only apply the controller to the nearest obstacles
        self.k_nearest = 3

    def move_left(self, times=1):
        if self.x > (const.SCREEN_WIDTH - const.ROAD_WIDTH) // 2:
            self.x -= self.speed * times
            self.front_x_coords -= self.speed * times

    def move_right(self, times=1):
        if self.x < (const.SCREEN_WIDTH + const.ROAD_WIDTH) // 2 - self.width:
            self.x += self.speed * times
            self.front_x_coords += self.speed * times

    def random_walk(self):
        from random import getrandbits
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

    def get_sensor_measurings(self, obstacles) -> tuple[list[int]]:
        """Gets measurements from the sensors.
        - Return order: `(y, right, left, center)`
        """
        dist_y = self.obstacle_sensor_y_axis(obstacles)
        dist_right = self.obstacle_sensor_right(obstacles)
        dist_left = self.obstacle_sensor_left(obstacles)
        dist_center = self.relative_road_location()

        return dist_y, dist_right, dist_left, dist_center

    def find_nearest_obstacles(self, obstacles : list, 
                        y_array : list, right : list, left : list) -> list:
        '''Returns the k nearest obstacles to the car.
        - The obstacles must be a list of Obstacle objects.
        - The k_nearest attribute must be set before calling this function.
        - `y_array` , `right` and `left` are the sensor measurings.
        '''
        if len(obstacles) < self.k_nearest:
            return obstacles

        nearest_list = []

        # cdist takes 2-D arrays, we must create one for each measuring        
        # we must unify the left and right distances from the sensor into a single one
        x_array = []
        for dists in zip(right, left):
            if dists[0] is None:
                x_array.append(dists[1])
            elif dists[1] is None:
                x_array.append(dists[0])
            else:
                x_array.append(0) # when it's in the center

        # now we find de distance between each element and the car
        car_coords = [(0, 0) for _ in obstacles] # since the sensor measurings are relative to the car
        obs_coords = list(zip(x_array, y_array))
        euclidean_dists = cdist(
            obs_coords, car_coords, metric='euclidean')[:,0]
        
        # now it's time to return the k nearest obstacles:
        for _ in range(0, self.k_nearest):
            index = euclidean_dists.argmin()
            nearest_list.append(obstacles[index])
            euclidean_dists[index] = float('inf') # don't pick again

        return nearest_list

    def control_system(self, dist_y, dist_right, dist_left, dist_center):
        '''Provides the needed logic to connect the sensors
        to the fuzzy control system. These are the steps:
        1. Get the distance from the sensors
        2. Pass the distance to the controller
        3. Get the output from the controller
        4. Move the car according to the output
        '''
        move_amount = 0
        total_move = 0
        move_right = True 
        for y, r, l in zip(dist_y, dist_right, dist_left):
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
            total_move += move_amount

            if move_right:
                self.move_right(times=move_amount)
            else:
                self.move_left(times=move_amount)

        # TODO cambiar lógica de esto: move amount queda determinado por el último sensor
        if total_move == 0: # if there's no activation in the side controllers, return to center
                
            move_amount = int(self.controller.center_controller(dist_center))
            #print('movement on car: ', move_amount)
                        
            center = (const.SCREEN_WIDTH - const.CAR_WIDTH) // 2
            if self.front_x_coords > center:
                self.move_left(times=move_amount)
            elif self.front_x_coords < center:
                self.move_right(times=move_amount)
            else: 
                print(f'Unexpected value un center move: {self.front_x_coords}')

if __name__ == '__main__':
    # to run as a module:
    # python3 -m elements.car
    test = 'find_nearest_obstacles'

    car = Car(None, (0, 0), (300, 300), 20, None)
    '''print(car.__dict__)
    # print(dir(car))
    method_list = [
        func for func in dir(car) if
        callable(getattr(car, func)) and not func.startswith("__")
    ]
    print(method_list)'''

    from .obstacle import Obstacle
    
    print('car x: ', car.x, ', car.y: ', car.y)
    obs1 = Obstacle(None, (0, 0), (100, 100), 20)
    obs12 = Obstacle(None, (0, 0), (200, 200), 20)
    obs2 = Obstacle(None, (0, 0), (300, 300), 20)
    obs3 = Obstacle(None, (0, 0), (400, 400), 20)
    obs4 = Obstacle(None, (0, 0), (500, 500), 20)
    obstacles = [obs1, obs12, obs2, obs3, obs4]

    if test == 'get_sensor_measurings':
        print('\n Testing sensors: \n')
        sensor_output = car.get_sensor_measurings(obstacles)
        print(sensor_output)
        y, right, left = sensor_output
        print('y: ', y)
        print('right: ', right)
        print('left: ', left)

    elif test == 'find_nearest_obstacles':
        print('\n Testing nearest obstacles: \n')
        car.k_nearest = 3
        eucl_dist = car.find_nearest_obstacles(obstacles)
        _ = [print(obs.x, ',', obs.y) for obs in eucl_dist]

        # test k bigger than the number of obstacles
        obj_adresses = {id(obs): obs for obs in obstacles}
        print('Distinct objects', len(obj_adresses))
        print('Returned objects', len(eucl_dist))

        # TODO si funciona hay que dibujar los sensores solo para los 
        # k obstaculos pillados

        

