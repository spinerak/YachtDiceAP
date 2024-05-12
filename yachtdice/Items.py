from BaseClasses import Item, ItemClassification
import typing

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification

class YachtDiceItem(Item):
    game: str = "Yacht Dice"

#the starting index is chosen semi-randomly to be 16871244000

item_table = {
    "Victory": ItemData(16871244000-1, ItemClassification.progression),

    "Dice": ItemData(16871244000, ItemClassification.progression),
    "Dice Fragment": ItemData(16871244001, ItemClassification.progression),
    "Roll": ItemData(16871244002, ItemClassification.progression),
    "Roll Fragment": ItemData(16871244003, ItemClassification.progression),
    "Score Multiplier": ItemData(16871244004, ItemClassification.progression),

    "Category Ones": ItemData(16871244103, ItemClassification.progression),
    "Category Twos": ItemData(16871244104, ItemClassification.progression),
    "Category Threes": ItemData(16871244105, ItemClassification.progression),
    "Category Fours": ItemData(16871244106, ItemClassification.progression),
    "Category Fives": ItemData(16871244107, ItemClassification.progression),
    "Category Sixes": ItemData(16871244108, ItemClassification.progression),
    "Category Choice": ItemData(16871244109, ItemClassification.progression),
    "Category Inverse Choice": ItemData(16871244110, ItemClassification.progression),
    "Category Pair": ItemData(16871244111, ItemClassification.progression),
    "Category Three of a Kind": ItemData(16871244112, ItemClassification.progression),
    "Category Four of a Kind": ItemData(16871244113, ItemClassification.progression),
    "Category Tiny Straight": ItemData(16871244114, ItemClassification.progression),
    "Category Small Straight": ItemData(16871244115, ItemClassification.progression),
    "Category Large Straight": ItemData(16871244116, ItemClassification.progression),
    "Category Full House": ItemData(16871244117, ItemClassification.progression),
    "Category Yacht": ItemData(16871244118, ItemClassification.progression),

    "Encouragement": ItemData(16871244200, ItemClassification.filler),
    "Fun Fact": ItemData(16871244201, ItemClassification.filler),
    "Story Chapter": ItemData(16871244202, ItemClassification.filler),
    "Good RNG": ItemData(16871244203, ItemClassification.filler),
    "Bad RNG": ItemData(16871244204, ItemClassification.trap),
    "Extra Point": ItemData(16871244205, ItemClassification.useful),
    
    "1 Extra Point": ItemData(16871244301, ItemClassification.progression),
    "10 Extra Points": ItemData(16871244302, ItemClassification.progression),
    "100 Extra Points": ItemData(16871244303, ItemClassification.progression)
}