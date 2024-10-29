import pygame as pg
from elements.car import Car
import monitor
from elements.environment import Constants as const
from elements.environment import Colors as clrs
from elements.environment import Environment
from monitor import car_img, obstacle_img
from fuzzy import FuzzyControl


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
    car_y = const.SCREEN_HEIGHT - const.CAR_HEIGHT - 20
    car = Car(car_img, (const.CAR_WIDTH, const.CAR_HEIGHT),
                (car_x, car_y), 1, controller)

    # decalre list(Obstacle()) and simulation constants
    obstacles = []
    score = 0
    running = True

    clock = pg.time.Clock()  # time variables, FPS rate is in entorno.py
    start_time = pg.time.get_ticks()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(clrs.GRAY)
        monitor.draw_road(screen)

        # activate sensors and draw them on the screen
        d_y = car.obstacle_sensor_y_axis(obstacles) # TODO eventually move this to car.control_system
        d_x_r = car.obstacle_sensor_right(obstacles)
        d_x_l = car.obstacle_sensor_left(obstacles)
        
        if obstacles: # FIXME este parche
            car.control_system(d_y, d_x_r, d_x_l)
            #control_movement(d_y, d_x_l, d_x_r)

        car.manual_control(7) # for demo purposes, it can be ignored
        
        car.draw(screen)

        score = Environment.spawn_despawn_obstacles(
            obstacles, obstacle_img, score, mode='multi_random')
        # simulation can theoretically handle several objects at once
        for obstacle in obstacles:
            obstacle.draw(screen)

        for obstacle, d_y, d_x_r, d_x_l in zip(obstacles, d_y, d_x_r, d_x_l):
            monitor.draw_y_sensor(screen, car, obstacle, d_y)
            monitor.draw_right_sensor(screen, car, obstacle, d_x_r)
            monitor.draw_left_sensor(screen, car, obstacle, d_x_l)

        collision = Environment.obstacle_collisions(obstacles, car)
        if collision:
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
