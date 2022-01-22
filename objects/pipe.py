import pygame
import random

class Pipe:
    DISTANCE = 200
    SPEED_PIPE = 5

    def __init__(self, img, x):
        self.x = x
        self.heigth = 0
        self.pos_top = 0
        self.pos_base = 0
        self.image_top = pygame.transform.flip(img, False, True)
        self.image_base = img
        self.passed = False
        self.define_height()
    
    def define_height(self):
        # TODO definir aparti dos valores da tela
        self.heigth = random.randrange(50, 450)
        self.pos_top = self.heigth - self.image_top.get_height()
        self.pos_base = self.heigth + self.DISTANCE
    
    def move(self):
        self.x -= self.SPEED_PIPE
    
    def draw(self, screen):
        screen.blit(self.image_top, (self.x, self.pos_top))
        screen.blit(self.image_base, (self.x, self.pos_base))
    
    def colision(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.image_top)
        base_mask = pygame.mask.from_surface(self.image_base)

        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_base = (self.x - bird.x, self.pos_base - round(bird.y))
        
        top_point = bird_mask.overlap(top_mask, distance_top)
        base_point = bird_mask.overlap(base_mask, distance_base)

        return base_point or top_point