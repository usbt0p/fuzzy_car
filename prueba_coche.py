import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_WIDTH = 70
CAR_HEIGHT = 80
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 100
ROAD_WIDTH = 400
FPS = 30  # Reduced frame rate

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load images
car_img = pygame.image.load('imgs/car.png')
car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulador de Control de coche con lógica difusa")

# Font for score
font = pygame.font.Font(None, 36)
distance_font = pygame.font.SysFont(None, 20)

# Car class


class Car:
    def __init__(self):
        self.image = car_img
        self.x = (SCREEN_WIDTH - CAR_WIDTH) // 2
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 10
        self.speed = 25

    def move_left(self):
        if self.x > (SCREEN_WIDTH - ROAD_WIDTH) // 2:
            self.x -= self.speed

    def move_right(self):
        if self.x < (SCREEN_WIDTH + ROAD_WIDTH) // 2 - CAR_WIDTH:
            self.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# TODO pasar distancia de pygame a metros
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
                    pygame.draw.line(screen, GREEN,
                                    (self.x + CAR_WIDTH // 2, self.y),
                                    (obstacle.x + OBSTACLE_WIDTH // 2,
                                    obstacle.y + OBSTACLE_HEIGHT), 2)
                    
                    text_surface = distance_font.render(
                        f'Y DIST: {distance_y_axis}', False, WHITE)
                    screen.blit(text_surface, (obstacle.x, obstacle.y))

        return distances

# Obstacle class


class Obstacle:
    def __init__(self):
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.x = random.randint(
            (SCREEN_WIDTH - ROAD_WIDTH) // 2, 
            (SCREEN_WIDTH + ROAD_WIDTH) // 2 - CAR_WIDTH)
        self.y = -self.height
        self.speed = 10  # Adjusted speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(
            screen, RED, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

    def check_collision(self, car):
        if self.y + self.height > car.y and self.y < car.y + CAR_HEIGHT:
            if self.x + self.width > car.x and self.x < car.x + CAR_WIDTH:
                return True
        return False

def moveInTimeIntervals(car, time_offset, start_time, last_time):
    
    if time_offset:
            last_time = (pygame.time.get_ticks() - start_time) / 1000
            time_offset = False

    now = (pygame.time.get_ticks() - start_time) / 1000

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.move_left()
        if keys[pygame.K_RIGHT]:
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

# TODO sensor debe tener un arco de acción
# TODO programar más sensores

# Game loop


def game_loop():
    car = Car()
    obstacles = []
    score = 0
    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks()
    last_time = start_time

    # New variables
    time_offset = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        last_time, time_offset = moveInTimeIntervals(
            car, time_offset, start_time, last_time)

        screen.fill(GRAY)
        pygame.draw.rect(
            screen, BLACK, ((SCREEN_WIDTH - ROAD_WIDTH) // 2, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        car.draw(screen)

        score = spawn_despawn_obstacles(obstacles, score)
        collision = obstacle_collisions(obstacles, car)
        if collision:
            pass#running = False


        # "linea" del sensor, el orden de dibujo importa
        car.obstacle_sensor_y_axis(obstacles)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_text, (SCREEN_WIDTH //
                2 - 100, SCREEN_HEIGHT // 2 - 50))

    # Calculate and display play time
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # in seconds
    time_text = font.render(f"Time: {elapsed_time} seconds", True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    pygame.time.wait(1000)  # Display final screen for 5 seconds

    pygame.quit()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
