import pygame

from  player import *
from  elements import Platform
from  levels import *
from died import level_name
from died import winner


def campaign_mp():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption(game_name)
 
    # Create the player
    player = Player()
    player2 = Player(color = 1)
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01_MP(player, player2))
    level_list.append(Level_02_MP(player, player2))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player2.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height-100
    
    player2.rect.x = 240
    player2.rect.y = SCREEN_HEIGHT - player2.rect.height-100

    active_sprite_list.add(player, player2)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
 
    enable_shoot = 30 # how often user can shoot
    enable_shoot2 = 30
    
    score = 0
    
    level_name(1)
    
    pygame.mixer.set_num_channels(12) 
    pygame.mixer.Channel(9).play(pygame.mixer.Sound("sounds/level1_music.wav"), -1)
 
    # -------- Main Program Loop -----------
    while not done:
        
        
        if player.dead == 1 or player2.dead == 1:
            from died import died
            died()
            
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        # player 1
        
        if player.marked_for_dead == 0:
            if keys[pygame.K_LEFT] and keys[pygame.K_o]:
                player.status = 7
            elif keys[pygame.K_RIGHT] and keys[pygame.K_o]:
                player.status = 6
            elif keys[pygame.K_LEFT]:
                player.status = 1
            elif keys[pygame.K_RIGHT]:
                player.status = 0
            elif keys[pygame.K_p]:
                player.status = 0
            elif keys[pygame.K_o] and player.direction == "R":
                player.status = 4
            elif keys[pygame.K_o] and player.direction == "L":
                player.status = 5
            elif player.direction == "R":
                player.status = 2
            else:
                player.status = 3
                
            if keys[pygame.K_DOWN] and keys[pygame.K_p]:
                player.go_down()
            
            if keys[pygame.K_ESCAPE]:
                pygame.mixer.fadeout(250)
                from  game_intro import game_intro_loop
                game_intro_loop()
                    
            for event in events:
    
                if event.type == pygame.QUIT:
                    done = True
     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                        player.direction = "L"
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                        player.direction = "R"
                    if event.key == pygame.K_p:
                        player.jump()
     
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()
            
            # Shoot    
            if(enable_shoot > 30):
                if keys[pygame.K_UP] and keys[pygame.K_o] and keys[pygame.K_RIGHT]:
                    bullet = Bullet_rocket(direction = 1)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    current_level.player_rockets.add(bullet)
                    enable_shoot = 0
                elif keys[pygame.K_UP] and keys[pygame.K_o] and keys[pygame.K_LEFT]:
                    bullet = Bullet_rocket(direction = 2)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    current_level.player_rockets.add(bullet)
                    enable_shoot = 0    
                elif keys[pygame.K_UP] and keys[pygame.K_o]:
                    bullet = Bullet_rocket(direction = 0)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    current_level.player_rockets.add(bullet)
                    enable_shoot = 0
                elif keys[pygame.K_DOWN] and keys[pygame.K_o]:
                    bullet = Bullet_rocket(direction = 3)
                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery
                    #active_sprite_list.add(bullet)
                    current_level.player_bullets.add(bullet)
                    enable_shoot = 0
                elif player.direction == "R" and keys[pygame.K_o]:
                    bullet = Bullet(direction = 180/360*2*math.pi)
                    bullet.rect.x = player.rect.x  + 90
                    bullet.rect.y = player.rect.y  + 45
                    #active_sprite_list.add(bullet)
                    current_level.player_bullets.add(bullet)
                    enable_shoot = 0
                elif keys[pygame.K_o]:
                    bullet = Bullet(direction=0/360*2*math.pi)
                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y  + 45
                    #active_sprite_list.add(bullet)
                    current_level.player_bullets.add(bullet)
                    enable_shoot = 0
            else:
                enable_shoot+=1

        # player 2
        
        if player2.marked_for_dead == 0:
            if keys[pygame.K_a] and keys[pygame.K_v]:
                player2.status = 7
            elif keys[pygame.K_d] and keys[pygame.K_v]:
                player2.status = 6
            elif keys[pygame.K_a]:
                player2.status = 1
            elif keys[pygame.K_d]:
                player2.status = 0
            elif keys[pygame.K_b]:
                player2.status = 0
            elif keys[pygame.K_v] and player2.direction == "R":
                player2.status = 4
            elif keys[pygame.K_v] and player2.direction == "L":
                player2.status = 5
            elif player2.direction == "R":
                player2.status = 2
            else:
                player2.status = 3
                
            if keys[pygame.K_s] and keys[pygame.K_b]:
                player2.go_down()
            
                    
            for event in events:
    
                if event.type == pygame.QUIT:
                    done = True
     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player2.go_left()
                        player2.direction = "L"
                    if event.key == pygame.K_d:
                        player2.go_right()
                        player2.direction = "R"
                    if event.key == pygame.K_b:
                        player2.jump()
     
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and player2.change_x < 0:
                        player2.stop()
                    if event.key == pygame.K_d and player2.change_x > 0:
                        player2.stop()
            
            # Shoot    
            
            if(enable_shoot2 > 30):
                if keys[pygame.K_w] and keys[pygame.K_v] and keys[pygame.K_d]:
                    bullet = Bullet_rocket(direction = 1)
                    bullet.rect.x = player2.rect.centerx
                    bullet.rect.y = player2.rect.centery
                    current_level.player2_rockets.add(bullet)
                    enable_shoot2 = 0
                elif keys[pygame.K_w] and keys[pygame.K_v] and keys[pygame.K_a]:
                    bullet = Bullet_rocket(direction = 2)
                    bullet.rect.x = player2.rect.centerx
                    bullet.rect.y = player2.rect.centery
                    current_level.player2_rockets.add(bullet)
                    enable_shoot2 = 0    
                elif keys[pygame.K_w] and keys[pygame.K_v]:
                    bullet = Bullet_rocket(direction = 0)
                    bullet.rect.x = player2.rect.centerx
                    bullet.rect.y = player2.rect.centery
                    current_level.player2_rockets.add(bullet)
                    enable_shoot2 = 0
                elif keys[pygame.K_s] and keys[pygame.K_v]:
                    bullet = Bullet_rocket(direction = 3)
                    bullet.rect.x = player2.rect.centerx
                    bullet.rect.y = player2.rect.centery
                    current_level.player2_bullets.add(bullet)
                    enable_shoot2 = 0
                elif player2.direction == "R" and keys[pygame.K_v]:
                    bullet = Bullet(direction = 180/360*2*math.pi)
                    bullet.rect.x = player2.rect.x  + 90
                    bullet.rect.y = player2.rect.y  + 45
                    current_level.player2_bullets.add(bullet)
                    enable_shoot2 = 0
                elif keys[pygame.K_v]:
                    bullet = Bullet(direction=0/360*2*math.pi)
                    bullet.rect.x = player2.rect.x
                    bullet.rect.y = player2.rect.y  + 45
                    current_level.player2_bullets.add(bullet)
                    enable_shoot2 = 0
            else:
                enable_shoot2+=1


        if player.rect.right > SCREEN_WIDTH - 30:
            player.rect.right = SCREEN_WIDTH - 30
        
        if player.rect.left < 30:
            player.rect.left = 30

        if player2.rect.right > SCREEN_WIDTH - 30:
            player2.rect.right = SCREEN_WIDTH - 30
        
        if player2.rect.left < 30:
            player2.rect.left = 30
        

        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        
        if player.rect.right >= 500 and player2.rect.left >= 30:
            diff = min(player.rect.right - 500, player2.rect.left - 30)
            #diff = player.rect.right - 500
            if player2.rect.left - diff >= 30:
                #player.rect.right = 500
                player.rect.right -= diff
                player2.rect.left -= diff
                current_level.shift_world(-diff)
        elif player.rect.left <= 120 and player2.rect.right <= SCREEN_WIDTH - 30:
            diff = min(120 - player.rect.left,SCREEN_WIDTH -30 - player2.rect.right)
            if player2.rect.right + diff <= SCREEN_WIDTH - 30:
                player2.rect.left += diff
                player.rect.left +=diff
                current_level.shift_world(diff)

        current_level.update()
 
 
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                pygame.mixer.fadeout(500)
                current_level = level_list[current_level_no]
                level_name(current_level_no+1)
                pygame.mixer.Channel(9).play(pygame.mixer.Sound("sounds/level1_music.wav"), -1)
                player.level = current_level
                player2.level = current_level
                current_level.player_bullets = pygame.sprite.Group()
                player.stop()
                player2.stop()
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
  
