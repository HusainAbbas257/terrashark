'''NOTE : do not call tis class from any igher level call it instead only from __init__.py'''

import pygame
import random
import os
from src.entities.base import Genome
from src.simulation import terrain
IMAGE_PATH = r'assets\characters'
_IMAGES = {}

def load_image(name):
    if name in _IMAGES:
        return _IMAGES[name]

    path = os.path.join(IMAGE_PATH, f"{name}.png")
    if os.path.exists(path):
        _IMAGES[name] = pygame.image.load(path)
    else:
        _IMAGES[name] = None
    return _IMAGES[name]


# --------------------------------------------------
# Base Organism Sprite
# --------------------------------------------------
class OrganismSprite(pygame.sprite.Sprite):
    """
    Technical parent class for all organisms (animals & plants).
    Handles physiology only. Behavior MUST be implemented by subclasses.
    """

    def __init__(
        self,#removed species name as it is not needed anymore
        genome: Genome,
        map: terrain.TileMap,
        tile: terrain.TileData | None = None,
        position:tuple=(0, 0),#removed color as it is not needed anymore
        radius=5
    ):
        super().__init__()

        # --- Core biological state ---
        self.genome = genome                # Genome is authoritative
        self.species = self.genome.species       

        self.map = map
        self.tile = tile

        self.position = pygame.Vector2(position)
        self.age = genome.age
        self.energy = genome.energy

        self.hunger = 0.0
        self.thirst = 0.0
        self.urge = 0.0
        self.time_till_move=0
        
        # movement memory 
        self.target:terrain.TileData=None
        self.path:list[terrain.TileData]=[]

        self.alive = True

        # --- Sprite visuals ---
        image = load_image(self.species)

        if image is None:
            # fallback circle (debug-safe)
            self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 255), (radius, radius), radius)
        else:
            self.image = image

        self.rect = self.image.get_rect(center=self.position)

    # ==========================================================
    # Life-cycle / physiology
    # ==========================================================
    def update(self, dt=1/6):
        """Handles aging, metabolism, hunger, thirst, and death."""
        if not self.alive:
            self.kill()
            return
        
        #  update time till next move
        if self.time_till_move-dt>0:
            self.time_till_move-=dt 
        else:
            self.time_till_move=0
            
        # Aging
        self.age += dt

        # Metabolism costs
        metabolic_cost = self.genome.metabolism * dt
        self.energy -= metabolic_cost
        self.hunger += metabolic_cost
        self.thirst += metabolic_cost

        # Clamp values (numerical stability)
        self.energy = max(0.0, self.energy)
        self.hunger = max(0.0, self.hunger)
        self.thirst = max(0.0, self.thirst)

        # Death conditions
        if (
            self.age >= self.genome.max_age
            or self.energy <= 0
            or self.hunger > getattr(self.genome, "hunger_max", 100)
            or self.thirst > getattr(self.genome, "thirst_max", 100)
        ):
            self.alive = False
        
        self.do_task(self.get_task())

    # ==========================================================
    # AI / behavior interface (must override)
    # ==========================================================
    def get_task(self):
        """
        Decide what to do next.
        Examples: 'eat', 'drink', 'reproduce', 'wander'
        """
        raise NotImplementedError

    def do_task(self, task, **kwargs):
        """
        Execute the task returned by get_task().
        """
        raise NotImplementedError

    # ==========================================================
    # Interaction interface
    # ==========================================================
    def eat(self, target):
        """
        Eat another entity (animal or plant).
        Subclasses define energy gain logic.
        """
        raise NotImplementedError

    def eaten(self, predator):
        """
        Called when this organism is eaten.
        Default behavior: die.
        """
        self.alive = False
        self.kill()

    def reproduce(self, partner):
        """
        Attempt reproduction.
        Subclasses decide rules and offspring type.
        """
        raise NotImplementedError

    # ==========================================================
    # Movement helpers
    # ==========================================================
    def get_target(self):
        area=self.map.get_neighbour(self.tile,rang=self.genome.vision)
        if not area:
            return None

        for tile in area:
            if tile.biome!='shallow-water':
                return tile
        return random.choice(area)
    def move(self,target=None,dt=1/60):
        """Move in a direction using genome speed."""
        if not self.alive:
            return
        if self.time_till_move>0:
            return
        if(target!=None):
            self.target=target
        if len(self.path)==0:
            if self.target==None:   # check for no variable call
                self.target=self.get_target()
                self.get_path()
                self.move(dt=dt)
                return 
            else: #there is a target but not a path
                self.get_path()
                self.move(dt=dt)
                return
        else:   #there is a path 
            if self.target==None: 
                #there is a path but no target so assuming the path to be in ascending order and assuming lest tile in path to be target doing move() again
                self.target=self.path[-1]
                self.move(dt=dt)
                return
            else:
                # the best case that there is a path and there is a target 
                next=self.path.pop(0)
                self.map.move(self.tile,next,self)
                self.tile=next
                self.position=next.world_pos
                # checking if we reached the destiny
                if next==self.target and  len(self.path)==0:
                    self.target=None
                
        # add waiting time till next movement 
        wait=(1/self.genome.speed) #time = distanse/speed
        self.time_till_move = wait

    def wander(self, dt=1.0/60):
        """Random wandering movement."""
        self.move(dt=dt)
    def get_path(self, target=None):
        """generates a greedy path toward the target (ITERATIVE + SAFE)"""

        if target is None:
            target = self.target
        if target is None:
            self.path = []
            return

        if self.tile == target:
            self.path = []
            self.target = None
            return

        self.path = []  # reset path every time (CRITICAL)

        current = self.tile
        visited = set()
        max_steps = 100  # hard safety cap

        for _ in range(max_steps):
            if current == target:
                return

            visited.add(current)
            adj = self.map.get_adjacent(current)

            if not adj:
                break

            best_tile = None
            best_dist = float("inf")

            for tile in adj:
                if tile == target:
                    self.path.append(tile)
                    return

                if tile in visited:
                    continue

                d = self.map.distance_to(tile, target)
                if d < best_dist:
                    best_tile = tile
                    best_dist = d

            if best_tile is None:
                break

            self.path.append(best_tile)
            current = best_tile

        # fail-safe cleanup
        if not self.path:
            self.target = None


    def __str__(self):
        return (
            f"Organism<{self.species}> "    
            f"age={self.age:.2f} "
            f"energy={self.energy:.2f} "
            f"hunger={self.hunger:.2f} "
            f"thirst={self.thirst:.2f}"
        )


print("OrganismSprite loaded from", __name__)
