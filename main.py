from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from elements.car import Car
import monitor
from elements.environment import Constants as const
from elements.environment import Colors as clrs
from elements.environment import Environment
from elements.entity import Entity
from monitor import car_img, obstacle_img
from fuzzy import FuzzyControl
import sys

commands = set(sys.argv[1:])

# Initialize pg
pg.init()

# Set up the display
screen = pg.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pg.display.set_caption("Simulador de Control de coche con lógica difusa")

# Simulation loop

def simulate():
    
    # initialize car position and car object
    controller = FuzzyControl('mom') # controller with defuzzification method
    car_x = (const.SCREEN_WIDTH - const.CAR_WIDTH) // 2 
    car_y = const.SCREEN_HEIGHT - const.CAR_HEIGHT - 80 # modify this constant to adjust car height
    car = Car(car_img, (const.CAR_WIDTH, const.CAR_HEIGHT),
                (car_x, car_y), 1, controller)
    car.k_nearest = 2

    # decalre list(Obstacle()) and simulation constants
    obstacles = []
    const.MAX_OBSTACLES = 6
    score = 0
    running = True
    Entity._hitbox = False
    const.SPAWN_RATE_INVERSE = 30
    const.FPS = 30
    if ('-h' in commands) or ('--show-hitbox' in commands):
        Entity._hitbox = True

    clock = pg.time.Clock()  # time variables, FPS rate is in entorno.py
    start_time = pg.time.get_ticks()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                Environment.pause_with_key(event, pg.K_SPACE)

        screen.fill(clrs.GRAY)
        monitor.draw_road(screen, 3)

        # activate sensors
        dist_y, dist_right, dist_left, dist_center = car.get_sensor_measurings(obstacles)
        
        # TODO mejora de rendimiento -> hacerlo cada x frames en vez de cada frame
        nearest_obstacles = car.find_nearest_obstacles(
            obstacles, dist_y, dist_right, dist_left)
        
        car.control_system(dist_y, dist_right, dist_left, dist_center)

        car.manual_control(7) # for demo purposes; this can be commented if you don't want to control it
        
        car.draw(screen)

        score = Environment.spawn_despawn_obstacles(
            obstacles, obstacle_img, score, mode='multi_random_balanced')
        # simulation can handle several objects at once
        for obstacle in obstacles:
            obstacle.draw(screen)

        if ('-s' in commands) or ('--show-sensors' in commands):
            for obstacle, d_y, d_x_r, d_x_l in zip(
                    nearest_obstacles, dist_y, dist_right, dist_left):
                monitor.draw_y_sensor(screen, car, obstacle, d_y)
                monitor.draw_right_sensor(screen, car, obstacle, d_x_r)
                monitor.draw_left_sensor(screen, car, obstacle, d_x_l)

        collision = Environment.obstacle_collisions(obstacles, car)
        if collision:
            if ('-nc' in commands) or ('--no-collision' in commands):
                running = True
            running = False

        monitor.display_monitor_text(screen, score, clock.get_fps())

        pg.display.flip()
        clock.tick(const.FPS)

    if ('--ds-death' in commands):
        monitor.you_died(screen, score, start_time)
    else:
        monitor.endgame_text(screen, score, start_time)

    pg.display.flip()

    flag = True
    while flag: # pause until user presses a key or closes the window
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                flag = False
            elif event.type == pg.QUIT:
                pg.quit()
                exit()

    pg.quit()


if __name__ == "__main__":
    # Valores por defecto: FPS 20, Velocidad objetos 10, mom, steering universe norm 6
    # otros valores: FPS 30, Velocidad objetos 7, mom, steering universe norm 5
    simulate()
