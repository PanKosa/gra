import pygame
import math
from spritesheet_functions import SpriteSheet
import numpy as np
from constants import *

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)
BLUE =  (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        
class Platform_grass(Platform):
    """ Definition for level 1. """
 
    def __init__(self, length, level = 0):
        """ Create level 1. """
 
        # Call the parent constructor
        Platform.__init__(self)
        
        width  = 128 
        height = 93
        
        
        sprites_names = [
            "animations/green_tiles/platforms/",
            "animations/desert_tiles/platforms/"
            ]
        
        self.image = pygame.Surface([width*(2+length), height])
        sprite_sheet = SpriteSheet(sprites_names[level]+"13.png")
        image = sprite_sheet.get_image(0,0,width,height)
        #image.set_colorkey(WHITE)
        image = pygame.transform.scale(image, (width, height))
        self.image.blit(image, dest=(0,0,width, height))
        
        sprite_sheet = SpriteSheet(sprites_names[level]+"14.png")
        for i in range(length):
            image = sprite_sheet.get_image(0,0,width,height)
            #image.set_colorkey(WHITE)
            image = pygame.transform.scale(image, (width, height))
            self.image.blit(image, dest=((i+1)*width,0,width, height))
            
        sprite_sheet = SpriteSheet(sprites_names[level]+"15.png")
        image = sprite_sheet.get_image(0,0,width,height)
        #image.set_colorkey(WHITE)
        image = pygame.transform.scale(image, (width, height))
        self.image.blit(image, dest=((length+1)*width,0,width, height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
        self.can_fall_through = 1
        
class Platform_grass_ground(Platform):
    """ Definition for level 1. """
 
    def __init__(self, length, level = 0):
        """ Create level 1. """
 
        # Call the parent constructor
        Platform.__init__(self)
        
        width  = 128 
        height = 93
        sprites_names = [
            "animations/green_tiles/platforms/",
            "animations/desert_tiles/platforms/"
            ]
        self.image = pygame.Surface([width*(2+length), height])
        sprite_sheet = SpriteSheet(sprites_names[level]+"1.png")
        image = sprite_sheet.get_image(0,0,width,height)
        #image.set_colorkey(WHITE)
        image = pygame.transform.scale(image, (width, height))
        self.image.blit(image, dest=(0,0,width, height))
        
        sprite_sheet = SpriteSheet(sprites_names[level]+"2.png")
        for i in range(length):
            image = sprite_sheet.get_image(0,0,width,height)
            #image.set_colorkey(WHITE)
            image = pygame.transform.scale(image, (width, height))
            self.image.blit(image, dest=((i+1)*width,0,width, height))
            
        sprite_sheet = SpriteSheet(sprites_names[level]+"3.png")
        image = sprite_sheet.get_image(0,0,width,height)
        #image.set_colorkey(WHITE)
        image = pygame.transform.scale(image, (width, height))
        self.image.blit(image, dest=((length+1)*width,0,width, height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
        self.can_fall_through = 0
        
        
        
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, direction):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        self.bullet_frames = []
        
        ##Load animations
        # walking
        sprite_sheet = SpriteSheet("animations/bullet.png")
        sizeX = 172
        sizeY = 28
        n = 5
        for i in range(n):
            image = sprite_sheet.get_image(i*sizeX/n, 0, sizeX/n, sizeY)
            if direction == 0:
                image = pygame.transform.flip(image, True, False)
            self.bullet_frames.append(image)
 
        # Set the image the player starts with
        self.image = self.bullet_frames[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        
        self.direction = direction
        
        # Play Sounds
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/laser.wav'))
        
 
    def update(self):
        """ Move the bullet. """
        
        self.rect.x -= 7*math.cos(self.direction)
        self.rect.y -= 7*math.sin(self.direction)
        
        pos = self.rect.x + self.rect.y 
        frame = (pos // 30) % len(self.bullet_frames)
        self.image = self.bullet_frames[frame]
        

class Bullet_enemy(pygame.sprite.Sprite):
    """ Definition for level 1. """
 
    def __init__(self, direction,rotate):
        """ Create level 1. """
        #Bullet.__init__(self, direction)
        super().__init__()
        sprite_sheet = SpriteSheet("animations/enemy/kunai/Kunai.png")
        image = sprite_sheet.get_image(0, 0,32,160)
        image = pygame.transform.rotate(image, 90)
        if rotate == True:
            image = pygame.transform.flip(image, True, False)
        self.image = pygame.transform.scale(image, (26, 16))
        
        self.rect = self.image.get_rect()
        
        self.direction = direction
        

    def update(self):
        """ Move the bullet. """
        
        # Options const
        opt_const = get_const()
        speed = get_bullet_speed(opt_const)
        
        self.rect.x -= speed*math.cos(self.direction)
        self.rect.y -= speed*math.sin(self.direction)
        
        
        
class Bullet_rocket(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, direction):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        ##Load animations
        self.movement = []
        list_up   = []
        list_45   = []
        list_135  = []
        list_down = []

        n = 4
        for i in range(n):
            #sprite_sheet = SpriteSheet("animations/enemy/kunai/Kunai.png")
            sprite_sheet = SpriteSheet("animations/player/rocket/"+str(i+1)+".png")
            image_base = sprite_sheet.sprite_sheet
            image = pygame.transform.rotozoom(image_base, 90, 0.1)
            image.set_colorkey(BLACK)
            list_up.append(image)
            image = pygame.transform.rotozoom(image_base, 45, 0.1)
            image.set_colorkey(BLACK)
            list_45.append(image)
            image = pygame.transform.rotozoom(image_base, 135, 0.1)
            image.set_colorkey(BLACK)
            list_135.append(image)
            image = pygame.transform.rotozoom(image_base, 270, 0.1)
            image.set_colorkey(BLACK)
            list_down.append(image)
        self.movement.append(list_up)
        self.movement.append(list_45)
        self.movement.append(list_135)
        self.movement.append(list_down)
        
        # up
        # 45
        # 135
        # down
 
        # Set the image the rocket starts with
        self.image = (self.movement[0])[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        
        #
        self.directions = [90, 45, 135, 270]
        self.direction = direction
        
        pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/rocket.wav'))

        
    def update(self):
        """ Move the bullet. """
        self.rect.x += 7*math.cos(self.directions[self.direction]/360*2*math.pi)
        self.rect.y -= 7*math.sin(self.directions[self.direction]/360*2*math.pi)
        pos = self.rect.x + self.rect.y 
        
        rocket_frames = self.movement[self.direction]
        
        frame = (pos // 30) % len(rocket_frames)
        self.image = rocket_frames[frame]        
  
class Bullet_track(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, player, enemy):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        ##Load animations
        self.movement = []

        n = 3
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/enemy/energy_ball/"+str(i+1)+".png")
            image = sprite_sheet.sprite_sheet
            image = pygame.transform.rotozoom(image, 90, 0.5)
            image.set_colorkey(BLACK)
            self.movement.append(image)

        # Set the image the rocket starts with
        self.image = self.movement[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        
        dx = player.rect.x - enemy.rect.x
        dy = player.rect.y - enemy.rect.y
        norm = math.sqrt(dx*dx + dy*dy)
        if norm <= 0.01:
            norm = 1
        
        self.direction = ( 
            (player.rect.x - enemy.rect.x)/norm,
            (-player.rect.y + enemy.rect.y)/norm
            )

        
    def update(self):
        """ Move the bullet. """
        
        # Options const
        opt_const = get_const()
        speed = get_bullet_speed(opt_const)
        
        self.rect.x += speed*self.direction[0]
        self.rect.y -= speed*self.direction[1]
        pos = self.rect.x + self.rect.y 
        
        frame = (pos // 30) % len(self.movement)
        self.image = self.movement[frame]        
    
  
        
class Enemy(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, typeE = 1):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.movement = []
               
        # List of sprites we can bump against
        self.direction = "L"
        self.status = 0
        self.typeE = typeE
        self.change_x = 0
        self.change_y = 0
        
        self.platforms = None
        
        # moveset 
        # 2 - dead right
        # 3 - dead left
        # 0 - idle rigth
        # 1 - idle left
        # 4 - shot right
        # 5 - shot left
        
        self.status = 2
        
        self.uneasy = 5
        
        self.marked_for_dead = 0 
        self.time_before_dead = 100
        self.dead = 0 # chyba nie poczebne
        self.shot = 0
        
        ##Load animations
        
        # idle

        list_r = []
        list_l = []
        
        n = 10
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/enemy/idle2/"+str(i)+".png")
            image = sprite_sheet.sprite_sheet
            #image = sprite_sheet.get_image(0, 0, 232, 439)
            #image = sprite_sheet.get_image(0, 0, 200, 200)
            im_height = image.get_height()
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image)            
            
        self.movement.append(list_r)
        self.movement.append(list_l)        
        
        #im_width = image.get_width()
        
        # take damage
        
        list_r = []
        list_l = []
        
        n = 10
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/enemy/dead2/"+str(i)+".png")
            image = sprite_sheet.sprite_sheet
            image = pygame.transform.scale(image, (round(image.get_width()/image.get_height()*im_height), im_height))
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image)   
        
        
        self.movement.append(list_r)
        self.movement.append(list_l)
        
        
        #throw

        list_r = []
        list_l = []
        
        n = 10
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/enemy/throw2/"+str(i)+".png")
            image = sprite_sheet.sprite_sheet
            image = pygame.transform.scale(image, (round(image.get_width()/image.get_height()*im_height), im_height))
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image)            
        
            
        self.movement.append(list_r)
        self.movement.append(list_l)
        

        # zmienna time zostala stworzona do obslugi animacji ktore odbywaja sie caly czas w tym samym miejscu
        self.time = 0
        self.direction = "R"
        self.dead_direction = None

        
        self.image = (self.movement[0])[0]
        
        self.rect = self.image.get_rect()    
        
    def update(self):
        """ Move the enemy. """
        
        # moveset 
        # 2 - dead right
        # 3 - dead left
        # 0 - idle rigth
        # 1 - idle left
        # 4 - shot right
        # 5 - shot left
        
        self.time += 1
        
        if self.shot <= 0 and self.rect.left <= SCREEN_WIDTH-10 and self.rect.right >= 10:
            if np.random.poisson(5, 1)>10:
                self.shot = 80
                self.status = 4
            else:
                self.status = 0
        else:
            self.shot -= 1
        
        if self.rect.left >= SCREEN_WIDTH or self.rect.right <= 0:
            self.status = 0
            
        
        if self.time >= 10000:
            self.time = 0
            
        if self.direction == "R":
            self.status = (self.status//2)*2
        else:
            self.status = (self.status//2)*2 + 1
        
        if self.marked_for_dead == 1:
            movement = self.movement[self.dead_direction+2]
            frame = 9 - self.time_before_dead // 10
            self.image = movement[frame]
        else:
            movement = self.movement[self.status]
            frame = (self.time//5) % len(movement)
            self.image = movement[frame]
 
        
class Health_pack(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        sprite_sheet = SpriteSheet("animations/player/health/health.png")
        image = sprite_sheet.sprite_sheet
        image = pygame.transform.rotozoom(image, 0, 0.2)
        image.set_colorkey((34,177,76))


        # Set the image the rocket starts with
        self.image = image
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        
class Decoration(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, level = 1, number = 0):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        if level == 1:
            deco = [
                "animations/green_tiles/object/Bush1.png",      # 0
                "animations/green_tiles/object/Bush2.png",      # 1
                "animations/green_tiles/object/Bush3.png",      # 2
                "animations/green_tiles/object/Bush4.png",      # 3
                "animations/green_tiles/object/Crate.png",      # 4
                "animations/green_tiles/object/Mushroom_1.png", # 5
                "animations/green_tiles/object/Mushroom_2.png", # 6
                "animations/green_tiles/object/Sign_1.png",     # 7
                "animations/green_tiles/object/Sign_2.png",     # 8
                "animations/green_tiles/object/Stone.png",      # 9
                "animations/green_tiles/object/Tree1.png",      # 10
                "animations/green_tiles/object/Tree2.png",      # 11
                "animations/green_tiles/object/Tree3.png"       # 12
                ]
        else:
            deco = [
                "animations/desert_tiles/object/Bush1.png",      # 0
                "animations/desert_tiles/object/Bush2.png",      # 1
                "animations/desert_tiles/object/Cactus1.png",    # 2
                "animations/desert_tiles/object/Cactus2.png",    # 3
                "animations/desert_tiles/object/Cactus3.png",    # 4
                "animations/desert_tiles/object/Crate.png",      # 5
                "animations/desert_tiles/object/Grass1.png",     # 6
                "animations/desert_tiles/object/Grass2.png",     # 7
                "animations/desert_tiles/object/Sign.png",       # 8
                "animations/desert_tiles/object/SignArrow.png",  # 9
                "animations/desert_tiles/object/Skeleton.png",   # 10
                "animations/desert_tiles/object/Stone.png",      # 11
                "animations/desert_tiles/object/StoneBlock.png", # 12
                "animations/desert_tiles/object/Tree.png"         # 13
                ]
            
        sprite_sheet = SpriteSheet(deco[number])
        image = sprite_sheet.sprite_sheet
        image = pygame.transform.rotozoom(image, 0, 1)
        image.set_colorkey(BLACK)


        # Set the image the rocket starts with
        self.image = image
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        

class Explosion(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        super().__init__()
        
        self.movement = []
        self.time = 0
        
        sprite_sheet = SpriteSheet("animations/player/explo/explosion.png")
        n = 16
        for i in range(n):
            image = sprite_sheet.get_image((i%4)*64, (i//4)*64, 64, 64)
            image.set_colorkey((34,177,76))
            self.movement.append(image)
        

        self.image = image
 
        self.rect = self.image.get_rect()
        
    def update(self):
        """ Move the enemy. """
        
        self.time += 1
        
        self.image  = self.movement[self.time//10]


    

  