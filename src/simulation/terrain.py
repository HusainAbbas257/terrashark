import random
from opensimplex import OpenSimplex

class Tile:
    '''Tile class representing a terrain tile.'''
    def __init__(self, elevation):
        '''Tile type determined by elevation.'''
        self.elevation = elevation  

    def get_colour(self):
        """Colour decided by elevation thresholds."""
        h = self.elevation
        if h < 0.30:
            return (0, 0, 150)      # deep water
        elif h < 0.40:
            return (20, 20, 200)    # shallow water
        elif h < 0.48:
            return (194, 178, 128)  # beach
        elif h < 0.65:
            return (34, 139, 34)    # grass
        elif h < 0.80:
            return (50, 100, 50)    # dark forest
        else:
            return (150, 150, 150)  # rock / mountain


class TerrainMap:
    '''TerrainMap class holding a grid of tiles.'''
    def __init__(self, grid):
        '''Initialize with a 2D grid of Tile objects.'''
        self.grid = grid

    def get_list(self):
        '''Return the 2D grid of tiles.'''
        return self.grid


class TerrainGenerator:
    '''Generates terrain using OpenSimplex noise.'''
    def __init__(self, seed:int, size:tuple, tile_size:int=40):
        '''Initialize with seed, size (width, height), and tile size.'''
        self.seed = seed
        self.width, self.height = size
        self.tile_size = tile_size
        self.noise = OpenSimplex(seed)

    def noise2d(self, x, y):
        """OpenSimplex 2D noise normalised to 0–1"""
        return (self.noise.noise2(x, y) + 1) / 2

    def generate_heightmap(self):
        """Multi-frequency octave system for realism."""
        heightmap = []
        
        scale = 20.0

        for y in range(self.height):
            row = []
            for x in range(self.width):
                nx = x / scale
                ny = y / scale

                # 4 octaves layered
                e  = 1.00 * self.noise2d(nx, ny)
                e += 0.50 * self.noise2d(nx * 2, ny * 2)
                e += 0.25 * self.noise2d(nx * 4, ny * 4)
                e /= (1.00 + 0.50 + 0.25)

                row.append(e)
            heightmap.append(row)

        return heightmap

    def generate_terrain(self):
        '''Generate TerrainMap from heightmap.'''
        heightmap = self.generate_heightmap()
        grid = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = Tile(heightmap[y][x])
                row.append(tile)
            grid.append(row)

        return TerrainMap(grid)
    
if __name__ == "__main__":
    # Example usage
    seed = random.randint(0, 100000)
    terrain_generator = TerrainGenerator(seed, (50, 50), tile_size=10)
    terrain_map = terrain_generator.generate_terrain()
    tile_grid = terrain_map.get_list()
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    for y, row in enumerate(tile_grid):
        for x, tile in enumerate(row):
            color = tile.get_colour()
            pygame.draw.rect(screen, color, (x * terrain_generator.tile_size, y * terrain_generator.tile_size, terrain_generator.tile_size, terrain_generator.tile_size))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
