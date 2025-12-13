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
        _IMAGES[name] = pygame.image.load(path).convert_alpha()
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
        position=(0, 0),#removed color as it is not needed anymore
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
    def update(self, dt=1.0):
        """Handles aging, metabolism, hunger, thirst, and death."""
        if not self.alive:
            self.kill()
            return

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
    def move(self, direction: pygame.Vector2, dt=1.0):
        """Move in a direction using genome speed."""
        if not self.alive:
            return

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.position += direction * self.genome.speed * dt
        self.rect.center = self.position

    def wander(self, dt=1.0):
        """Random wandering movement."""
        angle = random.uniform(0, 360)
        direction = pygame.Vector2(1, 0).rotate(angle)
        self.move(direction, dt)

    def distance_to(self, other) -> float:
        """Euclidean distance to another organism."""
        return self.position.distance_to(other.position)

    def __str__(self):
        return (
            f"Organism<{self.species}> "
            f"age={self.age:.2f} "
            f"energy={self.energy:.2f} "
            f"hunger={self.hunger:.2f} "
            f"thirst={self.thirst:.2f}"
        )


print("OrganismSprite loaded from", __name__)
