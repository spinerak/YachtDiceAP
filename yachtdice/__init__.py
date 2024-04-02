from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification
from .Items import YachtDiceItem, item_table
from .Locations import YachtDiceLocation, all_locations, ini_locations
from .Options import yachtdice_options
from .Rules import set_rules, set_completion_rules
from ..AutoWorld import World, WebWorld

client_version = 345



class YachtDiceWorld(World):
    """
    ChecksFinder is a game where you avoid mines and find checks inside the board
    with the mines! You win when you get all your items and beat the board!
    """
    game: str = "Yacht Dice"
    option_definitions = yachtdice_options
    # topology_present = True
    # web = ChecksFinderWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}


    location_name_to_id = {name: data.id for name, data in all_locations.items()}

    data_version = 4

    def _get_yachtdice_data(self):
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'race': self.multiworld.is_race,
        }


    def create_items(self):

        numDiceF = self.options.number_of_extra_dice.value
        numRollsF = self.options.number_of_extra_rolls.value

        amDiceF = self.options.number_of_dice_fragments_per_dice.value
        amRollsF = self.options.number_of_roll_fragments_per_roll.value

        # Generate item pool
        itempool = []
                
        if amDiceF == 1:
            itempool += ["Dice"] * numDiceF
        else:
            itempool += ["Dice Fragment"] * (amDiceF * numDiceF)

        if amRollsF == 1:
            itempool += ["Roll"] * numRollsF
        else:
            itempool += ["Roll Fragment"] * (amRollsF * numRollsF)

        itempool += ["Score Multiplier"] * 5
        itempool += ["Category Ones"]
        itempool += ["Category Twos"]
        itempool += ["Category Threes"]
        itempool += ["Category Fours"]
        itempool += ["Category Fives"]
        itempool += ["Category Sixes"]
        # itempool += ["Category Choice"]
        # itempool += ["Category Inverse Choice"]
        itempool += ["Category Pair"]
        itempool += ["Category Three of a Kind"]
        itempool += ["Category Four of a Kind"]
        itempool += ["Category Tiny Straight"]
        itempool += ["Category Small Straight"]
        itempool += ["Category Large Straight"]
        itempool += ["Category Full House"]
        itempool += ["Category Yacht"]

        itempool += ["Encouragement"] * 5
        itempool += ["Fun Fact"] * 5
        itempool += ["Story Chapter"] * 10

        #count the number of locations in the game
        last_pos_location = self.options.goal_score.value 
        number_of_locations = min(20, last_pos_location)
        number_of_locations += max(0,  min((200-20)//2, (last_pos_location-20)//2) )
        number_of_locations += max(0,  (last_pos_location - 200) // 10)

        itempool += ["Nothing"] * (number_of_locations - len(itempool))


        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        
        self.multiworld.push_precollected(self.create_item("Dice"))
        self.multiworld.push_precollected(self.create_item("Roll"))
        self.multiworld.push_precollected(self.create_item("Category Choice"))
        self.multiworld.push_precollected(self.create_item("Category Inverse Choice"))

        for item in itempool:
            self.multiworld.itempool += [item]
            
        for item in self.item_name_to_id.keys():
            if item == "Nothing":
                self.multiworld.local_items[self.player].value.add(item)
            

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)
        set_completion_rules(self.multiworld, self.player, self.options)

    def create_regions(self):
        location_table = ini_locations(self.options.goal_score.value, 100)

        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)


        board.locations += [YachtDiceLocation(self.player, loc_name, loc_data.id, board)
                            for loc_name, loc_data in location_table.items() if loc_data.region == board.name]

        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]

    def fill_slot_data(self):
        slot_data = self._get_yachtdice_data()
        for option_name in yachtdice_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = YachtDiceItem(name,
                                ItemClassification.progression if item_data.progression else ItemClassification.filler,
                                item_data.code, self.player)
        return item
