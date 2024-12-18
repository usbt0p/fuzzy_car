import pygame as pg
from random import randint
from typing import List

class Constants:
    # Dimensions
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 680
    ROAD_WIDTH = 600
    FPS = 40  # Reduced frame rate

    CAR_WIDTH = 45
    CAR_HEIGHT = 90
    OBSTACLE_WIDTH = 70
    OBSTACLE_HEIGHT = 55
    MAX_OBSTACLES = 5
    SPAWN_RATE_INVERSE = 50 # 1 out of 50 chance of spawning an obstacle


class Colors:
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    DARK_GRAY = (40, 40, 40)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (130, 130, 0)


class Environment:

    _spawn_alternate = True # Para el modo de obstáculos alternos

    def __init__(self, constants: Constants, colors: Colors):
        self.const = constants
        self.colors = colors # TODO arerglar esto: todos estan accediendo directamente 
        # a colors y constants cuando deberían acceder a self.colors y self.const
        # TODO self.obstacles = [] # y todos los cambios que esto conlleve

    @staticmethod
    def pause_with_key(event, key):
        if event.key == key:
            flag = True
            while flag:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == key:
                            flag = False
                    elif event.type == pg.QUIT:
                        pg.quit()
                        exit()

    @staticmethod
    def moveInTimeIntervals(car, time_offset, start_time, last_time):
        '''Legacy method for moving the car + doing other stuff in intervals'''
        if time_offset:
            last_time = (pg.time.get_ticks() - start_time) / 1000
            time_offset = False

        now = (pg.time.get_ticks() - start_time) / 1000

        if (now) > (last_time + 0.01):
            #do stuff here
            time_offset = True

        return last_time, time_offset

    @staticmethod
    def spawn_despawn_obstacles(
        obstacles : List, img : pg.image, score : int, mode : str, **kwargs) ->  int:
        """
        Modifies the passed obstacle list to spawn obstacles according to the 
        given `mode` parameter. Returns the score (number of obstacles that got offscreen 
        aka. despawned, without collisions). 
    
        Parameters
        ----------
        `mode` : str
            The spawn conditions to enforce when spawning. 
            
            Possible values are:
            `{'single_random', 'multi_random', 'multi_random_balanced', 'alternate', 'front_of_car'}`
        `**kwargs` : dict
            Additional keyword arguments to pass to the function. 
            Required when `mode` is 'front_of_car', must contain the car object.
        
        Returns
        -------
        int
            The updated score value after despawning cleared obstacles.
        
        """
        # weird circular import issue will give error for this function
        # obstacle.py calls from .entorno import Constants as const
        # environment.py calls from elements.obstacle import Obstacle
        # therefore one must call the other, cycle in dependency tree leads to error
        from .obstacle import Obstacle

        # make them appear only one at a time constantly
        if mode == 'single_random':
            if not obstacles:

                rand_x = randint(
                    (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2,
                    (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH) // 2 - Constants.OBSTACLE_WIDTH)

                new_obs = Obstacle(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (rand_x, -Constants.OBSTACLE_HEIGHT), 10)

                obstacles.append(new_obs)

        elif mode == 'multi_random':
            rand_x = randint(
                (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2,
                (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH) // 2 - Constants.OBSTACLE_WIDTH)
        
            if randint(1, 50) == 1:  # Adjusted obstacle frequency
                obstacles.append(Obstacle(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (rand_x, -Constants.OBSTACLE_HEIGHT), 7))

        elif mode == 'multi_random_balanced':
            
            # ensure no more than 5 obstacles are on screen
            if len(obstacles) < Constants.MAX_OBSTACLES:
                

                rand_x = randint(
                        (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2,
                        (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH) // 2 - Constants.OBSTACLE_WIDTH)
                y = -Constants.OBSTACLE_HEIGHT 

                new_obs = Obstacle(img,
                                (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                                (rand_x, y), 7)

                def no_obstacle_overlap(obstacle):
                    toret = True

                    for obs in obstacles: 
                        # esto solo comprueba los que están en el cuarto superior de la pantalla
                        if obs.y < Constants.SCREEN_HEIGHT // 4:  
                            if obstacle.check_collision(obs): 
                                toret = False
                                break
                    return toret
                

                if (no_obstacle_overlap(new_obs) and randint(1, Constants.SPAWN_RATE_INVERSE)) == 1:  
                    # Adjusted obstacle frequency
                    obstacles.append(new_obs)

        elif mode == 'alternate': # para testear moverse a derecha e izquierda
            if not obstacles:

                if Environment._spawn_alternate:
                    x = (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH
                            ) // 2 - Constants.OBSTACLE_WIDTH - 50
                        
                    Environment._spawn_alternate = False
                else: 
                    x = (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2 +50
                    Environment._spawn_alternate = True

                new_obs = Obstacle(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (x, -Constants.OBSTACLE_HEIGHT), 10)

                obstacles.append(new_obs)
        
        elif mode == 'front_of_car':
            car = kwargs['car'] 
            if not obstacles:
                new_obs = Obstacle(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (car.x, -Constants.OBSTACLE_HEIGHT), 7)
                print('obstacle x: ', new_obs.x, ', car x: ', car.x)
                obstacles.append(new_obs)

        for obstacle in obstacles[:]:
            obstacle.move()  # we don't draw here, not the job of entorno.py
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
                score += 1
        return score

    def obstacle_collisions(obstacles, car):
        for obstacle in obstacles:
            if obstacle.check_collision(car):
                return True  # if collision then; running = False
            else:
                return False


if __name__ == '__main__':
    from monitor import obstacle_img
    from obstacle import Obstacle

    e = Environment(Constants, Colors)
    print(e.const.FPS)
    print(e.colors.BLACK)

    ## TEST
    obstacles = []
    img = obstacle_img
    score = 0
    mode = 'multi_random_balanced'

    # This should lead to no obstacle spawning (obstacle list lenght remains 1) spawning
    obs = Obstacle(img,
                    (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                    (0, -Constants.OBSTACLE_HEIGHT), 7)
    bad_spawn = [obs]

    e.spawn_despawn_obstacles(obstacles, img, score, mode)
    assert len(obstacles) == 1, 'No obstacles must spawn if there is a collision between them'

    obs.y = 200
    good_spawn = [obs]

