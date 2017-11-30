import pygame

from  elements import *
from player import *
from buttons import *
import math


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)
BLUE =  (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Options const
opt_const = get_const()

damage = get_damage(opt_const)



class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.player_rockets = pygame.sprite.Group()
        self.player = player
        self.enemy_bullets = pygame.sprite.Group()
        self.health = pygame.sprite.Group()
        self.decoration = pygame.sprite.Group()
        self.explo = pygame.sprite.Group()
        
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.player_bullets.update()
        self.player_rockets.update()
        self.enemies.update()
        self.enemy_bullets.update()
        self.explo.update()
        
        
        # Options const
        opt_const = get_const()
        max_hp = get_max_hp(opt_const)
        damage = get_damage(opt_const)
        hp_rest = get_hp_rest(opt_const)
        
        
        player_hit_list = pygame.sprite.spritecollide(self.player, self.health, False)
        for health in player_hit_list:
            self.player.hitpoints += hp_rest
            self.player.hitpoints = min(self.player.hitpoints, max_hp)
            self.health.remove(health)
        
        
        
        # Fire enemies bullets
        for enemy in self.enemies:
            if enemy.shot == 40 and enemy.marked_for_dead == 0:
                if enemy.typeE == 1:
                    if enemy.direction == "L":
                        bullet = Bullet_enemy(direction = 0/360*2*math.pi,rotate = False)
                    else:
                        bullet = Bullet_enemy(direction = 180/360*2*math.pi, rotate = True)
                else:
                    bullet = Bullet_track(self.player, enemy)
                bullet.rect.x = enemy.rect.x
                bullet.rect.y = enemy.rect.y + 60
                self.enemy_bullets.add(bullet)
        
        for enemy in self.enemies:
            if enemy.marked_for_dead == 0:
                if self.player.rect.x > enemy.rect.x:
                    enemy.direction = "R"
                else:
                    enemy.direction = "L"
        
                    
        
        #Remove the bullet if it flies up off the screen
        for bullet in self.player_bullets:
            if bullet.rect.y < -50:
                self.player_bullets.remove(bullet)
            elif bullet.rect.y > SCREEN_HEIGHT + 50:
                self.player_bullets.remove(bullet)
            elif bullet.rect.x < -50:
                self.player_bullets.remove(bullet)
            elif bullet.rect.x > SCREEN_WIDTH + 50:
                self.player_bullets.remove(bullet)
                
        for bullet in self.player_rockets:
            if bullet.rect.y < -50:
                self.player_rockets.remove(bullet)
            elif bullet.rect.y > SCREEN_HEIGHT + 50:
                self.player_rockets.remove(bullet)
            elif bullet.rect.x < -50:
                self.player_rockets.remove(bullet)
            elif bullet.rect.x > SCREEN_WIDTH + 50:
                self.player_rockets.remove(bullet)
                
        for bullet in self.enemy_bullets:
            if bullet.rect.y < -50:
                self.enemy_bullets.remove(bullet)
            elif bullet.rect.y > SCREEN_HEIGHT + 50:
                self.enemy_bullets.remove(bullet)
            elif bullet.rect.x < -50:
                self.enemy_bullets.remove(bullet)
            elif bullet.rect.x > SCREEN_WIDTH + 50:
                self.enemy_bullets.remove(bullet)
                
                
                

        # For each block hit, remove the bullet and add to the score
        for bullet in self.player_bullets:
            enemies_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if len(enemies_hit_list) > 0:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound('sounds/explo.wav'))
            for enemy in enemies_hit_list:
                expl = Explosion()
                expl.rect.x = bullet.rect.x
                expl.rect.y = bullet.rect.y
                self.explo.add(expl)
                
                enemy.marked_for_dead = 1
                if enemy.dead_direction == None:
                    if enemy.direction == "R":
                        enemy.dead_direction = 0
                    else:
                        enemy.dead_direction = 1
                self.player_bullets.remove(bullet)
                
        # For each block hit, remove the bullet and add to the score
        for bullet in self.player_rockets:
            enemies_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if len(enemies_hit_list) > 0:
                pygame.mixer.Channel(7).play(pygame.mixer.Sound('sounds/explo.wav'))
            for enemy in enemies_hit_list:
                expl = Explosion()
                expl.rect.x = bullet.rect.x
                expl.rect.y = bullet.rect.y
                self.explo.add(expl)
                
                enemy.marked_for_dead = 1
                if enemy.dead_direction == None:
                    if enemy.direction == "R":
                        enemy.dead_direction = 0
                    else:
                        enemy.dead_direction = 1
                self.player_rockets.remove(bullet)
        
        for enemy in self.enemies:
            if enemy.marked_for_dead == 1:
                enemy.time_before_dead-=1
                if enemy.time_before_dead<=0:
                    self.enemies.remove(enemy)
                    
        # remove old explosions
        for expl in self.explo:
            if expl.time > 158:
                self.explo.remove(expl)
                    
        hit_list = pygame.sprite.spritecollide(self.player, self.enemy_bullets , True) 
        if len(hit_list)>0:
            pygame.mixer.Channel(5).play(pygame.mixer.Sound('sounds/take_damage.wav'))
        self.player.hitpoints -= len(hit_list)*damage
        self.player.hitpoints = max(self.player.hitpoints, 0)

 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.blit(self.background, dest=(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemies.draw(screen)
        self.enemy_bullets.draw(screen)
        self.player_bullets.draw(screen)
        self.player_rockets.draw(screen)
        self.health.draw(screen)
        self.decoration.draw(screen)
        self.explo.draw(screen)
        self.player.draw_hitpoints(screen)
        
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemies:
            enemy.rect.x += shift_x
            
        for rocket in self.player_rockets:
            rocket.rect.x += shift_x
        
        for bullet in self.player_bullets:
            bullet.rect.x += shift_x
        
        for bullet in self.enemy_bullets:
            bullet.rect.x += shift_x
            
        for health in self.health:
            health.rect.x += shift_x
                    
        for deco in self.decoration:
            deco.rect.x += shift_x
            
        for expl in self.explo:
            expl.rect.x += shift_x
    
 
# Create platforms for the level
class Level_MP(Level):
    """ Definition for level 1. """
 
    def __init__(self, player, player2):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
        
        self.player2_bullets = pygame.sprite.Group()
        self.player2_rockets = pygame.sprite.Group()
        self.player2 = player2
        
    def update(self):
        """ Update everything in this level."""
        Level.update(self)
        
        # Options const
        opt_const = get_const()
        max_hp = get_max_hp(opt_const)
        damage = get_damage(opt_const)
        hp_rest = get_hp_rest(opt_const)
        
        self.player2_bullets.update()
        self.player2_rockets.update()
        
        player2_hit_list = pygame.sprite.spritecollide(self.player2, self.health, False)
        for health in player2_hit_list:
            self.player2.hitpoints += hp_rest
            self.player2.hitpoints = min(self.player2.hitpoints, max_hp)
            self.health.remove(health)
            pygame.mixer.Channel(5).play(pygame.mixer.Sound('sounds/take_damage.wav'))
        
                            
        #Remove the bullet if it flies up off the screen
        for bullet in self.player2_bullets:
            if bullet.rect.y < -50:
                self.player2_bullets.remove(bullet)
            elif bullet.rect.y > SCREEN_HEIGHT + 50:
                self.player2_bullets.remove(bullet)
            elif bullet.rect.x < -50:
                self.player2_bullets.remove(bullet)
            elif bullet.rect.x > SCREEN_WIDTH + 50:
                self.player2_bullets.remove(bullet)
                
        for bullet in self.player2_rockets:
            if bullet.rect.y < -50:
                self.player2_rockets.remove(bullet)
            elif bullet.rect.y > SCREEN_HEIGHT + 50:
                self.player2_rockets.remove(bullet)
            elif bullet.rect.x < -50:
                self.player2_rockets.remove(bullet)
            elif bullet.rect.x > SCREEN_WIDTH + 50:
                self.player2_rockets.remove(bullet)
                

        # For each block hit, remove the bullet and add to the score
        for bullet in self.player2_bullets:
            enemies_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if len(enemies_hit_list) > 0:
                pygame.mixer.Channel(7).play(pygame.mixer.Sound('sounds/explo.wav'))
            for enemy in enemies_hit_list:
                expl = Explosion()
                expl.rect.x = bullet.rect.x
                expl.rect.y = bullet.rect.y
                self.explo.add(expl)
                
                enemy.marked_for_dead = 1
                if enemy.dead_direction == None:
                    if enemy.direction == "R":
                        enemy.dead_direction = 0
                    else:
                        enemy.dead_direction = 1
                self.player2_bullets.remove(bullet)
                
        # For each block hit, remove the bullet and add to the score
        for bullet in self.player2_rockets:
            enemies_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if len(enemies_hit_list) > 0:
                pygame.mixer.Channel(7).play(pygame.mixer.Sound('sounds/explo.wav'))
            for enemy in enemies_hit_list:
                expl = Explosion()
                expl.rect.x = bullet.rect.x
                expl.rect.y = bullet.rect.y
                self.explo.add(expl)
                
                enemy.marked_for_dead = 1
                if enemy.dead_direction == None:
                    if enemy.direction == "R":
                        enemy.dead_direction = 0
                    else:
                        enemy.dead_direction = 1
                self.player2_rockets.remove(bullet)
        
        for enemy in self.enemies:
            if enemy.marked_for_dead == 1:
                enemy.time_before_dead-=1
                if enemy.time_before_dead<=0:
                    self.enemies.remove(enemy)    # optymalizacja - zamiana kolejnosci if
                    
        hit_list = pygame.sprite.spritecollide(self.player2, self.enemy_bullets , True) # to bedzie rozbudowane o warunek ze uderza dopiero jak odleglosc bedzie wieksz od brzegu Surface
        if len(hit_list)>0:
            pygame.mixer.Channel(5).play(pygame.mixer.Sound('sounds/take_damage.wav'))
        self.player2.hitpoints -= len(hit_list)*damage
        self.player2.hitpoints = max(self.player2.hitpoints, 0)

    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.blit(self.background, dest=(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemies.draw(screen)
        self.enemy_bullets.draw(screen)
        self.player_bullets.draw(screen)
        self.player_rockets.draw(screen)
        self.health.draw(screen)
        self.decoration.draw(screen)
        self.explo.draw(screen)
        self.player.draw_hitpoints(screen)
        self.player2_bullets.draw(screen)
        self.player2_rockets.draw(screen)
        self.player2.draw_hitpoints(screen, side = "R")
        
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -5000
 
        # Array with width, height, x, and y of platform
        level_grass = [[500,  450,2],
                       [600,  250,4],
                       [700,  350,0],
                       [1250,  430,0],
                       [1900, 350,2],
                       [1500, 270,0],
                       [1800, 150,2],
                       [2900, 350,2],
                       [3100, 150,2],
                       [3600, 450,0],
                       [3900, 350,0],
                       [4200, 250,0],
                       [4900, 250,1]
                      ]
                      
        level_ground = [[0,    550,4],
                        [2500, 550,4],
                        [1600, 550,2],
                        [2900, 550,3],
                        [4700, 550,8]
                       ]
                 
        enemies = [
            [600, 550],
            [1550, 270],
            [1850, 150],
            [4000, 350],
            [4300, 250]
                 ]
                 
        enemies_track = [
            [700, 250],
            [1950, 350],
            [2050, 350],
            [3650, 450],
            [3000, 350],
            [3190, 150],
            [4950, 550],
            [5100, 250]
            
                        ]
                        
        health_pack = [
            [650 , 250],
            [2000, 350],
            [3500, 550]
            ]
            
        #               x   y    level number
        decorations = [ 
            [50,   550, 1, 0],
            [700,  250, 1, 12],
            [1300, 430, 1, 0],
            [700,  350, 1, 9],
            [650,  550, 1, 10],
            [1870, 150, 1, 10],
            [2070, 150, 1, 1],
            [1700, 550, 1, 5],
            [1760, 550, 1, 6],
            [2450, 550, 1, 11],
            [3640, 450, 1, 9],
            [3300, 150, 1, 1],
            [3390, 150, 1, 4],
            [2550, 550, 1, 6],
            [2650, 550, 1, 5],
            [5400, 550, 1, 8],
            [5700, 550, 1, 8],
            [5550, 550, 1, 3],
            [5600, 550, 1, 6],
            [5350, 550, 1, 11],
            [5000, 250, 1, 0],
            [5100, 250, 1, 1]
                      ]
 
        # Go through the array above and add platforms
        for platform in level_grass:
            block = Platform_grass(platform[2])
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            self.platform_list.add(block)
            
        for platform in level_ground:
            block = Platform_grass_ground(platform[2])
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            self.platform_list.add(block)
            
        # Go through the array above and add platforms
        for enemy in enemies:
            block = Enemy()
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.platforms  = self.platform_list
            self.enemies.add(block)
            
        for enemy in enemies_track:
            block = Enemy(typeE = 2)
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.platforms  = self.platform_list
            self.enemies.add(block)
        
        for health in health_pack:
            block = Health_pack()
            block.rect.left = health[0]
            block.rect.bottom = health[1]
            self.health.add(block)
            
        for deco in decorations:
            block = Decoration(deco[2], deco[3])
            block.rect.left = deco[0]
            block.rect.bottom = deco[1]
            self.decoration.add(block)
            
            
        sprite_sheet = SpriteSheet("animations/green_tiles/BG/BG.png")
        image = sprite_sheet.get_image(0,0,1000,750)
        self.background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect_background = self.background.get_rect()
 
 
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -5800
 
        # Array with width, height, x, and y of platform
        level_desert = [[700,  450,2],
                       [600,  230,4],
                       [1350,  430,0],
                       [1550,  150,0],
                       [1650,  550,0],
                       [1950,  150,0],
                       [2050,  550,0],
                       [2350,  250,0],
                       [3050,  100,3],
                       [3750,  250,1],
                       [5300,  150,3]
                      ]
                      
        level_ground = [[0,    550,4],
                        [2500, 550,4],
                        [3450, 550,3],
                        [4450, 550,3],
                        [5300, 450,3],
                        [6000, 550,5]
                       ]
                 
        enemies = [
            [600, 550],
            [1650, 150],
            [4600, 550],
            [4750, 550],
            [3450, 550]
                 ]
                 
        enemies_track = [
            [700, 230],
            [2100, 550],
            [2240, 550],
            [2000, 150],
            [2380, 250],
            [3150, 100],
            [3350, 100],
            [3450, 100],
            [3650, 550],
            [5450, 450],
            [5600, 450],
            [5450, 150],
            [5650, 150]
                        ]
                        
        health_pack = [
            [650 , 230],
            [2000, 350],
            [3500, 550],
            [4650, 550],
            ]
            
        #               x   y    level number
        decorations = [ 
            [50,   550, 2, 13],
            [800,  230, 2, 2],
            [970,  230, 2, 4],
            [1380, 430, 2, 0],
            [1000, 450, 2, 9],
            [6300, 550, 3, 10],
            [6350, 550, 2, 9],
            [6500, 550, 2, 13],
            [6700, 550, 2, 9],
            [4450, 550, 2, 10],
            [4750, 550, 2, 11],
            [3350, 550, 2, 13],
            [3850, 550, 2, 7],
            [3950, 550, 2, 3],
            [3450, 100, 2, 1],
            [2650, 550, 2, 11],
            [2750, 550, 2, 0]
                      ]
 
        # Go through the array above and add platforms
        for platform in level_desert:
            block = Platform_grass(platform[2],1)
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            self.platform_list.add(block)
            
        for platform in level_ground:
            block = Platform_grass_ground(platform[2],1)
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            self.platform_list.add(block)
            
        # Go through the array above and add platforms
        for enemy in enemies:
            block = Enemy()
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.platforms  = self.platform_list
            self.enemies.add(block)
            
        for enemy in enemies_track:
            block = Enemy(typeE = 2)
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.platforms  = self.platform_list
            self.enemies.add(block)
        
        for health in health_pack:
            block = Health_pack()
            block.rect.left = health[0]
            block.rect.bottom = health[1]
            self.health.add(block)
            
        for deco in decorations:
            block = Decoration(deco[2], deco[3])
            block.rect.left = deco[0]
            block.rect.bottom = deco[1]
            self.decoration.add(block)
            
        sprite_sheet = SpriteSheet("animations/desert_tiles/BG/BG.png")
        image = sprite_sheet.get_image(0,0,1000,750)
        self.background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect_background = self.background.get_rect()

class Level_01_MP(Level_MP):
    """ Definition for level 1. """
 
    def __init__(self, player, player2):
        """ Create level 1. """
 
        # Call the parent constructor
        Level_MP.__init__(self, player, player2)
 
        self.level_limit = -5000
 
        # Array with width, height, x, and y of platform
        level_grass = [[500,  450,2],
                       [600,  250,4],
                       [700,  350,0],
                       [1250,  430,0],
                       [1900, 350,2],
                       [1500, 270,0],
                       [1800, 150,2],
                       [2900, 350,2],
                       [3100, 150,2],
                       [3600, 450,0],
                       [3900, 350,0],
                       [4200, 250,0],
                       [4900, 250,1]
                      ]
                      
        level_ground = [[0,    550,4],
                        [2500, 550,4],
                        [1600, 550,2],
                        [2900, 550,3],
                        [4700, 550,8]
                       ]
                 
        enemies = [
            [600, 550],
            [1550, 270],
            [1850, 150],
            [4000, 350],
            [4300, 250]
                 ]
                 
        enemies_track = [
            [700, 250],
            [1950, 350],
            [2050, 350],
            [3650, 450],
            [3000, 350],
            [3190, 150],
            [4950, 550],
            [5100, 250]
            
                        ]
                        
        health_pack = [
            [650 , 250],
            [2000, 350],
            [3500, 550]
            ]
            
        #               x   y    level number
        decorations = [ 
            [50,   550, 1, 0],
            [700,  250, 1, 12],
            [1300, 430, 1, 0],
            [700,  350, 1, 9],
            [650,  550, 1, 10],
            [1870, 150, 1, 10],
            [2070, 150, 1, 1],
            [1700, 550, 1, 5],
            [1760, 550, 1, 6],
            [2450, 550, 1, 11],
            [3640, 450, 1, 9],
            [3300, 150, 1, 1],
            [3390, 150, 1, 4],
            [2550, 550, 1, 6],
            [2650, 550, 1, 5],
            [5400, 550, 1, 8],
            [5700, 550, 1, 8],
            [5550, 550, 1, 3],
            [5600, 550, 1, 6],
            [5350, 550, 1, 11],
            [5000, 250, 1, 0],
            [5100, 250, 1, 1]
                      ]
 
        # Go through the array above and add platforms
        for platform in level_grass:
            block = Platform_grass(platform[2])
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            block.player2 = self.player2
            self.platform_list.add(block)
            
        for platform in level_ground:
            block = Platform_grass_ground(platform[2])
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            self.platform_list.add(block)
            
        # Go through the array above and add platforms
        for enemy in enemies:
            block = Enemy()
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.player2 = self.player2
            block.platforms  = self.platform_list
            self.enemies.add(block)
            
        for enemy in enemies_track:
            block = Enemy(typeE = 2)
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.player2 = self.player2
            block.platforms  = self.platform_list
            self.enemies.add(block)
        
        for health in health_pack:
            block = Health_pack()
            block.rect.left = health[0]
            block.rect.bottom = health[1]
            self.health.add(block)
            
        for deco in decorations:
            block = Decoration(deco[2], deco[3])
            block.rect.left = deco[0]
            block.rect.bottom = deco[1]
            self.decoration.add(block)
            
            
        sprite_sheet = SpriteSheet("animations/green_tiles/BG/BG.png")
        image = sprite_sheet.get_image(0,0,1000,750)
        self.background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect_background = self.background.get_rect()
 
# Create platforms for the level
class Level_02_MP(Level_MP):
    """ Definition for level 2. """
 
    def __init__(self, player, player2):
        """ Create level 1. """
 
        # Call the parent constructor
        Level_MP.__init__(self, player, player2)
 
        self.level_limit = -5800
 
        # Array with width, height, x, and y of platform
        level_desert = [[700,  450,2],
                       [600,  230,4],
                       [1350,  430,0],
                       [1550,  150,0],
                       [1650,  550,0],
                       [1950,  150,0],
                       [2050,  550,0],
                       [2350,  250,0],
                       [3050,  100,3],
                       [3750,  250,1],
                       [5300,  150,3]
                      ]
                      
        level_ground = [[0,    550,4],
                        [2500, 550,4],
                        [3450, 550,3],
                        [4450, 550,3],
                        [5300, 450,3],
                        [6000, 550,5]
                       ]
                 
        enemies = [
            [600, 550],
            [1650, 150],
            [4600, 550],
            [4750, 550],
            [3450, 550]
                 ]
                 
        enemies_track = [
            [700, 230],
            [2100, 550],
            [2240, 550],
            [2000, 150],
            [2380, 250],
            [3150, 100],
            [3350, 100],
            [3450, 100],
            [3650, 550],
            [5450, 450],
            [5600, 450],
            [5450, 150],
            [5650, 150]
                        ]
                        
        health_pack = [
            [650 , 230],
            [2000, 350],
            [3500, 550],
            [4650, 550],
            ]
            
        #               x   y    level number
        decorations = [ 
            [50,   550, 2, 13],
            [800,  230, 2, 2],
            [970,  230, 2, 4],
            [1380, 430, 2, 0],
            [1000, 450, 2, 9],
            [6300, 550, 3, 10],
            [6350, 550, 2, 9],
            [6500, 550, 2, 13],
            [6700, 550, 2, 9],
            [4450, 550, 2, 10],
            [4750, 550, 2, 11],
            [3350, 550, 2, 13],
            [3850, 550, 2, 7],
            [3950, 550, 2, 3],
            [3450, 100, 2, 1],
            [2650, 550, 2, 11],
            [2750, 550, 2, 0]
                      ]
 
        # Go through the array above and add platforms
        for platform in level_desert:
            block = Platform_grass(platform[2],1)
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            block.player2 = self.player2
            self.platform_list.add(block)
            
        for platform in level_ground:
            block = Platform_grass_ground(platform[2],1)
            block.rect.left = platform[0]
            block.rect.top = platform[1]
            block.player = self.player
            block.player2 = self.player2
            self.platform_list.add(block)
            
        # Go through the array above and add platforms
        for enemy in enemies:
            block = Enemy()
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.player2 = self.player2
            block.platforms  = self.platform_list
            self.enemies.add(block)
            
        for enemy in enemies_track:
            block = Enemy(typeE = 2)
            block.rect.left = enemy[0]
            block.rect.bottom = enemy[1]
            block.player = self.player
            block.platforms  = self.platform_list
            self.enemies.add(block)
        
        for health in health_pack:
            block = Health_pack()
            block.rect.left = health[0]
            block.rect.bottom = health[1]
            self.health.add(block)
            
        for deco in decorations:
            block = Decoration(deco[2], deco[3])
            block.rect.left = deco[0]
            block.rect.bottom = deco[1]
            self.decoration.add(block)
            
        sprite_sheet = SpriteSheet("animations/desert_tiles/BG/BG.png")
        image = sprite_sheet.get_image(0,0,1000,750)
        self.background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect_background = self.background.get_rect()
