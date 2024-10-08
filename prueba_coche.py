import pygame as pg 
import random

# Initialize pg
pg.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_WIDTH = 75
CAR_HEIGHT = 85
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 80
ROAD_WIDTH = 400
FPS = 40  # Reduced frame rate

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 40)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (130, 130, 0)

# Load images
car_img = pg.image.load('imgs/car.png')
car_img = pg.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))

obstacle_img = pg.image.load('imgs/granny.png')
obstacle_img = pg.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Set up the display
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Simulador de Control de coche con lógica difusa")

# Font for score
font = pg.font.Font(None, 36)
distance_font = pg.font.SysFont(None, 20)

# Car class


class Car:
    def __init__(self):
        self.image = car_img
        self.x = (SCREEN_WIDTH - CAR_WIDTH) // 2
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 10
        self.speed = FPS//(FPS*0.04)
        print(self.speed)

    def move_left(self):
        if self.x > (SCREEN_WIDTH - ROAD_WIDTH) // 2:
            self.x -= self.speed

    def move_right(self):
        if self.x < (SCREEN_WIDTH + ROAD_WIDTH) // 2 - CAR_WIDTH:
            self.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# TODO pasar distancia de pg a metros
# TODO crear sensores para distancias de x_left y x_right
# TODO crear una función de nearest_point? para que no vaya al centro, si no
# al punto más cercano del obstáculo, como un sensor real...
# TODO velocidad depende de fps, ajustar para que sea escalado


    def obstacle_sensor_y_axis(self, obstacles, visualize=True):
        distances = []

        for obstacle in obstacles:
            if self.y > obstacle.y + OBSTACLE_HEIGHT: # para sensor cuando esté detrás del coche
                distance_y_axis = abs(
                    (obstacle.y + OBSTACLE_HEIGHT) - (self.y))
                distances.append(distance_y_axis)

                if visualize:
                    
                    pg.draw.line(screen, GREEN,
                                    (self.x + CAR_WIDTH // 2, self.y),
                                    (obstacle.x + OBSTACLE_WIDTH // 2,
                                    obstacle.y + OBSTACLE_HEIGHT), 2)
                    text_surface = distance_font.render(
                        f'Y DIST: {distance_y_axis}', False, WHITE)
                    screen.blit(text_surface, (
                        obstacle.x + OBSTACLE_WIDTH, obstacle.y))

        return distances

# Obstacle class


class Obstacle:
    def __init__(self):
        self.image = obstacle_img
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.x = random.randint(
            (SCREEN_WIDTH - ROAD_WIDTH) // 2, 
            (SCREEN_WIDTH + ROAD_WIDTH) // 2 - CAR_WIDTH)
        self.y = -self.height
        self.speed = FPS//(FPS*0.1) # Adjusted speed
        print(self.speed)

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        if self.image is None:
            pg.draw.rect(
                screen, RED, (self.x, self.y, self.width, self.height))
        else:
            screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

    def check_collision(self, car):
        if self.y + self.height > car.y and self.y < car.y + CAR_HEIGHT:
            if self.x + self.width > car.x and self.x < car.x + CAR_WIDTH:
                return True
        return False

def moveInTimeIntervals(car, time_offset, start_time, last_time):
    
    if time_offset:
            last_time = (pg.time.get_ticks() - start_time) / 1000
            time_offset = False

    now = (pg.time.get_ticks() - start_time) / 1000

    if (now) > (last_time + 0.007):
        # hace un random walk hacia los lados cada 0.007ms
        # si se cambia la resolucion en now y last time se mueve mas fluido

        direction = bool(random.getrandbits(1))
        if direction == 1:
            car.move_left()
            car.draw(screen)
        else:
            car.move_right()
            car.draw(screen)

        time_offset = True

    return last_time, time_offset

def manual_control(car):
    # legacy for manual car movement
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            car.move_left()
        if keys[pg.K_RIGHT]:
            car.move_right()

def spawn_despawn_obstacles(obstacles, score):

    '''if random.randint(1, 50) == 1:  # Adjusted obstacle frequency
        obstacles.append(Obstacle())'''
    
    # make them appear only one at a time constantly
    if not obstacles:
        obstacles.append(Obstacle())

    for obstacle in obstacles[:]:
        obstacle.move()
        obstacle.draw(screen)
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
        
def draw_road():
    draw_coords = (SCREEN_WIDTH - ROAD_WIDTH)
    line_width = ROAD_WIDTH //40
    line_separation = 50
    line_height = SCREEN_HEIGHT//30

    # asphalt
    pg.draw.rect(
        screen, DARK_GRAY, (draw_coords // 2, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    #center
    pg.draw.rect(
        screen, YELLOW, (draw_coords, 0, line_width, SCREEN_HEIGHT))
    # right line
    pg.draw.rect(
        screen, YELLOW, ((draw_coords//2)+10, 0, line_width, SCREEN_HEIGHT))
    #left line
    pg.draw.rect(
        screen, YELLOW, ((draw_coords//2)+(ROAD_WIDTH-20), 0, line_width, SCREEN_HEIGHT))
    # false discontinuous line
    
    for i in range(-10, SCREEN_HEIGHT, line_separation):
        pg.draw.rect(screen, DARK_GRAY, 
            (draw_coords, i, line_width, line_height))

# TODO sensor debe tener un arco de acción
# TODO programar más sensores

# Game loop


def game_loop():
    car = Car()
    obstacles = []
    score = 0
    clock = pg.time.Clock()
    running = True
    start_time = pg.time.get_ticks()
    last_time = start_time

    # New variables
    time_offset = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        last_time, time_offset = moveInTimeIntervals(
            car, time_offset, start_time, last_time)

        screen.fill(GRAY)
        
        draw_road()

        car.draw(screen)

        score = spawn_despawn_obstacles(obstacles, score)
        collision = obstacle_collisions(obstacles, car)
        if collision:
            running = False


        # "linea" del sensor, el orden de dibujo importa
        car.obstacle_sensor_y_axis(obstacles)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pg.display.flip()
        clock.tick(FPS)

    death_text = font.render(f"Abuelita atropellada!!", True, WHITE)
    screen.blit(death_text, (SCREEN_WIDTH //
                2 - 100, SCREEN_HEIGHT // 2 - 100))

    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_text, (SCREEN_WIDTH //
                2 - 100, SCREEN_HEIGHT // 2 - 50))

    # Calculate and display play time
    elapsed_time = (pg.time.get_ticks() - start_time) // 1000  # in seconds
    time_text = font.render(f"Time: {elapsed_time} seconds", True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    pg.display.flip()
    pg.time.wait(1000)  # Display final screen for 5 seconds

    pg.quit()

    pg.quit()


if __name__ == "__main__":
    game_loop()
