import pygame

from  player import *
from  elements import Platform
from  levels import *
from died import level_name
from died import winner


def campaign_sp(color = 0):
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption(game_name)
 
    # Create the player
    player = Player(color)
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height-100
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
 
    enable_shoot = 30 # how often user can shoot
    
    score = 0
    
    level_name(1)
    pygame.mixer.set_num_channels(12) 
    pygame.mixer.Channel(9).play(pygame.mixer.Sound("sounds/level1_music.wav"), -1)
 
    # -------- Main Program Loop -----------
    while not done:
        
        
        if player.dead == 1:
            from died import died
            died()
            
        #print(player.rect.x + current_level.world_shift)
                
        keys = pygame.key.get_pressed()
        
        if player.marked_for_dead == 0:
            if keys[pygame.K_LEFT] and keys[pygame.K_z]:
                player.status = 7
            elif keys[pygame.K_RIGHT] and keys[pygame.K_z]:
                player.status = 6
            elif keys[pygame.K_LEFT]:
                player.status = 1
            elif keys[pygame.K_RIGHT]:
                player.status = 0
            elif keys[pygame.K_x]:
                player.status = 0
            elif keys[pygame.K_z] and player.direction == "R":
                player.status = 4
            elif keys[pygame.K_z] and player.direction == "L":
                player.status = 5
            elif player.direction == "R":
                player.status = 2
            else:
                player.status = 3
                
            if keys[pygame.K_DOWN] and keys[pygame.K_x]:
                player.go_down()
            
            if keys[pygame.K_ESCAPE]:
                pygame.mixer.fadeout(250)
                from  game_intro import game_intro_loop
                game_intro_loop()
                    
            for event in pygame.event.get():
    
                if event.type == pygame.QUIT:
                    done = True
     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                        player.direction = "L"
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                        player.direction = "R"
                    if event.key == pygame.K_x:
                        player.jump()
     
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()
            
            # Shoot    
            
            if(enable_shoot > 30):
                if keys[pygame.K_UP] and keys[pygame.K_z] and keys[pygame.K_RIGHT]:
                    bullet = Bullet_rocket(direction = 1)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    current_level.player_rockets.add(bullet)
                    enable_shoot = 0
                elif keys[pygame.K_UP] and keys[pygame.K_z] and keys[pygame.K_LEFT]:
                    bullet = Bullet_rocket(direction = 2)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    current_level.player_rockets.add(bullet)
                    enable_shoot = 0    
                elif keys[pygame.K_UP] and keys[pygame.K_z]:
                    bullet = Bullet_rocket(direction = 0)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    current_level.player_rockets.add(bullet)
                    enable_shoot = 0
                elif keys[pygame.K_DOWN] and keys[pygame.K_z]:
                    bullet = Bullet_rocket(direction = 3)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    #active_sprite_list.add(bullet)
                    current_level.player_bullets.add(bullet)
                    enable_shoot = 0
                elif player.direction == "R" and keys[pygame.K_z]:
                    bullet = Bullet(direction = 180/360*2*math.pi)
                    bullet.rect.x = player.rect.x  + 90
                    bullet.rect.y = player.rect.y  + 45
                    #active_sprite_list.add(bullet)
                    current_level.player_bullets.add(bullet)
                    enable_shoot = 0
                elif keys[pygame.K_z]:
                    bullet = Bullet(direction=0/360*2*math.pi)
                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y  + 45
                    #active_sprite_list.add(bullet)
                    current_level.player_bullets.add(bullet)
                    enable_shoot = 0
            else:
                enable_shoot+=1



        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                pygame.mixer.fadeout(500)
                level_name(current_level_no+1)
                pygame.mixer.Channel(9).play(pygame.mixer.Sound("sounds/level1_music.wav"), -1)
                player.level = current_level
                current_level.player_bullets = pygame.sprite.Group()

                player.stop()
            else:
                pygame.mixer.fadeout(500)
                winner()    
                
        
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
  