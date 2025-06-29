from resources_classes import Plant, Water
from animal_base import Animal
from herbivorous_class import Herbivorous
from carnivorous_class import Carnivorous
from Environment import Environment


"""This is the base wich I'll be working with. In this code there are not all the features that I explained at the doc README,
but is a funcitional code that shows how works (at least an initial version) the AI of the entities (now managed with a weight-based logic),
how they search for elements, how do they move towards them... In every function you'll see a little description of what do they do,
although there are some that won't be used for now. I've created a little function, main, that shows how does the project work.
There are mone than one of this functions, that shows different functionalities of the project.

As the user interface is one of the last things that I'll programm, and the one in wich I need more help, for now I'll be printing the
grid in the terminal with symbols, with the function print_grid().

All print functions, except the grid, are just for seeing how the new functionalities work, and won't be maintained.

IMPORTANT! If the animals don't do anything during certain turns, it's not an error, is just the basic night functionality, wich will be improved"""


def main():
    # Show of how does the project work. 
    mundo = Environment("Ecosystem Test", 10, 10)
    herbivorous = Herbivorous(5, 5, world= mundo, vision=5, velocity=2, hunger= 20, thirst= 14)
    herbivorous2 = Herbivorous(8, 5, world= mundo, vision=5, velocity=2, hunger= 20, thirst= 14)

    plant = Plant(6, 7, 33)
    plant2= Plant(0, 0, 29)
    water1= Water(4, 3, 20)
    water2= Water(3, 1, 18)

    # Add entities to the world
    mundo.add_entity(herbivorous)
    mundo.add_entity(herbivorous2)
    mundo.add_entity(plant)
    mundo.add_entity(plant2)
    mundo.add_entity(water1)
    mundo.add_entity(water2)

    # 100 cycle simulation
    for _ in range(100):
        mundo.execute_turn()

def main_reproduce():
    # Show of how does the reproduction logic works. As reproduction requires almost idilic conditoins, at least for now, they're setted at an initial point.
    # As you will see, this function shows one of the main problems of the explore function, explained in the own function.
    mundo = Environment("Ecosystem Test", 10, 10)
    herbivorous = Herbivorous(5, 5, world= mundo, vision=5, velocity=2, hunger= 20, thirst= 14)
    herbivorous2 = Herbivorous(8, 5, world= mundo, vision=5, velocity=2, hunger= 20, thirst= 14)

    herbivorous.turns_without_eat= 0
    herbivorous.turns_without_drink= 0
    herbivorous2.turns_without_eat= 0
    herbivorous2.turns_without_drink= 0
    herbivorous.gender= "male"
    herbivorous2.gender= "female"
    herbivorous.reproduction_cooldown= 0
    herbivorous2.reproduction_cooldown= 0
    herbivorous.stats["reproduction_rate"]= 90
    herbivorous2.stats["reproduction_rate"]= 90

    # Add the entities to the world
    mundo.add_entity(herbivorous)
    mundo.add_entity(herbivorous2)

    mundo.current_turn= 300000 # As the animals must be over 20 years to reproduce, and their age is calculated via this var and their birth turn, wich can't be modified, this is the best way to
    # simulate the scenario, as the entities were added previously to changing this property (wich means that current turn=  300000, birth turn = 0)

    # 100 cycle simulation
    for _ in range(100):
        mundo.execute_turn()

main()