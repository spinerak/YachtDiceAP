from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class YachtDiceItem(Item):
    game: str = "Yacht Dice"



starting_index = 16871244000

item_table = {
    "Victory": ItemData(16871244000-1, True),

    "Dice": ItemData(16871244000, True),
    "Dice Fragment": ItemData(16871244001, True),
    "Roll": ItemData(16871244002, True),
    "Roll Fragment": ItemData(16871244003, True),
    "Score Multiplier": ItemData(16871244004, True),

    "Category Ones": ItemData(16871244103, True),
    "Category Twos": ItemData(16871244104, True),
    "Category Threes": ItemData(16871244105, True),
    "Category Fours": ItemData(16871244106, True),
    "Category Fives": ItemData(16871244107, True),
    "Category Sixes": ItemData(16871244108, True),
    "Category Choice": ItemData(16871244109, True),
    "Category Inverse Choice": ItemData(16871244110, True),
    "Category Pair": ItemData(16871244111, True),
    "Category Three of a Kind": ItemData(16871244112, True),
    "Category Four of a Kind": ItemData(16871244113, True),
    "Category Tiny Straight": ItemData(16871244114, True),
    "Category Small Straight": ItemData(16871244115, True),
    "Category Large Straight": ItemData(16871244116, True),
    "Category Full House": ItemData(16871244117, True),
    "Category Yacht": ItemData(16871244118, True),


    "Encouragement": ItemData(16871244200, False),
    "Fun Fact": ItemData(16871244201, False),
    "Story Chapter": ItemData(16871244202, False),
    "Good RNG": ItemData(16871244203, False),
    "Bad RNG": ItemData(16871244204, False)


}


#lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
