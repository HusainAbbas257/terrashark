from src.entities import Organism
import random
import pygame


class Tree(Organism.OrganismSprite):
    """
    Passive plant organism.
    Gains energy via photosynthesis.
    Can be eaten and can reproduce via seeds.
    """

    def __init__(
        self,
        genome,
        map,
        tile=None,
        position=(0, 0),
        radius=6,
        apples=0
    ):
        super().__init__(
            genome=genome,
            map=map,
            tile=tile,
            position=position,
            radius=radius
        )

        self.apples = apples
        self.seeds = 0

        #   enforce tile ownership invariant 
        if self.tile is not None:
            self.tile.place(self)

    # Decision making
    def get_task(self):
        # NOTE: death is already handled by base update()
        if self.energy < self.genome.energy * 0.75:
            return "photosynthesis"

        if self.seeds < 3 and self.age > 5:
            return "reproduce"

        return "idle"

    def do_task(self, task, **kwargs):
        if task == "photosynthesis":
            return self.eat()

        elif task == "reproduce":
            return self.reproduce()

        elif task == "idle":
            return

    # Plant-specific behavior
    def eat(self, target=None):
        """
        Photosynthesis:
        - restores energy
        - reduces hunger/thirst
        - may grow apples
        """
        energy_gain = self.genome.energy * 0.1

        self.energy = min(self.genome.energy, self.energy + energy_gain)
        self.hunger = max(0.0, self.hunger - energy_gain * 0.5)
        self.thirst = max(0.0, self.thirst - energy_gain * 0.5)

        if self.apples < 3:
            self.apples += 1

    def eaten(self, predator):
        """
        Animal eats apples first.
        Tree dies only if depleted.
        """
        if self.apples > 0:
            self.apples -= 1
            return 1
        else:
            self.alive = False
            self.kill()
            return -1

    def reproduce(self):
        """
        Drop a seed into a nearby tile.
        """
        if self.seeds >= 3 or not self.tile:
            return None

        neighbors = self.map.get_neighbour(self.tile, self.genome.vision)
        if not neighbors:
            return None

        #   biome + occupancy validation 
        valid_tiles = [
            t for t in neighbors
            if t.biome not in ("deep-ocean", "shallow-water")
            and len(t.organism) == 0
        ]

        if not valid_tiles:
            return None

        target_tile = random.choice(valid_tiles)

        #   genome reproduction API 
        child_genome = self.genome.reproduce()

        child = Tree(
            genome=child_genome,
            map=self.map,
            tile=target_tile,
            position=target_tile.world_pos
        )

        #   energy + seed cost 
        self.energy *= 0.5
        self.seeds += 1

        return child
