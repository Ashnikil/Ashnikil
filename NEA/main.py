#a mining game where u can mine ores and sell them to make money to buy upgrades ,
# there will be an online database where u can create a username and password (with input
# sanitisation and a minimum/maximum length for the username and password) also it will be randomly
# generated and i might add more stuff later on for example achievements
# -> users will be able to sign up and log in
# -> users can save their data to ensure its not lost
# -> users will be able to move with arrow keys
# -> users can dig down and will find ores that are randomly placed
# -> there will be an achievements page which tracks if the user has done/is doing a certain achievement and the user will be able to see what progress they have made in the achievements
# -> there will be a shop where they can buy things and will tell them if they have enough money or not , and when they buy something their money will go down accordingly
# -> there will be a wide variety of ores worth different amounts of money
# -> there will be walls that can not be broken down (eg: on the sides of the map)
# -> there will be different layers of rock (down) that can only be broken with the correct pickaxe which can be bought in the shop
# -> there will be a functioning options page with achievements and settings where the user can change certain things , eg: volume / controls

#
# my game will be a 2d mining game where u can move left and right (until the end of the screen , where there will be a wall of sorts) and down , and u have to dig down to find ores which u can sell (maybe later ill adding a crafting mechanism) for money to buy better equipment.
#
# in my game i want to add a sign up and login page where they will be able to choose a username and password which will be saved online/locally so they can continue where they left off and will save certain parts of data
#
# also i want to create a bot in my game which can be acquired later on which , using ai , can collect certain ores for the user
#the ai will look at what ores the players collect and decide what the players needs more and collects those automatically

#zombie dust font for title

#importing necessary libraries
import copy

import pygame , random

#creating a class for images
#I am inheriting pygame.sprite.Sprite into this class so i can use this class with sprites
class Images(pygame.sprite.Sprite):

    #code used when initialising the images class which takes in a few variables which are the image , x position on screen , y position on screen , the size of the image in the x direction and the size of the image in the y direction
    def __init__(self, image, x, y, sizex, sizey):

        #this is needed so I can inherit pygame.sprite.Sprite into my class
        super().__init__()

        #this is the image variable for the class
        self.image = pygame.transform.scale(image, (sizex, sizey))

        #this is the x and y position of the center of the image on screen
        self.rect = self.image.get_rect(center=(x, y))

        #this creates a mask of the image which removes the transparent pixels in my image
        self.mask = pygame.mask.from_surface(self.image)

#creating a class for my building images
#I am inheriting pygame.sprite.Sprite into this class so i can use this class with sprites
class Buildings(pygame.sprite.Sprite):

    #code run when initialising this class
    def __init__(self,image,x,y):

        # I am inheriting pygame.sprite.Sprite into this class so i can use this class with sprites
        super().__init__()

        #this is the image variable for the class
        self.image=image

        #this is the x and y position of the center of the image on screen
        self.rect = self.image.get_rect(topleft=(x,y))


#creating a class for my tile images
#I am inheriting pygame.sprite.Sprite into this class so i can use this class with sprites
class Tiles(pygame.sprite.Sprite):

    #code run when initialising this class
    def __init__(self,image, x , y):

        # I am inheriting pygame.sprite.Sprite into this class so i can use this class with sprites
        super().__init__()

        #this is the image variable for the class
        self.image=image

        #this is the x and y position of the center of the image on screen
        self.rect=self.image.get_rect(topleft=(x,y))




#creating a class for my entire game
class Game:

    #the code that will run when initialising the game
    def __init__(self):

        #this will load the screen inside of pygame and I have decided to use pygame.FULLSCREEN which makes the window fill the screen
        self.screen = pygame.display.set_mode((1280,720))

        #I am using pygame.display.get_surface().get_size() so i can get the size of the screen as I have gone into fullscreen I do not know the height and width of the screen
        self.width, self.height = pygame.display.get_surface().get_size()

        #this variable will be used to state whether the game is running or not
        self.running = True

        #I decided to use pygame.event.set_allowed() which limits the amount of events that pygame checks , this will help reduce any lag
        pygame.event.set_allowed([pygame.QUIT,pygame.MOUSEBUTTONDOWN])

        #this initialises the pygame.font module
        pygame.font.init()

        #this code is the different fonts that i will be using
        self.stats_on_screen_font = pygame.font.SysFont(None, int(self.width/35))
        self.slider_font = pygame.font.SysFont(None, int(self.width/16))
        self.cost_font = pygame.font.SysFont(None, int(self.width/20))
        self.sell_font = pygame.font.SysFont(None, int(self.width/20))
        self.shop_font = pygame.font.SysFont(None, int(self.width/30))
        self.shop_item_name_font = pygame.font.SysFont(None, int(self.width / 30),bold=True)
        self.save_name_font = pygame.font.SysFont(None, int(self.width / 16))
        self.save_file_names_font = pygame.font.SysFont(None, int(self.width / 20))
        self.on_screen_notes_font_1 = pygame.font.SysFont(None, int(self.width/20))
        self.on_screen_notes_font_2 = pygame.font.SysFont(None, int(self.width/50))
        self.item_counter_font = pygame.font.SysFont(None, int(self.width/20))


        #this makes the font underlined
        self.shop_item_name_font.set_underline(True)

        #this will be used to max out the fps of my game to whatever i want , i have chosen 60 fps later in the code
        self.clock = pygame.time.Clock()

        #this will be used as a variable to hold the index of an ore which i can use for randomly generating ores later in the code (currently set to 0)
        self.random_ore_number=0

        #these are variables which will be used when offsetting all the buildings , tiles and the background image , and is used to ensure they are all offset by a certain amount
        self.game_x_offset = 0
        self.game_y_offset=0

        #this is the maximum allowed offset value in the y direction , this is needed to stop the player from going too far up
        self.game_y_offset_max=0

        #this code runs some functions which initialise the images and groups I will be using
        self.load_starting_images()
        self.load_starting_groups()

        #this is the maximum allowed offset value in the x direction , this is needed to stop the player from going too far left or right
        self.game_x_offset_max=(self.game_background_image.get_size()[0]-(self.width))/2

        #this code runs a function which loads user data so they can continue from where they left off
        self.load_starting_files()

        # this is a list with different functions in it so i can easily change which screen the user is on
        self.phase = [self.main_menu,self.select_file,self.game,self.shop,self.fuel,self.parts,self.how_to_play,self.winning_screen]

        # this is a variable which says which function should be running from the list above
        self.phase_on = 0

        # this code creates a sprite at the users cursor position so i can use this for collisions
        self.cursor_sprite = pygame.sprite.Sprite()
        self.cursor_sprite.image = pygame.Surface([1, 1])
        self.cursor_sprite.rect = self.cursor_sprite.image.get_rect(topleft=(pygame.mouse.get_pos()))

        #this is a number which direction the player is facing where 3 means the player sprite is facing down
        self.miner_rotation=3

        #this is a number which will be used to cycle through different images to give the illusion that the player is mining
        self.miner_animation=1

        #this will be a value which will determine which direction the user is currently moving in where 0 means the player is not moving , this will be used to stop the user from moving in multiple directions at once
        self.moving=0

        #these are values which show which block in a 2d array the user is currently over and this will be used so i can edit value in an array so i can , for example , remove health from a tile and then save this data in a file so that the health of the user can save if the user decides to quit
        self.x_value_on=0
        self.y_value_on = 0

        #this is a variable i will use when mining to keep track of whether there is a tile/block in front of the user
        self.there_is_a_block_there=False

        #this is the movement speed of the user , this shows how far relative to the size of the screen the buildings and tiles will move
        self.movement_speed=self.width / 256

        #this is the amount of health removed from tiles when the user mines into them
        self.mining_speed=10

        #this holds the amount of money the user has
        self.money_counter=0

        #this holds the amount of fuel the user has
        self.fuel_counter=100

        #this holds the weight the user holds
        self.weight_counter=0

        #this is the maximum fuel the user can have
        self.fuel_max=100

        #this is the maximum weight the user can have
        self.weight_max=100

        #this is a variable to show if the user clicked on the slider or not
        self.mouse_clicked_on_slider=False

        #this is the sliders x location relative to the screen
        self.slider_x_location=self.width/2

        #this is the value that will display on the slider to show how much fuel the user is going to buy
        self.slider_fuel_reading=0

        #this is the value for the amount of fuel the user will consume relative to a dirt block
        self.fuel_consumption=1

        #this is the price that the fuel will cost
        self.fuel_cost_amount=0

        #this value is a multiplier on the cost of shop items which can be increased or reduced
        self.shop_price_reduction_multiplier=1

        #this is the players hitbox when mining up
        self.miner_sprite_up = pygame.sprite.Sprite()
        self.miner_sprite_up.image = pygame.Surface([1,self.drill_1_image.get_size()[1]/2])
        self.miner_sprite_up.rect = self.miner_sprite_up.image.get_rect(topleft=((self.width/2),(self.height*3/4)-(self.drill_1_image.get_size()[1])))

        # this is the players hitbox when mining down
        self.miner_sprite_down = pygame.sprite.Sprite()
        self.miner_sprite_down.image = pygame.Surface([1, self.drill_1_image.get_size()[1]/2])
        self.miner_sprite_down.rect = self.miner_sprite_down.image.get_rect(topleft=((self.width / 2), (self.drill_1_image.get_size()[1]/2)+(self.height * 3 / 4) - (self.drill_1_image.get_size()[1])))

        # this is the players hitbox when mining left
        self.miner_sprite_left = pygame.sprite.Sprite()
        self.miner_sprite_left.image = pygame.Surface([self.drill_1_image.get_size()[1]/2,1])
        self.miner_sprite_left.rect = self.miner_sprite_left.image.get_rect(topleft=((self.width/2)-(self.drill_1_image.get_size()[1]/2),(self.height*3/4)-(self.drill_1_image.get_size()[1]/2)))

        # this is the players hitbox when mining right
        self.miner_sprite_right = pygame.sprite.Sprite()
        self.miner_sprite_right.image = pygame.Surface([self.drill_1_image.get_size()[1]/2,1])
        self.miner_sprite_right.rect = self.miner_sprite_right.image.get_rect(topleft=((self.drill_1_image.get_size()[1]/2)+(self.width/2)-(self.drill_1_image.get_size()[1]/2),(self.height*3/4)-(self.drill_1_image.get_size()[1]/2)))

        #this tells my code whether the user is choosing a save file name or not
        self.saving_screen = False

        #this contains what the user types when choosing their save file name
        self.new_game_save_name = ""

        #this tells the code which save file the user clicked on
        self.which_save_file = 1

        #this is true if the user is trying to delete a save file
        self.deleting_screen = False


        #this is the order which data is saved in the notepads
        self.variable_data_order = [self.new_game_save_name, self.tile_list, self.tile_health_list, self.fuel_counter,
                                    self.fuel_max, self.weight_counter, self.weight_max, self.backpack,
                                    self.fuel_consumption, self.shop_item_bought_list,self.game_x_offset,self.game_y_offset,self.money_counter , self.item_backpack]

        #this is a list of the inital values of data from the self.variable_data_order list
        self.initial_variable_data_order = copy.deepcopy(self.variable_data_order)

        #this is the names of the variables which will be saved inside of notepads
        self.variable_data_name_order = ["self.new_game_save_name", "self.tile_list", "self.tile_health_list", "self.fuel_counter", "self.fuel_max",
         "self.weight_counter", "self.weight_max", "self.backpack", "self.fuel_consumption", "self.shop_item_bought_list",
         "self.game_x_offset","self.game_y_offset","self.money_counter" , "self.item_backpack"]

        #this checks whether to double the ore gained from the next ore or not.
        self.doubled = False

        #this is the multiplier gained from god mode
        self.god_multiplier = 1

        #this is a timer of how long god mode should last
        self.god_item_timer = 0

        #this tells the code which how to screen to show the user
        self.which_how_to_screen = 0

        #this tells the code whether the user has seen each how to screen yet or not
        self.how_to_screen_seen  = [False,False,False]



    #this function loads the game files in saving the users data
    def load_starting_files(self):

        #this loops 3 times for the 3 save files
        for i in range(1,4):

            #this code checks if the save file exists and creates a new file if it does or passes onto the "except" code
            try:
                with open(f"file_{i}.txt", "x+") as f:
                    exec(f'self.file_{i}_data = f.readlines()')

            #this code only runs if the file exists and will read the data in the files
            except:
                with open(f"file_{i}.txt", "r") as f:
                    exec(f'self.file_{i}_data = f.readlines()')



    # this is a function which loads the images I will be using
    def load_starting_images(self):

        #this loads the start image
        self.start_image = pygame.image.load("start_image.png")

        #this changes the size of the start image relative to the height and width of the screen
        self.start_image = pygame.transform.scale(self.start_image, (self.width / 5.2459, self.height / 5.90163))

        #this loads the title image which is an image of the background and the title of my game
        self.title_image = pygame.image.load("title_image.png")

        #this changes the size of the title image relative to the height and width of the screen
        self.title_image = pygame.transform.scale(self.title_image, (self.width,self.height))

        #this loads the back image
        self.back_image = pygame.image.load("back_image.png")

        #this changes the size of the back image relative to the height and width of the screen
        self.back_image = pygame.transform.scale(self.back_image, ((self.width / (3.5555*2)), (self.height/(4*2))))

        # this loads the "choose which file" title image
        self.choose_which_file_image = pygame.image.load("choose_which_file_image.png")

        #this changes the size of the "choose which file" image relative to the height and width of the screen
        self.choose_which_file_image = pygame.transform.scale(self.choose_which_file_image, ((self.width / (2*1.39130434782)), (self.height / (2*4))))

        # this loads the background image
        self.game_background_image = pygame.image.load("background_sand.png")

        #this changes the size of the background image relative to the height and width of the screen
        self.game_background_image = pygame.transform.scale(self.game_background_image, ((self.width/0.66840731070),self.height*3/4))

        # this loads the first drill image used in the animation
        self.drill_1_image = pygame.image.load("drill_1.png")

        #this changes the size of the first drill image relative to the height and width of the screen
        self.drill_1_image = pygame.transform.scale(self.drill_1_image, (self.width / 27.82608, self.height / 8))

        # this loads the second drill image used in the animation
        self.drill_2_image = pygame.image.load("drill_2.png")

        #this changes the size of the second drill image relative to the height and width of the screen
        self.drill_2_image = pygame.transform.scale(self.drill_2_image, (self.width / 27.82608, self.height / 8))

        # this loads the third drill image used in the animation
        self.drill_3_image = pygame.image.load("drill_3.png")

        #this changes the size of the third drill image relative to the height and width of the screen
        self.drill_3_image = pygame.transform.scale(self.drill_3_image, (self.width / 27.82608, self.height / 8))

        # this loads the forth drill image used in the animation
        self.drill_4_image = pygame.image.load("drill_4.png")

        #this changes the size of the forth drill image relative to the height and width of the screen
        self.drill_4_image = pygame.transform.scale(self.drill_4_image, (self.width / 27.82608, self.height / 8))

        #this loops 4 times for the 4 different drill images used in the animation
        for animation in range(1,5):

            #this loops 4 times for the 4 different directions the drill can be facing
            for direction in range(4):

                #this code creates a new image for the different directions and the different animation images
                exec(f'self.drill_{animation}_image_{direction+1} = pygame.transform.rotate(self.drill_{animation}_image, 90 + ({direction+1}*90))')

        # this loads the "new game" image
        self.new_game_image = pygame.image.load("new_game_image.png")

        #this changes the size of the "new game" image relative to the height and width of the screen
        self.new_game_image = pygame.transform.scale(self.new_game_image, (self.width/(2*2),self.height/(4*2)))

        # this loads the "continue" image
        self.continue_image = pygame.image.load("continue_image.png")

        # this changes the size of the "continue" image relative to the height and width of the screen
        self.continue_image = pygame.transform.scale(self.continue_image, (self.width/(2*2),self.height/(4*2)))

        # this loads the top grass image
        self.top_grass_image = pygame.image.load("top_grass_image.png")

        # this changes the size of the top grass image relative to the height and width of the screen
        self.top_grass_image = pygame.transform.scale(self.top_grass_image, (self.width/14.222222,self.height/8))

        # this loads the middle grass image (which is a normal dirt block)
        self.middle_grass_image = pygame.image.load("middle_grass.png")

        # this changes the size of the middle grass image (which is a normal dirt block) relative to the height and width of the screen
        self.middle_grass_image = pygame.transform.scale(self.middle_grass_image, (self.width/14.222222,self.height/8))

        # this loads the rock image
        self.rock_image = pygame.image.load("rock.png")

        # this changes the size of the rock image relative to the height and width of the screen
        self.rock_image = pygame.transform.scale(self.rock_image, (self.width/14.222222,self.height/8))

        # this loads the "lots of rock" image
        self.lots_of_rock_images = pygame.image.load("lots_of_rock_images.png")

        # this changes the size of the "lots of rock" image relative to the height and width of the screen
        self.lots_of_rock_images = pygame.transform.scale(self.lots_of_rock_images, (self.width*6/14.222222,self.height*7/8))

        # this loads the iron ore image
        self.iron_ore = pygame.image.load("iron_ore.png")

        # this changes the size of the iron ore image relative to the height and width of the screen
        self.iron_ore = pygame.transform.scale(self.iron_ore, (self.width/14.222222,self.height/8))

        # this loads the amethyst ore image
        self.emerald_ore = pygame.image.load("emerald_ore.png")

        # this changes the size of the amethyst ore image relative to the height and width of the screen
        self.emerald_ore = pygame.transform.scale(self.emerald_ore, (self.width/14.222222,self.height/8))

        # this loads the gold ore image
        self.gold_ore  = pygame.image.load("gold_ore.png")

        # this changes the size of the gold ore image relative to the height and width of the screen
        self.gold_ore = pygame.transform.scale(self.gold_ore, (self.width/14.222222,self.height/8))

        # this loads the diamond ore image
        self.diamond_ore  = pygame.image.load("diamond_ore.png")

        # this changes the size of the diamond ore image relative to the height and width of the screen
        self.diamond_ore = pygame.transform.scale(self.diamond_ore, (self.width/14.222222,self.height/8))

        # this loads the emerald ore image
        self.amethyst_ore = pygame.image.load("amethyst_ore.png")

        # this changes the size of the emerald ore image relative to the height and width of the screen
        self.amethyst_ore = pygame.transform.scale(self.amethyst_ore, (self.width/14.222222,self.height/8))

        # this loads the shop image
        self.shop_image = pygame.image.load("shop_image.png")

        # this changes the size of the shop image relative to the height and width of the screen
        self.shop_image = pygame.transform.scale(self.shop_image, (self.width*4/7.11111,self.height*4/7.0826666))

        # this loads the fuel store image
        self.fuel_store = pygame.image.load("fuel_store.png")

        # this changes the size of the fuel store image relative to the height and width of the screen
        self.fuel_store = pygame.transform.scale(self.fuel_store, (self.width * 2 / 7.11111, self.height*0.5/1.285714285))

        # this loads the garage image
        self.garage = pygame.image.load("garage.png")

        # this changes the size of the garage image relative to the height and width of the screen
        self.garage = pygame.transform.scale(self.garage, (self.width *4 / 7.11111,self.height*0.5/0.8746090072580))

        # this loads the "buy button" image
        self.fuel_buy_image = pygame.image.load("buy_button.png")

        # this changes the size of the "buy button" image relative to the height and width of the screen
        self.fuel_buy_image = pygame.transform.scale(self.fuel_buy_image, (self.width*0.5/4.252491694,self.height*0.5/2.392026578))

        # this loads the "slider bar" image
        self.slider_bar = pygame.image.load("slider_bar.png")

        # this changes the size of the "slider bar" image relative to the height and width of the screen
        self.slider_bar = pygame.transform.scale(self.slider_bar, (self.width*4/5,self.height/5.74622844827))

        # this loads the "sell or buy" image
        self.sell_or_buy_image = pygame.image.load("sell_or_buy.png")

        # this changes the size of the "sell or buy" image relative to the height and width of the screen
        self.sell_or_buy_image = pygame.transform.scale(self.sell_or_buy_image, (self.width,self.height/12.413793103))

        # this loads the "sell all" image
        self.sell_all_image = pygame.image.load("sell_all_image.png")

        # this changes the size of the "sell all" image relative to the height and width of the screen
        self.sell_all_image = pygame.transform.scale(self.sell_all_image, (self.width/2.383612662,self.height/7.91208))

        # this loads the "shop buy button" image
        self.shop_buy_image = pygame.image.load("shop_buy_image.png")

        # this changes the size of the "shop buy button" image relative to the height and width of the screen
        self.shop_buy_image = pygame.transform.scale(self.shop_buy_image, (self.width/4,self.height/14.4))

        # this loads the "name_your_save_file" image
        self.name_your_save_file = pygame.image.load("name_your_save_file_image.png")

        # this changes the size of the "name_your_save_file" image relative to the height and width of the screen
        self.name_your_save_file = pygame.transform.scale(self.name_your_save_file, (self.width,self.height))

        # this loads the how_to_play image
        self.how_to_play_image = pygame.image.load("how_to_play_image.png")

        # this changes the size of the how_to_play image relative to the height and width of the screen
        self.how_to_play_image = pygame.transform.scale(self.how_to_play_image, (self.width,self.height))

        #this loads the delete image
        self.delete_image = pygame.image.load("delete_image.png")

        #this changes the size of the delete image relative to the height and width of the screen
        self.delete_image = pygame.transform.scale(self.delete_image, ((self.width / (3.5555*2)), (self.height/(4*2))))

        #this loads the play image
        self.play_image = pygame.image.load("play_image.png")

        #this changes the size of the play image relative to the height and width of the screen
        self.play_image = pygame.transform.scale(self.play_image, ((self.width / (3.5555*2)), (self.height/(4*2))))

        #this loads the bomb_item image
        self.bomb_item_image = pygame.image.load("bomb_item_image.png")

        #this changes the size of the play bomb_item image relative to the height and width of the screen
        self.bomb_item_image = pygame.transform.scale(self.bomb_item_image, (self.width/2.1548821548,self.height/6.315789))

        #this loads the teleport_item image
        self.teleport_item_image = pygame.image.load("teleport_item_image.png")

        #this changes the size of the play teleport_item image relative to the height and width of the screen
        self.teleport_item_image = pygame.transform.scale(self.teleport_item_image, (self.width/2.1548821548,self.height/6.315789))

        #this loads the double_up_item image
        self.double_up_item_image = pygame.image.load("double_up_item_image.png")

        #this changes the size of the play double_up_item image relative to the height and width of the screen
        self.double_up_item_image = pygame.transform.scale(self.double_up_item_image, (self.width/2.1548821548,self.height/6.315789))

        #this loads the god_mode_item image
        self.god_mode_item_image = pygame.image.load("god_mode_item_image.png")

        #this changes the size of the play god_mode_item image relative to the height and width of the screen
        self.god_mode_item_image = pygame.transform.scale(self.god_mode_item_image, (self.width/2.1548821548,self.height/6.315789))

        # this loads the how_to_use_the_upgrade_shop_image image
        self.how_to_use_the_upgrade_shop_image = pygame.image.load("how_to_use_the_upgrade_shop_image.png")

        # this changes the size of the how_to_use_the_upgrade_shop_image image relative to the height and width of the screen
        self.how_to_use_the_upgrade_shop_image = pygame.transform.scale(self.how_to_use_the_upgrade_shop_image, (self.width,self.height))

        # this loads the how_to_use_the_fuel_shop_image image
        self.how_to_use_the_fuel_shop_image = pygame.image.load("how_to_use_the_fuel_shop_image.png")

        # this changes the size of the how_to_use_the_fuel_shop_image image relative to the height and width of the screen
        self.how_to_use_the_fuel_shop_image = pygame.transform.scale(self.how_to_use_the_fuel_shop_image, (self.width,self.height))

        # this loads the how_to_use_the_garage_image image
        self.how_to_use_the_garage_image = pygame.image.load("how_to_use_the_garage_image.png")

        # this changes the size of the how_to_use_the_garage_image image relative to the height and width of the screen
        self.how_to_use_the_garage_image = pygame.transform.scale(self.how_to_use_the_garage_image, (self.width,self.height))

        # this loads the winning_screen_image image
        self.winning_screen_image = pygame.image.load("winning_screen_image.png")

        # this changes the size of the winning_screen_image image relative to the height and width of the screen
        self.winning_screen_image = pygame.transform.scale(self.winning_screen_image,(self.width, self.height))

    #this function is used to spawn an entire layer of 1 ore
    def spawning_layers(self,ore_num):

        #this code adds a new empty layer into the 2d list which can be filled with different ores
        for _ in range(1):
            self.tile_list.append([])
            self.tile_health_list.append([])

        #this loops through the code for each tile along a layer and assigns x as the x position of each tile relative to the tiles
        for x in range(-11, 25):

            #this is the y value of the tiles , this is how far down in the list the tile is
            y = len(self.tile_list)-1

            #this adds the tile to the tile group
            self.tile_group.add(Tiles(self.ore_list[ore_num], x * self.middle_grass_image.get_size()[0],(self.top_grass_image.get_size()[1]*y)+ self.height * 3 / 4))

            #this adds which ore it is to the tile list
            self.tile_list[y].append(ore_num)

            #this adds the starting health of the tile to the health list
            self.tile_health_list[y].append(self.ore_health_list[ore_num])

    #this creates a layer of random ores which are chosen using a given probability for each ore
    def random_layers(self,p1,p2,p3,p4,p5,p6):

        #this code adds a new empty layer into the 2d list which can be filled with different ores
        for _ in range(1):
            self.tile_list.append([])
            self.tile_health_list.append([])

        #this loops through the code for each tile along a layer and assigns x as the x position of each tile relative to the tiles
        for x in range(-11, 25):

            #this is the y value of the tiles , this is how far down in the list the tile is
            y = len(self.tile_list)-1

            #this code goes through each ore and has a random chance to choose each ore using the given probabilities in the function and if each ore is chosen it will overwrite the previous ore
            for ore in range(1, 7):
                exec(f'if (random.random())<=p{ore}: self.random_ore_number={ore}')

            # this adds the tile to the tile group
            self.tile_group.add(Tiles(self.ore_list[self.random_ore_number], x * self.middle_grass_image.get_size()[0],(self.top_grass_image.get_size()[1]*y)+ self.height * 3 / 4))

            # this adds which ore it is to the tile list
            self.tile_list[y].append(self.random_ore_number)

            # this adds the starting health of the tile to the health list
            self.tile_health_list[y].append(self.ore_health_list[self.random_ore_number])

    #this functions adds the descriptions in the shop
    def update_shop_descriptions(self):

        # this is a list of the shop item descriptions
        self.shop_item_description_list = [
            f"increases your drilling power , however increases fuel consumption\nprice: {(self.shop_item_price_list[0] * (self.shop_item_bought_list[0] + 1) if (self.shop_item_max_buy_list[0] - self.shop_item_bought_list[0]) else self.na_value)}\nupgrade: {self.shop_item_bought_list[0]}/{self.shop_item_max_buy_list[0]}",
            f"this increases the sell price of ores\nprice: {(self.shop_item_price_list[1] * (self.shop_item_bought_list[1] + 1) if (self.shop_item_max_buy_list[1] - self.shop_item_bought_list[1]) else self.na_value)}\nupgrade: {self.shop_item_bought_list[1]}/{self.shop_item_max_buy_list[1]}",
            f"this reduces the cost of all items\nprice: {(self.shop_item_price_list[2] * (self.shop_item_bought_list[2] + 1) if (self.shop_item_max_buy_list[2] - self.shop_item_bought_list[2]) else self.na_value)}\nupgrade: {self.shop_item_bought_list[2]}/{self.shop_item_max_buy_list[2]}",
            f"this increases your mining speed\nprice: {(self.shop_item_price_list[3] * (self.shop_item_bought_list[3] + 1) if (self.shop_item_max_buy_list[3] - self.shop_item_bought_list[3]) else self.na_value)}\nupgrade: {self.shop_item_bought_list[3]}/{self.shop_item_max_buy_list[3]}",
            f"this increases your max fuel and reduces fuel consumption\nprice: {(self.shop_item_price_list[4] * (self.shop_item_bought_list[4] + 1) if (self.shop_item_max_buy_list[4] - self.shop_item_bought_list[4]) else self.na_value)}\nupgrade: {self.shop_item_bought_list[4]}/{self.shop_item_max_buy_list[4]}",
            f"this increases your max weight\nprice: {(self.shop_item_price_list[5] * (self.shop_item_bought_list[5] + 1) if (self.shop_item_max_buy_list[5] - self.shop_item_bought_list[5]) else self.na_value)}\nupgrade: {self.shop_item_bought_list[5]}/{self.shop_item_max_buy_list[5]}"]


        #this code creates the text and adds it to the self.shop_item_name_group so the text can be displayed on screen
        def add_to_shop_description():

            #this creates a temporary image with the text
            temp_img = (self.shop_font.render(temp, True, "black"))

            #this gets the position of where the image will be placed on screen
            temp_img_rect = temp_img.get_rect(center=((self.shop_buy_image.get_size()[0] / 2) + (self.width * x / 4),self.back_image.get_size()[1] + ((y) * ((self.height - self.back_image.get_size()[1]) / 2)) +temporary_item_name_image.get_size()[1] + ((temp_counter + 0.5) *(self.shop_font.render("g", True,"black")).get_size()[1])))

            #this code adds the image to the self.shop_item_name_group
            self.shop_item_name_group.add(Tiles(temp_img, temp_img_rect.x, temp_img_rect.y))

        #this clears the self.shop_item_name_group to make sure it is empty as the rest of the code will add all of the item descriptions
        for item in self.shop_item_name_group:
            item.kill()

        #this goes through the 6 different shop items
        for x in range(3):
            for y in range(2):

                #this creates the image for the title text of the shop item and puts it in the self.shop_item_name_group
                temporary_item_name_image = self.shop_item_name_font.render(self.shop_item_name_list[(x*2)+y],True,"green")
                self.shop_item_name_group.add(Tiles(temporary_item_name_image,(self.width*((2*x)+1)/8)-(temporary_item_name_image.get_size()[0]/2),self.back_image.get_size()[1]+((y)*((self.height-self.back_image.get_size()[1])/2))))

                #this creates a counter which can be changed later in my code
                temp_counter=0

                #this iterates through the current shop item description and seperates any new lines (so if there is 1 "\n" the description will be split into 2 items)
                for count,lines in enumerate((self.shop_item_description_list[(x*2)+y]).splitlines()):

                    #this creates a temporary string variable
                    temp = ""

                    #this defines temp2 as the first word in the desciption
                    temp2=lines.split()[0]

                    #this goes through the first line in the shop item description word by word
                    for number,word in enumerate(lines.split()):

                        #this checks if this is not the first word in the line to avoid a space in the start of the word as the temp variable would be "" and if this is not the first word it will then make temp2 the previous sentence and the new word
                        if number!=0:
                            temp2 = (f"{temp} {word}")

                        #this checks if the added new word makes the combined length of the words in temp bigger than the max allowed by space
                        if ((self.shop_font.render(temp2,True,"black")).get_size()[0]>=self.shop_buy_image.get_size()[0]):

                            #this uses the temp and creates an image of the text and adds it to the self.shop_item_name_group
                            add_to_shop_description()

                            #this resets the temp variable
                            temp=""

                            #this incraments the temp counter by 1 to show that there is a new line added
                            temp_counter+=1

                        #if the added new word does not make the combined length of the words in temp bigger than the maximum allowed by space then it makes temp = temp2
                        else:
                            temp=temp2

                    #this stops the chance that the last line added was a \n for new line from adding another new line as this code checks if the last thing added was a new line and if it was it doesnt add another line
                    if temp!="" and temp!=" ":

                        #after all the words have been added this runs to add the final line onto the screen
                        add_to_shop_description()

                        # this incraments the temp counter by 1 to show that there is a new line added
                        temp_counter+=1

    #this is a function which loads the groups i will be using as well as lists and such
    def load_starting_groups(self):

        #this creates a sprite group for the main menu sprites (start button) which can hold sprite images which i can use for collisions
        self.start_group = pygame.sprite.Group()

        #this adds a sprite into the sprite group using the Images class to take the start image and the x and y position and x and y size of the image to create the sprite
        self.start_group.add(Images(self.start_image, self.width / 2, self.height *2/3, self.width / 5.2459, self.height / 5.90163))

        #this creates a sprite group for the tiles
        self.tile_group = pygame.sprite.Group()

        #this creates a sprite group for the images in the fuel shop
        self.fuel_group = pygame.sprite.Group()

        #this adds the buy button image to the self.fuel_group
        self.fuel_group.add(Images(self.fuel_buy_image, self.width*3/4 , self.height*3/4 , self.fuel_buy_image.get_size()[0] , self.fuel_buy_image.get_size()[1]))

        #this creates a sprite group for the rocks
        self.rock_group = pygame.sprite.Group()

        #this adds rocks to the self.rock_group , this uses rock images that are 7 tiles long so this code only runs for every 7 layers
        for rock_layer_number in range(0,200,7):
            self.rock_group.add(Tiles(self.lots_of_rock_images, -17 * self.rock_image.get_size()[0], (self.height * 3 / 4)+(self.middle_grass_image.get_size()[0]*rock_layer_number)))
            self.rock_group.add(Tiles(self.lots_of_rock_images, 25* self.rock_image.get_size()[0],(self.height * 3 / 4) + (self.middle_grass_image.get_size()[0] * rock_layer_number)))

        #this creates a sprite group for the buy button images in the shop
        self.shop_buy_group = pygame.sprite.Group()

        #this creates a sprite group for the images in the shop
        self.shop_item_name_group = pygame.sprite.Group()

        #this is a list of the shop item names
        self.shop_item_name_list = ["drill upgrade","tax reduction","bargaining","speed","fuel","backpack"]

        #this is a list for the amount of shop items that have been bought for each shop item
        self.shop_item_bought_list = [0,0,0,0,0,0]

        #this is the maximum amount you can buy each shop item
        self.shop_item_max_buy_list = [10,10,5,5,7,15]

        #this is the initial prices of the shop items
        self.shop_item_price_list = [30,50,200,150,20,30]

        # this is used to display N/A when the user has maxed out a certain shop item
        self.na_value = "N/A"

        #this iterates for each item in the shop
        for x in range(3):
            for y in range(2):

                #this adds a buy button for each item in the shop in the self.shop_buy_group
                self.shop_buy_group.add(Tiles(self.shop_buy_image,self.width*x/4,-self.shop_buy_image.get_size()[1]+self.back_image.get_size()[1]+((y+1)*((self.height-self.back_image.get_size()[1])/2))))

        #this runs the function to update the shop item descriptions
        self.update_shop_descriptions()

        #this is the multiplier of fuel usage for the different ores
        self.ore_fuel_list = [1,1,2,4,8,20,50]

        # this is the multiplier of the weight for the different ores
        self.ore_weight_list = [1,1,3,7,15,31,63]

        #this is the users backpack and contains the amount of each item the user has
        self.backpack=[0,0,0,0,0,0,0]

        #this creates a 2d list for the tiles
        self.tile_list = []

        #this creates a 2d list for the health of the tiles
        self.tile_health_list = []

        #this is a list of the ores
        self.ore_list = [self.top_grass_image , self.middle_grass_image , self.iron_ore, self.gold_ore , self.diamond_ore , self.emerald_ore , self.amethyst_ore]

        #this is a list of the names of the ores
        self.ore_name_list = ["grass","dirt","iron","gold","diamond","emerald","amethyst"]

        #this is the initial sell prices of the ores
        self.ore_start_price_list = [0,0,10,50,100,200,500]

        #this is a variable to show how much the prices of the ores have increased
        self.ore_price_increase = 1

        #this is the health of the ores
        self.ore_health_list = [100,100,200,300,1000,2000,5000]

        #this makes the first layer of grass ore
        self.spawning_layers(0)

        # this code spawns in the rest of the tiles
        for layer in range(300):
            self.random_layers(1,layer/300,(layer-50)/300,(layer-100)/300,(layer-150)/300,(layer-200)/300)

        #this creates a group for the buildings
        self.building_group = pygame.sprite.Group()

        #this adds the shop image to the self.building_group
        self.building_group.add(Buildings(self.shop_image, -10* self.rock_image.get_size()[0] + self.game_x_offset*5,(self.height*3/4)-self.shop_image.get_size()[1]+self.game_y_offset))

        #this adds the fuel shop image to the self.building_group
        self.building_group.add(Buildings(self.fuel_store, 5 * self.rock_image.get_size()[0] + self.game_x_offset*5,(self.height*3/4)-self.fuel_store.get_size()[1]+self.game_y_offset))

        #this adds the garage image to the self.building_group
        self.building_group.add(Buildings(self.garage , 15 * self.rock_image.get_size()[0] + self.game_x_offset * 5,(self.height * 3 / 4) - self.garage.get_size()[1] + self.game_y_offset))

        #this puts information on screen after certain events
        self.notes_group = pygame.sprite.Group()

        #a 2d list used to store each note and the time the note should stay on screen.
        self.notes_list = []

        #this is used to display the items in the garage
        self.item_group = pygame.sprite.Group()

        #this is a list of the items
        self.item_list = [self.bomb_item_image,self.teleport_item_image,self.double_up_item_image,self.god_mode_item_image]

        #this goes through each item and adds it to the item group
        for y,item in enumerate(self.item_list):
            self.item_group.add(Tiles(item,self.width-self.bomb_item_image.get_size()[0],self.sell_or_buy_image.get_size()[1]+self.back_image.get_size()[1]+(y*(self.bomb_item_image.get_size()[1]+1))))

        self.item_backpack = [0,0,0,0]

        self.item_price_list = [[0,0,3,1,0,0,0],[0,0,0,3,1,0,0],[0,0,0,0,3,1,0],[0,0,0,0,0,3,1]]




    #this function displays the main menu
    def main_menu(self):

        #this puts the title image (which is the background image and title image) onto the screen , filling the entire screen
        self.screen.blit(self.title_image,(0,0))

        #this puts the start group onto the screen which contains the start button
        self.start_group.draw(self.screen)

        #this updates the sprite on the cursor to the users cursor location
        self.cursor_sprite.rect = self.cursor_sprite.image.get_rect(topleft=(pygame.mouse.get_pos()))

        #this code checks for collisions between the sprite on the cursor and the sprite group
        if pygame.sprite.spritecollide(self.cursor_sprite,self.start_group,False,pygame.sprite.collide_mask):

            #this code finds if the mouse button is down and will move onto the next screen (save file selection screen) if it is
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        self.phase_on=1

    # this function displays the save file selection screen
    def select_file(self):

        #this checks if the user is choosing a save file
        if self.saving_screen == False:

            #this makes the screen white
            self.screen.fill("white")

            #this puts the back image on the topleft of the screen
            self.screen.blit(self.back_image,(0,0))

            #this puts the delete image on the topright of the screen
            self.screen.blit((self.delete_image if self.deleting_screen==False else self.play_image),(self.width-self.delete_image.get_size()[0],0))

            #this puts the choose_which_file image on the screen
            self.screen.blit(self.choose_which_file_image,self.choose_which_file_image.get_rect(center=(self.width/2,self.choose_which_file_image.get_size()[1]/2)))

            # this gets the current mouse position in the y direction
            mouse_y_pos = pygame.mouse.get_pos()[1]

            #this checks if the user is not trying to delete a save file
            if self.deleting_screen==False:

                #this loops 3 times for the 3 different save files
                for i in range(1,4):

                    #this makes the save file the user is hovering over red
                    if mouse_y_pos >= (i * self.height / 4) and mouse_y_pos < ((i + 1) * self.height / 4):
                        self.screen.fill("red", (0, i * self.height / 4, self.width, self.height / 4))

                    #this draws 3 lines across the screen
                    pygame.draw.line(self.screen,"black",(0,self.height*3*i/12),(self.width,self.height*3*i/12))

                    #this puts either the new_game image or the continue image depending on whether there is any save data for each file
                    exec(f'self.screen.blit(self.new_game_image, (0,self.height*i/4)) if self.file_{i}_data==[] else self.screen.blit(self.continue_image, (0,self.height*i/4))')

                    #this puts the name of the ~save file onto the screen if the player has played in that file before
                    #this puts the name of the save file onto the screen if the player has played in that file before
                    exec(f'if self.file_{i}_data!=[]:'
                         f'   \n\tself.screen.blit(self.save_file_names_font.render(self.file_{i}_data[0].strip(),True,"black"),(self.width/2,{i}*self.height/4))')

            #this runs if the user is trying to delete a save file
            else:

                #this makes all the save files red
                self.screen.fill("red",(0,self.height/4,self.width,self.height))

                #this loops 3 times for the 3 different save files
                for i in range(1,4):

                    # this draws 3 lines across the screen
                    pygame.draw.line(self.screen, "black", (0, self.height * 3 * i / 12),
                                     (self.width, self.height * 3 * i / 12))


                    #this makes the save file the user is hovering over red
                    if mouse_y_pos >= (i * self.height / 4) and mouse_y_pos < ((i + 1) * self.height / 4):

                        # this puts either the new_game image or the continue image depending on whether there is any save data for each file
                        exec(f'if self.file_{i}_data!=[]:'
                             f'   \n\tself.screen.blit(self.new_game_image, (0+random.randint(0,self.width//(256*0.75)),random.randint(0,self.width//(256*0.75))+self.height*i/4)) if self.file_{i}_data==[] else self.screen.blit(self.continue_image, (0+random.randint(0,self.width//(256*0.75)),random.randint(0,self.width//(256*0.75))+self.height*i/4))'
                             f'   \nelse:'
                             f'   \n\tself.screen.blit(self.new_game_image, (0,self.height*i/4)) if self.file_{i}_data==[] else self.screen.blit(self.continue_image, (0,self.height*i/4))')

                        # this puts the name of the save file onto the screen if the player has played in that file before
                        exec(f'if self.file_{i}_data!=[]:'
                             f'   \n\tself.screen.blit(self.save_file_names_font.render(self.file_{i}_data[0].strip(),True,"black"),(random.randint(0,self.width//(256*0.75))+self.width/2,random.randint(0,self.width//(256*0.75))+{i}*self.height/4))')



                    else:
                        # this puts either the new_game image or the continue image depending on whether there is any save data for each file
                        exec(f'self.screen.blit(self.new_game_image, (0,self.height*i/4)) if self.file_{i}_data==[] else self.screen.blit(self.continue_image, (0,self.height*i/4))')

                        # this puts the name of the save file onto the screen if the player has played in that file before
                        exec(f'if self.file_{i}_data!=[]:'
                             f'   \n\tself.screen.blit(self.save_file_names_font.render(self.file_{i}_data[0].strip(),True,"black"),(self.width/2,{i}*self.height/4))')


        # this checks if the user is choosing a save name for a new game file
        else:

            #this puts the name_your_save_file image on the screen
            self.screen.blit(self.name_your_save_file,(0,0))

            #this puts the text that the user is typing on screen
            self.new_game_save_image = self.save_name_font.render(self.new_game_save_name,True,"black")
            self.screen.blit(self.new_game_save_image,self.new_game_save_image.get_rect(center=((self.width/2),(self.height/2.9032258)+(self.new_game_save_image.get_size()[1]/2))))



    #this function takes in the user inputs
    def game_inputs(self):

        #this gets the keys that are being pushed down by the user
        keys = pygame.key.get_pressed()

        #this checks if the user is either not moving or is already moving up , which stops the user from moving in multiple directions at once
        if self.moving==0 or self.moving==1:

            #this checks if the w or up arrow button is being pushed down
            if keys[pygame.K_w] or keys[pygame.K_UP]:

                #this temporarily changes the value of this variable to false so that later in the code I can check if the user has collisions with a tile so i can make this True , this code resets that every time
                self.there_is_a_block_there = False

                #this code makes the player sprite face up
                self.miner_rotation=1

                #this tells the code that the user is currently moving up
                self.moving=1

                # this checks if the games y offset is less than the maximum allowed so that the player wont be able to move if this the y offset is bigger than the max offset
                if self.game_y_offset < self.game_y_offset_max:

                    #this goes through every tile in the tile group
                    for tile in self.tile_group:

                        #this checks if the tile is in contact with the player
                        if pygame.sprite.collide_rect(tile,self.miner_sprite_up):

                            #this tells the code that there is a collision
                            self.there_is_a_block_there = True

                            #this checks if you have enough fuel to mine the block
                            if self.fuel_counter >= self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on - 2][(self.x_value_on)]]:

                                #this checks if you have enough weight remaining to mine the block
                                if (self.weight_max-self.weight_counter) >= self.ore_weight_list[self.tile_list[self.y_value_on - 2][(self.x_value_on)]]:

                                    #this goes through the list using the current x and y value and reduces the health of the block by the players mining speed
                                    self.tile_health_list[self.y_value_on-2][(self.x_value_on)] -= self.mining_speed * self.god_multiplier

                                    #this makes the drill move to give a mining animation
                                    self.miner_animation+=1

                                    #this checks if the tiles health is below or equal zero
                                    if self.tile_health_list[self.y_value_on-2][(self.x_value_on)] <= 0:

                                        #this kills the tile
                                        tile.kill()

                                        #this adds some temporary notes on screen which show which ore was mined
                                        note=self.on_screen_notes_font_2.render(
                                            f"mined {(self.ore_name_list[self.tile_list[self.y_value_on - 2][(self.x_value_on)]])}",
                                            True, "pink")
                                        note.set_alpha(128)
                                        self.notes_group.add(Tiles(note, random.randint((self.width//3)-note.get_size()[0]//2,(self.width*2//3)-note.get_size()[0]//2),(random.randint(self.height*3//8,self.height*7//8))))
                                        self.notes_list.append([1200,self.pygame_time])

                                        #this adds the tile to your backpack
                                        self.backpack[self.tile_list[self.y_value_on - 2][(self.x_value_on)]] += 1

                                        #this reduces your fuel value by the amount the tile takes to mine it
                                        self.fuel_counter-=self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on - 2][(self.x_value_on)]]

                                        #this increases your weight value by the weight of the tile
                                        self.weight_counter+=self.ore_weight_list[self.tile_list[self.y_value_on - 2][(self.x_value_on)]]

                                        #this resets this variable so the next time the code can check for collisions again and have this as False unless there is a collision
                                        self.there_is_a_block_there = False

                                        #this code runs if the user uses the double up item
                                        if self.doubled==True:
                                            self.doubled = False

                                            # this increases your weight value by the weight of the tile
                                            self.weight_counter += self.ore_weight_list[self.tile_list[self.y_value_on - 2][(self.x_value_on)]]

                                            # this adds the tile to your backpack
                                            self.backpack[self.tile_list[self.y_value_on - 2][(self.x_value_on)]] += 1

                                        #this updates the tile_list to show the tile as dead
                                        self.tile_list[self.y_value_on - 2][(self.x_value_on)]=-1






                                #this is if the user does not have enough weight remaining to mine the tile
                                else:
                                    note = self.on_screen_notes_font_1.render(
                                        "BACKPACK FULL",
                                        True, "pink")
                                    note.set_alpha(128)
                                    self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                                    self.notes_list.append([15, self.pygame_time])

                            #this is if the user does not have enough fuel to mine the tile
                            else:
                                note = self.on_screen_notes_font_1.render(
                                    "NOT ENOUGH FUEL",
                                    True, "pink")
                                note.set_alpha(128)
                                self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                                self.notes_list.append([15, self.pygame_time])

                    #this happens if there is no tile there
                    if self.there_is_a_block_there==False:

                        #this code moves all the tiles , buildings , rocks and background image by the players movement speed
                        for tile in self.tile_group:
                            tile.rect.y += self.movement_speed
                        for building in self.building_group:
                            building.rect.y += self.movement_speed
                        for rock in self.rock_group:
                            rock.rect.y += self.movement_speed
                        self.game_y_offset += self.movement_speed

            #this happens if the user is not holding down this button any more
            else:

                #this tells the code that the user is currently not moving
                self.moving=0

        # this checks if the user is either not moving or is already moving left , which stops the user from moving in multiple directions at once
        if self.moving==0 or self.moving==2:

            # this checks if the a or left arrow button is being pushed down
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:

                #this temporarily changes the value of this variable to false so that later in the code I can check if the user has collisions with a tile so i can make this True , this code resets that every time
                self.there_is_a_block_there = False

                # this code makes the player sprite face left
                self.miner_rotation=2

                # this tells the code that the user is currently moving left
                self.moving=2

                # this checks if the games x offset is less than the maximum allowed so that the player wont be able to move if this the x offset is bigger than the max offset
                if self.game_x_offset < self.game_x_offset_max:

                    # this goes through every tile in the tile group
                    for tile in self.tile_group:

                        # this checks if the tile is in contact with the player
                        if pygame.sprite.collide_rect(tile,self.miner_sprite_left):

                            # this tells the code that there is a collision
                            self.there_is_a_block_there = True

                            # this checks if you have enough fuel to mine the block
                            if self.fuel_counter >= self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]]:

                                # this checks if you have enough weight remaining to mine the block
                                if (self.weight_max-self.weight_counter)>=self.ore_weight_list[self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]]:

                                    # this goes through the list using the current x and y value and reduces the health of the block by the players mining speed
                                    self.tile_health_list[self.y_value_on-1][(self.x_value_on)-1] -= self.mining_speed * self.god_multiplier

                                    #this makes the drill move to give a mining animation
                                    self.miner_animation+=1

                                    # this checks if the tiles health is below or equal zero
                                    if self.tile_health_list[self.y_value_on-1][(self.x_value_on)-1] <= 0:

                                        # this kills the tile
                                        tile.kill()

                                        #this adds some temporary notes on screen which show which ore was mined
                                        note=self.on_screen_notes_font_2.render(
                                            f"mined {(self.ore_name_list[self.tile_list[self.y_value_on-1][(self.x_value_on)-1]])}",
                                            True, "pink")
                                        note.set_alpha(128)
                                        self.notes_group.add(Tiles(note, random.randint((self.width//3)-note.get_size()[0]//2,(self.width*2//3)-note.get_size()[0]//2),(random.randint(self.height*3//8,self.height*7//8))))
                                        self.notes_list.append([1280,self.pygame_time])

                                        # this adds the tile to your backpack
                                        self.backpack[self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]] += 1

                                        # this reduces your fuel value by the amount the tile takes to mine it
                                        self.fuel_counter-=self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]]

                                        # this increases your weight value by the weight of the tile
                                        self.weight_counter+=self.ore_weight_list[self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]]

                                        #this resets this variable so the next time the code can check for collisions again and have this as False unless there is a collision
                                        self.there_is_a_block_there = False

                                        # this code runs if the user uses the double up item
                                        if self.doubled==True:
                                            self.doubled = False

                                            # this adds the tile to your backpack
                                            self.backpack[self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]] += 1

                                            # this increases your weight value by the weight of the tile
                                            self.weight_counter+=self.ore_weight_list[self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]]

                                        #this updates the tile_list to show the tile as dead
                                        self.tile_list[self.y_value_on - 1][(self.x_value_on - 1)]=-1


                                # this is if the user does not have enough weight remaining to mine the tile
                                else:
                                    note = self.on_screen_notes_font_1.render(
                                        "BACKPACK FULL",
                                        True, "pink")
                                    note.set_alpha(128)
                                    self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                                    self.notes_list.append([15, self.pygame_time])

                            # this is if the user does not have enough fuel to mine the tile
                            else:
                                note = self.on_screen_notes_font_1.render(
                                    "NOT ENOUGH FUEL",
                                    True, "pink")
                                note.set_alpha(128)
                                self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                                self.notes_list.append([15, self.pygame_time])

                    #this happens if there is no tile there
                    if self.there_is_a_block_there==False:

                        #this code moves all the tiles , buildings , rocks and background image by the players movement speed
                        for tile in self.tile_group:
                            tile.rect.x += self.movement_speed
                        for building in self.building_group:
                            building.rect.x += self.movement_speed
                        for rock in self.rock_group:
                            rock.rect.x += self.movement_speed
                        self.game_x_offset += self.movement_speed/5

                # this checks if  the x offset is more than the maximum allowed
                if self.game_x_offset >= self.game_x_offset_max:

                    # if the x offset is above the maximum allowed this will set the x offset as the maximum
                    self.game_x_offset=self.game_x_offset_max

            #this happens if the user is not holding down this button any more
            else:

                #this tells the code that the user is currently not moving
                self.moving=0

        # this checks if the user is either not moving or is already moving down , which stops the user from moving in multiple directions at once
        if self.moving == 0 or self.moving ==3:

            # this checks if the s or down arrow button is being pushed down
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:

                #this temporarily changes the value of this variable to false so that later in the code I can check if the user has collisions with a tile so i can make this True , this code resets that every time
                self.there_is_a_block_there = False

                # this code makes the player sprite face down
                self.miner_rotation=3

                # this tells the code that the user is currently moving down
                self.moving=3

                # this goes through every tile in the tile group
                for tile in self.tile_group:

                    # this checks if the tile is in contact with the player
                    if pygame.sprite.collide_rect(tile, self.miner_sprite_down):

                        # this tells the code that there is a collision
                        self.there_is_a_block_there=True

                        # this checks if you have enough fuel to mine the block
                        if self.fuel_counter >= self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on][(self.x_value_on)]]:

                            # this checks if you have enough weight remaining to mine the block
                            if (self.weight_max-self.weight_counter)>= self.ore_weight_list[self.tile_list[self.y_value_on][(self.x_value_on)]]:

                                # this goes through the list using the current x and y value and reduces the health of the block by the players mining speed
                                self.tile_health_list[self.y_value_on][(self.x_value_on)]-=self.mining_speed * self.god_multiplier

                                # this makes the drill move to give a mining animation
                                self.miner_animation += 1

                                # this checks if the tiles health is below or equal zero
                                if self.tile_health_list[self.y_value_on][(self.x_value_on)]<=0:

                                    # this kills the tile
                                    tile.kill()

                                    #this adds some temporary notes on screen which show which ore was mined
                                    note = self.on_screen_notes_font_2.render(
                                        f"mined {(self.ore_name_list[self.tile_list[self.y_value_on][(self.x_value_on)]])}",
                                        True, "pink")
                                    note.set_alpha(128)
                                    self.notes_group.add(Tiles(note, random.randint((self.width // 3) - note.get_size()[0] // 2,(self.width * 2 // 3) - note.get_size()[0] // 2), (random.randint(self.height * 3 // 8,self.height * 7 // 8))))
                                    self.notes_list.append([1280,self.pygame_time])

                                    # this adds the tile to your backpack
                                    self.backpack[self.tile_list[self.y_value_on][(self.x_value_on )]] += 1

                                    # this reduces your fuel value by the amount the tile takes to mine it
                                    self.fuel_counter-=self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on][(self.x_value_on )]]

                                    # this checks if you have enough weight remaining to mine the block
                                    self.weight_counter+=self.ore_weight_list[self.tile_list[self.y_value_on][(self.x_value_on )]]

                                    # this resets this variable so the next time the code can check for collisions again and have this as False unless there is a collision
                                    self.there_is_a_block_there=False

                                    # this code runs if the user uses the double up item
                                    if self.doubled==True:

                                        self.doubled=False

                                        # this adds the tile to your backpack
                                        self.backpack[self.tile_list[self.y_value_on][(self.x_value_on)]] += 1

                                        # this checks if you have enough weight remaining to mine the block
                                        self.weight_counter += self.ore_weight_list[self.tile_list[self.y_value_on][(self.x_value_on)]]


                                    # this updates the tile_list to show the tile as dead
                                    self.tile_list[self.y_value_on][(self.x_value_on)] = -1

                            # this is if the user does not have enough weight remaining to mine the tile
                            else:
                                note = self.on_screen_notes_font_1.render(
                                    "BACKPACK FULL",
                                    True, "pink")
                                note.set_alpha(128)
                                self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                                self.notes_list.append([15, self.pygame_time])

                        # this is if the user does not have enough fuel to mine the tile
                        else:
                            note = self.on_screen_notes_font_1.render(
                                "NOT ENOUGH FUEL",
                                True, "pink")
                            note.set_alpha(128)
                            self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                            self.notes_list.append([15, self.pygame_time])


                #this happens if there is no tile there
                if self.there_is_a_block_there==False:

                        #this code moves all the tiles , buildings , rocks and background image by the players movement speed
                    for tile in self.tile_group:
                        tile.rect.y -= self.movement_speed
                    for building in self.building_group:
                        building.rect.y -= self.movement_speed
                    for rock in self.rock_group:
                        rock.rect.y -= self.movement_speed
                    self.game_y_offset-=self.movement_speed

            #this happens if the user is not holding down this button any more
            else:

                #this tells the code that the user is currently not moving
                self.moving=0

        # this checks if the user is either not moving or is already moving right , which stops the user from moving in multiple directions at once
        if self.moving == 0 or self.moving ==4:

            # this checks if the d or right arrow button is being pushed down
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:

                #this temporarily changes the value of this variable to false so that later in the code I can check if the user has collisions with a tile so i can make this True , this code resets that every time
                self.there_is_a_block_there = False

                # this code makes the player sprite face right
                self.miner_rotation=4

                # this tells the code that the user is currently moving right
                self.moving=4

                # this checks if the games x offset is less than the maximum allowed so that the player wont be able to move if this the x offset is bigger than the max offset
                if self.game_x_offset >- self.game_x_offset_max:

                    # this goes through every tile in the tile group
                    for tile in self.tile_group:

                        # this checks if the tile is in contact with the player
                        if pygame.sprite.collide_rect(tile,self.miner_sprite_right):

                            # this tells the code that there is a collision
                            self.there_is_a_block_there = True

                            # this checks if you have enough fuel to mine the block
                            if self.fuel_counter >= self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on-1][(self.x_value_on+1)]]:

                                # this checks if you have enough weight remaining to mine the block
                                if (self.weight_max-self.weight_counter)>=self.ore_weight_list[self.tile_list[self.y_value_on-1][(self.x_value_on+1)]]:

                                    # this goes through the list using the current x and y value and reduces the health of the block by the players mining speed
                                    self.tile_health_list[self.y_value_on-1][(self.x_value_on+1)] -= self.mining_speed * self.god_multiplier

                                    #this makes the drill move to give a mining animation
                                    self.miner_animation+=1

                                    # this checks if the tiles health is below or equal zero
                                    if self.tile_health_list[self.y_value_on-1][(self.x_value_on+1)] <= 0:

                                        # this kills the tile
                                        tile.kill()

                                        #this adds some temporary notes on screen which show which ore was mined
                                        note = self.on_screen_notes_font_2.render(
                                            f"mined {(self.ore_name_list[self.tile_list[self.y_value_on-1][(self.x_value_on+1)]])}",
                                            True, "pink")
                                        note.set_alpha(128)
                                        self.notes_group.add(Tiles(note, random.randint((self.width // 3) - note.get_size()[0] // 2,(self.width * 2 // 3) - note.get_size()[0] // 2), (random.randint(self.height * 3 // 8,self.height * 7 // 8))))
                                        self.notes_list.append([1280,self.pygame_time])

                                        # this adds the tile to your backpack
                                        self.backpack[self.tile_list[self.y_value_on-1][(self.x_value_on+1)]]+=1

                                        # this reduces your fuel value by the amount the tile takes to mine it
                                        self.fuel_counter-=self.fuel_consumption*self.ore_fuel_list[self.tile_list[self.y_value_on-1][(self.x_value_on+1)]]

                                        # this checks if you have enough weight remaining to mine the block
                                        self.weight_counter+=self.ore_weight_list[self.tile_list[self.y_value_on-1][(self.x_value_on+1)]]

                                        #this resets this variable so the next time the code can check for collisions again and have this as False unless there is a collision
                                        self.there_is_a_block_there = False

                                        # this code runs if the user uses the double up item
                                        if self.doubled==True:

                                            self.doubled=False

                                            # this adds the tile to your backpack
                                            self.backpack[self.tile_list[self.y_value_on - 1][(self.x_value_on + 1)]] += 1

                                            # this checks if you have enough weight remaining to mine the block
                                            self.weight_counter += self.ore_weight_list[self.tile_list[self.y_value_on - 1][(self.x_value_on + 1)]]

                                        #this updates the tile_list to show the tile as dead
                                        self.tile_list[self.y_value_on-1][(self.x_value_on+1)]=-1

                                # this is if the user does not have enough weight remaining to mine the tile
                                else:
                                    note = self.on_screen_notes_font_1.render(
                                        "BACKPACK FULL",
                                        True, "pink")
                                    note.set_alpha(128)
                                    self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                                    self.notes_list.append([15, self.pygame_time])

                            # this is if the user does not have enough fuel to mine the tile
                            else:
                                note = self.on_screen_notes_font_1.render(
                                    "NOT ENOUGH FUEL",
                                    True, "pink")
                                note.set_alpha(128)
                                self.notes_group.add(Tiles(note, (self.width/2)-(note.get_size()[0]/2), self.height*6.5/8))
                                self.notes_list.append([15, self.pygame_time])


                    # this happens if there is no tile there
                    if self.there_is_a_block_there == False:

                        # this code moves all the tiles , buildings , rocks and background image by the players movement speed
                        for tile in self.tile_group:
                            tile.rect.x -= self.movement_speed
                        for building in self.building_group:
                            building.rect.x -= self.movement_speed
                        for rock in self.rock_group:
                            rock.rect.x -= self.movement_speed
                        self.game_x_offset -= self.movement_speed/5

                #this checks if  the x offset is less than the minimum allowed
                if self.game_x_offset <= -self.game_x_offset_max:

                    #if the x offset is below the minimum allowed this will set the x offset as the minimum
                    self.game_x_offset=-self.game_x_offset_max

            # this happens if the user is not holding down this button any more
            else:

                # this tells the code that the user is currently not moving
                self.moving = 0

    #this functions checks if the user is trying to enter a building
    def entering_buildings(self):

        #this goes through each item in the building group
        for number,building in enumerate(self.building_group):

            #this checks for collisions between the building and the user
            if pygame.sprite.collide_rect(building,self.miner_sprite_left) or pygame.sprite.collide_rect(building,self.miner_sprite_right):

                #this gets the keys that are being pushed down by the user
                keys = pygame.key.get_pressed()

                #this checks if the e key is being pushed down
                if keys[pygame.K_e]:

                    #this checks if the user has not seen the how to screen yet or not
                    if self.how_to_screen_seen[number]==False:

                        #this puts the how to screen for each building
                        self.which_how_to_screen = 1+number

                        #this shows the user the how to screen
                        self.phase_on=6

                    else:
                        #this changes the phase which changes the screen to each building
                        self.phase_on=3+number

                    #this sets the slider reading at half of the max value the slider can be which is used when entering the fuel store
                    self.slider_fuel_reading=int(round(1/2 * (self.fuel_max - self.fuel_counter),2))

                    #this puts the slider at half of the screen across
                    self.slider_x_location=self.width/2

    #this puts the stats on screen
    def stats_put_on_screen(self,text):

        #this splits the text onto different lines if there is a "\n" in the text and then goes through this list of different lines
        for line, text in enumerate(text.splitlines()):

            #this puts the text on screen
            self.screen.blit(self.stats_on_screen_font.render(text, True, "black"),self.stats_on_screen_font.render(text, True, "black").get_rect(topright=(self.width,self.stats_on_screen_font.render("g", True, "black").get_size()[1] * line)))

    #this function displays the game
    def game(self):

        #this fills the screen with a colour of rgb value of (181 , 101 , 29)
        self.screen.fill((181,101,29))

        #this goes to code which takes in user inputs
        self.game_inputs()

        #this updates the x and y value of which tile in the 2d array the user is currently over
        self.x_value_on = int(35-(((self.game_x_offset + self.game_x_offset_max+4) // 17.997)))
        self.y_value_on = int(((-self.game_y_offset)+(self.middle_grass_image.get_size()[0]/2))//(self.middle_grass_image.get_size()[0]))

        #this puts the background image on the screen
        self.screen.blit(self.game_background_image,(self.game_x_offset-((self.game_background_image.get_size()[0])-self.width)/2,self.game_y_offset))

        #this puts the building images on the screen
        self.building_group.draw(self.screen)

        #this leads to some code which checks if the user is trying to enter a builing
        self.entering_buildings()

        #this puts the rock images on the screen
        self.rock_group.draw(self.screen)

        #this displays the player sprite
        exec(f'self.screen.blit(self.drill_{(self.miner_animation%4)+1}_image_{self.miner_rotation} ,self.drill_{(self.miner_animation%4)+1}_image_{self.miner_rotation}.get_rect(center=(((self.width/2),(self.height*3/4)-self.drill_{(self.miner_animation%4)+1}_image.get_size()[1]/2))))')

        #this puts the tiles on screen
        self.tile_group.draw(self.screen)

        #this puts the notes on screen
        self.notes_group.draw(self.screen)

        #this moves the notes up the screen
        for i in self.notes_group:
            i.rect.y-=1

        #this checks for each note if a certain time , depending on each note , has gone. if it has then it deletes the note
        for i,j in self.notes_list:
            if (self.pygame_time-j)>=i:
                self.notes_group.sprites()[0].kill()
                self.notes_list.pop(0)

        #this checks if gode mode is or or not
        if self.pygame_time-60000>=self.god_item_timer:
            self.god_multiplier=1


        #this checks if the user has reached the winning screen.
        if self.y_value_on>=302:
            self.phase_on=7

        # #this displays the users hit boundaries
        self.screen.blit(self.miner_sprite_up.image,self.miner_sprite_up.rect)
        self.screen.blit(self.miner_sprite_down.image,self.miner_sprite_down.rect)
        self.screen.blit(self.miner_sprite_left.image,self.miner_sprite_left.rect)
        self.screen.blit(self.miner_sprite_right.image,self.miner_sprite_right.rect)

    #this function applies the effect of each shop item
    def shop_item_bought(self):

        #this changes the fuel consumption in accordance with the shop upgrades
        self.fuel_consumption=1+((self.shop_item_bought_list[0])*2)/(self.shop_item_bought_list[4]+2)

        # this changes the mining damage in accordance with the shop upgrades
        self.mining_speed=((self.shop_item_bought_list[0])*20)+10

        # this changes the ore price increase in accordance with the shop upgrades
        self.ore_price_increase = ((self.shop_item_bought_list[1]) / 2)+1

        # this changes the shop price reduction in accordance with the shop upgrades
        self.shop_price_reduction_multiplier=1-((self.shop_item_bought_list[2])*0.05)

        # this changes the movement speed in accordance with the shop upgrades
        self.movement_speed=(self.width/256)*(1+self.shop_item_bought_list[3])

        # this changes the fuel_max in accordance with the shop upgrades
        self.fuel_max=(100*((3*self.shop_item_bought_list[4])+1))

        # this changes the max_weight in accordance with the shop upgrades
        self.weight_max=(50*(self.shop_item_bought_list[5]+1))+50

    # this function displays the shop
    def shop(self):

        #this fills the screen red
        self.screen.fill("red")
        #
        #this fills the top of the screen white
        self.screen.fill("white",(0,0,self.width,self.back_image.get_size()[1]))

        #this puts the back button on the screen
        self.screen.blit(self.back_image, (0, 0))

        #this puts the shop buy buttons on the screen
        self.shop_buy_group.draw(self.screen)
        #
        #this puts the shop item name and description on the screen.
        self.shop_item_name_group.draw(self.screen)

        #this draws lines to seperate the shop items
        for i in range(1,4):
            pygame.draw.line(self.screen,"black",(self.width*i/4,self.back_image.get_size()[1]),(self.width*i/4,self.height),width=1)


    # this function displays the fuel shop
    def fuel(self):

        #this fills the screen white
        self.screen.fill("white")

        #this gets the cursor rect
        self.cursor_sprite.rect = self.cursor_sprite.image.get_rect(topleft=(pygame.mouse.get_pos()))

        #this puts the back button on the screen
        self.screen.blit(self.back_image, (0, 0))

        #this puts the fuel buy button on the screen
        self.fuel_group.draw(self.screen)

        #this puts the slider bar on the screen
        self.screen.blit(self.slider_bar,(self.width/10,(self.height/2)-(self.slider_bar.get_size()[1]/2)))

        #this gets the mouse position
        self.mousewhere = pygame.mouse.get_pos()

        #this makes an image of the fuel reading to be put onto the slider
        self.slider_info_image = self.slider_font.render(str(self.slider_fuel_reading),True,"black")

        #this is to put the fuel reading onto the center of the slider image and this is the location of where to put it
        self.slider_info_rect = self.slider_info_image.get_rect(center=(self.slider_x_location,self.height/2))

        #this makes a circle which acts as the circle on the slider
        pygame.draw.circle(self.screen,"red",(self.slider_x_location,self.height/2),self.height/7.2,100)

        #this puts the fuel reading onto the circle
        self.screen.blit(self.slider_info_image,self.slider_info_rect)

        #this is the cost amount
        self.fuel_cost_amount=self.fuel_consumption*self.slider_fuel_reading

        #this checks if you have enough money to buy the fuel: if you do the cost will be black and if not red
        if self.fuel_cost_amount<=self.money_counter:
            self.cost_image = self.cost_font.render(f"cost: {self.fuel_cost_amount}",True,"black")
        else:
            self.cost_image = self.cost_font.render(f"cost: {self.fuel_cost_amount}",True,"red")

        #this is where the cost will be put on screen
        self.cost_rect = self.cost_image.get_rect(center=(self.width/4,self.height*3/4))

        #this puts the cost on screen
        self.screen.blit(self.cost_image,self.cost_rect)

        #this checks if you clicked on the slider
        if self.mouse_clicked_on_slider==True:

            #this checks if you are holding down the button
            if pygame.mouse.get_pressed()[0]==True:

                #this checks if your mouse is within the slider in the x direction
                if self.mousewhere[0]>=(self.width/10) and self.mousewhere[0]<=(self.width*9/10):

                    #this moves the slider to your mouse location
                    self.slider_x_location=pygame.mouse.get_pos()[0]

                    #this gets the value of the fuel in the new place of the slider
                    self.slider_fuel_reading=int(abs(round(((self.width / 10) - self.mousewhere[0]) / (self.width * 8 / 10) * (self.fuel_max - self.fuel_counter),2)))

            #this means you are no longer holding down the button
            else:
                self.mouse_clicked_on_slider=False



    #this takes in the users backpack and the price of ores and puts them onto the garage on different lines
    def selling_inventory(self,text):
        for i, l in enumerate(text.splitlines()):
            self.screen.blit(self.sell_font.render(l, True, "black"),self.sell_font.render(l, True, "black").get_rect(topleft=(0,self.back_image.get_size()[1]+self.sell_or_buy_image.get_size()[1]+(self.sell_font.render("g", True, "black").get_size()[1] * i))))

    # this function displays the garage
    def parts(self):

        #this fills the screen white
        self.screen.fill("white")

        #this is the back button
        self.screen.blit(self.back_image, (0, 0))

        #this is a title which shows that the left side of the garage is for selling ores and the right side is for buying items
        self.screen.blit(self.sell_or_buy_image, (0,self.back_image.get_size()[1]))

        #this is a temporary variable
        self.has_item=""

        #this gets the self.backpack and turns it into a single string with "\n" inside of it for new lines and puts the ore and the sell price
        for a,i in enumerate(self.backpack):
            if i!=0:
                self.has_item=self.has_item+f"{self.ore_name_list[a]}: {i} , worth: {self.ore_start_price_list[a]*self.ore_price_increase*self.backpack[a]}\n"

        #this puts the temporary variable into the self.selling_inventory function to be put on screen
        self.selling_inventory(self.has_item)

        #this puts the sell all button on the screen
        self.screen.blit(self.sell_all_image,self.sell_all_image.get_rect(center=(self.width/4.44444444,self.height*8/9)))

        #this puts all the items on screen
        self.item_group.draw(self.screen)

        #this loops for the 4 items
        for i in range(4):

            #this is the image of a counter of how many of each item the user has
            item_image = self.item_counter_font.render(str(self.item_backpack[i]),True,"black")

            #this is the location of the counter of how many of each item the user has
            item_rect = item_image.get_rect(topright=(self.width-self.bomb_item_image.get_size()[0],self.sell_or_buy_image.get_size()[1]+self.back_image.get_size()[1]+(i*(self.bomb_item_image.get_size()[1]+1))))

            #this puts the counter on the screen
            self.screen.blit(item_image,item_rect)


    #this displays the how to play screen
    def how_to_play(self):

        #this is the how to play
        if self.which_how_to_screen==0:

            #this puts the how to play image on the screen
            self.screen.blit(self.how_to_play_image,(0,0))

        #this is the how to use the upgrade shop screen
        elif self.which_how_to_screen==1:

            # this puts the how to use the upgrade shop image on the screen
            self.screen.blit(self.how_to_use_the_upgrade_shop_image,(0,0))

        # this is the how to use the fuel shop screen
        elif self.which_how_to_screen==2:

            # this puts the how to use the fuel shop image on the screen
            self.screen.blit(self.how_to_use_the_fuel_shop_image,(0,0))

        #this is the how to use the garage screen
        elif self.which_how_to_screen==3:

            # this puts the how to use the garage image on the screen
            self.screen.blit(self.how_to_use_the_garage_image,(0,0))

    #this is the winning screen
    def winning_screen(self):

        #this puts the winning message on the screen
        self.screen.blit(self.winning_screen_image,(0,0))


    #this function saves some information in the chosen save file
    def save_game(self):

        #this goes through the name of each variable i want to save in the notepad
        for a, i in enumerate(self.variable_data_name_order):

            #this checks if the variable is not empty
            if i!="":

                #this updates the self.variable_data_order with the current values
                exec(f'self.variable_data_order[{a}]={i}')

            #this is if the variable is empty
            else:

                #this sets the save name as empty
                self.new_game_save_name=""

        #this opens the notepad and clears the current contents
        with open(f"file_{self.which_save_file}.txt", "w") as f:

            #this goes to every item that i want to save and puts it into the notepad
            for i in self.variable_data_order:
                f.write(str(i))
                f.write("\n")
                f.write("\n")


    #this is used for continuing a save file
    def continuing(self,load_variables):

        #this checks if the code needs to load the variables from the notepads
        if load_variables:

            #this code gets the data using the save file data and updated the self.variable_data_order list
            exec(f'self.variable_data_order[0] = self.file_{self.which_save_file}_data[0].strip()')
            for a in range(1,len(self.variable_data_order)):
                if (2*a) in [0,2,4,14,18,26]:
                    exec(f'self.variable_data_order[{a}]=eval(self.file_{self.which_save_file}_data[{(2*a)}])')
                else:
                    exec(f'self.variable_data_order[{a}]=float(self.file_{self.which_save_file}_data[{(2*a)}].strip())')

        #this makes all the values in the variables equal to the value inside the self.variable_data_order list
        for a,i in enumerate(self.variable_data_name_order):
            if i!="":
                exec(f'{i}=self.variable_data_order[{a}]')

        #this removes all the tiles in the self.tile_group
        for tile in self.tile_group:
            tile.kill()

        #this code adds the tiles using the self.ore_list
        for y,a in enumerate(self.tile_list):
            for x,b in zip(range(-11,25),a):
                if b!=-1:
                    self.tile_group.add(Tiles(self.ore_list[b], x * self.middle_grass_image.get_size()[0],(self.top_grass_image.get_size()[1] * y) + self.height * 3 / 4))

        #this removes all the rock images
        for rock in self.rock_group:
            rock.kill()

        #this adds rocks to the self.rock_group , this uses rock images that are 7 tiles long so this code only runs for every 7 layers
        for rock_layer_number in range(0,200,7):
            self.rock_group.add(Tiles(self.lots_of_rock_images, -17 * self.rock_image.get_size()[0], (self.height * 3 / 4)+(self.middle_grass_image.get_size()[0]*rock_layer_number)))
            self.rock_group.add(Tiles(self.lots_of_rock_images, 25* self.rock_image.get_size()[0],(self.height * 3 / 4) + (self.middle_grass_image.get_size()[0] * rock_layer_number)))

        #this removes all the building images
        for building in self.building_group:
            building.kill()

        #this adds the shop image to the self.building_group
        self.building_group.add(Buildings(self.shop_image, -10* self.rock_image.get_size()[0],(self.height*3/4)-self.shop_image.get_size()[1]))

        #this adds the fuel shop image to the self.building_group
        self.building_group.add(Buildings(self.fuel_store, 5 * self.rock_image.get_size()[0],(self.height*3/4)-self.fuel_store.get_size()[1]))

        #this adds the garage image to the self.building_group
        self.building_group.add(Buildings(self.garage , 15 * self.rock_image.get_size()[0],(self.height * 3 / 4) - self.garage.get_size()[1]))

        #this moves the tiles , buildings and rock images to where they should be.
        for tile in self.tile_group:
            tile.rect.y += self.game_y_offset
            tile.rect.x += self.game_x_offset*5
        for building in self.building_group:
            building.rect.y += self.game_y_offset
            building.rect.x += self.game_x_offset*5
        for rock in self.rock_group:
            rock.rect.y += self.game_y_offset
            rock.rect.x += self.game_x_offset*5

        #this updates the shop descriptions
        self.update_shop_descriptions()

        #this updates the shop item effects
        self.shop_item_bought()

    #this code is a function which will run whenever it is called and i have made this function so that after initialising the game this code will start the game up
    def run(self):

        #this code loops while the game is running
        #this code loops while the game is running
        while self.running:

            #this checks the pygame event handler if there are any events , such as keyboard or mouse inputs
            for event in pygame.event.get():

                #this will check if the user has done something to try and close the game
                if event.type == pygame.QUIT:

                    #this will make running false and so my code will exit out of the loop
                    self.running = False

                #this checks if the user presses down any key
                elif event.type == pygame.KEYDOWN:

                    #this checks if the user pressed the escape button
                    if event.key==pygame.K_ESCAPE:

                        #this checks if the user is in the save file selection menu or are choosing their save file name
                        if self.phase_on==1:

                            #this checks if the user is not choosing their save file name
                            if self.saving_screen==False:

                                #this makes the user go back if they pressed escape
                                self.deleting_screen = False
                                self.phase_on=0

                            # this checks if the user is choosing their save file name
                            else:

                                #this puts the user back in the save file selection menu
                                self.saving_screen=False

                        #this checks if the user is in the main game
                        elif self.phase_on==2:

                            #this puts the user back into the save file selection menu
                            self.saving_screen=False
                            self.load_starting_files()
                            self.phase_on=1
                            self.how_to_screen_seen = [False,False,False]
                            self.variable_data_order=copy.deepcopy(self.initial_variable_data_order)
                            self.continuing(False)

                        #this checks if the user is in a building
                        elif self.phase_on in [3,4,5]:

                            #this code puts the user back in the main game
                            self.phase_on=2

                        #this checks if the user is looking at the how to play screen
                        elif self.phase_on==6:

                            #this checks if the user is looking at the how to play screen
                            if self.which_how_to_screen==0:

                                #this puts the user back into the save file selection screen
                                self.phase_on=1

                            #this happens for every other how to screen
                            else:

                                #this puts the user back to the main game
                                self.phase_on=2

                        #this checks if the user is in the winning screen
                        elif self.phase_on==7:

                            #this puts the user to the main menu
                            self.saving_screen=False
                            self.load_starting_files()
                            self.phase_on=0
                            self.how_to_screen_seen = [False,False,False]
                            self.variable_data_order=copy.deepcopy(self.initial_variable_data_order)
                            self.continuing(False)

                    #this checks if the user is in the save file selection screen and is choosing their save file name
                    if self.phase_on==1 and self.saving_screen==True:

                        #this gets a string of which key was pressed
                        self.which_key_pressed = pygame.key.name(event.key)

                        #this code checks if capslock is on
                        self.capslock = (True if pygame.key.get_mods() & pygame.KMOD_CAPS else False)

                        #this code checks if shift and or ctrl is being held down
                        self.keys=pygame.key.get_pressed()
                        self.shift_is_on = (True if (self.keys[pygame.K_RSHIFT] or self.keys[pygame.K_LSHIFT]) else False)
                        self.ctrl_is_on = (True if (self.keys[pygame.K_RCTRL] or self.keys[pygame.K_LCTRL])else False)

                        #this checks the length of the string of which letter was pressed to check if its a single letter and not "space" or "return" etc.
                        if len(self.which_key_pressed)==1:

                            #this checks if the users save file name is not over 16
                            if len(self.new_game_save_name)<=15:

                                #this checks if either capslock or shift is on to add capitalisation and this checks if both shift and capslock are on which would cancel out and make the text uncapitilised
                                if self.capslock ^ self.shift_is_on:

                                    #this checks if shift is being pressed and a number is pressed and this is to stop the user from trying to add special characters using shift and a number button
                                    if (self.shift_is_on and (self.which_key_pressed not in "0123456789")) or self.shift_is_on==False:

                                        #this makes the text capitilised
                                        self.new_game_save_name+=self.which_key_pressed.upper()

                                #this is if both capslock and shift is off or on
                                else:
                                    self.new_game_save_name+=self.which_key_pressed.lower()

                        #this is if a button is pressed which is not a single character to be added
                        else:

                            #this checks if the user pressed space
                            if self.which_key_pressed=="space":

                                #this checks if the users save file name is not over 16
                                if len(self.new_game_save_name)<=15:

                                    #this adds a space
                                    self.new_game_save_name+=" "

                            #tihs checks if the user pressed the backspace button
                            elif self.which_key_pressed=="backspace":

                                #this checks if ctrl is being held down
                                if self.ctrl_is_on:

                                    #if the user is holding down ctrl and pressed backspace this code removes an entire word from the end of the save file name
                                    self.new_game_save_name = " ".join(self.new_game_save_name.split()[:len((self.new_game_save_name).split())-1])

                                #this checks if ctrl is not being held down
                                else:

                                    #this removes the last character added
                                    self.new_game_save_name = self.new_game_save_name[:len(self.new_game_save_name) - 1]

                            #this checks if the user pressed enter and then brings the user to the how to play screen
                            elif self.which_key_pressed=="return":
                                self.save_game()
                                self.phase_on=6
                                self.which_how_to_screen=0

                    #this checks if the key pressed is the enter key
                    elif pygame.key.name(event.key)=="return":

                        #this checks if the user is in the fuel shop
                        if self.phase_on==4:

                            #this buys the current amount of fuel and decreases the money by the cost and increases the fuel by the amount bought and then brings the user back to the main game
                            if float(self.money_counter) >= float(self.fuel_cost_amount):
                                self.money_counter -= float(self.fuel_cost_amount)
                                self.fuel_counter += float(self.slider_fuel_reading)
                                self.phase_on = 2

                        # this checks if the user is in the how to play screen
                        elif self.phase_on == 6:

                            # this checks which of the 4 how to screen's the user is on and changes the phase_on accordingly
                            for number in range(4):
                                if self.which_how_to_screen == number:
                                    self.phase_on = number + 2
                                    if number!=0:
                                        self.how_to_screen_seen[number-1]=True

                        # this checks if the user is in the winning screen
                        elif self.phase_on == 7:

                            # this puts the user to the main menu
                            self.saving_screen = False
                            self.load_starting_files()
                            self.phase_on = 0
                            self.how_to_screen_seen = [False, False, False]
                            self.variable_data_order = copy.deepcopy(self.initial_variable_data_order)
                            self.continuing(False)

                    #this checks if the player is in the main game
                    if self.phase_on==2:

                        #this checks if the user pressed the b key
                        if event.key == pygame.K_b:

                            #this checks if the user has a bomb item
                            if self.item_backpack[0]>0:

                                #this removes 1 bomb item from the user
                                self.item_backpack[0]-=1

                                # this code damages the tiles around the user
                                for y_value in range(3):
                                    for x_value in range(3):
                                        if (self.y_value_on-y_value)>=0 and (self.y_value_on-y_value)<=301:
                                            if (self.x_value_on-1+x_value)>=0 and (self.x_value_on-1+x_value)<=35:
                                                if (self.tile_list[self.y_value_on-y_value][self.x_value_on-1+x_value])!=-1:
                                                    self.tile_health_list[self.y_value_on-y_value][self.x_value_on-1+x_value] -= self.mining_speed
                                                    if (self.tile_health_list[self.y_value_on - y_value][self.x_value_on - 1 + x_value]) <=0:
                                                        counter=0
                                                        list_thing=("\n".join(map(str, [value for list in self.tile_health_list for value in list]))).splitlines()
                                                        for a,b in enumerate(list_thing):
                                                            if a<((self.x_value_on-1+x_value) + ((self.y_value_on-y_value) * 36)):
                                                                if int(b)<=0:
                                                                    counter+=1
                                                            else:
                                                                break
                                                        self.backpack[self.tile_list[self.y_value_on-y_value][self.x_value_on-1+x_value]]+=1
                                                        self.weight_counter+=self.ore_weight_list[self.tile_list[self.y_value_on-y_value][self.x_value_on-1+x_value]]
                                                        self.tile_list[self.y_value_on - y_value][self.x_value_on - 1 + x_value] = -1
                                                        self.tile_group.sprites()[(self.x_value_on-1+x_value) + ((self.y_value_on-y_value) * 36) - (counter)].kill()

                        # this checks if the user pressed the t key
                        elif event.key == pygame.K_t:

                            # this checks if the user has a teleport item
                            if self.item_backpack[1]>0:

                                # this removes 1 teleport item from the user
                                self.item_backpack[1]-=1

                                #this resets the offset values
                                self.game_x_offset=0
                                self.game_y_offset=0
                                self.x_value_on=0
                                self.y_value_on=0

                                # this removes all the tiles in the self.tile_group
                                for tile in self.tile_group:
                                    tile.kill()

                                #this code adds the tiles using the self.ore_list
                                for y, a in enumerate(self.tile_list):
                                    for x, b in zip(range(-11, 25), a):
                                        if b != -1:
                                            self.tile_group.add(
                                                Tiles(self.ore_list[b], x * self.middle_grass_image.get_size()[0],
                                                      (self.top_grass_image.get_size()[1] * y) + self.height * 3 / 4))

                                # this removes all the rock images
                                for rock in self.rock_group:
                                    rock.kill()

                                # this adds rocks to the self.rock_group , this uses rock images that are 7 tiles long so this code only runs for every 7 layers
                                for rock_layer_number in range(0, 200, 7):
                                    self.rock_group.add(Tiles(self.lots_of_rock_images, -17 * self.rock_image.get_size()[0],(self.height * 3 / 4) + (self.middle_grass_image.get_size()[0] * rock_layer_number)))
                                    self.rock_group.add(Tiles(self.lots_of_rock_images, 25 * self.rock_image.get_size()[0],(self.height * 3 / 4) + (self.middle_grass_image.get_size()[0] * rock_layer_number)))

                                # this removes all the building images
                                for building in self.building_group:
                                    building.kill()

                                # this adds the shop image to the self.building_group
                                self.building_group.add(Buildings(self.shop_image, -10 * self.rock_image.get_size()[0],
                                                                  (self.height * 3 / 4) - self.shop_image.get_size()[1]))

                                # this adds the fuel shop image to the self.building_group
                                self.building_group.add(Buildings(self.fuel_store, 5 * self.rock_image.get_size()[0],
                                                                  (self.height * 3 / 4) - self.fuel_store.get_size()[1]))

                                # this adds the garage image to the self.building_group
                                self.building_group.add(Buildings(self.garage, 15 * self.rock_image.get_size()[0],
                                                                  (self.height * 3 / 4) - self.garage.get_size()[1]))

                        # this checks if the user pressed the u key
                        elif event.key == pygame.K_u:

                            # this checks if the user has a double up item
                            if self.item_backpack[2]>0:

                                # this checks if the double up item is not currently in use
                                if self.doubled==False:

                                    # this removes 1 double up item from the user
                                    self.item_backpack[2]-=1
                                    self.doubled=True

                        # this checks if the user pressed the g key
                        elif event.key == pygame.K_g:

                            # this checks if the user has a god mode item
                            if self.item_backpack[3]>0:

                                #this checks if the gode mode item is not currently in use
                                if self.god_multiplier==1:

                                    # this removes 1 god mode item from the user
                                    self.item_backpack[3]-=1
                                    self.god_multiplier=2
                                    self.god_item_timer = self.pygame_time




                #this checks if the user pressed any mouse buttons (primary click/secondary click/middle click/middle scroll)
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    #this checks if the mouse button was the primary click
                    if event.button==1:

                        #this gets the x and y value of the players cursor
                        self.mousewhere=pygame.mouse.get_pos()

                        #this checks if the user is in the save file select menu and are not choosing a save file name
                        if self.phase_on==1 and self.saving_screen==False:

                            #this checks if the user pressed the back button
                            if self.mousewhere[0]<=self.back_image.get_size()[0] and self.mousewhere[1]<=self.back_image.get_size()[1]:
                                self.phase_on=0
                                self.deleting_screen=False

                            #this checks if the user pressed the delete button
                            if self.mousewhere[0]>=(self.width-self.delete_image.get_size()[0]) and self.mousewhere[1]<=self.delete_image.get_size()[1]:
                                self.deleting_screen = not self.deleting_screen

                            #this checks if the user is not in deleting mode
                            if self.deleting_screen==False:

                                #this checks if the user clicked each save file and then if the user clicked a save file with data or not and if it does have data the code carries on into thegame but if it doesnt then it puts the user on the save file name menu where the user creates the name of the file
                                for i in range(1,4):
                                    exec(f'if self.mousewhere[1]>=self.height*{i}/4 and self.mousewhere[1]<self.height*(1+{i})/4:'
                                         f'   \n\tself.which_save_file={i}\n\tif self.file_{i}_data==[]:'
                                         f'      \n\t\tself.saving_screen=True'
                                         f'   \n\telse:'
                                         f'      \n\t\tself.continuing(True)'
                                         f'      \n\t\tself.which_how_to_screen=0'
                                         f'      \n\t\tself.phase_on=6')

                            # this checks if the user is in deleting mode
                            else:

                                #this checks if the user is trying to delete each save file and clears the save file if they are
                                for i in range(1,4):
                                    exec(f'if self.mousewhere[1]>=self.height*{i}/4 and self.mousewhere[1]<self.height*(1+{i})/4:'
                                         f'   \n\tself.file_{i}_data=[]'
                                         f'   \n\topen("file_{i}.txt","w").close()'
                                         f'   \n\tself.variable_data_order=copy.deepcopy(self.initial_variable_data_order)'
                                         f'   \n\tself.load_starting_files()'
                                         f'   \n\tself.continuing(False)')


                        #for each of the buildings if the user pressed the back button this code will put them back into the main game where they left off
                        if self.phase_on in [3,4,5]:
                            if self.mousewhere[0] <= self.back_image.get_size()[0] and self.mousewhere[1] <= self.back_image.get_size()[1]:
                                self.phase_on = 2

                        #this only runs if the user is in the upgrade shop
                        if self.phase_on==3:

                            #this goes through each upgrade buy button
                            for a,i in enumerate(self.shop_buy_group):

                                #this checks if the user clicked on the buy button
                                if i.rect.collidepoint(pygame.mouse.get_pos()):

                                    #this checks if the user does not have the maximum allowed upgrades for that upgrade
                                    if self.shop_item_bought_list[a]!=self.shop_item_max_buy_list[a]:

                                        #this checks if the user has enough money to buy the upgrade
                                        if self.money_counter-(self.shop_item_price_list[a]*(self.shop_item_bought_list[a]+1)*self.shop_price_reduction_multiplier)>=0:

                                            #this code updates the effect of buying the item as well as reducing the players money counter and increasing the amount of upgrades the user has for this particular upgrade and changing the price shown in the shop (to buy the next upgrade)
                                            self.money_counter-=(self.shop_item_price_list[a]*(self.shop_item_bought_list[a]+1)*self.shop_price_reduction_multiplier)
                                            self.shop_item_bought_list[a]+=1
                                            self.shop_item_bought()
                                            self.update_shop_descriptions()

                        # this only runs if the user is in the fuel shop
                        elif self.phase_on==4:

                            #this checks if the user clicked on the fuel shop buy button
                            if pygame.sprite.spritecollide(self.cursor_sprite, self.fuel_group, False,pygame.sprite.collide_mask):

                                # this buys the current amount of fuel and decreases the money by the cost and increases the fuel by the amount bought and then brings the user back to the main game
                                if float(self.money_counter) >= float(self.fuel_cost_amount):
                                    self.money_counter -= float(self.fuel_cost_amount)
                                    self.fuel_counter += float(self.slider_fuel_reading)
                                    self.phase_on = 2

                            #this checks if the user clicked on the slider bar and if the user did this tells my code that the slider bar was clicked
                            if self.mousewhere[1]>=((self.height/2)-self.slider_bar.get_size()[1]/2) and self.mousewhere[1]<=((self.height/2)+self.slider_bar.get_size()[1]/2):
                                if self.mousewhere[0]>=(self.width/10) and self.mousewhere[0]<=(self.width*9/10):
                                    self.mouse_clicked_on_slider=True

                        # this only runs if the user is in the garage
                        elif self.phase_on==5:

                            #this checks if the user presses the sell all button
                            if self.mousewhere[0]>=((self.width/4.44444444)-(self.sell_all_image.get_size()[0]/2)) and self.mousewhere[0]<=((self.width/4.44444444)+(self.sell_all_image.get_size()[0]/2)):
                                if self.mousewhere[1]>=((self.height*8/9)-(self.sell_all_image.get_size()[1]/2)) and self.mousewhere[1]<=((self.height*8/9)+(self.sell_all_image.get_size()[1]/2)):

                                    #this goes through each item in the users backpack
                                    for a,i in enumerate(self.backpack):

                                        #this increases the users money buy how much of each ore the user has and the price of the ore
                                        self.money_counter+=(i*self.ore_start_price_list[a]*self.ore_price_increase)

                                    #ths resets the users backpack
                                    self.backpack=[0,0,0,0,0,0,0]

                                    #this resets the users weight
                                    self.weight_counter=0

                            #this code goes through each item
                            for a, i in enumerate(self.item_group):

                                #this code checks if the user clicked on any item
                                if i.rect.collidepoint(pygame.mouse.get_pos()):

                                    #this code checks if the user has enough ores to buy the item
                                    if(all(i>=j for i,j in zip(self.backpack,self.item_price_list[a]))):

                                        #this adds the item to the users item backpack
                                        self.item_backpack[a]+=1

                                        #this code removes the ores from the users backpack
                                        self.backpack = [self.backpack[i]-j for i,j in enumerate(self.item_price_list[a])]

            #this maintains my game at 60 fps
            self.clock.tick(60)  # 60 fps

            #this records the run time in milliseconds
            self.pygame_time = pygame.time.get_ticks()

            #this displays the different screens with self.phase_on being the value for which screen the user is currently on and self.phase[]() running the function
            self.phase[self.phase_on]()

            #this checks if the player is in the main game or a building
            if self.phase_on in [2,3,4,5]:

                # this puts the user information , the money , fuel , etc. , on the screen
                self.stats_put_on_screen(f"money: £{self.money_counter:.2f}\nfuel: {self.fuel_counter:.2f}/{self.fuel_max}\nweight: {self.weight_counter}/{self.weight_max}")

                # this saves the game
                self.save_game()

            #this updates the screen so the user can see what has changed in the code
            pygame.display.update()

            #this holds the run time for the previous loop
            self.previous_pygame_time = self.pygame_time



#this code checks if the code was run
if __name__ == "__main__":

    #this code starts the init function in my game class
    game = Game()
    #this code starts the run function in my game class
    game.run()