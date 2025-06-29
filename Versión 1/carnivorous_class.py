from animal_base import Animal

class Carnivorous(Animal):
    def __init__(self, x, y, **kwargs):
        defaults = {"velocity": 0,  # If a value is not entered, these are used, which are different from those of the animal class. They must be filled, and will be random.
                    "defense": 0,
                    "reproduction_rate": 0,
                    "food_efficiency": 0,
                    "max_age": 0,
                    "deterioration": 0,
                    "illness_resistance": 0,
                    "hunger": 0,
                    "thirst": 0,
                    "vision": 0,
                    }  # Defaults specífics
        combined = {**defaults, **kwargs}
        super().__init__(x, y, **combined)
        self.type= "carnivorous"

    def chase_animal(self):
        pass

    def kill_animal(self):
        pass

    def eat_animal(self):
        pass