import pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

RED = (255, 0, 0)
OBSTACLE_SIZE = 50


class Obstacle():
    def __init__(self):
        self.position = pygame.Vector2(350, 230)
        self.width = 200
        self.height = 100

    def draw_obstacle(self, screen):
        pygame.draw.circle(screen, RED, (int(self.position.x), int(self.position.y)),OBSTACLE_SIZE)
    



        



    
