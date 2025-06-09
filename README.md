# PyEcosystem-Simulator
Ecosystem simulator with Python. Several elements, such as herbivors and predators, react in a 2D matrix to needs, threats...

First of all, I'd like to advise that I'm not a native English speaker, so I apologize for any mistake I may commit.
I'd be thankfull to any type of message related to the code, like corrections, possibilities to optimize it, and suggestions for further implementations.

This is an educational and experimental project, that tryes to explore how the Object-Oriented Programming (POO) in Python allows to create modular and escalable projects.

How does it work?
It's all based in a 2d grid, where many entities are present, and depending on the other elements nearby, can do:
- Search for food or water
- Escape threats (like predators)
- Rest or reproduce
- Die of hunger, thirst, or age
- Interact with evolving environmental conditions
between others

The project is now on its initial fase, where I'm starting to develop all the base logic. That's why I would be very gratefull to any suggestion. The idea is to create various functionalities, explained below, and all this to be shown through something like Tkinter. The final version should have an interface, and also collect and show all the data from the simulation. All the project works with turns, wich represent an hour.
Functionalities that will be implemented:
-Resources: plants and poodles of water will be regenerated continuosly, depending on the season.
- Age: every entity will have a property with the "turn" when they were born, and by compering it with the cycle actual, they'll know their age. Their stats will decrease as they approach their maximum age, and when they reach it they will die.
- Energy: if they don't eat or drink for a while, they'll lose some. As well as if they're ill or attacked. If is equal to 0, they die.
- Illness: it will be a class, and will attack to some statistics of the animal at every turn, until the animal die or recovers. May be lethal if the illness is very developed
- Statistics of every entitie: such as velocity, defense (to illness and predators), max_age, vision...
- Genome: (the name is indicative). Every entity will have some statistics that will change very slow with the time, and will be influenced by the environment (if there's a drought, the animal will need less water). And also, every animal will be able to pass a few of it's statistics to their descendence, and the others will be random.
- Artificial Inteligence to decide what to do: every entitie will have to decide where to move, depending on the elements they've on view, the hunger or thirst they have, the presence of predators...
Although there are many other functions, these are most of the principals.

If the project was a success, I would like to implement some other functions. For example, that there were herds, special illness or animals, logic of scavengers and corpses, events (as floods)...

License:  MIT license. This is an open and free code, and I'd love for you to experiment with it.
