import pygame
 
from  buttons import *
from campaign_sp import *
from campaign_mp import *
from constants import*
    
    
class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30, font_color=WHITE, pos_x = 0, pos_y=0):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
        self.is_selected = False
 
    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
        
################################################################################################
        
class GameMenu():
    def __init__(self, screen, items, bg_color=WHITE, font=None, font_size=60,font_color=GREEN):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.chosen = None
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.items = []
        
        poz_x_all = (400, 400, 400, 400)
        poz_y_all = (270, 330, 390, 450)
        it = 0
        
        for index, item in enumerate(items):
            if it == 0:
                menu_item = MenuItem(item, font, font_size, RED)
                
            else:
                menu_item = MenuItem(item, font, font_size, font_color)
            
            pos_x = poz_x_all[it]
            pos_y = poz_y_all[it]
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            
            it += 1
 
        self.cur_item = 0
        
 
 
    def set_item_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(GREEN)
 

        # Find the chosen item
        if key == pygame.K_UP and self.cur_item > 0:
            self.cur_item -= 1
        elif key == pygame.K_UP and self.cur_item == 0:
            self.cur_item = len(self.items) - 1
        elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
            self.cur_item += 1
        elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
            self.cur_item = 0
        if key == pygame.K_RETURN :
            self.chosen = self.cur_item
 
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(RED)

 
    def run(self):
        mainloop = True
        
        sprite_sheet = SpriteSheet("animations/menu/menu.png")
        image = sprite_sheet.sprite_sheet
        background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        hero = []
        
        n = 10
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/player/idle2/"+str(i+1)+".png")
            image = sprite_sheet.get_image(135, 50, 260, 470)
            image = pygame.transform.rotozoom(image, 0, 0.8)
            image.set_colorkey((34,177,76))
            hero.append(image)
            #image = pygame.transform.flip(image, True, False)

        
        song = "sounds/menu_music.wav"
        song = pygame.mixer.Sound(song)
        song.play(-1)
        
        iter = -1
        while mainloop:
            self.clock.tick(60)
            
            iter += 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound("sounds/click.wav"))
                    self.set_item_selection(event.key)
                    
            self.screen.blit(background, dest=(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))
            
            self.screen.blit(hero[(iter//5)%len(hero)], dest=(150,180,200, 200))
            
            for item in self.items:
                self.screen.blit(item.label, item.position)
                
            largeText = pygame.font.SysFont("comicsansms",140)
            TextSurf, TextRect = text_objects(game_name, largeText)
            TextRect.center = (400,120)
            self.screen.blit(TextSurf, TextRect)
 
            pygame.display.flip()
            
            if self.chosen == 0:
                pygame.mixer.fadeout(500)
                #campaign_sp()
                game_character_loop()
            elif self.chosen == 1:
                pygame.mixer.fadeout(500)
                campaign_mp()
            elif self.chosen == 2:
                pygame.mixer.fadeout(500)
                game_options_loop()
            elif self.chosen == 3:
                pygame.mixer.fadeout(500)
                quitgame()

##################################################################

class GameOptions():
    def __init__(self, screen, items, bg_color=WHITE, font=None, font_size=90,font_color=GREEN):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.chosen = None
        self.exit = False
        self.options = options
        self.opt_cur = list(items)
        
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = []
        it = 0
        
        poz_x_all = (530, 550, 550, 550)
        poz_y_all = (170, 270, 370, 470)
        
        for index, item in enumerate(items):
            if it == 0:
                menu_item = MenuItem(str((self.options[it])[item]), font, font_size, RED)
            else:
                menu_item = MenuItem(str((self.options[it])[item]), font, font_size, font_color)

            pos_x = poz_x_all[it]
            pos_y = poz_y_all[it] 
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            it += 1
 
        self.cur_item = 0
        
 
 
    def set_item_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(GREEN)
 
        # Find the chosen item
        if key == pygame.K_UP and self.cur_item > 0:
            self.cur_item -= 1
        elif key == pygame.K_UP and self.cur_item == 0:
            self.cur_item = len(self.items) - 1
        elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
            self.cur_item += 1
        elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
            self.cur_item = 0
        elif key == pygame.K_LEFT:
            self.opt_cur[self.cur_item] = max(self.opt_cur[self.cur_item] - 1, 0)
            self.items[self.cur_item].text = str((self.options[self.cur_item])[self.opt_cur[self.cur_item]])
        elif key == pygame.K_RIGHT:
            self.opt_cur[self.cur_item] = min(self.opt_cur[self.cur_item] + 1, len(self.options[self.cur_item]) - 1)
            self.items[self.cur_item].text = str((self.options[self.cur_item])[self.opt_cur[self.cur_item]])
        elif key == pygame.K_RETURN :
            self.chosen = self.cur_item
            
        if key == pygame.K_ESCAPE:
            pygame.mixer.fadeout(500)
            with open("options.txt", "w") as myfile:
                for i in self.opt_cur:
                    myfile.write(str(i) + "\n")
            myfile.close()
            game_intro_loop()
                
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(RED)

 
    def run(self):
        song = "sounds/menu_music.wav"
        song = pygame.mixer.Sound(song)
        song.play(-1)
        
        mainloop = True
        width, height = 50, 50 
        sprite_sheet = SpriteSheet("animations/buttons/right.png")
        image = sprite_sheet.sprite_sheet
        image.set_colorkey(BLACK)
        image_plus = pygame.transform.scale(image, (width, height))
        
        sprite_sheet = SpriteSheet("animations/buttons/left.png")
        image = sprite_sheet.sprite_sheet
        image.set_colorkey(BLACK)
        image_minus = pygame.transform.scale(image, (width, height))
        
        sprite_sheet = SpriteSheet("animations/menu/opt.png")
        image = sprite_sheet.sprite_sheet
        background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        while mainloop:
            self.clock.tick(60)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound("sounds/click.wav"))
                    self.set_item_selection(event.key)
                    
            self.screen.blit(background, dest=(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))
            
            for item in self.items:
                self.screen.blit(item.label, item.position)
            
            largeText = pygame.font.SysFont("comicsansms",120)
            TextSurf, TextRect = text_objects("Settings", largeText)
            TextRect.center = (400,80)
            self.screen.blit(TextSurf, TextRect)


            opt_names = ["Max health", "Damage taken","Health restoration","Projectile speed"]
            it = 0
            poz_x = (50, 50, 50, 50)
            poz_y = (200, 300, 400, 500)

            for name in opt_names:
                largeText = pygame.font.SysFont("comicsansms",60)
                TextSurf, TextRect = text_objects(name, largeText)
                TextRect.left = poz_x[it]
                TextRect.centery  = poz_y[it]
                self.screen.blit(TextSurf, TextRect)
                it += 1
                
            poz_x = (450, 450, 450, 450)
            poz_y = (170, 270, 370, 470)
            it = 0
            for it in range(len(poz_x)):
                self.screen.blit(image_minus, (poz_x[it], poz_y[it]))
                
                
            poz_x = (670, 670, 670, 670)
            poz_y = (170, 270, 370, 470)
            it = 0
            for it in range(len(poz_x)):
                self.screen.blit(image_plus, (poz_x[it], poz_y[it]))    
                
            largeText = pygame.font.SysFont("comicsansms",40)
            TextSurf, TextRect = text_objects("To exit settings press ESC", largeText)
            TextRect.center = (400,575)
            self.screen.blit(TextSurf, TextRect)
            
            pygame.display.flip()

##################################################################

class CharacterOptions():
    def __init__(self, screen, bg_color=WHITE, font=None, font_size=90,font_color=GREEN):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.chosen = None
        self.opt_cur = 0
        
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.cur_item = 0
        
 
 
    def set_item_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
 
        # Find the chosen item
        if key == pygame.K_LEFT:
            self.opt_cur= max(self.opt_cur - 1, 0)
        elif key == pygame.K_RIGHT:
            self.opt_cur = min(self.opt_cur + 1, len(colors) - 1)
        elif key == pygame.K_RETURN :
            self.chosen = self.opt_cur
            pygame.mixer.fadeout(500)
            campaign_sp(self.opt_cur)
            
        if key == pygame.K_ESCAPE:
            pygame.mixer.fadeout(500)
            game_intro_loop()
                

 
    def run(self):
        mainloop = True
        width, height = 50, 50 
        images = []
        
        song = "sounds/menu_music.wav"
        song = pygame.mixer.Sound(song)
        song.play(-1)
        
        sprite_sheet = SpriteSheet("animations/player/idle2/1.png")
        image = sprite_sheet.get_image(135, 50, 260, 470)
        image = pygame.transform.rotozoom(image, 0, 0.5)
        image.set_colorkey((34,177,76))
        
        for i in range(len(colors)):
                    image2 = image.copy()
                    if not i == 0:
                        image_pixel = pygame.PixelArray(image2)
                        image_pixel.replace(YELLOW1, colors[i])
                        image_pixel.replace(YELLOW2, colors[i])
                    images.append(image2)
        del image_pixel
        
        sprite_sheet = SpriteSheet("animations/buttons/right.png")
        image = sprite_sheet.sprite_sheet
        image.set_colorkey(BLACK)
        image_plus = pygame.transform.scale(image, (width, height))
        
        sprite_sheet = SpriteSheet("animations/buttons/left.png")
        image = sprite_sheet.sprite_sheet
        image.set_colorkey(BLACK)
        image_minus = pygame.transform.scale(image, (width, height))
        
        sprite_sheet = SpriteSheet("animations/menu/opt.png")
        image = sprite_sheet.sprite_sheet
        background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        while mainloop:
            self.clock.tick(60)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound("sounds/click.wav"))
                    self.set_item_selection(event.key)
                    
            self.screen.blit(background, dest=(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))

            self.screen.blit(images[self.opt_cur], (365, 230)) 
            
            
            largeText = pygame.font.SysFont("comicsansms",120)
            TextSurf, TextRect = text_objects("Choose character", largeText)
            TextRect.center = (400,80)
            self.screen.blit(TextSurf, TextRect)

            self.screen.blit(image_minus, (200, 300))
                
            self.screen.blit(image_plus, (600, 300))    
                
            largeText = pygame.font.SysFont("comicsansms",40)
            TextSurf, TextRect = text_objects("To exit to menu press ESC", largeText)
            TextRect.center = (400,575)
            self.screen.blit(TextSurf, TextRect)
            
            pygame.display.flip()
            


###############################################################

def game_intro_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
 
    menu_items = ('Start Single', 'Start Multi', 'Settings', 'Quit')
 
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()
    quit()
    
def game_options_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    
    # read table
    with open("options.txt", "r") as myfile:
	    x = myfile.readlines()
    myfile.close() 
    for i in range(len(x)):
        x[i] = int((x[i])[0])
    
    menu_items = x
 
    pygame.display.set_caption('Game Options')
    go = GameOptions(screen, menu_items)
    go.run()
    quit()
    
def game_character_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
 
    pygame.display.set_caption('Character Select')
    gm = CharacterOptions(screen)
    gm.run()
    quit()
    
