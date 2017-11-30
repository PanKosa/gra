import pygame
import time 
 
from constants import *
from buttons import *
from spritesheet_functions import SpriteSheet

def screen_level_massage(string, level = 0):
    
    from  game_intro import game_intro_loop
    
    pygame.init()
        
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption(game_name)
    clock = pygame.time.Clock()
    
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    intro = 1
    images = [
        "animations/level_bcg/level1.png",
        "animations/level_bcg/level2.png",
        "animations/level_bcg/winner.png"
        ]
    
    sprite_sheet = SpriteSheet(images[level])
    image = sprite_sheet.sprite_sheet
    background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while intro<1000:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.blit(background, dest=(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))    
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects(string, largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(1000)
        intro+=1
    time.sleep(2)    
    pygame.mixer.fadeout(250)
    game_intro_loop()
    
def died():
    pygame.mixer.fadeout(250)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/dead.wav"))
    screen_level_massage("You've died", level = 0)
    
def winner():
    pygame.mixer.fadeout(250)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/bravo.wav"))
    screen_level_massage("Winner", level = 2)
    
def level_name(number):
    
    pygame.init()
    
    images = [
        "animations/level_bcg/level1.png",
        "animations/level_bcg/level2.png"
        ]
        
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption(game_name)
    clock = pygame.time.Clock()
    
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    intro = 1

    sprite_sheet = SpriteSheet(images[number - 1])
    image = sprite_sheet.sprite_sheet
    background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while intro<1000:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.blit(background, dest=(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))        
        
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Level "+str(number), largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(1000)
        intro+=1