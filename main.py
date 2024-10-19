import pygame as pg
from entornoEntidades.coche import Coche
import monitor
from entornoEntidades.entorno import Constants as const
from entornoEntidades.entorno import Colors as clrs
from entornoEntidades.entorno import Entorno
from monitor import car_img, obstacle_img


# Initialize pg
pg.init()

# Set up the display
screen = pg.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pg.display.set_caption("Simulador de Control de coche con lógica difusa")

# Simulation loop

def simulate():

    # initialize car position and car object
    car_x = (const.SCREEN_WIDTH - const.CAR_WIDTH) // 2
    car_y = const.SCREEN_HEIGHT - const.CAR_HEIGHT - 10
    car = Coche(car_img, (const.CAR_WIDTH, const.CAR_HEIGHT),
                (car_x, car_y), 25)

    # decalre list(Obstacle()) and simulation constants
    obstacles = []
    score = 0
    running = True

    clock = pg.time.Clock()  # time variables, FPS rate is in entorno.py
    start_time = pg.time.get_ticks()
    last_time = start_time
    time_offset = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(clrs.GRAY)
        monitor.draw_road(screen)

        last_time, time_offset = Entorno.moveInTimeIntervals(
            car, time_offset, start_time, last_time)
        car.draw(screen)

        score = Entorno.spawn_despawn_obstacles(
            obstacles, obstacle_img, score)
        # simulation can theoretically handle several objects at once
        for obstacle in obstacles:
            obstacle.draw(screen)

        collision = Entorno.obstacle_collisions(obstacles, car)
        if collision:
            running = False

        # activate sensors and draw them on the screen
        d_y = car.obstacle_sensor_y_axis(obstacles)
        d_x_r = car.obstacle_sensor_right(obstacles)
        d_x_l = car.obstacle_sensor_left(obstacles)

        for obstacle, d_y, d_x_r, d_x_l in zip(obstacles, d_y, d_x_r, d_x_l):
            monitor.draw_y_sensor(screen, car, obstacle, d_y)
            monitor.draw_right_sensor(screen, car, obstacle, d_x_r)
            monitor.draw_left_sensor(screen, car, obstacle, d_x_l)

        monitor.display_monitor_text(screen, score)

        pg.display.flip()
        clock.tick(const.FPS)

    monitor.endgame_text(screen, score, start_time)

    pg.display.flip()
    pg.time.wait(2500)  # Display final screen for 1 seconds

    pg.quit()


if __name__ == "__main__":
    simulate()
