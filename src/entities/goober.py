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
            species="goober",
            genome=genome,
            map=map,
            tile=tile,
            position=position,
            radius=radius
        )

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

    def do_task(self, task, **kwargs):
        if task == "eat":
            plant = kwargs.get("target")
            if plant:
                self.eat(plant)

        elif task == "drink":
            # placeholder for water tiles later
            self.thirst = max(0.0, self.thirst - self.genome.energy * 0.1)

        elif task == "reproduce":
            return self.reproduce(kwargs.get("partner"))

        elif task == "wander":
            self.wander()

    # ==================================================
    # Herbivore behavior
    # ==================================================
    def eat(self, target:'tree.Tree'):
        """
        Eat a plant (Tree).
        """
        if not target or not target.alive:
            return

        energy_gain = target.genome.energy * 0.2
        self.energy = min(self.genome.energy, self.energy + energy_gain)
        self.hunger = max(0.0, self.hunger - energy_gain)

        target.eaten(self)

    def reproduce(self, partner=None):
        """
        Simple asexual reproduction for now.
        """
        if self.energy < self.genome.energy * 0.7:
            return None

        neighbors = self.map.get_neighbour(self.tile, self.genome.vision)
        if not neighbors:
            return None

        tile = random.choice(neighbors)
        child_genome = self.genome.reproduce(self.genome)

        child = Goober(
            genome=child_genome,
            map=self.map,
            tile=tile,
            position=tile.world_pos
        )

        self.energy *= 0.5
        return child
