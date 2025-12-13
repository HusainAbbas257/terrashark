import random

metabolism_constant = 5
variation = 0.1

class Genome:
    """
    Represents a species genome with traits and methods to reproduce with realistic variations.
    """
    def __init__(self, species, speed, vision, hunger_max,thirst_max, max_age, reproductive_crit, size, fertility, energy=100, age=0):
        self.species = species
        self.speed = speed
        self.vision = vision
        self.hunger = hunger_max
        self.thirst=thirst_max
        self.max_age = max_age
        self.reproductive_crit = reproductive_crit
        self.size = size
        self.fertility = fertility
        self.age = age
        self.energy = energy
        self.metabolism = self.get_metabolism()

    def get_metabolism(self):
        """Metabolism scales with size (Kleiber's law) and activity traits."""
        return metabolism_constant * (self.size ** 0.75) * (self.hunger*self.thirst)**0.5 / (self.speed * self.vision)

    def distance(self, other: 'Genome'):
        """Weighted trait distance; inf if species differ."""
        if self.species != other.species:
            return float('inf')
        dist = (
            2 * abs((self.speed - other.speed) / self.speed) +
            1.5 * abs((self.vision - other.vision) / self.vision) +
            1.0 * abs((self.hunger - other.hunger) / (self.hunger*self.thirst)**0.5) +
            0.5 * abs((self.max_age - other.max_age) / self.max_age) +
            abs((self.reproductive_crit - other.reproductive_crit) / self.reproductive_crit) +
            1.0 * abs((self.size - other.size) / self.size)
        )
        return dist / 6

    @staticmethod
    def child_factor(father_factor, mother_factor):
        """Child trait with small or occasional big mutation."""
        mean = (father_factor + mother_factor) / 2
        if random.random() < 0.1:
            # 10% chance of big mutation
            return max(0, random.gauss(mean, variation * 3))
        return max(0, random.gauss(mean, variation))

    def can_reproduce(self, partner):
        """Checks if reproduction is possible (distance + energy + age)."""
        if self.distance(partner) > self.reproductive_crit:
            return False
        # Ensure both parents have enough energy and are mature
        if self.energy < 20 or partner.energy < 20:
            return False
        if self.age < 1 or partner.age < 1:
            return False
        return True

    def reproduce(self, partner:'Genome'):
        """Produces a child Genome if species are compatible and conditions met."""
        if not self.can_reproduce(partner):
            return None
        child = Genome(
            species=self.species,
            speed=self.child_factor(self.speed, partner.speed),
            vision=self.child_factor(self.vision, partner.vision),
            hunger_rate=self.child_factor(self.hunger, partner.hunger),
            thirst_max=self.child_factor(self.thirst, partner.thirst),
            max_age=self.child_factor(self.max_age, partner.max_age),
            reproductive_crit=self.child_factor(self.reproductive_crit, partner.reproductive_crit),
            size=self.child_factor(self.size, partner.size),
            fertility=self.child_factor(self.fertility, partner.fertility)
        )
        # Reduce parent energy after reproduction
        self.energy -= 10
        partner.energy -= 10
        return child
    def __str__(self):
        return f'genome for {self.species}'

# quick test
if __name__ == '__main__':
    g1 = Genome('shark', speed=5, vision=10, hunger_rate=3,thirst_max=10, max_age=20, reproductive_crit=0.3, size=50, fertility=2)
    g2 = Genome('shark', speed=6, vision=9, hunger_rate=4,thirst_max=12, max_age=18, reproductive_crit=0.3, size=55, fertility=3)
    child = g1.reproduce(g2)
    print(vars(child) if child else "Too different to reproduce")
