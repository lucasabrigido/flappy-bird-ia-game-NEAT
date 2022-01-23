import pygame
import os
import neat

from objects import bird, floor, pipe

pygame.font.init()

ai_playing = True
generate = 0

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FONT_POINTS = pygame.font.SysFont('arial', 40)

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
    
    if ai_playing:
        text2 = FONT_POINTS.render(f"Geração: {generate}", 1, (255, 255, 255))
        screen.blit(text2, (10, 10))
    pygame.display.update()

def for_entity(entitys, method, callback = None):
    for index, entity in enumerate(entitys):
        getattr(entity, method)()
        if callback:
            callback(entity, index)

def main(all_genomas, config): # FITNESS FUNCTION
    global generate
    generate += 1
    if ai_playing:
        redes = []
        genomas = []
        birds = []
        # _ -> id do genoma
        for _, genoma in all_genomas:
            redes.append(neat.nn.FeedForwardNetwork.create(genoma, config))
            genoma.fitness = 0
            genomas.append(genoma)
            birds.append(Bird(IMAGE_BIRDS, 230, 350))
    else:
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
                pygame.quit()
                quit()
            if not ai_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for_entity(birds, 'jump')
        pipe_index = 0
        if len(birds) > 0:
            # pass #descobrir qual cano olhar
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].image_top.get_width()):
                pipe_index = 1
        else:
            loop = False
            break
        # MOVER AS COISAS
        def move_bird(bird, i):
            if not ai_playing:
                return;
            genomas[i].fitness += 0.1
            output = redes[i].activate((
                bird.y,
                abs(bird.y - pipes[pipe_index].heigth),
                abs(bird.y - pipes[pipe_index].pos_base)
            ))
            # -1 e 1 -> se o output for > 0.5 então pula
            if output[0] > 0.5:
                bird.jump()
        for_entity(birds, 'move', move_bird) #aumentar um pouco o fitness a ia diz se pula ou não
        for_entity(floors, 'move')
        # for_entity(pipes, 'move')
        add_pipes = False
        remove_pipes = []
        for current_pipe in pipes:
            for i, current_bird in enumerate(birds):
                if current_pipe.colision(current_bird):
                    birds.pop(i)
                    if ai_playing:
                        genomas[i].fitness-=1
                        genomas.pop(i)
                        redes.pop(i)
                if not current_pipe.passed and current_bird.x > current_pipe.x:
                    current_pipe.passed = True
                    add_pipes = True
            current_pipe.move()
            if current_pipe.x + current_pipe.image_top.get_width() < 0:
                remove_pipes.append(current_pipe)
        if add_pipes:
            points+=1
            pipes.append(Pipe(IMAGE_PIPE, 600))
            if ai_playing:
                for genoma in genomas:
                    genoma.fitness+=5;
        for removed_pipe in remove_pipes:
            pipes.remove(removed_pipe)
        
        for i, current_bird in enumerate(birds):
            if (current_bird.y + current_bird.image.get_height()) > 730 or current_bird.y < 0:
                birds.pop(i)
                if ai_playing:
                    genomas[i].fitness-=0.1
                    genomas.pop(i)
                    redes.pop(i)

        # if len(birds) == 0:
        #     # ToDo mudar para False
        #     loop = True
        draw_screen(screen, birds, pipes, floors, points)

def build(path):
    if ai_playing:
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            path
        )
        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())
        # 50 gerações
        population.run(main, 50)
    else:
        main(None, None)
if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), 'config.txt')
    build(path)