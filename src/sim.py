"""
Main entry point for Terrashark simulation
"""

import pygame
import random

from src.entities import goober, tree, base
from src.simulation import terrain


# ---------------- CONFIG ----------------
SCREEN_SIZE = (800, 600)
TILE_SIZE = 5
MAP_SIZE = (50, 50)
SEED = 123

TREE_COUNT = 10
GOOBER_COUNT = 10

LOGIC_FPS = 10
# ---------------------------------------


def get_empty_tile(tilemap: "terrain.TileMap"):
    """Return a random valid empty land tile or None."""
    valid = [
        t for t in tilemap.tiles
        if t.biome not in ("shallow-water", "deep-ocean")
        and not t.organism
    ]
    return random.choice(valid) if valid else None


def init_entities(tilemap):
    """Spawn trees and goobers safely."""
    trees = []
    goobers = []

    for _ in range(TREE_COUNT):
        tile = get_empty_tile(tilemap)
        if not tile:
            break

        ent = tree.Tree(
            base.Genome("tree", 1, 1, 20, 20, random.randrange(30,40), 20, 4, 20),
            tilemap,
            tile,
            tile.world_pos,
        )

        # FIX: Tree now self-registers into tile
        trees.append(ent)

    for _ in range(GOOBER_COUNT):
        tile = get_empty_tile(tilemap)
        if not tile:
            break

        ent = goober.Goober(
            base.Genome("goober", 10, 10, 10, 10,random.randrange(10,20), 10, 10, 10, 100, 0),
            tilemap,
            tile,
            tile.world_pos,
        )

        # FIX: Goober now self-registers into tile
        goobers.append(ent)

    return trees, goobers


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Terrashark Simulation")

    # --- Terrain setup (display FIRST) ---
    terrain.TileImageCache.load_images(TILE_SIZE, "assets/tiles")

    generator = terrain.TerrainGenerator(SEED, MAP_SIZE)
    tilemap = generator.generate_tilemap()

    renderer = terrain.TerrainRenderer(TILE_SIZE)
    bg = renderer.build_background(
        tilemap,
        screen.get_size(),
        f"cache/simulation_bg_{SEED}.png",
    )

    trees, goobers = init_entities(tilemap)

    clock = pygame.time.Clock()
    logic_accumulator = 0.0
    LOGIC_DT = 1.0 / LOGIC_FPS

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        logic_accumulator += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ---- LOGIC UPDATE (FIXED STEP) ----
        while logic_accumulator >= LOGIC_DT:

            # FIX: update() MUST be called (metabolism, death, movement timers)
            for t in trees[:]:
                t.update(LOGIC_DT)
                if not t.alive:
                    trees.remove(t)

            for g in goobers[:]:
                g.update(LOGIC_DT)
                if not g.alive:
                    goobers.remove(g)

            # FIX: handle reproduction results
            for t in trees[:]:
                child = t.do_task(t.get_task())
                if isinstance(child, tree.Tree):
                    trees.append(child)

            for g in goobers[:]:
                child = g.do_task(g.get_task())
                if isinstance(child, goober.Goober):
                    goobers.append(child)

            logic_accumulator -= LOGIC_DT

        # ---- RENDER ----
        screen.blit(bg, (0, 0))

        for t in trees:
            screen.blit(t.image, t.position)

        for g in goobers:
            screen.blit(g.image, g.position)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
