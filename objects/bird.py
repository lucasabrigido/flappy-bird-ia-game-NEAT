import pygame

class Bird:
    def __init__(self, imgs, x, y):  
        self.imgs = imgs
        # animações de rotação
        self.max_rotate = 25
        self.speed_rotate = 20
        self.animate_time = 5
        # caracteristicas do bird
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        # parametro auxiliar
        self.time = 0
        self.count_image = 0
        self.image = imgs[0]
    
    def jump(self):
        # formula de deslocamento sorvertão S = so + voT + at²/2
        self.speed = -10.5
        self.time = 0
        self.height = self.y
    
    def move(self):
        # calcular o deslocamento
        self.time+=1
        # testar o 1.5 (aceleação)
        displacement = 1.5 * (self.time**2) + self.speed * self.time
        
        # restriguir o deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement-=2
        
        self.y+=displacement
        
        # o angulo do passaro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.max_rotate:
                self.angle = self.max_rotate
        else:
            if self.angle > -90:
                self.angle -= self.speed_rotate

    def draw(self, screen):
        # definir qual imagem do passaro usar
        self.count_image+=1

        if self.count_image < self.animate_time:
            self.image = self.imgs[0]
        elif self.count_image < self.animate_time*2:
            self.image = self.imgs[1]
        elif self.count_image < self.animate_time*3:
            self.image = self.imgs[2]
        elif self.count_image < self.animate_time*4:
            self.image = self.imgs[1]
        elif self.count_image >= self.animate_time*4 + 1:
            self.image = self.imgs[0]
            self.count_image = 0
        
        # se o passaro tiver caindo não bater asa
        if self.angle <= -80:
            self.image = self.imgs[1]
            self.count_image = self.animate_time*2
        
        # desenhar a imagem
        image_rotate = pygame.transform.rotate(self.image, self.angle)
        pos_center_image = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = image_rotate.get_rect(center=pos_center_image)
        screen.blit(image_rotate, rectangle.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
        