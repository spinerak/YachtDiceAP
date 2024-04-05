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

    def simulateRolls(self, nbDice, nbRolls):
        if nbDice == 0 or nbRolls == 0:
            return 0
        return \
            random.choices(list(yacht_weights[self.name, nbDice, nbRolls].keys()),
                           yacht_weights[self.name, nbDice, nbRolls].values(), k=1)[0]




cache = {}
# count_cache = 0
# count_not_cache = 0
def canReachScore(state: CollectionState, player, scoretarget: int, options, seed, it_game, perc_req):
    if scoretarget <= 10:
        return True
    # global count_cache
    # global count_not_cache

    [c, r, d, m] = extractProgression(state, player, options)
    thisState = [*sorted([a.name for a in c]), r, d, m]

    

    if tuple(thisState) in cache.keys():
        # index = list(cache.keys()).index(tuple(thisState))
        # print("Index:", index, "Total length of cache:", len(cache))

        scores = cache[tuple(thisState)]
        # count_cache += 1
        # print(f"{count_cache} {count_not_cache}")
    else:
        [a1, a2, a3, a4] = extractProgression(state, player, options)
        scores = diceSimulation(seed, [a1, a2, a3, a4], it_game)
        state = [*sorted([a.name for a in a1]), a2, a3, a4]
        cache[tuple(state)] = scores
        # count_not_cache += 1
        # print(f"{count_cache} {count_not_cache}")
    
    # if scoretarget == 500:
    #     print(verifyAccessibility(scoretarget))
    return verifyAccessibility(scores, scoretarget, it_game, perc_req)

def verifyAccessibility(scores, score, it_game, perc_req):
    
    P = perc_req
    if score < 50:
        P = min(P,2)
    elif score < 100:
        P = min(P,6)

    wins = len(list(filter(lambda s:s>=score, scores)))
    if wins == 0:
        return False
        

    return wins / it_game >= P / 100

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
    
def diceSimulation(seed, ST, it_game):
    categories, nbDice, nbRolls, multiplier = ST
    
    random.seed(42)

    scores = []

    categories.sort(key=lambda category: category.meanScore(nbDice, nbRolls))
    for i in range(it_game):
        total = 0
        for j in range(len(categories)):
            roll = int(categories[j].simulateRolls(nbDice, nbRolls) * (1 + j * multiplier))
            total += roll
        scores.append(total)

    return scores

# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int, options, goal_score, seed, it_game, perc_req):

    num_locs = 140

    curscore = 0
    for i in range(140):
        if i < 20:
            curscore += 1
        elif i < 110:
            curscore += 2
        else:
            curscore = int(200 + (i-109) / (num_locs-109) * (goal_score - 200)) 



        set_rule(world.get_location(f"{curscore} score", player), 
                 lambda state, 
                 curscore=curscore, 
                 player=player: 
                 canReachScore(state, player, curscore, options, seed, it_game, perc_req))
    
    set_rule(world.get_location(f"{goal_score} score", player), 
                 lambda state,
                 player=player: 
                 canReachScore(state, player, goal_score, options, seed, it_game, perc_req))

    

# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: state.has("Victory", player)
