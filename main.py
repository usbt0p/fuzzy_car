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
    car_y = const.SCREEN_HEIGHT - const.CAR_HEIGHT - 80
    car = Car(car_img, (const.CAR_WIDTH, const.CAR_HEIGHT),
                (car_x, car_y), 1, controller)

    # decalre list(Obstacle()) and simulation constants
    obstacles = []
    score = 0
    running = True
    Entity._hitbox = False
    if ('-h' in commands) or ('--show-hitbox' in commands):
        Entity._hitbox = True

    clock = pg.time.Clock()  # time variables, FPS rate is in entorno.py
    start_time = pg.time.get_ticks()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(clrs.GRAY)
        monitor.draw_road(screen)

        # activate sensors
        dist_y, dist_right, dist_left = car.get_sensor_measurings(obstacles)
        
        # TODO mejora de rendimiento -> hacerlo cada x frames en vez de cada frame
        nearest_obstacles = car.find_nearest_obstacles(
            obstacles, dist_y, dist_right, dist_left)
        
        if nearest_obstacles: # FIXME este parche
            car.control_system(dist_y, dist_right, dist_left)

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

        monitor.display_monitor_text(screen, score)

        pg.display.flip()
        clock.tick(const.FPS)

    monitor.endgame_text(screen, score, start_time)

    pg.display.flip()
    pg.time.wait(2500)  # Display final screen for 1 seconds

    pg.quit()


if __name__ == "__main__":
    # Valores por defecto: FPS 20, Velocidad objetos 10, mom, steering universe norm 6
    # otros valores: FPS 30, Velocidad objetos 7, mom, steering universe norm 5
    simulate()
