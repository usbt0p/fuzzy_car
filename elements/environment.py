import pygame as pg
from random import randint


class Constants:
    # Dimensions
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 680
    ROAD_WIDTH = 600
    FPS = 30  # Reduced frame rate

    CAR_WIDTH = 80
    CAR_HEIGHT = 85
    OBSTACLE_WIDTH = 60
    OBSTACLE_HEIGHT = 80


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
        

    def moveInTimeIntervals(car, time_offset, start_time, last_time):

        if time_offset:
            last_time = (pg.time.get_ticks() - start_time) / 1000
            time_offset = False

        now = (pg.time.get_ticks() - start_time) / 1000

        if (now) > (last_time + 0.01):
            #car.random_walk()


            time_offset = True

        return last_time, time_offset

    @staticmethod
    def spawn_despawn_obstacles(obstacles, img, score, mode):
        # BUG weird aah circular import issue will give error for this function
        # obscatulo.py calls from .entorno import Constants as const
        # entorno.py calls from entornoEntidades.obstaculo import Obstaculo
        # therefore one must call the other, cycle in dependency tree leads to error
        from .obstacle import Obstacle
        

        
        # TODO test
        # make them appear only one at a time constantly
        if mode == 'single_random':
            if not obstacles:

                rand_x = randint(
                    (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2,
                    (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH) // 2 - Constants.OBSTACLE_WIDTH)

                obs = Obstacle(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (rand_x, -Constants.OBSTACLE_HEIGHT), 10)

                obstacles.append(obs)

        elif mode == 'multi_random':
            rand_x = randint(
                (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2,
                (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH) // 2 - Constants.OBSTACLE_WIDTH)
        
            if randint(1, 50) == 1:  # Adjusted obstacle frequency
                obstacles.append(Obstacle(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (rand_x, -Constants.OBSTACLE_HEIGHT), 7))

        elif mode == 'alternate': # para testear moverse a derecha e izquierda
            if not obstacles:

                if Environment._spawn_alternate:
                    x = (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH
                            ) // 2 - Constants.OBSTACLE_WIDTH - 50
                        
                    Environment._spawn_alternate = False
                else: 
                    x = (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2 +50
                    Environment._spawn_alternate = True

                obs = Obstacle(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (x, -Constants.OBSTACLE_HEIGHT), 10)

                obstacles.append(obs)


        for obstacle in obstacles[:]:
            obstacle.move()  # we don't draw here, not the job of entorno.py
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
                score += 1
        return score

    # TODO test
    def obstacle_collisions(obstacles, car):
        for obstacle in obstacles:
            if obstacle.check_collision(car):
                return True  # para running = False
            else:
                return False


if __name__ == '__main__':
    # TODO test
    e = Environment(Constants, Colors)
    print(e.const.FPS)
    print(e.colors.BLACK)
