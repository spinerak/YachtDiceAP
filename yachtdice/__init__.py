from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification
from .Items import YachtDiceItem, item_table
from .Locations import YachtDiceLocation, all_locations, ini_locations, AdvData
from .Options import yachtdice_options
from .Rules import set_rules, set_completion_rules, diceSimulationStrings, Category
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

    
    PERCENTAGE_REQUIRED = 100000
    NUMBER_OF_ITERATIONS = 100
    

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

        # print(f"For Yacht Dice debug purposes: here's the options {self.options} for player {self.player}\n\n")


        numDiceF = self.options.number_of_extra_dice.value
        numRollsF = self.options.number_of_extra_rolls.value

        amDiceF = self.options.number_of_dice_fragments_per_dice.value
        amRollsF = self.options.number_of_roll_fragments_per_roll.value
        
        extra_plando_items = 0
        
        for plando_setting in self.multiworld.plando_items[self.player]:
            if plando_setting.get("from_pool", False) is False:
                extra_plando_items += sum(value for value in plando_setting['items'].values())


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
        
        #count the number of locations in the game
        number_of_locations = 140
        already_items = len(itempool) + extra_plando_items
        
        import sys
        if already_items > number_of_locations:
            sys.exit("In Yacht Dice, there are more items than locations.")

        itempool += ["Story Chapter"] * min(number_of_locations - already_items, 10)
        already_items = len(itempool) + extra_plando_items

        itempool += ["Encouragement"] * min(number_of_locations - already_items, 5)
        already_items = len(itempool) + extra_plando_items

        itempool += ["Fun Fact"] * min(number_of_locations - already_items, 5)
        already_items = len(itempool) + extra_plando_items

        import random

        itempool += ["Good RNG" if random.random() < 0.5 else "Bad RNG" for _ in range(number_of_locations - already_items)]



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
        set_rules(self.multiworld, self.player, self.options, self.goal_score, self.PERCENTAGE_REQUIRED)
        set_completion_rules(self.multiworld, self.player)

    goal_score = -1

    def create_regions(self):

        seed = 42
        if (self.multiworld.seed_name).isdigit():  # Check if seed_name contains only digits
            seed = int(self.multiworld.seed_name) % 1000

        categories = []

        categories.append(Category("Choice"))
        categories.append(Category("Choice")) #<- this is inverse choice :)
        categories.append(Category("Sixes"))
        categories.append(Category("Fives"))
        categories.append(Category("TinyStraight"))
        categories.append(Category("Threes"))
        categories.append(Category("Fours"))
        categories.append(Category("Pair"))
        categories.append(Category("ThreeOfAKind"))
        categories.append(Category("FourOfAKind"))
        categories.append(Category("Ones"))
        categories.append(Category("Twos"))
        categories.append(Category("SmallStraight"))
        categories.append(Category("LargeStraight"))
        categories.append(Category("FullHouse"))
        categories.append(Category("Yacht"))




        
        


        game_difficulty = self.options.game_difficulty.value

        dif = 50
        if game_difficulty == 1:
            dif = 54
        elif game_difficulty == 2:
            dif = 73
        elif game_difficulty == 3:
            dif = 95
        elif game_difficulty == 4:
            dif = 99

        self.PERCENTAGE_REQUIRED = dif

        self.goal_score = diceSimulationStrings(categories, 
                                                  1 + self.options.number_of_extra_dice.value, 
                                                  1 + self.options.number_of_extra_rolls.value, 
                                                  0.1, 
                                                  dif)
        



        print(f"Yacht dice debug: goal score for player {self.player} is {self.goal_score} and difficulty {dif}\noptions {self.options}")

        location_table = ini_locations(self.goal_score, 140)

        location_table[f'{self.goal_score} score'] = AdvData(id=16871244500+self.goal_score, region='Board')



        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)


        board.locations = [YachtDiceLocation(self.player, loc_name, loc_data.id, board)
                            for loc_name, loc_data in location_table.items() if loc_data.region == board.name]

        
        
        board.locations[-1].place_locked_item(self.create_item("Victory"))


        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]

        self.ITERATIONS_PER_GAME = 100 - dif




    def fill_slot_data(self):

        slot_data = self._get_yachtdice_data()
        for option_name in yachtdice_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        slot_data["goal_score"] = self.goal_score
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]

        if name == "Bad RNG":
            item = YachtDiceItem(name,
                        ItemClassification.trap,
                        item_data.code, self.player)
            ItemClassification.trap
        else:
            item = YachtDiceItem(name,
                                    ItemClassification.progression if item_data.progression else ItemClassification.filler,
                                    item_data.code, self.player)
        return item
