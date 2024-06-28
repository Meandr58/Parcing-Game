import pygame
import sys
import time

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_WIDTH = 50
CAR_HEIGHT = 100
PARKING_SPOT_WIDTH = 60
PARKING_SPOT_HEIGHT = 120

# Цвета
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 128)

# Основной экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Припаркуй автомобиль")

# Классы
class Car:
    def __init__(self):
        self.image = pygame.image.load('car_image.png')  # Загрузка изображения машины
        self.image = pygame.transform.scale(self.image, (CAR_WIDTH, CAR_HEIGHT))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.speed = 5

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class ParkingSpot:
    def __init__(self):
        self.image = pygame.Surface((PARKING_SPOT_WIDTH, PARKING_SPOT_HEIGHT))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 100))

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Obstacle:
    def __init__(self, x, y):
        self.image = pygame.image.load('obstacle_image.png')  # Загрузка изображения препятствия
        self.image = pygame.transform.scale(self.image, (CAR_WIDTH, CAR_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

def display_message(message, color):
    font = pygame.font.SysFont(None, 55)
    text = font.render(message, True, color)
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    time.sleep(3)

def main():
    clock = pygame.time.Clock()
    car = Car()
    parking_spot = ParkingSpot()
    obstacles = [Obstacle(200, 300), Obstacle(400, 300), Obstacle(600, 300)]

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        car.update(keys)

        parking_spot.draw()  # Сначала рисуем парковочное место
        car.draw()  # Затем рисуем машину
        for obstacle in obstacles:
            obstacle.draw()

        # Проверка на столкновение с препятствиями
        for obstacle in obstacles:
            if car.rect.colliderect(obstacle.rect):
                display_message("Авария!!!", BLUE)
                car = Car()  # Сброс позиции машины

        # Проверка на парковку
        if (car.rect.left >= parking_spot.rect.left and
            car.rect.right <= parking_spot.rect.right and
            car.rect.top >= parking_spot.rect.top and
            car.rect.bottom <= parking_spot.rect.bottom):
            display_message("Успех!!!", BLUE)
            car = Car()  # Сброс позиции машины

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
