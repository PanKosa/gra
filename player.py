import pygame

from spritesheet_functions import SpriteSheet

from constants import *
import time

 
 
class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self, color = 0):
        """ Constructor function """
        
        # Options const
        opt_const = get_const()
        max_hp = get_max_hp(opt_const)
        damage = get_damage(opt_const)
        hp_rest = get_hp_rest(opt_const)
 
        # Call the parent's constructor
        super().__init__()

        width = 40
        height = 60

        
        self.inner_clock = 0
        
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 

        self.movement = []
        # List of sprites we can bump against
        self.direction = "R"
        
        self.marked_for_dead = 0
        self.dead = 0
        self.time_before_dead = 100
        self.dead_direction = 'R'
        self.diff = None
        
        self.hitpoints = max_hp
        
        self.level = None
        
        ##Load animations
        # walking
        
        list_r = []
        list_l = []

        n = 8
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/player/run2/"+str(i+1)+".png")
            image = sprite_sheet.sprite_sheet
            image = sprite_sheet.get_image(105, 50, 320, 470)
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            if not color == 0:
                image_pixel = pygame.PixelArray(image)
                image_pixel.replace(YELLOW1, colors[color])
                image_pixel.replace(YELLOW2, colors[color])
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image)             
        self.movement.append(list_r)
        self.movement.append(list_l)
        
        # idle
        
        list_r = []
        list_l = []
        
        n = 10
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/player/idle2/"+str(i+1)+".png")
            image = sprite_sheet.get_image(135, 50, 260, 470)
            if not color == 0:
                image_pixel = pygame.PixelArray(image)
                image_pixel.replace(YELLOW1, colors[color])
                image_pixel.replace(YELLOW2, colors[color])
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image) 
            
        self.movement.append(list_r)
        self.movement.append(list_l)
        
        
        # shot
        
        list_r = []
        list_l = []

        n = 4
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/player/shot2/"+str(i+1)+".png")
            image = sprite_sheet.get_image(93, 50, 387, 470)
            if not color == 0:
                image_pixel = pygame.PixelArray(image)
                image_pixel.replace(YELLOW1, colors[color])
                image_pixel.replace(YELLOW2, colors[color])
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image) 
            
        self.movement.append(list_r)
        self.movement.append(list_l)       
        
        
        # runshot
        
        list_r = []
        list_l = []

        n = 8
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/player/runshot2/"+str(i+1)+".png")
            image = sprite_sheet.get_image(92, 50, 389, 470)
            if not color == 0:
                image_pixel = pygame.PixelArray(image)
                image_pixel.replace(YELLOW1, colors[color])
                image_pixel.replace(YELLOW2, colors[color])
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image)         
        
        
        self.movement.append(list_r)
        self.movement.append(list_l)
        
        # dead
        
        list_r = []
        list_l = []
        
        n = 10
        for i in range(n):
            sprite_sheet = SpriteSheet("animations/player/dead2/"+str(i+1)+".png")
            image = sprite_sheet.sprite_sheet
            if not color == 0:
                image_pixel = pygame.PixelArray(image)
                image_pixel.replace(YELLOW1, colors[color])
                image_pixel.replace(YELLOW2, colors[color])
            image = pygame.transform.rotozoom(image, 0, 0.25)
            image.set_colorkey((34,177,76))
            list_r.append(image)
            image = pygame.transform.flip(image, True, False)
            list_l.append(image)         
        
        
        self.movement.append(list_r)
        self.movement.append(list_l)
        
        # Load Sounds
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        song = "sounds/robot-walk.wav"
        self.walk_sound = pygame.mixer.Sound(song)

        self.status = 2
        
        self.fall_idle = 0 

        # Set the image the player starts with
        self.image = (self.movement[2])[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
        
        if self.rect.top > SCREEN_HEIGHT:
            self.dead = 1
            
        
        # 0 - walk right
        # 1 - walk left 
        # 2 - idle right
        # 3 - idle left
        # 4 - shot right
        # 5 - shot left
        # 6 - runshot right
        # 7 - runshot left

        if self.hitpoints <=0 and self.marked_for_dead == 0:
            self.marked_for_dead = 1
            if self.status % 2 == 0:
                self.dead_direction = 'R'
            else:
                self.dead_direction = 'L'
        
        if self.time_before_dead <=0:
            self.dead = 1
            

        if self.marked_for_dead == 1 and self.dead == 0:
            if self.dead_direction == 'R':
                movement = self.movement[8]
            else:
                movement = self.movement[9]
            self.time_before_dead -= 2    
            frame = max(9 - self.time_before_dead // 9,0)
            self.image = movement[frame]
            self.walk_sound.stop()
            
        elif self.dead == 0:
            if self.status in [2,3,4,5]:
                self.inner_clock +=5
                movement = self.movement[self.status]
                frame = (self.inner_clock // 30) % len(movement)
                self.image = movement[frame]
                self.walk_sound.stop()
            else:
                self.inner_clock = 0 
                pos = self.rect.x + self.level.world_shift 
                movement = self.movement[self.status]
                frame = (pos // 30) % len(movement)
                self.image = movement[frame]
                self.walk_sound.play()

        # Move left/right
        self.rect.x += self.change_x
        
        
        self.fall_idle += 1
        
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if block.rect.top >= self.rect.bottom-+ 5:
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
            
 
        # Move up/down
        self.rect.centery += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if block.rect.top >= self.rect.bottom - 15 :
                # Reset our position based on the top/bottom of the object.
                self.rect.bottom = block.rect.top
                # Stop our vertical movement
                if self.change_y > 0:
                    self.change_y = 0 
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        elif self.change_y < 7:
            self.change_y += .35

 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0:
            self.change_y = -10

 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5
        
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5

        
    def go_down(self):
        """ Called when the user hits the right arrow. """
        self.rect.y += 3
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        can_fall = 1
        for platform in platform_hit_list:
            if platform.can_fall_through == 0:
                can_fall = 0
                
        if can_fall == 1 and self.rect.y + 30 < 600 and self.fall_idle > 20:
            self.rect.y += 20
            self.change_y = 0
            self.fall_idle = 0
        else:
                    self.rect.y -= 3
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
    
    def draw_hitpoints(self, screen, side = "L"):
        pygame.font.init() 
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        if side == "L":
            poz = (5,0)
        else:
            poz = (800 - 75,0)
        textsurface = myfont.render('HP: '+str(self.hitpoints), False, (0, 0, 0))
        screen.blit(textsurface,poz)
        
    
