import pygame
import os
from objects import bird, floor, pipe

pygame.font.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FONT_POINTS = pygame.font.SysFont('arial', 50)

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
IMAGE_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
IMAGE_BIRDS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))
]

Bird = bird.Bird
Floor = floor.Floor
Pipe = pipe.Pipe

def draw_screen(screen, birds, pipes, floors, points):
    screen.blit(IMAGE_BG, (0,0))
    for current_bird in birds:
        current_bird.draw(screen)
    for current_pipe in pipes:
        current_pipe.draw(screen)
    for current_floor in floors:
        current_floor.draw(screen)
    
    text = FONT_POINTS.render(f"Pontuação: {points}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()

def for_entity(entitys, method):
    for entity in entitys:
        getattr(entity, method)()

def main():
    birds = [Bird(IMAGE_BIRDS, 230, 350)]
    floors = [Floor(IMAGE_FLOOR, 730)]
    pipes = [Pipe(IMAGE_PIPE, 700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    points = 0
    clock = pygame.time.Clock()
    loop = True
    while loop:
        clock.tick(30)
        # interação com o usuario MELHORAR
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for_entity(birds, 'jump')
        # MOVER AS COISAS
        for_entity(birds, 'move')
        for_entity(floors, 'move')
        # for_entity(pipes, 'move')
        add_pipes = False
        remove_pipes = []
        for current_pipe in pipes:
            for i, current_bird in enumerate(birds):
                if current_pipe.colision(current_bird):
                    birds.pop(i)
                if not current_pipe.passed and current_bird.x > current_pipe.x:
                    current_pipe.passed = True
                    add_pipes = True
            current_pipe.move()
            if current_pipe.x + current_pipe.image_top.get_width() < 0:
                remove_pipes.append(current_pipe)
        if add_pipes:
            points+=1
            pipes.append(Pipe(IMAGE_PIPE, 600))
        for removed_pipe in remove_pipes:
            pipes.remove(removed_pipe)
        
        for i, current_bird in enumerate(birds):
            if (current_bird.y + current_bird.image.get_height()) > 730 or current_bird.y < 0:
                birds.pop(i)

        if len(birds) == 0:
            loop = False
        draw_screen(screen, birds, pipes, floors, points)
    
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()