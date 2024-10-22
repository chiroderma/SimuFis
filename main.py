import pygame
import numpy
import engine.rendering as renderer
import engine.phys_xd as phys

pygame.init()

phys_xd = phys.PhysXD()
planet1 = phys.Planet(8000, [400, 500], [100000, 0], [0, 0], 500.0, 5.0, [255, 0, 0, 255])
phys_xd.add_planet(planet1)
render = renderer.Renderer(1280, 720, [planet1])

clock = pygame.time.Clock()

game_loop = True

#o lop conta o prgresso no tempo
loops = 0

while game_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
    
    phys_xd.update()
    render.render()

    #O flip muda o buffer da tela
    clock.tick(60)
    loops += 1

pygame.quit()