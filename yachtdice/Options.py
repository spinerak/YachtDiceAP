import typing
from Options import Choice, Option, Toggle, Range


class numberOfDiceAndRolls(Choice):
    """
    Total number of dice and rolls in the pool.
    You start with one dice and one roll.
    This option does not change the final goal.
    """
    display_name = "Number of dice and rolls in pool"
    option_5_dice_and_5_rolls = 5
    option_6_dice_and_4_rolls = 6
    option_7_dice_and_3_rolls = 7
    option_8_dice_and_2_rolls = 8
    default = 5

# class numberOfExtraRolls(Range):
#     """Total number of extra rolls you can add to your collection.
#     Wait this is always 4? Yes, I removed other options, but they might return."""
#     display_name = "Number of extra rolls"
#     range_start = 4
#     range_end = 4
#     default = 4

class numberDiceFragmentsPerDice(Range):
    """
    Dice can be split into fragments, gathering enough will give you an extra dice. 
    You start with one dice, and there will always be one full dice in the pool. 
    The other dice are split into fragments, according to this setting. 
    Setting this to 1 fragment per dice, just puts 'Dice' objects in the pool.
    """
    display_name = "Number of dice fragments per dice"
    range_start = 1
    range_end = 5
    default = 4
    
    

class numberRollFragmentsPerRoll(Range):
    """
    Rolls can be split into fragments, gathering enough will give you an extra roll. 
    You start with one roll, and there will always be one full roll in the pool. 
    The other three rolls are split into fragments, according to this setting.
    Setting this to 1 fragment per roll, just puts 'Roll' objects in the pool.
    """
    display_name = "Number of roll fragments per roll"
    range_start = 1
    range_end = 5
    default = 4
    

class numberExtraDiceFragments(Range):
    """
    Number of extra dice fragments in the pool. 
    The number cannot exceed the number of dice fragments per dice,
    if it does, the generation will lower this setting automatically.
    The option will never give an extra full dice, but makes it easier to collect all dice.
    """
    display_name = "Number of extra dice fragments in the pool"
    range_start = 1
    range_end = 4
    default = 3
    
    

class numberExtraRollFragments(Range):
    """
    Number of extra roll fragments in the pool. 
    The number cannot exceed the number of roll fragments per roll
    if it does, the generation will lower this setting automatically.
    The option will never give an extra full roll, but makes it easier to collect all roll.
    """
    display_name = "Number of extra roll fragments in the pool"
    range_start = 1
    range_end = 4
    default = 3


class gameDifficulty(Choice):
    """
    Difficulty. This setting determines how difficult the scores are to achieve. 
    Easy: for beginners. No luck required, just roll the dice and have fun. Lower final goal.
    Medium: intended difficulty. If you play smart, you'll finish the game without any trouble.
    Hard: you may need to play smart, be lucky and understand the score multiplier mechanic. Higher final goal.
    Extreme: more strict logic, higher final goal. NOT RECOMMENDED FOR MULTIWORLDS.
    """
    display_name = "Game difficulty"
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_extreme = 4
    
    default = 2
    
    
class goalLocationPercentage(Range):
    """
    What percentage of checks you need to get, to 'finish' the game.
    Low percentage means you can probably 'finish' the game with some of the dice/rolls/categories.
    High percentage means you probably need most of the usefull items, and on higher difficulties you might need them all.
    """
    display_name = "Goal percentage location"
    range_start = 70
    range_end = 100
    default = 90
      
    
    
class scoreMultiplierType(Choice):
    """
    There are 10 Score Multiplier items available.
    This options decides how the Score Multipliers work.
    Both options are of similar difficulty.
    
    fixed_multiplier: every multiplier item gives you +10%. 
    Every score gets multiplied with the multiplier.
    So with all score multipliers, all scores get +100%.
    
    step_multiplier: every multiplier item gives you +1%. 
    Your multiplier increases with this percentage after every turn. 
    So in the first turn you have no multiplier, but in turn 16, you can have a +150% multiplier. 
    So, save your high-scoring categories for last. This option allow for more strategic games. 
    """
    display_name = "Score multiplier type"
    option_fixed_multiplier = 1
    option_step_multiplier = 2
    default = 1 
    
    
    
    
class addExtraPoints(Choice):
    """
    Yacht Dice typically has space for more items.
    Would you like extra points shuffled in the item pool?
    They make the game a little bit easier.
    """
    display_name = "Extra points in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 2
    
class addStoryChapters(Choice):
    """
    Yacht Dice typically has space for more items.
    Would you like story chapters shuffled in the item pool?
    Note: if you have extra points on "all_of_it" there won't be story chapters.
    """
    display_name = "Extra story chapters in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 2
    
    

class whichStory(Choice):
    """
    The most important part of Yacht Dice is the narrative. 
    10 story chapters are shuffled into the item pool. 
    You can read them in the feed on the website.
    Which story would you like to read?
    """
    display_name = "Story"
    option_the_quest_of_the_dice_warrior = 1
    option_the_tragedy_of_fortunas_gambit = 2
    option_the_dicey_animal_dice_game = 3
    option_whispers_of_fate = 4
    option_a_yacht_dice_odyssey = 5
    option_a_rollin_rhyme_adventure = 6
    option_random = -1
    default = -1
    



yachtdice_options: typing.Dict[str, type(Option)] = {
    "number_of_dice_and_rolls": numberOfDiceAndRolls,
    # "number_of_extra_rolls": numberOfExtraRolls,
    "number_of_dice_fragments_per_dice": numberDiceFragmentsPerDice,
    "number_of_extra_dice_fragments": numberExtraDiceFragments,
    "number_of_roll_fragments_per_roll": numberRollFragmentsPerRoll,
    "number_of_extra_roll_fragments": numberExtraRollFragments,
    "game_difficulty": gameDifficulty,
    "goal_location_percentage": goalLocationPercentage,
    "score_multiplier_type": scoreMultiplierType,
    "add_extra_points": addExtraPoints,
    "add_story_chapters": addStoryChapters,
    "which_story": whichStory
}
