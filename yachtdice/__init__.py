from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification
from .Items import YachtDiceItem, item_table
from .Locations import YachtDiceLocation, all_locations, ini_locations, AdvData
from .Options import yachtdice_options
from .Rules import set_yacht_rules, set_yacht_completion_rules, diceSimulationStrings, Category
from ..AutoWorld import World, WebWorld
from Fill import FillError
import math


client_version = 345


class YachtDiceWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Yacht Dice. This guide covers "
        "single-player, multiworld, and website.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Spineraks"]
    )]


class YachtDiceWorld(World):
    """
    Yacht Dice is a game where you roll dice to reach high scores, which unlocks items.
    You can find more dice, more rolls, higher multipliers and unlock categories.
    You 'beat' the game if you reach the target score.
    """
    game: str = "Yacht Dice"
    option_definitions = yachtdice_options
    options_dataclass = yachtdice_options
    
    web = YachtDiceWeb()

    number_of_locations = -146
    
    

    item_name_to_id = {name: data.code for name, data in item_table.items()}


    location_name_to_id = {name: data.id for name, data in all_locations.items()}

    ap_world_version = "0.4"

    

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
        # print(f"For Yacht Dice debug purposes: here's the options {self.options} for player {self.player}\n\n")


        numDiceF = self.options.number_of_dice_and_rolls.value
        numRollsF = 10 - numDiceF # self.options.number_of_extra_rolls.value

        amDiceF = self.options.number_of_dice_fragments_per_dice.value
        amRollsF = self.options.number_of_roll_fragments_per_roll.value
        
        exDiceF = max(0, min(amDiceF - 1, self.options.number_of_extra_dice_fragments.value) )
        exRollsF = max(0, min(amRollsF - 1, self.options.number_of_extra_roll_fragments.value) )
        
        
        extra_plando_items = 0
        
        for plando_setting in self.multiworld.plando_items[self.player]:
            if plando_setting.get("from_pool", False) is False:
                extra_plando_items += sum(value for value in plando_setting['items'].values())


        # Generate item pool
        itempool = []
                
        if amDiceF == 1:
            itempool += ["Dice"] * (numDiceF-1) #minus one because one is in start inventory
        else:
            itempool += ["Dice"] #always add a full dice to make generation easier
            itempool += ["Dice Fragment"] * (amDiceF * (numDiceF-2) + exDiceF)

        if amRollsF == 1:
            itempool += ["Roll"] * (numRollsF-1) #minus one because one is in start inventory
        else:
            itempool += ["Roll"] #always add a full roll to make generation easier
            itempool += ["Roll Fragment"] * (amRollsF * (numRollsF-2) + exRollsF)
            

        itempool += ["Score Multiplier"] * 10
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
        
        #count the number of locations in the game
        already_items = len(itempool) + extra_plando_items
        
        import sys
        if already_items > self.number_of_locations:
            sys.exit(f"In Yacht Dice, there are more items than locations. Items: {already_items}, locations: {self.number_of_locations}")
        
        
        
        already_items = len(itempool) + extra_plando_items
        if self.options.add_extra_points.value == 1:
            itempool += ["Extra Point"] * min(self.number_of_locations - already_items, 100)
            
        already_items = len(itempool) + extra_plando_items
        if self.options.add_story_chapters.value == 1:
            itempool += ["Story Chapter"] * min(self.number_of_locations - already_items, 100)
            
            
        already_items = len(itempool) + extra_plando_items
        if self.options.add_extra_points.value == 2:
            itempool += ["Extra Point"] * min(self.number_of_locations - already_items, 10)
            
        already_items = len(itempool) + extra_plando_items
        if self.options.add_story_chapters.value == 2:
            if(self.number_of_locations - already_items >= 10):
                itempool += ["Story Chapter"] * 10
                
        already_items = len(itempool) + extra_plando_items
        if self.options.add_extra_points.value == 2:
            itempool += ["Extra Point"] * min(self.number_of_locations - already_items, 10)
         
  

        already_items = len(itempool) + extra_plando_items
        itempool += ["Encouragement"] * min(self.number_of_locations - already_items, 5)

        already_items = len(itempool) + extra_plando_items
        itempool += ["Fun Fact"] * min(self.number_of_locations - already_items, 5)
        

        import random


        p = 0.5
        if self.options.game_difficulty.value == 1:
            p = 0.9
        elif self.options.game_difficulty.value == 2:
            p = 0.7
        elif self.options.game_difficulty.value == 3:
            p = 0.5
        elif self.options.game_difficulty.value == 4:
            p = 0.1
            
        already_items = len(itempool) + extra_plando_items
        itempool += ["Good RNG" if random.random() > p else "Bad RNG" for _ in range(self.number_of_locations - already_items)]

        
        already_items = len(itempool) + extra_plando_items
        if len(itempool) != self.number_of_locations:
            sys.exit("Number in itempool is not number of locations.")

        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        
        self.multiworld.push_precollected(self.create_item("Dice"))
        self.multiworld.push_precollected(self.create_item("Roll"))
        self.multiworld.push_precollected(self.create_item("Category Choice"))
        self.multiworld.push_precollected(self.create_item("Category Inverse Choice"))

        for item in itempool:
            self.multiworld.itempool += [item]
            
        # for item in self.item_name_to_id.keys():
        #     if item == "Nothing":
        #         self.multiworld.local_items[self.player].value.add(item)
            

    def set_rules(self):
        seed = 42
        if (self.multiworld.seed_name).isdigit():  # Check if seed_name contains only digits
            seed = int(self.multiworld.seed_name) % 1000
        set_yacht_rules(self.multiworld, self.player, self.options, self.options.game_difficulty.value)
        set_yacht_completion_rules(self.multiworld, self.player)

    goal_score = -1
    
    def generate_early(self):
        numDiceF = self.options.number_of_dice_and_rolls.value
        numRollsF = 10 - numDiceF # self.options.number_of_extra_rolls.value

        amDiceF = self.options.number_of_dice_fragments_per_dice.value
        amRollsF = self.options.number_of_roll_fragments_per_roll.value
        
        exDiceF = max(0, min(amDiceF - 1, self.options.number_of_extra_dice_fragments.value) )
        exRollsF = max(0, min(amRollsF - 1, self.options.number_of_extra_roll_fragments.value) )
        
        self.number_of_locations = 1 + (numDiceF - 2) * amDiceF + exDiceF \
                                    + 1 + (numRollsF - 2) * amRollsF + exRollsF \
                                    + 10 \
                                    + 16 
        self.number_of_locations = min(100, math.floor(self.number_of_locations * 1.7))

    def create_regions(self):
        
   

        game_difficulty = self.options.game_difficulty.value


        # if(self.options.number_of_extra_rolls.value != 4):
        #     import sys
        #     sys.exit("Logic only implemented for 4 extra rolls.")

        max_score = 500
        
        if game_difficulty == 1:
            max_score = 400
        elif game_difficulty == 2:
            max_score = 500
        elif game_difficulty == 3:
            max_score = 630
        elif game_difficulty == 4:
            max_score = 683

        
        location_table = ini_locations(max_score, self.number_of_locations, game_difficulty)




        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)


        board.locations = [YachtDiceLocation(self.player, loc_name, loc_data.score, loc_data.id, board)
                            for loc_name, loc_data in location_table.items() if loc_data.region == board.name]

        goal_percentage_location = self.options.goal_location_percentage.value
        
        victory_id = int(goal_percentage_location / 100 * len(board.locations))-1
        
        #Add the victory item to the correct location. The website declares that the game is complete when the victory item is obtained.
        board.locations[victory_id].place_locked_item(self.create_item("Victory"))
        
        
        
        


        self.goal_score = board.locations[victory_id].yacht_dice_score
        self.max_score = board.locations[-1].yacht_dice_score
        

        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]
        
        #print(self.options)


    def pre_fill(self):
        self.multiworld.early_items[self.player]["Dice"] = 1
        self.multiworld.early_items[self.player]["Roll"] = 1
        
        
        
 
            

    def fill_slot_data(self):

        slot_data = self._get_yachtdice_data()
        for option_name in yachtdice_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        slot_data["goal_score"] = self.goal_score
        slot_data["last_check_score"] = self.max_score
        slot_data["ap_world_version"] = self.ap_world_version
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        
        item = YachtDiceItem(name, item_data.classification, item_data.code, self.player)
        return item
