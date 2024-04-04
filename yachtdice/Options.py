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
    range_start = 4
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

class goalScore(Range):
    """The score you need to get to beat the game!"""
    display_name = "Goal score"
    range_start = 300
    range_end = 500
    default = 500

class gameDifficulty(Range):
    """If you set the value of this setting to 5, it means that in order for a score to be in logic, a score must be reachable
    at least 1 out of 5 games on average.
    Note: a larger number means that the game MIGHT be more difficult. But it's not a given."""
    display_name = "Game difficulty"
    range_start = 2
    range_end = 200
    default = 5

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
    "goal_score": goalScore,
    "game_difficulty": gameDifficulty,
    "which_story": whichStory
}
