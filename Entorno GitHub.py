import random
import time

"""This is the base wich I'll be working with. In this code there are not all the features that I explained at the doc README,
but is a funcitional code that shows how works (at least an initial version) the AI of the entities, how they search for elements,
how do they move towards them... In every function you'll see a little description of what do they do, although there are some that
won't be used for now. I've created a little function, main, that shows how does the project work.

As the user interface is one of the last things that I'll programm, and the one in wich I need more help, for now I'll be printing the
grid in the terminal with symbols, with the function print_grid()"""

class Environment():
    def __init__(self, name, columns, rows, season= "spring"):
        self.name= name
        self.rows= rows
        self.cols= columns
        self.current_turn= 0
        self.current_day= 0
        self.current_month= 0
        self.current_year= 0
        self.active_rain= False
        self.season= season
        self.world_dic= {}
        self.entities= []
        m= columns
        for x in range(self.cols):
            for y in range(self.rows):
                self.world_dic[(x, y)] = None

    def add_entity(self, entity):  
        # Add the entity to the world matrix. The position is defined in the entity itself (entity.position). It doesn't return anything.
        x, y= entity.position
        if self.valid_section(entity.position):
            self.world_dic[(x, y)]= entity
            self.entities.append(entity)

    def move_entity(self, entity, pos_x, pos_y):  
        # Update the previous position and the one where it wants to move. It doesn't return anything. 
        x_ant, y_ant= entity.position
        if self.valid_section((pos_x, pos_y)):
            self.world_dic[x_ant, y_ant]= None
            self.world_dic[pos_x, pos_y]= entity
            entity.position= (pos_x, pos_y)

    def calculate_path(self, start, end): 
        # Retorns the shortest path between 2 points (tuples (x, y)), a list with every step is needed to archieve the final position. Includes the initial and final position
        x1, y1 = start
        x2, y2 = end
        path = [(x1, y1)]
        
        while (x1, y1) != (x2, y2):
            moves = []
            
            if x1 < x2:
                moves.append((x1+1, y1))
            elif x1 > x2:
                moves.append((x1-1, y1))
                
            if y1 < y2:
                moves.append((x1, y1+1))
            elif y1 > y2:
                moves.append((x1, y1-1))
                
            # Randomly choose between the options given
            x1, y1 = random.choice(moves)
            path.append((x1, y1))
            
        return path
    
    def calculate_distance(self, entity, objective):
        # Returns the number of steps. Includes the initial and final position
        return len(self.calculate_path(entity.position, objective.position))
    
    def find_nearest_objective(self, entity, objectives): 
        # Just returns the nearest object to an entity. objectives= list with elements.
        if not objectives: 
            return None
        x_entity, y_entity = entity.position

        nearest_objective = None
        minimum_distance = float('inf')
        for objective in objectives:
            x_objective, y_objective = objective.position
            distance = abs(x_entity - x_objective) + abs(y_entity - y_objective)

            if distance < minimum_distance:
                minimum_distance = distance
                nearest_objective = objective

        return nearest_objective
    
    def classify_objects_by_tipe(self, objects, type): 
        # Returns a list with all the objects of the type specifyed from the list. objects= list of elements.
        valid_types = {"water", "plant", "herbivorous", "carnivorous"}
        if type not in valid_types:
            return []
        
        return [objetivo for objetivo in objects if objetivo.type == type]

    def chose_movement(self, entity, options): 
        # AI of the animals. Will be more complex. Depending on the stats of the entity, chooses an object from the list given. It needs an option when eny of them is useful, or
        # the list is empty and needs something. options= list of elements
        
        #Priority 1: Critic thirst 
        if entity.turns_without_drink >= entity.stats["thirst"]:
            water = [obj for obj in options if obj.type == "water"]
            if water:
                return self.find_nearest_objective(entity, water)
                
        # Priority 2: Critic hunger
        if entity.turns_without_eat >= entity.stats["hunger"]:
            if entity.type == "herbivorous":
                plants = [obj for obj in options if obj.type == "plant"]
                if plants:
                    return self.find_nearest_objective(entity, plants)
                else:
                    return None
            else:
                # Logic for carnivorous (ex: search for a prey)
                return None
        
        # Priority 3: Anticipation of needs
        if entity.turns_without_drink >= entity.stats["thirst"] - 5:
            water = [obj for obj in options if obj.type == "water"]
            if water:
                return self.find_nearest_objective(entity, water)
        
        if entity.turns_without_eat >= entity.stats["hunger"] - 10:
            if entity.type == "herbivorous":
                plants = [obj for obj in options if obj.type == "plant"]
                if plants:
                    return self.find_nearest_objective(entity, plants)
        
        # Priority 4: Rest
        if entity.energy < 40:
            return "rest" # Logic of resting

        return False  
    

    def remove_entity(self, entity): 
        # Removes an entity from the dic world_dic, and from the list entities. It doesn't return anything.
        x, y= entity.position
        self.world_dic[x, y]= None
        if isinstance(entity, Animal):
            entity.alive= False
        self.entities.remove(entity)

    def take_a_look_around(self, entity):
        # Returns a list with the nearby entities to the entity, depending on its vision (analyze_entity_environment).
        # Just don't ask. It works, due to Manhatan distance or wathever is it.
        x, y = entity.position
        vision = entity.stats["vision"]
        neraby_entities = []

        x_min = max(0, x - vision)
        x_max = min(self.cols - 1, x + vision)
        y_min = max(0, y - vision)
        y_max = min(self.rows - 1, y + vision)

        for cx in range(x_min, x_max + 1):
            for cy in range(y_min, y_max + 1):
                if (cx, cy) == (x, y):
                    continue

                distance = abs(cx - x) + abs(cy - y)
                if distance <= vision:
                    cell_entity = self.world_dic.get((cx, cy))
                    if cell_entity and cell_entity != entity:
                        neraby_entities.append(cell_entity)

        return neraby_entities

    def empty_section(self, section):
        # Returns True if the section isn't occupied (section= casilla in Spanish).
        if self.world_dic.get(section):
            return False
        else:
            return True

    def valid_section(self, casilla): 
        # Checks that the section is free and inside the limits of the world.
        x, y = casilla
        if (0 <= x < self.cols and 0 <= y < self.rows) and self.empty_section(casilla):
            return True
        else:
            return False
    
    def calculate_possible_positions(self, entity, radius):
        # Returns a list of tuples with the available positions inside the map and around the entity, depending on a radious given.
        x, y = entity.position
        possible = []
        x_min = max(0, x - radius)
        x_max = min(self.cols - 1, x + radius)
        y_min = max(0, y - radius)
        y_max = min(self.rows - 1, y + radius)
        
        for cx in range(x_min, x_max + 1):
            for cy in range(y_min, y_max + 1):
                distance = abs(cx - x) + abs(cy - y)
                if distance <= radius:
                    section = (cx, cy)
                    if self.valid_section(section):
                        possible.append(section)
        return possible

    def get_adjacent_objects(self, entity):
        # Returns a list with all the entities the entity has immediately near (up, down, left and right).
        x, y= entity.position
        possible_positions= [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        objects= []
        for position in possible_positions:
            object= self.world_dic.get(position)
            if object:
                objects.append(object)
        return objects
    
    def check_interactions(self, entity):
    # Checks if it can do any useful interaction, and does it in an affirmative case. It doesn't return anything.
        objects= self.get_adjacent_objects(entity)
        if len(objects)== 0:
            return None
        else:
            object= self.chose_movement(entity, objects)
            if not object:
                return None
            elif object == "descansar":
                print("The animal is resting")  # Implement resting logic
            elif object.type == "water":
                self.drink(entity, object)
            elif object.type == "plant":
                self.eat_plant(entity, object)

    def drink(self, entity, source):
        # Update turns_without_drink of the entity and the poodle of water.It doesn't return anything.
        if source.quantity <= 0:
            self.remove_entity(source)
        else:
            print(f"The animal is drinking from {source.quantity}")
            if source.quantity < 10:
                source.quantity = 0
            else:
                source.quantity -= 10
            if source.quantity <= 0:
                self.remove_entity(source)
            entity.turns_without_drink= 0
        

    def eat_plant(self, entity, plant):
        # Updates turns_without_eat of the entity and the plant. It doesn't return anything. 
        if plant.quantity <= 0:
            self.remove_entity(plant)
        else:
            print(f"The animal is eating from {plant.quantity}")
            if plant.quantity < 10:
                plant.quantity = 0
            else:
                plant.quantity -= 10
            if plant.quantity <= 0:
                self.remove_entity(plant)
            entity.turns_without_eat = 0

    def rest(self):
        pass
    def update_animal_stats(self, entity):
        # Updates age, turns_without_eat/drink, energy, deterioration of the stats due to aging... It doesn't return anything.
        turns_for_years=  24 * 30 * 12
        turns_passed_by = self.current_turn - entity.turn_of_birth
        entity.age = turns_passed_by // turns_for_years  # Actualizar edad
        entity.turns_without_eat += 1
        entity.turns_without_drink += 1

    def opposite_directions_to_object(self, entity, object):
        # Returns a list with tuples, with positions that add distance between the entity and another entity.
        x_ent, y_ent = entity.position
        x_obj, y_obj = object.position
        current_distance = abs(x_ent - x_obj) + abs(y_ent - y_obj)

        adjacent_positions = [
            (x_ent + 1, y_ent),
            (x_ent - 1, y_ent),
            (x_ent, y_ent + 1),
            (x_ent, y_ent - 1)
        ]
        valid_escapes = []
        for pos in adjacent_positions:
            if self.valid_section(pos):
                x_new, y_new = pos
                new_distance = abs(x_new - x_obj) + abs(y_new - y_obj)
                if new_distance > current_distance:
                    valid_escapes.append(pos)

        return valid_escapes

    def spawn_initial_entities(self):
        # This function, between others, will start all the simulation. For now is used manually, as it isn't completely developed.
        pass

    def restart_ecosystem(self):
        pass

    def update_turn(self):
        # Updates the current turn, and also in wich month and year we are. Will also manage the seasons. It doesn't return anything.
        self.current_turn += 1
        
        if self.current_turn % 24 == 0:
            self.current_day += 1
            
            if self.current_day % 30 == 0:
                self.current_month += 1

                if self.current_month % 12 == 0:
                    self.current_year += 1

    def execute_turn(self): 
        # Is the "main" function of the code. Update the stats, removes entities, execute movements and interactions... It doesn't return anything.

        self.update_turn()

        for animal in self.entities:
            if isinstance(animal, Animal):
                if isinstance(animal, Herbivorous):
                    
                    nearby_entities = self.take_a_look_around(animal)
                    objective = self.chose_movement(animal, nearby_entities)
                    self.check_interactions(animal)
                        
                    if objective == "descansar":
                        print("The animal is resting")
                    else:
                        if objective:
                            print(f"Objective detected: {objective.type} en {objective.position}")
                            path = self.calculate_path(animal.position, objective.position)
                            print(f"Path to objective: {path}")
                            
                            if len(path) > 1:
                                next_pos = path[1]
                                self.move_entity(animal, *next_pos)
                            else:
                                print("Any objective found")
                self.update_animal_stats(animal)
                        
        # Simular tiempo entre ciclos
        self.print_grid()
        time.sleep(0.5)


    
    def print_grid(self):
        #While the UI isn't developed, all the changes will be shown in the terminal with this function.
        print(f"\nCurrent state of {self.name} ({self.cols}x{self.rows}):")
        print("+" + "---+" * self.cols)
        
        for y in range(self.rows-1, -1, -1):  # Reverse order so that (0,0) is at the bottom
            row = "|"
            for x in range(self.cols):
                cell= self.world_dic[(x, y)]
                if cell == None:
                    cell= "-"
                else:
                    cell= cell.type
                    if cell== "herbivorous":
                        cell= "H"
                    elif cell== "carnivorous":
                        cell= "C"
                    elif cell== "plant":
                        cell= "P"
                    elif cell == "water":
                        cell= "="
                row += f" {cell} |"
            print(row)
            print("+" + "---+" * self.cols)


class Animal():
    def __init__(self, x, y, velocity= 1, defense= 60, reproduction_rate= 70, food_efficiency= 90, max_age= 500, deterioration= 0.93, illness_resistance= 80, hunger= 36, thirst= 12, vision= 4):
        self.position= (x, y)
        self.alive= True
        self.age= 0
        self.energy= 100 # From 0 to 100. When energy= 0, the entity dies.
        self.illness= {"ill": False}
        self.turns_without_eat= 0
        self.turns_without_drink= 0
        self.turn_of_birth= 0
        self.stats= {
            "velocity": velocity, # Sections for turn. When running, it's multiplied *2.
            "defense": defense, # Resistance in front of predator's attacks and diseases.
            "reproduction_rate": reproduction_rate, # % of reproducing
            "food_efficiency": food_efficiency, # % of food turned into energy, it's usually very high (more in carnivorous than in herbivorous). The diseases lower it a lot.
            "max_age": max_age, # Estimated turns to live. Must arrive at them with minimum a 25% of its stats.
            "deterioration": deterioration, # How much the stats will go down in every turn, once passed half of the spectation of life. (stats * deterioration, usually 0.9995-0.99)
            "illness_resistance": illness_resistance, # Probability of not get a disease.
            "hunger": hunger, # Turns without eating before starting to loose energy. The animal will search for food previously.
            "thirst": thirst, # The same as hunger.
            "vision": vision, # Number of sections that can detect. Higher in carnivorous.
        }

class Herbivorous(Animal):
    def __init__(self, x, y, **kwargs):
        defaults = {"velocity": 0,  # Si no se introduce un valor, se usan estos, que son distintos a los de la clase animal. They must be filled, and will be random.
                    "defense": 0,
                    "reproduction_rate": 0,
                    "food_efficiency": 0,
                    "max_age": 0,
                    "deterioration": 0,
                    "illness_resistance": 0,
                    "hunger": 0,
                    "thirst": 0,
                    "vision": 0,
                    }  # Defaults specifics
        combined = {**defaults, **kwargs}
        super().__init__(x, y, **combined)
        self.type = "herbivorous"

    def eat_plant(self):
        pass


class Carnivorous(Animal):
    def __init__(self, x, y, **kwargs):
        defaults = {"velocity": 0,  # Si no se introduce un valor, se usan estos, que son distintos a los de la clase animal
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


class Plant():
    def __init__(self, x, y, quantity):
        self.position= (x, y)
        self.type= "plant"
        self.quantity= quantity

    def grow(self):
        pass

    def reproduce(self):
        pass

    def update_stats(self): # Plants won't be affected by their age, but by any extern condition or illness.
        pass



class Water():
    def __init__(self, x, y, quantity):
        self.position= (x, y)
        self.type= "water"
        self.quantity= quantity

def main():
    # Show of how does the project work. 
    mundo = Environment("Ecosistema Test", 10, 10)
    herbivorous = Herbivorous(5, 5, vision=5, velocity=2, hunger= 20, thirst= 14)  # Posición central
    herbivorous2 = Herbivorous(7, 9, vision=5, velocity=2, hunger= 20, thirst= 14)

    herbivorous.turns_without_eat= 40
    herbivorous.turns_without_drink= 40
    herbivorous2.turns_without_eat= 40
    herbivorous2.turns_without_drink= 40

    plant = Plant(6, 7, 33)
    water1= Water(4, 3, 20)
    water2= Water(3, 1, 18)

    # Añadir entidades al mundo
    mundo.add_entity(herbivorous)
    mundo.add_entity(herbivorous2)
    mundo.add_entity(plant)
    mundo.add_entity(water1)
    mundo.add_entity(water2)

    # Simulación de 10 ciclos
    for ciclo in range(100):
        mundo.execute_turn()

main()