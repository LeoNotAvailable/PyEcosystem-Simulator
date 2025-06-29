def calc_weights(weights):
    # An AI-created function that, teorically, returns a result between 0 and 1 considering every condition. If any condition is 0, the action is discarted.
    values = list(weights.values())
    if 0 in values:
        return 0
    product = 1.0
    for w in values:
        product *= w
    return product ** (1.0 / len(values))  # Geometric average, I don't know if it's the best options, but the results seem to be good enough

def weight_reproduce(entity):
    # The next functions will consider every condition for an action, and return a value between 0-1.
    mate = entity.find_potential_mate()
    if not mate:
        return 0

    base_desire = 1  # All those weights have been selected without any deep research, so may be not the most functional. Any suggestion to improve this is apreciated
    hunger_penalty = (entity.turns_without_eat / entity.stats["hunger"]) * 0.2
    thirst_penalty = (entity.turns_without_drink / entity.stats["thirst"]) * 0.2
    energy_bonus = (entity.energy / 100) ** 0.5
    age_factor = min(1, 0.9 * (20 / (entity.age if entity.age > 0 else float('inf'))) ** 1.3)

    final_weight = base_desire * (1 - hunger_penalty) * (1 - thirst_penalty) * energy_bonus * age_factor
    if entity.current_action == "reproduce":
        priority_bonus = 1.5  # Will be better implemented. Every function weight will be modified depending on if it's the same action as the previous one.
        final_weight *= priority_bonus
    return max(0, min(1, final_weight))

def weight_explore(entity, disposables):
    # Altough the reproduction functoin was different, this modular structure will be the common one, as only a line is needed in order to add a condition.
    # In the previous attempt,the final weight was calculated by multiplying all the conditions, what resulted in a small result that, as more conditions were added, smaller the result was.
    # I don't know how the actual method works, but theorically, it doesn't depends on the number of conditoins.
    world= entity.world

    if len(disposables) <= 0:
        weights= {
            "night_weight": 0 if world.is_night else 1,
            "urge_weight": (min(1, entity.turns_without_eat / entity.stats["hunger"]) + min(1, entity.turns_without_drink / entity.stats["thirst"])) / 2,
            "energy_weight": min(1, entity.energy / 100),
            "curiosity_weight": min(1, entity.stats["curiosity"] / 100),
            "persistence_weight": (1.0 if entity.current_action != "explore" else max(0.2, 1.0 - entity.current_action_duration * 0.2)),
            "tuning": 0.2
        }

        return calc_weights(weights)
    
    else:
        return 0

def weight_food(entity, disposables):
    world= entity.world

    if len(disposables) <= 0:
        return 0
    weights= {
        "night_weight": 0 if world.is_night else 1,
        "urge_weight": min(1, entity.turns_without_eat / entity.stats["hunger"]),
        "near_weight": min(1, entity.stats["vision"] / (world.calculate_distance(entity, entity.find_nearest_objective(disposables)) + 1)),
        "energy_weight": min(1, entity.energy / 100),
        "persistence_weight": (0.8 if entity.current_action != "eat" else max(0.2, 1.0 - entity.current_action_duration * 0.05))
    }

    return calc_weights(weights)

def weight_water(entity, disposables):
    world= entity.world

    if len(disposables) <= 0:
        return 0
    weights= {
        "night_weight": 0 if world.is_night else 1,
        "urge_weight": min(1, entity.turns_without_eat / entity.stats["thirst"]),
        "near_weight": min(1, entity.stats["vision"] / (world.calculate_distance(entity, entity.find_nearest_objective(disposables)) + 1)),
        "energy_weight": min(1, entity.energy / 100),
        "persistence_weight": (0.8 if entity.current_action != "drink" else max(0.2, 1.0 - entity.current_action_duration * 0.05))
    }

    return calc_weights(weights)

def weight_rest(entity):
    world= entity.world

    norm_energy = max(0, min(1, (100 - entity.energy) / 100))
    weights = {
        "energy_weight": norm_energy ** 3 + 0.08 * norm_energy,
        "night_weight": 1.15 if world.is_night else 1.0,
        "persistence_weight": (0.8 if entity.current_action != "rest" else max(0.2, 1.0 - entity.current_action_duration * 0.1))
    }

    return calc_weights(weights)