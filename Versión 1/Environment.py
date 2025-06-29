import random
import time
from animal_base import Animal
from herbivorous_class import Herbivorous


class Environment():
    def __init__(self, name, columns, rows, season= "spring"):
        self.name= name
        self.rows= rows
        self.cols= columns
        self.current_turn= 0
        self.current_day= 0
        self.current_month= 0
        self.current_year= 0
        self.is_night= False
        self.active_rain= False
        self.season= season
        self.world_dic= {}
        self.entities= []
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
    
    def classify_objects_by_tipe(self, objects, type): 
        # Returns a list with all the objects of the type specifyed from the list. objects= list of elements.
        valid_types = {"water", "plant", "herbivorous", "carnivorous"}
        if type not in valid_types:
            return []
        
        return [objetivo for objetivo in objects if objetivo.type == type]

    def remove_entity(self, entity): 
        # Removes an entity from the dic world_dic, and from the list entities. It doesn't return anything.
        x, y= entity.position
        self.world_dic[x, y]= None
        if isinstance(entity, Animal):
            entity.alive= False
        self.entities.remove(entity)


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
    
    def are_adjacent_objects(self, obj1, obj2):
        # Returns True if both objects are side by side
        x1, y1 = obj1.position
        x2, y2 = obj2.position
        return abs(x1 - x2) + abs(y1 - y2) == 1



    def opposite_directions_to_position(self, entity, position):
        # Returns a list with tuples, with positions that add distance between the entity and another entity.
        x_ent, y_ent = entity.position
        x_obj, y_obj = position
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
        # Updates the current turn, and also in wich month and year we are. Will also manage the seasons, and if it's night. It doesn't return anything.
        self.current_turn += 1
        
        if self.current_turn % 24 == 0:
            self.current_day += 1
            
            if self.current_day % 30 == 0:
                self.current_month += 1

                if self.current_month % 12 == 0:
                    self.current_year += 1

        if self.current_turn % 24 >= 22 or self.current_turn % 24 < 6:
            self.is_night= True
        else:
            self.is_night= False

    def is_object(var):
        # Checks if the variable is an object, not a primitive type. It returns True if it is an object, and False if it isn't.
        return isinstance(var, object) and not isinstance(var, (int, float, str, bool, list, dict, tuple, set))

    def execute_turn(self): 
        # Is the "main" function of the code. Update the stats, removes entities, execute movements and interactions... It doesn't return anything.

        self.update_turn()

        for animal in self.entities:
            if isinstance(animal, Animal):
                if isinstance(animal, Herbivorous):
                    nearby_entities = animal.take_a_look_around()
                    animal.chose_movement(nearby_entities)
                animal.update_animal_stats()

        self.print_grid()
        time.sleep(0.5)

    
    def print_grid(self):
        #While the UI isn't developed, all the changes will be shown in the terminal with this function.
        print(f"\nCurrent state of {self.name}, turn {self.current_turn} ({self.cols}x{self.rows}):")
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

