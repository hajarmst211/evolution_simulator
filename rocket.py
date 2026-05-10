import pygame
import numpy as np
import random

from obstacle import OBSTACLE_SIZE 

ROCKET_SIZE = 7


class Rocket():
    def __init__(self, DNA):
        self.dna = DNA # An array of 400 pygame.Vector2 objects.Each vector represents a tiny "shove" (force) applied to the rocket at that specific frame.
        self.position = pygame.Vector2((800//2), (600 //2)) # Start at the bottom left corner of the screen, with a margin of 20 pixels from the left and bottom edges.
        self.dna_index = 0
        self.had_hit_target = False
        

    def update_dna(self):
        if (not self.had_hit_target and self.dna_index < len(self.dna)):
            self.position += self.dna[self.dna_index]
            self.dna_index += 1
        else:
            self.dna_index = len(self.dna) #Directly reaches the end of the dna
    
    def draw_rocket(self,screen):
        pygame.draw.circle(screen, (255,150,0), (int(self.position.x), int(self.position.y)), ROCKET_SIZE, 2)
    

    def has_collided(self, obstacle):
        obstacle_position: np.ndarray = obstacle.position
        current_position: np.ndarray = self.position
        distance : np.float32 = np.linalg.norm(current_position - obstacle_position)
        self.had_hit_obstacle = distance < (OBSTACLE_SIZE + ROCKET_SIZE)
        return


    def calculate_collission_bounce(self, obstacle):
        current_position = self.position
        obstacle_position = obstacle.position
        distance = np.linalg.norm(current_position - obstacle_position)
        collision_normal = (current_position - obstacle_position) / distance
        bounce_force = collision_normal * (OBSTACLE_SIZE + ROCKET_SIZE - distance)
        overlap = (OBSTACLE_SIZE + ROCKET_SIZE) - distance
        self.position += bounce_force * (overlap / (OBSTACLE_SIZE + ROCKET_SIZE))
        return 

    def check_collision(self, obstacle):
        self.has_collided(obstacle)
        if self.had_hit_obstacle:
            self.calculate_collission_bounce(obstacle)
            
    def calculate_score(self, reward):
        distance_to_reward = np.linalg.norm(self.position - reward.position)
        score = 1 / (distance_to_reward + 1e-6)  
        return score

def create_random_dna(number_of_frames):
    dna = np.array([pygame.Vector2(random.randint(-1,1), random.randint(-1,1)) for _ in range(number_of_frames)])
    return dna

def generate_rockets(num_rockets = 50, number_of_frames=400):
    return [Rocket(create_random_dna(number_of_frames)) for _ in range(num_rockets)]


def update_and_draw_rockets(screen, rockets, obstacle):
    for rocket in rockets:
        rocket.update_dna()
        rocket.check_collision(obstacle)
        rocket.draw_rocket(screen)


def get_scores(rockets, reward):
    return np.array([rocket.calculate_score(reward) for rocket in rockets])

def select_mating_parents(rockets, reward, number_of_parents):
    scores = get_scores(rockets, reward)

    sorted_indices = np.argsort(scores)[::-1]
    best_rockets = [rockets[i] for i in sorted_indices[:number_of_parents]]
    
    return best_rockets


def child_rocket(father_rocket, mother_rocket, mutation_rate=0.01):
    new_rocket_dna = np.zeros_like(father_rocket.dna)
    for i in range(len(father_rocket.dna)):
        if random.random() < mutation_rate:
            new_rocket_dna[i] = pygame.Vector2(random.randint(-1,1), random.randint(-1,1))

        else:
            new_rocket_dna[i] = random.choice([father_rocket.dna[i], mother_rocket.dna[i]])

    return Rocket(new_rocket_dna)


def create_new_generation(rockets, reward):
    if rockets is None or len(rockets) == 0:
        return generate_rockets()
    num_rockets = len(rockets)
    number_of_parents = max(2,num_rockets //2)
    parents = select_mating_parents(rockets, reward, number_of_parents)
    new_generation = []
    for _ in range(num_rockets):
        parent1, parent2 = random.sample(parents, 2)
        child = child_rocket(parent1, parent2)
        new_generation.append(child)
    return new_generation


def get_best_rocket(rockets, reward):
    scores = get_scores(rockets, reward)
    best_index = np.argmax(scores)
    return rockets[best_index], scores[best_index]

