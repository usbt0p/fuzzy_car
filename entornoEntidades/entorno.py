import pygame as pg
from random import getrandbits, randint


class Constants:
    # Dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    ROAD_WIDTH = 400
    FPS = 30  # Reduced frame rate

    CAR_WIDTH = 75
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


class Entorno:
    def __init__(self, constants: Constants, colors: Colors):
        self.const = constants
        self.colors = colors

    def moveInTimeIntervals(car, time_offset, start_time, last_time):

        if time_offset:
            last_time = (pg.time.get_ticks() - start_time) / 1000
            time_offset = False

        now = (pg.time.get_ticks() - start_time) / 1000

        if (now) > (last_time + 0.01):
            # hace un random walk hacia los lados cada 0.007ms
            # si se cambia la resolucion en now y last time se mueve mas fluido

            direction = bool(getrandbits(1))
            if direction:
                car.move_left()
            else:
                car.move_right()

            time_offset = True

        return last_time, time_offset

    def manual_control(car):
        # legacy for manual car movement
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            car.move_left()
        if keys[pg.K_RIGHT]:
            car.move_right()

    def spawn_despawn_obstacles(obstacles, img, score):
        # BUG weird aah circular import issue will give error for this function
        # obscatulo.py calls from .entorno import Constants as const
        # entorno.py calls from entornoEntidades.obstaculo import Obstaculo
        # therefore one must call the other, cycle in dependency tree leads to error
        from entornoEntidades.obstaculo import Obstaculo

        """if random.randint(1, 50) == 1:  # Adjusted obstacle frequency
            obstacles.append(Obstacle())"""

        # make them appear only one at a time constantly
        if not obstacles:

            rand_x = randint(
                (Constants.SCREEN_WIDTH - Constants.ROAD_WIDTH) // 2,
                (Constants.SCREEN_WIDTH + Constants.ROAD_WIDTH) // 2 - Constants.OBSTACLE_WIDTH)

            obs = Obstaculo(img,
                            (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT),
                            (rand_x, -Constants.OBSTACLE_HEIGHT), 10)

            obstacles.append(obs)

        for obstacle in obstacles[:]:
            obstacle.move() # we don't draw here, not the job of entorno.py
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
                score += 1
        return score

    def obstacle_collisions(obstacles, car):
        for obstacle in obstacles:
            if obstacle.check_collision(car):
                return True  # para running = False
            else:
                return False


if __name__ == '__main__':
    e = Entorno(Constants, Colors)
    print(e.const.FPS)
    print(e.colors.BLACK)
