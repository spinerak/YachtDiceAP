import typing
from Options import Choice, Option, Toggle, Range


class numberOfExtraDice(Range):
    """Total number of extra dice you can add to your collection."""
    display_name = "Number of extra dice"
    range_start = 4
    range_end = 7
    default = 4

class numberOfExtraRolls(Range):
    """Total number of extra rolls you can add to your collection."""
    display_name = "Number of extra rolls"
    range_start = 1
    range_end = 7
    default = 4

class numberDiceFragmentsPerDice(Range):
    """Number of dice fragments you need for a new dice. Setting it to one will simply add 'Dice' items into the pool."""
    display_name = "Number of dice fragments per dice"
    range_start = 1
    range_end = 6
    default = 4

class numberRollFragmentsPerRoll(Range):
    """Number of roll fragments you need for a new roll. Setting it to one will simply add 'Roll' items into the pool."""
    display_name = "Number of roll fragments per roll"
    range_start = 1
    range_end = 6
    default = 4


class gameDifficulty(Choice):
    """
    Difficulty. This setting determines what scores you should be able to achieve given your current items.
    Easy: for beginners. No luck required, just roll the dice and have fun.
    Medium: intended difficulty. If you play smart, you'll finish the game without any trouble.
    Hard: you will need to play smart and have a bit of luck as well. Make sure you understand the score multiplier mechanic!
    Extreme: you will need to play smart, and possibly need a lot of luck.
    """
    display_name = "Game difficulty"
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_extreme = 4
    
    default = 2
    
# class startingLoadOut(Choice):
#     """
#     With which item you start the game.
#     Options are:
#     -Default: start with one Dice, one Roll, and Categories Choice and Inverse Choice.
#     -TWO: start with two Dice, two Rolls, and the Category Twos.
#     """
#     display_name = "Starting items"

#     option_default = 0
#     option_two = 1

#     default = 0

class whichStory(Range):
    """The most important part of Yacht Dice is the narrative. 
    Which story would you like to read?
    1: The Quest of the Dice Warrior
    2: The Tragedy of Fortuna's Gambit"""
    display_name = "Which story"
    range_start = 1
    range_end = 2
    default = 2


yachtdice_options: typing.Dict[str, type(Option)] = {
    "number_of_extra_dice": numberOfExtraDice,
    "number_of_extra_rolls": numberOfExtraRolls,
    "number_of_dice_fragments_per_dice": numberDiceFragmentsPerDice,
    "number_of_roll_fragments_per_roll": numberRollFragmentsPerRoll,
    "game_difficulty": gameDifficulty,
    # "starting_loadout": startingLoadOut,
    "which_story": whichStory
}
