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

    def obstacle_sensor(self, obstacles):
        for obstacle in obstacles:
            
            pygame.draw.line(screen, GREEN, 
                             (self.x + CAR_WIDTH // 2, self.y), 
                             (obstacle.x + OBSTACLE_WIDTH // 2, 
                              obstacle.y + OBSTACLE_HEIGHT), 2)

# Obstacle class
class Obstacle:
    def __init__(self):
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.x = random.randint((SCREEN_WIDTH - ROAD_WIDTH) // 2, (SCREEN_WIDTH + ROAD_WIDTH) // 2 - CAR_WIDTH)
        self.y = -self.height
        self.speed = 10  # Adjusted speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

# TODO revisa que esto no afecte a lo otro de colisiones
    def check_collision(self, car):
        if self.y + self.height > car.y and self.y < car.y + CAR_HEIGHT:
            if self.x + self.width > car.x and self.x < car.x + CAR_WIDTH:
                return True
        return False

#def moveInTimeIntervals(time_offset, move_left, start_time):

def spawn_despawn_obstacles(obstacles, score):

    if random.randint(1, 50) == 1:  # Adjusted obstacle frequency
            obstacles.append(Obstacle())

    for obstacle in obstacles[:]:
            obstacle.move()
            obstacle.draw(screen)
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
                score += 1

def obstacle_collisions(obstacles, car):
    for obstacle in obstacles:
        if obstacle.check_collision(car):
            return True #para running = False
        else:
            return False
        
# TODO spawnear solo cuando no haya más obstaculos en la carretera
# TODO sensor debe funcionar solo hasta que estén a la misma altura
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

    # New variables
    time_offset = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #moveInTimeIntervals(move_left, time_offset, start_time)

        if time_offset:
            last_time = (pygame.time.get_ticks() - start_time) / 1000  # medio segundo
            time_offset = False

        now = (pygame.time.get_ticks() - start_time) / 1000

        if (now) >  (last_time + 0.001): 
            # hace un random walk hacia los lados cada 0.007ms
            # si se cambia la resolucion en now y last time se mueve mas fluido

            direction = random.randint(1, 2)
            if direction == 1:
                car.move_left()
                car.draw(screen)
            else:         
                car.move_right()
                car.draw(screen)
        
            time_offset = True
        
        # legacy for manual car movement
        '''keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.move_left()
        if keys[pygame.K_RIGHT]:
            car.move_right()'''

        screen.fill(GRAY)
        pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH - ROAD_WIDTH) // 2, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        car.draw(screen)

        #TODO problema: desacolpar el check de colisión del spawn??
        # si colisionan o sale de la pantalla se dereferencia el obstaculo...
        spawn_despawn_obstacles(obstacles, score)
        collision = obstacle_collisions(obstacles, car)
        if collision:
            running = False
    
        # "linea" del sensor, el orden de dibujo importa
        car.obstacle_sensor(obstacles)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    
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