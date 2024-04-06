from ..generic.Rules import set_rule
from BaseClasses import MultiWorld, CollectionState
from statistics import mean
import random
from .YachtWeights import yacht_weights






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
    score_mult = 0.02 *  number_of_mults

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

def diceSimulationStrings(categories, nbDice, nbRolls, multiplier, perc):

    tup = tuple([tuple(sorted([c.name for c in categories])), nbDice, nbRolls, multiplier, perc])

    if tup in cache.keys():
        return cache[tup]
    
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
        total_dist = add_distributions(total_dist, dist, 1 + j * multiplier )

    #it's fine to put higher difficulty on earlier scores, you sometimes need this to get to certain scores.
    perc = max(perc, 100 - mean_distribution(total_dist)//2) 

    cache[tup] = percentile_distribution(total_dist, perc/100)
    return cache[tup]

def diceSimulation(state, player, options, perc):
    categories, nbDice, nbRolls, multiplier = extractProgression(state, player, options)

    return diceSimulationStrings(categories, nbDice, nbRolls, multiplier, perc)


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int, options, goal_score, perc_req):

    num_locs = 140

    curscore = 0
    for i in range(140):
        if i < 30:
            curscore += 1
        elif i < 115:
            curscore += 2
        else:
            curscore = int(200 + (i-114) / (num_locs-114) * (goal_score - 200)) 



        set_rule(world.get_location(f"{curscore} score", player), 
                 lambda state, 
                 curscore=curscore, 
                 player=player: 
                 diceSimulation(state, player, options, perc_req) >= curscore)
    
    set_rule(world.get_location(f"{goal_score} score", player), 
                 lambda state,
                 player=player: 
                 diceSimulation(state, player, options, perc_req) >= curscore)

    

# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: state.has("Victory", player)
