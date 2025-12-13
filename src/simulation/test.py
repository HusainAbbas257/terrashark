'''this file will be used to test he procedural generation of terrain using pygame. all the codes will be imported from terrain.py'''

import pygame
import random
import terrain

SCREEN_SIZE = (800, 600)
MAP_SIZE = (200, 150)
TILE_SIZE = 5


def run_test():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Terrain Test")

    # must load images AFTER display init
    terrain.TileImageCache.load_images(TILE_SIZE, "assets/tiles")

    seed = random.randint(0, 100_000)
    generator = terrain.TerrainGenerator(seed, MAP_SIZE)
    tilemap = generator.generate_tilemap()

    renderer = terrain.TerrainRenderer(TILE_SIZE)
    background = renderer.build_background(
        tilemap,
        SCREEN_SIZE,
        f"cache/test_bg_{seed}.png"
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run_test()