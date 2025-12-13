"""
terrain.py — static terrain + logical tilemap for simulation research.

Design:
- TileData holds ONLY simulation data (no pygame, no images).
- TileMap is the single source of truth for world state.
- TerrainRenderer converts TileMap → static background image (cached PNG).
- Runtime rendering = single blit per frame.
- Entities query TileMap for biome/buffs, never visuals.

This file intentionally avoids mixing simulation logic with rendering.
"""

import os
import random
from opensimplex import OpenSimplex
import pygame
pygame.init()

# top of module
BIOME_THRESHOLDS = [
    ("deep-ocean", 0.30),
    ("shallow-water", 0.40),
    ("sand", 0.45),
    ("grass", 0.65),
    ("forest", 0.78),
    ("rock", 1.0),
]

# ---------------------------------------------------------------------
# Tile Image Cache (visual-only, renderer-facing)
# ---------------------------------------------------------------------
class TileImageCache:
    """
    Loads and caches biome tile images once.

    This is strictly a rendering helper. Simulation code must never
    touch this class.
    """
    cache = {}
    _biomes = ("deep-ocean", "shallow-water", "sand", "grass", "forest", "rock")

    @staticmethod
    def load_images(tile_size: int, tiles_path: str):
        """
        Load biome PNG tiles and convert them to display format.

        Must be called AFTER pygame.display.set_mode for fastest blits.
        """
        TileImageCache.cache.clear()
        display_ready = pygame.display.get_surface() is not None

        for name in TileImageCache._biomes:
            path = os.path.join(tiles_path, f"{name}.png")
            img = pygame.image.load(path)

            if display_ready:
                img = img.convert_alpha()

            if img.get_size() != (tile_size, tile_size):
                img = pygame.transform.scale(img, (tile_size, tile_size))

            TileImageCache.cache[name] = img

    @staticmethod
    def get(biome_name: str) -> pygame.Surface:
        """Return cached surface for a biome name."""
        return TileImageCache.cache[biome_name]


# ---------------------------------------------------------------------
# TileData (simulation-only)
# ---------------------------------------------------------------------
class TileData:
    """
    Logical representation of one tile.

    This object contains NO pygame surfaces and NO rendering data.
    Safe to use in headless simulations.
    """
    __slots__ = ("elevation", "biome")

    def __init__(self, elevation: float):
        self.elevation = float(elevation)
        self.biome = self._classify_biome()

    def _classify_biome(self) -> str:
        """Classify biome based on elevation."""
        
        for biome, thresh in BIOME_THRESHOLDS:
            if self.elevation < thresh:
                return biome
        raise ValueError(f"invalid biome for elevation {self.elevation!r}")



# ---------------------------------------------------------------------
# TileMap (world data container)
# ---------------------------------------------------------------------
class TileMap:
    """
    Stores all TileData in a flat array for fast lookup.

    Acts as the authoritative world state for entities.
    """
    def __init__(self, width: int, height: int, tiles: list['TileData']):
        if len(tiles) != width * height:
            raise ValueError("tiles length must equal width * height")  

        self.width = width
        self.height = height
        self.tiles = tiles  # flat list: index = y * width + x

    def get_tile(self, x: int, y: int) -> TileData:
        """Return TileData at tile coordinates (x, y)."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"tile coords out of bounds: {(x,y)}")
        loc = y * self.width + x
        return self.tiles[loc]



# ---------------------------------------------------------------------
# Terrain Generator (logic-only)
# ---------------------------------------------------------------------
class TerrainGenerator:
    """
    Generates a TileMap using OpenSimplex noise.
    """
    def __init__(self, seed: int, size: tuple[int, int]):
        self.seed = seed
        self.width, self.height = size
        self.noise = OpenSimplex(seed)

    def _noise(self, x: float, y: float) -> float:
        """Normalized OpenSimplex noise [0..1]."""
        return (self.noise.noise2(x, y) + 1) /2

    def generate_tilemap(self) -> TileMap:
        """
        Generate and return a TileMap containing TileData only.
        """
        scale = 20.0
        tiles = []

        for y in range(self.height):
            for x in range(self.width):
                h = (
                    1.00 * self._noise(x/scale,     y/scale) +
                    0.50 * self._noise(x/scale*2.0, y/scale*2.0) +
                    0.25 * self._noise(x/scale*4.0, y/scale*4.0)
                ) / 1.75
                tiles.append(TileData(h))

        return TileMap(self.width, self.height, tiles)


# ---------------------------------------------------------------------
# Terrain Renderer (one-time, visual-only)
# ---------------------------------------------------------------------
class TerrainRenderer:
    """
    Converts a TileMap into a static background image.

    Used once per seed. Never touched by simulation logic.
    """
    def __init__(self, tile_size: int):
        self.tile_size = tile_size

    def build_background(
        self,
        tilemap: TileMap,
        screen_size: tuple[int, int],
        out_path: str
    ) -> pygame.Surface:
        """
        Render the tilemap into a cached PNG and return a converted surface.
        """
        if os.path.exists(out_path):
            surf = pygame.image.load(out_path)
            if surf.get_size() != tuple(screen_size):
                surf = pygame.transform.scale(surf, screen_size)
            return surf.convert()


        map_w = tilemap.width * self.tile_size
        map_h = tilemap.height * self.tile_size
        surface = pygame.Surface((map_w, map_h)).convert()

        blit = surface.blit
        ts = self.tile_size

        for y in range(tilemap.height):
            for x in range(tilemap.width):
                tile = tilemap.get_tile(x, y)
                img = TileImageCache.get(tile.biome)
                blit(img, (x * ts, y * ts))

        if surface.get_size() != screen_size:
            surface = pygame.transform.scale(surface, screen_size)

        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        pygame.image.save(surface, out_path)
        return surface


# ---------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------
if __name__ == "__main__":
    SCREEN_SIZE = (1400, 700)
    TILE_SIZE = 16

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Static Terrain Simulation")

    TileImageCache.load_images(TILE_SIZE, "assets/tiles")

    seed = random.randint(0, 100_000)
    generator = TerrainGenerator(seed, (280, 140))
    tilemap = generator.generate_tilemap()

    renderer = TerrainRenderer(TILE_SIZE)
    bg = renderer.build_background(
        tilemap,
        SCREEN_SIZE,
        f"cache/terrain_bg_{seed}.png"
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.blit(bg, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
