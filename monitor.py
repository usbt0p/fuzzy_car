import pygame as pg
from elements.environment import Colors as clrs
from elements.environment import Constants as const

pg.font.init()

font = pg.font.Font(None, 36)
medium_font = pg.font.Font(None, 26)
distance_font = pg.font.SysFont(None, 20)

car_img = pg.image.load('imgs/white_car.png')
obstacle_img = pg.image.load('imgs/roadblock_yellow.png')

def draw_y_sensor(screen, car, obstacle, distance):

    pg.draw.line(screen, clrs.GREEN,
                 (car.front_x_coords, car.y),
                 (car.front_x_coords,
                  obstacle.y + obstacle.height), 2)

    pg.draw.line(screen, clrs.YELLOW,
                 (car.front_x_coords, car.y),
                 (obstacle.x + obstacle.width // 2,
                  obstacle.y + obstacle.height), 2)

    text_surface = distance_font.render(
        f'Y DIST: {distance}', False, clrs.WHITE)
    screen.blit(text_surface, (
        obstacle.x + obstacle.width, obstacle.y))


def draw_right_sensor(screen, car, obstacle, distance):

    if distance != None:
        pg.draw.line(screen, clrs.RED,
                     (car.front_x_coords, car.y),
                     (obstacle.front_x_coords,
                      car.y), 2)

    text_surface = distance_font.render(
        f'RIGHT DIST: {distance}', False, clrs.WHITE)
    screen.blit(text_surface, (
        obstacle.x + obstacle.width, obstacle.y + 20))


def draw_left_sensor(screen, car, obstacle, distance):

    if distance != None:
        pg.draw.line(screen, clrs.BLUE,
                     (car.front_x_coords, car.y),
                     (obstacle.front_x_coords,
                      car.y), 2)

    text_surface = distance_font.render(
        f'LEFT DIST: {distance}', False, clrs.WHITE)
    screen.blit(text_surface, (
        obstacle.x + obstacle.width, obstacle.y + 40))


def draw_road(screen, num_lanes):
    draw_coords = (const.SCREEN_WIDTH - const.ROAD_WIDTH)
    line_width = 12 #const.ROAD_WIDTH // 40
    line_separation = 50
    line_height = 30

    # asphalt
    pg.draw.rect(
        screen, clrs.DARK_GRAY, (draw_coords // 2, 0, const.ROAD_WIDTH, const.SCREEN_HEIGHT))

    # right line
    pg.draw.rect(
        screen, clrs.DARK_YELLOW, ((draw_coords//2)+10, 0, line_width, const. SCREEN_HEIGHT))
    # left line
    pg.draw.rect(
        screen, clrs.DARK_YELLOW, (
            (draw_coords//2)+(const.ROAD_WIDTH-20), 0, line_width, const.SCREEN_HEIGHT))
    
    road_x_origin = (const.SCREEN_WIDTH - const.ROAD_WIDTH)//2 
    dist_between_lines = const.ROAD_WIDTH // num_lanes

    # discontinuous lines
    for lane in range(1, num_lanes):
        # TODO hacer que se mueva la linea
        for i in range(-10, const.SCREEN_HEIGHT, line_separation):
            pg.draw.rect(screen, clrs.DARK_YELLOW,
                        (road_x_origin + dist_between_lines*lane, 
                         i, line_width, line_height))


def display_monitor_text(screen, score, fps):
    score_text1 = font.render(f"Obstacles", True, clrs.BLACK)
    score_text2 = font.render(f"cleared:   {score}", True, clrs.BLACK)
    screen.blit(score_text1, (10, 10))
    screen.blit(score_text2, (10, 36))
    info = distance_font.render("Press 'space' to pause", True, clrs.BLACK)
    screen.blit(info, (10, 100))

    fps_text = medium_font.render(f"FPS={fps:.2f}", True, clrs.BLACK)
    fps_offset = fps_text.get_width()
    screen.blit(fps_text, (const.SCREEN_WIDTH-fps_offset, 10))


def endgame_text(screen, score, start_time):
    death_text = font.render(f"You crashed!!", True, clrs.WHITE)
    screen.blit(death_text, (const.SCREEN_WIDTH //
                2 - 100, const.SCREEN_HEIGHT // 2 - 100))

    final_score_text = font.render(f"Final Score: {score}", True, clrs.WHITE)
    screen.blit(final_score_text, (const.SCREEN_WIDTH //
                2 - 100, const.SCREEN_HEIGHT // 2 - 50))

    # Calculate and display play time
    elapsed_time = (pg.time.get_ticks() - start_time) // 1000  # in seconds
    time_text = font.render(f"Time: {elapsed_time} seconds", True, clrs.WHITE)
    screen.blit(time_text, (const.SCREEN_WIDTH //
                2 - 100, const.SCREEN_HEIGHT // 2))


if __name__ == "__main__":
    car_img = pg.image.load('imgs/coche_estrecho.png')
    width = car_img.get_width()
    height = car_img.get_height()
    print("width: ", width , ", height: ", height)

    obstacle_img = pg.image.load('imgs/roadblock_yellow.png')
    width = obstacle_img.get_width()
    height = obstacle_img.get_height()
    print("width: ", width , ", height: ", height)