import typing
from Options import Choice, Option, Toggle, Range


class numberOfExtraDice(Range):
    """Total number of extra dice you can add to your collection."""
    display_name = "Number of extra dice"
    range_start = 4
    range_end = 6
    default = 4

class numberOfExtraRolls(Range):
    """Total number of extra rolls you can add to your collection."""
    display_name = "Number of extra rolls"
    range_start = 4
    range_end = 6
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
    range_start = 200
    range_end = 500
    default = 500

class gameDifficulty(Range):
    """How difficult you want the game. Intended difficulty is 100. Smaller number makes it easier, larger number makes it harder.
    Note: a larger number means that the game MIGHT be more difficult. But it's not a given."""
    display_name = "Game difficulty"
    range_start = 60
    range_end = 150
    default = 100


yachtdice_options: typing.Dict[str, type(Option)] = {
    "number_of_extra_dice": numberOfExtraDice,
    "number_of_extra_rolls": numberOfExtraRolls,
    "number_of_dice_fragments_per_dice": numberDiceFragmentsPerDice,
    "number_of_roll_fragments_per_roll": numberRollFragmentsPerRoll,
    "goal_score": goalScore,
    "game_difficulty": gameDifficulty
}
