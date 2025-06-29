import random
import ai_entities as brain

class Animal():
    def __init__(self, x, y, world, velocity= 1, defense= 60, reproduction_rate= 70, food_efficiency= 90, max_age= 500, deterioration= 0.93, illness_resistance= 80, hunger= 36, thirst= 12, vision= 5, curiosity= 80):
        self.position= (x, y)
        self.world= world # As all the animal-related functionalities will be managed by this class, here's an instance of the world they'll be placed in.
        self.alive= True
        self.age= 0
        self.energy= 100 # From 0 to 100. When energy= 0, the entity dies.
        self.illness= {"ill": False}
        self.turns_without_eat= 0
        self.turns_without_drink= 0
        self.current_action= None  # Action that the entity is doing at the moment. Will affect the actoins weights
        self.current_action_duration= 0
        self.turn_of_birth= 0
        self.reproduction_cooldown= 0 # Tame the animal has to wait, in turns, to reproduce.
        self.gender= random.choice(["male", "female"]) # Just for the reproduction logic, it may affect the animal properties in a future.
        self.stats= {
            "velocity": velocity, # Sections for turn. When running, it's multiplied *2. It isn't actually implemented, and may be discarted
            "defense": defense, # Resistance in front of predator's attacks and diseases.
            "reproduction_rate": reproduction_rate, # % of reproducing
            "food_efficiency": food_efficiency, # % of food turned into energy, it's usually very high (more in carnivorous than in herbivorous). The diseases lower it a lot.
            "max_age": max_age, # Estimated turns to live. Must arrive at them with minimum a 25% of its stats.
            "deterioration": deterioration, # How much the stats will go down in every turn, once passed half of the spectation of life. (stats * deterioration, usually 0.9995-0.99)
            "illness_resistance": illness_resistance, # Probability of not get a disease.
            "hunger": hunger, # Turns without eating before starting to loose energy. The animal will search for food previously.
            "thirst": thirst, # The same as hunger.
            "vision": vision, # Number of sections that can detect. Higher in carnivorous.
            "curiosity": curiosity # Between 0 and 100, defines how much the animal will explore.
        }
        self.memory= {
            "directions": [],  # Memory of the last 5 directions taken, so it can avoid going back to them.
            "turns_exploring": 0, # Continued turns expended exploring, so it changes the direction sometimes.
        }

    def find_nearest_objective(self, objectives): 
        # Just returns the nearest object to an entity. objectives= list with elements.
        if not objectives: 
            return None
        x_entity, y_entity = self.position

        nearest_objective = None
        minimum_distance = float('inf')
        for objective in objectives:
            x_objective, y_objective = objective.position
            distance = abs(x_entity - x_objective) + abs(y_entity - y_objective)

            if distance < minimum_distance:
                minimum_distance = distance
                nearest_objective = objective

        return nearest_objective
    
    def actualize_memory_directions(self, last_objective):
        # Updates the memory of the entity with the last objective, so it can avoid going back to it. Can only store up to 5 positions.It doesn't return anything.
        if not last_objective.position in self.memory["directions"]:
            self.memory["directions"].append(last_objective.position)
            if len(self.memory["directions"]) > 5:
                self.memory["directions"].pop(0)


    def chose_movement(self, options): 
        # This is the AI of the entities, where they choose what to do depending on their urges and a list of elements (generally created caring about the vision property of the entity)
        # Has a dictionary with every possible actoin, which calls a specific functoin for every action.    
        world= self.world

        disposables = {
            "water": [obj for obj in options if obj.type == "water"],
            "plant": [obj for obj in options if obj.type == "plant"],
        }

        weights = {
            "drink": brain.weight_water(self, disposables["water"]),
            "eat": brain.weight_food(self, disposables["plant"]),
            "rest": brain.weight_rest(self),
            "explore": brain.weight_explore(self, disposables["water"] + disposables["plant"]),
            "reproduce": brain.weight_reproduce(self)
        }
        best_action = max(weights, key=weights.get)
        if weights[best_action] == 0: # This is just to avoid errors when initializing when the stats values are not stable
            best_action= "rest"
        print(f"Weights calculated: {weights}\nThe best option is: {best_action}")

        if self.current_action== best_action:
            self.current_action_duration += 1
        else:
            self.current_action = best_action
            self.current_action_duration = 1

        print("Current action:", self.current_action, "with duration:", self.current_action_duration)

        self.execute_action(best_action, disposables)

    def execute_action(self, best_action, disposables):
        # Executes the best possible action, the function is called just after the chose_movement function. It doesn't return anything.
        world= self.world
        
        if best_action == "drink":
            water= self.find_nearest_objective(disposables["water"])
            self.actualize_memory_directions(water) # You add the current objective position to the "directions" list
            if world.are_adjacent_objects(self, water):
                self.drink(water)
            else:
                print(f"Objective detected: water in {water.position}")
                path = world.calculate_path(self.position, water.position)
                print(f"Path to objective: {path}")
                next_pos = path[1]
                world.move_entity(self, *next_pos)
        elif best_action == "eat":
            food= self.find_nearest_objective(disposables["plant"])
            self.actualize_memory_directions(food)
            if world.are_adjacent_objects(self, food):
                self.eat_plant(food)
            else:
                print(f"Objective detected: food in {food.position}")
                path = world.calculate_path(self.position, food.position)
                print(f"Path to objective: {path}")
                next_pos = path[1]
                world.move_entity(self, *next_pos)
        elif best_action == "explore":
            self.explore()        
        elif best_action == "rest":
            self.rest()        
        elif best_action == "reproduce":
            self.reproduce(self.find_potential_mate())

    

    def take_a_look_around(self):
        # Returns a list with the nearby entities to the entity, depending on its vision (analyze_entity_environment).
        # Just don't ask. It works, due to Manhatan distance or wathever is it.
        world= self.world

        x, y = self.position
        vision = self.stats["vision"]
        neraby_entities = []

        x_min = max(0, x - vision)
        x_max = min(world.cols - 1, x + vision)
        y_min = max(0, y - vision)
        y_max = min(world.rows - 1, y + vision)

        for cx in range(x_min, x_max + 1):
            for cy in range(y_min, y_max + 1):
                if (cx, cy) == (x, y):
                    continue

                distance = abs(cx - x) + abs(cy - y)
                if distance <= vision:
                    cell_entity = world.world_dic.get((cx, cy))
                    if cell_entity and cell_entity != self:
                        neraby_entities.append(cell_entity)

        return neraby_entities

    def check_interactions(self):
    # Checks if it can do any useful interaction, and does it in an affirmative case. It doesn't return anything.
    # This function, for now, is't used, as leaded to double excutions, and could be activated when it wasn't meant to...
    # It is "substituded" by the function "execute_action"
        world= self.world
        objects= world.get_adjacent_objects(self)
        if len(objects)== 0:
            return None
        else:
            object= self.chose_movement(objects)
            if not object:
                return None
            elif object == "rest":
                print("The animal is resting")  # Implement resting logic
            elif object== "explore":
                self.explore()
            elif object.type == "water":
                self.drink(object)
            elif object.type == "plant":
                self.eat_plant(object)

    def drink(self, source):
        # Update turns_without_drink of the entity and the poodle of water.It doesn't return anything.
        world= self.world

        if source.quantity <= 0:
            world.remove_entity(source)
        else:
            print(f"The animal is drinking from {source.quantity}")
            if source.quantity < 10:
                source.quantity = 0
            else:
                source.quantity -= 10
            if source.quantity <= 0:
                world.remove_entity(source)
            self.turns_without_drink= 0
        

    def eat_plant(self, plant):
        # Updates turns_without_eat of the entity and the plant. It doesn't return anything. 
        world= self.world

        if plant.quantity <= 0:
            world.remove_entity(plant)
        else:
            print(f"The animal is eating from {plant.quantity}")
            if plant.quantity < 10:
                plant.quantity = 0
            else:
                plant.quantity -= 10
            if plant.quantity <= 0:
                world.remove_entity(plant)
            self.turns_without_eat = 0

    def rest(self):
        # A simple function added just to be able to run the project. Possibly, the final feature won't be like this...
        self.energy += 5

    def update_animal_stats(self):
        # Updates age, turns_without_eat/drink, energy, deterioration of the stats due to aging... It doesn't return anything.
        turns_for_years=  24 * 30 * 12
        turns_passed_by = self.world.current_turn - self.turn_of_birth
        self.age = turns_passed_by // turns_for_years  # Actualizar edad
        self.turns_without_eat += 1
        self.turns_without_drink += 1
        self.energy -= 1  # Decrease energy each turn, YOU MUST MODIFY THIS (depending on the current activity they're realizing)
        if self.reproduction_cooldown > 0: # New property, wich ensure the animal will wait between 280 and 360 days to reproduce again.
            self.reproduction_cooldown -= 1
        else:
            self.reproduction_cooldown= 0

    def explore(self):
        # As you can see, the function is really emty. For now, if the animal wants to explore, it just separates from its last objective. If the animal never had an objective, the logic brakes,
        # if it gets to a corner, it gets stuck... this feature will be improved soon.
        world= self.world

        directions= self.memory["directions"] # New property, wich will help to develop further features (as remember visited places or resources out of the vision camp, remember a past mate to reproduce...)
        if directions:
            positions= world.opposite_directions_to_position(self, directions[-1])
            if positions:
                position= random.choice(positions)
                x, y= position
                world.move_entity(self, x, y)
            else:
                pass

    def find_potential_mate(self):
        # Returns, if found a compatible mate to reproduce. Needs to accomplish some conditions, just as the main entity.
        nearby = self.take_a_look_around()
        for ne in nearby:
            if (isinstance(ne, Animal) and ne.type == self.type and 
                ne.reproduction_cooldown <= 0 and ne.gender != self.gender and
                ne.age >= 20 and ne.energy >= 90 and ne.turns_without_eat < 10 and
                ne.turns_without_drink < 10):
                return ne
        return None

    def reproduce(self, mate):
        # Reproduction logic. For now, the new entity spawns just at the moment, in a future a boolean state like "pregnant" will be modified, and the animal will wait ~9 months.
        world= self.world
        if not world.are_adjacent_objects(self, mate):
            # The animals approximate if they're not near. That's one of the reasons it's important, when deciding the action, for the animal to try mantaining the current action, as two animals
            # could be interested in reproducing, but when they get side by side the reproduction weight is not the biggest.
            path= world.calculate_path(self.position, mate.position)
            next_pos = path[1] if len(path) > 1 else path[0]
            world.move_entity(self, *next_pos)
            print("Moving towards the mate to reproduce")
        else:
            value= random.random()
            if value < (self.stats["reproduction_rate"] / 100):
                self.make_baby(mate)
                self.energy -= 50
                mate.energy -= 50
                self.reproduction_cooldown= random.randint(280, 360) * 24 # --> 1 turn= 1 hour, we * 24 because the animal will wait for mostly a year
                mate.reproduction_cooldown= random.randint(280, 360)
                print("The reproduction was succesful!!")
            else:
                print(f"The reproduction was not succesfull, {value} was not less than {self.stats["reproduction_rate"] / 100}")

    def make_baby(self, mate):
        # This function will hold the functionalities of the heredation, wich will be much more richer... for now, just sums the fathers's properties and divides them by 2... also places the animal in the grid.
        from herbivorous_class import Herbivorous
        from carnivorous_class import Carnivorous
        
        world= self.world

        possible_positions = [
            (self.position[0]+dx, self.position[1]+dy)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
        ] + [
            (mate.position[0]+dx, mate.position[1]+dy)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
        ]

        positions = [pos for pos in possible_positions if world.valid_section(pos)]
        if not positions:
            return
        position = random.choice(positions)

        x, y= position
        velocity= 1
        defense= (self.stats["defense"] + mate.stats["defense"]) / 2
        reproduction_rate= (self.stats["reproduction_rate"] + mate.stats["reproduction_rate"]) / 2
        food_efficiency= (self.stats["food_efficiency"] + mate.stats["food_efficiency"]) / 2
        max_age= (self.stats["max_age"] + mate.stats["max_age"]) / 2
        deterioration= (self.stats["deterioration"] + mate.stats["deterioration"]) / 2
        illness_resistance= (self.stats["illness_resistance"] + mate.stats["illness_resistance"]) / 2
        hunger= (self.stats["hunger"] + mate.stats["hunger"]) / 2
        thirst= (self.stats["thirst"] + mate.stats["thirst"]) / 2
        vision= 5
        curiosity= 100

        if self.type== "herbivorous":
            new_entity= Herbivorous(x, y, world= world, velocity= velocity, defense= defense, reproduction_rate= reproduction_rate, food_efficiency= food_efficiency, max_age= max_age, deterioration= deterioration, illness_resistance= illness_resistance, hunger= hunger, thirst= thirst, vision= vision, curiosity= curiosity)
        elif self.type== "carnivorous":
            new_entity= Carnivorous(x, y, world= world, velocity= velocity, defense= defense, reproduction_rate= reproduction_rate, food_efficiency= food_efficiency, max_age= max_age, deterioration= deterioration, illness_resistance= illness_resistance, hunger= hunger, thirst= thirst, vision= vision, curiosity= curiosity)
        else:
            print(f"The animal isn't a carnivorous or herbivorous. Animal tyoe: {self.type}")
            return None
        world.add_entity(new_entity)