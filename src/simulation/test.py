'''this file will be used to test he procedural generation of terrain using pygame. all the codes will be imported from terrain.py'''



import pygame 
import terrain
import random 

pygame.init()
sizex =200
sizey =150
screen = pygame.display.set_mode((800,600))

seed=6306354746
terrain_generator = terrain.TerrainGenerator(seed, (sizex, sizey), tile_size=4)
terr=terrain_generator.generate_terrain()
world=terr.get_list()

def draw_world(screen, world, tile_size):
    for y, row in enumerate(world):
        for x, tile in enumerate(row):
            color =tile.get_colour()  # default to black if unknown tile
            pygame.draw.rect(screen, color, (x * tile_size, y * tile_size, tile_size, tile_size))
            

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_world(screen, world, terrain_generator.tile_size)
    pygame.display.flip()
pygame.quit()
