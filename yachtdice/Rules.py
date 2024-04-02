from ..generic.Rules import set_rule
from BaseClasses import MultiWorld, CollectionState


def canReachScore(state: CollectionState, player, scoretarget: int, options):

    number_of_dice = state.count("Dice", player) + state.count("Dice Fragment", player) // options.number_of_dice_fragments_per_dice.value

    number_of_rerolls = state.count("Roll", player) + state.count("Roll Fragment", player) // options.number_of_roll_fragments_per_roll.value

    number_of_mults = state.count("Score Multiplier", player)
    score_mult = 0.02 *  number_of_mults


    num_categories = 0

    F1 = (1 + score_mult * (num_categories-1) / 2)
    F2 = 1
    F3 = options.game_difficulty.value / 100

    if number_of_rerolls == 0:
        F2 = 0.5
    elif number_of_rerolls == 1:
        F2 = 0.6
    elif number_of_rerolls == 2:
        F2 = 0.7
    elif number_of_rerolls == 3:
        F2 = 0.8
    else:
        F2 = 0.85


    factor = F1 * min(1, F2 * F3)

    max_score = 0
    if state.has("Category Choice", player, 1):
        max_score += number_of_dice * 6
        num_categories += 1
    if state.has("Category Inverse Choice", player, 1):
        max_score += number_of_dice * 6
        num_categories += 1
    
    if max_score * factor >= scoretarget:
        return True
    
    if state.has("Category Sixes", player, 1):
        max_score += number_of_dice * 6
        num_categories += 1
    if state.has("Category Fives", player, 1):
        max_score += number_of_dice * 5
        num_categories += 1
    if state.has("Category Tiny Straight", player, 1) and ((number_of_dice >= 3 and number_of_rerolls >= 2) or (number_of_dice >= 4)):
        max_score += 20
        num_categories += 1

    if max_score * factor >= scoretarget:
        return True

    
    if state.has("Category Threes", player, 1):
        max_score += number_of_dice * 3
        num_categories += 1
    if state.has("Category Fours", player, 1):
        max_score += number_of_dice * 4
        num_categories += 1
    if state.has("Category Pair", player, 1) and ((number_of_dice >= 2 and number_of_rerolls >= 1) or (number_of_dice >= 3)):
        max_score += 10
        num_categories += 1
    if state.has("Category Three of a Kind", player, 1) and ((number_of_dice >= 3 and number_of_rerolls >= 2) or (number_of_dice >= 4 and number_of_rerolls >= 1) or (number_of_dice >= 5)):
        max_score += 20
        num_categories += 1
    if state.has("Category Four of a Kind", player, 1) and ((number_of_dice >= 4 and number_of_rerolls >= 3) or (number_of_dice >= 5)):
        max_score += 30
        num_categories += 1
    
    if max_score * factor >= scoretarget:
        return True


    if state.has("Category Ones", player, 1):
        max_score += number_of_dice * 1
        num_categories += 1
    if state.has("Category Twos", player, 1):
        max_score += number_of_dice * 2
        num_categories += 1
    if state.has("Category Small Straight", player, 1) and ((number_of_dice >= 4 and number_of_rerolls >= 3) or (number_of_dice >= 5 and number_of_rerolls >= 1) or (number_of_dice >= 6)):
        max_score += 30
        num_categories += 1
    if state.has("Category Large Straight", player, 1) and ((number_of_dice >= 5 and number_of_rerolls >= 3) or (number_of_dice >= 6 and number_of_rerolls >= 1)):
        max_score += 40
        num_categories += 1
    if state.has("Category Full House", player, 1) and ((number_of_dice >= 5 and number_of_rerolls >= 3) or (number_of_dice >= 6 and number_of_rerolls >= 1)):
        max_score += 25
        num_categories += 1
    if state.has("Category Yacht", player, 1) and ((number_of_dice >= 5 and number_of_rerolls >= 4) or (number_of_dice >= 6 and number_of_rerolls >= 2)):
        max_score += 50
        num_categories += 1
    
    
    F1 = (1 + score_mult * (num_categories - 1) / 2)
    factor = F1 * min(1, F2 * F3)
    

    return max_score * factor >= scoretarget
    


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int, options):
    for i in range(1, options.goal_score.value):
        if i < 20 or (i < 200 and i % 2 == 0) or (i % 10 == 0):
            set_rule(world.get_location(f"{i} score", player), lambda state, i=i, player=player: canReachScore(state, player, i, options))
    

# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int, options):
    world.completion_condition[player] = lambda state: canReachScore(state, player, options.goal_score.value, options)
