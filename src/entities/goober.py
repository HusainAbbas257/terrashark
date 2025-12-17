from src.entities import Organism,tree
import random


class Goober(Organism.OrganismSprite):
    """
    Herbivorous animal.
    Eats plants, wanders, reproduces.
    """

    def __init__(
        self,
        genome,
        map,
        tile=None,
        position=(0, 0),
        radius=5
    ):
        super().__init__(
            genome=genome,
            map=map,
            tile=tile,
            position=position,
            radius=radius
        )

        self.partner = None
        self.task = None
        self.target = None

        #memory / meeting-point system
        self.memory_water = None      # remembers water tile
        self.memory_partner = None    # remembers partner tile
        self.memory_food = None       # remembers last food tile

        #enforce tile ownership
        if self.tile is not None:
            self.tile.place(self)

    # ==================================================
    # Decision making
    # ==================================================
    def get_task(self):
        # priority order matters
        if self.hunger > self.genome.hunger * 0.6:
            return "eat"

        if self.thirst > self.genome.thirst * 0.6:
            return "drink"

        if self.energy > self.genome.energy * 0.8 and self.age > 5:
            return "reproduce"

        return "wander"

    def find_organism(self, organisms):
        """
        Scan nearby tiles for a specific organism type.
        """
        for tile in self.map.get_neighbour(self.tile, self.genome.vision):
            for org in tile.organism:
                if isinstance(org, organisms):
                    return (org, tile)
        return (None, None)

    def do_task(self, task):
        self.task = task

        if task == "eat":
            plant, plant_tile = self.find_organism(tree.Tree)

            if plant and plant_tile:
                #remember food location
                self.memory_food = plant_tile
                self.move(plant_tile)
                self.eat(plant)
                return

            #fallback to remembered food
            if self.memory_food:
                self.move(self.memory_food)
                return

        elif task == "drink":
            #use remembered water if exists
            if self.memory_water:
                self.move(self.memory_water)
                self.thirst = max(0.0, self.thirst - self.genome.energy * 0.1)
                return

            # placeholder: passive thirst reduction
            self.thirst = max(0.0, self.thirst - self.genome.energy * 0.05)

        elif task == "reproduce":
            #partner memory 
            if self.partner:
                return self.reproduce(self.partner)

            partner, partner_tile = self.find_organism(Goober)
            if partner and partner_tile and partner is not self:
                self.partner = partner
                self.memory_partner = partner_tile
                self.move(partner_tile)
                return self.reproduce(partner)

            # fallback: move toward remembered partner
            if self.memory_partner:
                self.move(self.memory_partner)
                return

        elif task == "wander":
            self.wander()

    # ==================================================
    # Herbivore behavior
    # ==================================================
    def eat(self, target: 'tree.Tree'):
        """
        Eat a plant (Tree).
        """
        if not target or not target.alive:
            return

        energy_gain = target.genome.energy * 0.2
        self.energy = min(self.genome.energy, self.energy + energy_gain)
        self.hunger = max(0.0, self.hunger - energy_gain)

        result = target.eaten(self)

        #forget food if depleted
        if result == -1:
            self.memory_food = None

    def reproduce(self, partner=None):
        """
        Simple asexual reproduction for now.
        """
        if self.energy < self.genome.energy * 0.7:
            return None

        neighbors = self.map.get_neighbour(self.tile, self.genome.vision)
        if not neighbors:
            return None

        #biome + occupancy check
        valid_tiles = [
            t for t in neighbors
            if t.biome not in ("deep-ocean", "shallow-water")
            and len(t.organism) == 0
        ]

        if not valid_tiles:
            return None

        tile = random.choice(valid_tiles)

        #genome API
        child_genome = self.genome.reproduce()

        child = Goober(
            genome=child_genome,
            map=self.map,
            tile=tile,
            position=tile.world_pos
        )

        self.energy *= 0.5
        return child
