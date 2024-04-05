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

def all_locations_fun(max_score):
    location_table = {}
    for i in range(max_score):
        location_table[f"{i} score"] = AdvData(starting_index+i, 'Board')
    return location_table

def ini_locations(goal_score, num_locs):
    
    location_table = {}

    curscore = 0
    for i in range(num_locs):
        if i < 20:
            curscore += 1
        elif i < 110:
            curscore += 2
        else:
            curscore = int(200 + (i-109) / (num_locs-109) * (goal_score - 200)) 
            
        location_table[f"{curscore} score"] = AdvData(starting_index+curscore, 'Board')

    return location_table


all_locations = all_locations_fun(1000)


    


exclusion_table = {
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in all_locations.items() if data.id}