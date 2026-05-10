
import pygame
import random
import numpy as np

from rocket import  generate_rockets, update_and_draw_rockets, create_new_generation, get_best_rocket
from obstacle import Obstacle
from reward import Reward

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    max_frames = 400
    clock = pygame.time.Clock()
    obstacle = Obstacle()
    reward = Reward()
    rockets = generate_rockets()
    running = True
    frames = 0
    generation =1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frames < max_frames:            
            screen.fill((105,105,105))
            obstacle.draw_obstacle(screen)
            reward.draw_reward(screen)
            update_and_draw_rockets(screen, rockets, obstacle)
            pygame.display.flip()
            clock.tick(60)  
            frames += 1


        else:
            print("------------------------------------")
            print(f"Generation {generation} complete")
            best_rocket, best_score = get_best_rocket(rockets, reward)
            print(f"Best Score: {best_score}")
            rockets = create_new_generation(rockets, reward)
            frames = 0
            generation += 1
            clock.tick(120)  


    quit()



if __name__ == "__main__":
    main()


    
