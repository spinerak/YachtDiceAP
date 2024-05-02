from ..generic.Rules import set_rule
from BaseClasses import MultiWorld, CollectionState
from statistics import mean
import random
from .YachtWeights import yacht_weights
import math






class Category:
    def __init__(self, name):
        self.name = name

    def maxScore(self, nbDice, nbRolls):
        if nbDice == 0 or nbRolls == 0:
            return 0
        return max(yacht_weights[self.name, nbDice, nbRolls])

    def meanScore(self, nbDice, nbRolls):
        if nbDice == 0 or nbRolls == 0:
            return 0
        meanScore = 0
        for key in yacht_weights[self.name, nbDice, nbRolls]:
            meanScore += key*yacht_weights[self.name, nbDice, nbRolls][key]/100000
        return meanScore



def extractProgression(state, player, options):
    number_of_dice = state.count("Dice", player) + state.count("Dice Fragment", player) // options.number_of_dice_fragments_per_dice.value

    number_of_rerolls = state.count("Roll", player) + state.count("Roll Fragment", player) // options.number_of_roll_fragments_per_roll.value

    number_of_mults = state.count("Score Multiplier", player)
    
    score_mult = -10000
    if options.score_multiplier_type.value == 1: #fixed
        score_mult = 0.1 * number_of_mults
    if options.score_multiplier_type.value == 2: #step
        score_mult = 0.01 * number_of_mults
   
    categories = []

    if state.has("Category Choice", player, 1):
        categories.append(Category("Choice"))
    if state.has("Category Inverse Choice", player, 1):
        categories.append(Category("Choice"))
    if state.has("Category Sixes", player, 1):
        categories.append(Category("Sixes"))
    if state.has("Category Fives", player, 1):
        categories.append(Category("Fives"))
    if state.has("Category Tiny Straight", player, 1):
        categories.append(Category("TinyStraight"))
    if state.has("Category Threes", player, 1):
        categories.append(Category("Threes"))
    if state.has("Category Fours", player, 1):
        categories.append(Category("Fours"))
    if state.has("Category Pair", player, 1):
        categories.append(Category("Pair"))
    if state.has("Category Three of a Kind", player, 1):
        categories.append(Category("ThreeOfAKind"))
    if state.has("Category Four of a Kind", player, 1):
        categories.append(Category("FourOfAKind"))
    if state.has("Category Ones", player, 1):
        categories.append(Category("Ones"))
    if state.has("Category Twos", player, 1):
        categories.append(Category("Twos"))
    if state.has("Category Small Straight", player, 1):
        categories.append(Category("SmallStraight"))
    if state.has("Category Large Straight", player, 1):
        categories.append(Category("LargeStraight"))
    if state.has("Category Full House", player, 1):
        categories.append(Category("FullHouse"))
    if state.has("Category Yacht", player, 1):
        categories.append(Category("Yacht"))

    return [categories, number_of_dice, number_of_rerolls, score_mult]
    

cache = {}

def diceSimulationStrings(categories, nbDice, nbRolls, multiplier, diff, scoremulttype):
    

    tup = tuple([tuple(sorted([c.name for c in categories])), nbDice, nbRolls, multiplier])
    
    
    
    # tup = (('Choice', 'Choice', 
    #         'Sixes', 'Fours',
    #         'Yacht','LargeStraight', 
    #         'Fives', 'FourOfAKind', 'Ones', 'SmallStraight'), 4, 3, 0.06)

    if tup in cache.keys():
        return cache[tup]
    
    # print(tup)
    # categories = []
    # for t in tup[0]:
    #     categories.append(Category(t))
    # nbDice = tup[1]
    # nbRolls = tup[2]
    # multiplier = tup[3]
    
    categories.sort(key=lambda category: category.meanScore(nbDice, nbRolls))

    def add_distributions(dist1, dist2, mult):
        combined_dist = {}
        for val1, prob1 in dist1.items():
            for val2, prob2 in dist2.items():
                if int(val1 + val2 * mult) in combined_dist.keys():
                    combined_dist[int(val1 + val2 * mult)] += prob1 * prob2
                else:
                    combined_dist[int(val1 + val2 * mult)] = prob1 * prob2
        return combined_dist
    
    def max_dist(dist1, times):
        # Perform multiplication 'times' times
        new_dist = {0: 1}
        for _ in range(times):
            c = new_dist.copy()
            new_dist = {}
            for val1, prob1 in c.items():
                for val2, prob2 in dist1.items():
                    new_val = max(val1, val2)
                    new_prob = prob1 * prob2
                    
                    # Update the probability for the new value
                    if new_val in new_dist:
                        new_dist[new_val] += new_prob
                    else:
                        new_dist[new_val] = new_prob
            
        
        return new_dist

    
    def percentile_distribution(dist, percentile):
        sorted_values = sorted(dist.keys())
        cumulative_prob = 0
        prev_val = None
        
        for val in sorted_values:
            prev_val = val
            cumulative_prob += dist[val]
            if cumulative_prob >= percentile:
                return prev_val  # Return the value before reaching the desired percentile
        return prev_val if prev_val is not None else sorted_values[0]  # Return the first value if percentile is lower than all probabilities

            
    def mean_distribution(dist):
        total_mean = sum(val * prob for val, prob in dist.items())
        return total_mean


    total_dist = {0: 1}
    for j in range(len(categories)):
        dist = yacht_weights[categories[j].name, nbDice, nbRolls].copy()
        for key in dist.keys():
            dist[key] /= 100000
            
        dist = max_dist(dist, max(1, len(categories) // (6 - diff)))
        
        cur_mult = -100
        if scoremulttype == 1: #fixed
            cur_mult = multiplier
        if scoremulttype == 2: #step
            cur_mult = j * multiplier
        total_dist = add_distributions(total_dist, dist, 1 + cur_mult )
    
    cache[tup] = math.floor(percentile_distribution(total_dist, .40))
    
    # print(cache[tup])
    # print()
    
    return cache[tup]




def diceSimulation(state, player, options, diff):
    categories, nbDice, nbRolls, multiplier = extractProgression(state, player, options)


    return diceSimulationStrings(categories, nbDice, nbRolls, multiplier, diff, options.score_multiplier_type.value)


# Sets rules on entrances and advancements that are always applied
def set_yacht_rules(world: MultiWorld, player: int, options, diff):
        
    for l in world.get_locations(player):
        set_rule(l, 
                    lambda state, 
                    curscore=l.yacht_dice_score, 
                    player=player: 
                    diceSimulation(state, player, options, diff) >= curscore)

    

# Sets rules on completion condition
def set_yacht_completion_rules(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: state.has("Victory", player)
