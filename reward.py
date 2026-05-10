import pygame

REWARD_SIZE = 20
BLUE= (0,0,255)

class Reward():
    def __init__(self, ):
        self.position = pygame.Vector2(150, 100)
        
    def draw_reward(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.position.x), int(self.position.y)), REWARD_SIZE)
    

