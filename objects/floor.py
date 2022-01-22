import pygame

class Floor:
    SPEED = 5

    def __init__(self, image, y):
        self.width = image.get_width()
        self.image = image
        self.y = y
        # os dois floor x1 e x2
        self.x1 = 0
        self.x2 = self.width
    
    def move(self):
        self.x1-= self.SPEED
        self.x2-= self.SPEED

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))