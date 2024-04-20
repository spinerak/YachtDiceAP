from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: int
    region: str
    score: int


class YachtDiceLocation(Location):
    game: str = "Yacht Dice"

    def __init__(self, player: int, name: str, score: int, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.yacht_dice_score = score
        self.event = not address

all_locations = {}
starting_index = 16871244500

def all_locations_fun(max_score):
    location_table = {}
    for i in range(max_score):
        location_table[f"{i} score"] = AdvData(starting_index+i, 'Board', i)
    return location_table

def ini_locations(max_score, num_locs, dif):
    print(f"GENERATING LOCATIONS {num_locs}")
    
    location_table = {}
    
    scaling = 1.7 #parameter that determines how many low-score location there are.
    if dif == 1:
        scaling = 3 #need more low-score locations or lower difficulties
    elif dif == 2:
        scaling = 2

    hiscore = 0
    for i in range(num_locs):
        perc = (i/num_locs)
        curscore = int( 1 + (perc ** scaling) * (max_score-1) )
        if(curscore <= hiscore):
            curscore = hiscore + 1
        hiscore = curscore
        location_table[f"{curscore} score"] = AdvData(starting_index + curscore, 'Board', curscore)
        
    location_table[f'{max_score} score'] = AdvData(starting_index + max_score, 'Board', max_score)
    return location_table


all_locations = all_locations_fun(1000) #we need to do this function to initialize all scores from 1 to 1000, even though not all are used


    


exclusion_table = {
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in all_locations.items() if data.id}