from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class YachtDiceLocation(Location):
    game: str = "Yacht Dice"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address

all_locations = {}
starting_index = 16871244500

def ini_locations(goal_score, num_items):
    
    count = 0
    location_table = {}
    for i in list(range(1, goal_score)):
        if i < 20 or (i < 200 and i % 2 == 0) or (i % 10 == 0):
            location_table[f"{i} score"] = AdvData(starting_index+i, 'Board')
            count += 1
    return location_table


all_locations = ini_locations(1000, 1000)


    


exclusion_table = {
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in all_locations.items() if data.id}