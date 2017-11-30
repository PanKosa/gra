"""
Global constants
"""

game_name = "Henio Killa"
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREEN2 = (0, 255, 50)
RED =   (255, 0, 0)
BLUE =  (0, 0, 255)
YELLOW1 = (255,255,0)
YELLOW2 = (255,204,0)



colors = (RED, RED, BLACK, BLUE, GREEN)

options = [
            [100, 200, 300, 400, 500],
            [5, 10,20,30,40, 50],
            [10,20,30,40,50,100],
            [3,4,5,6,7,8,9]
        ]
 
# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600



black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (102,255,102)
bright_green = (120,255,102)
bright_red = (255,0,15)

display_width = 800
display_height = 600

def get_const():
    with open("options.txt", "r+") as myfile:
	    x = myfile.readlines()
    myfile.close() 
    for i in range(len(x)):
        x[i] = int((x[i])[0])
        opt = options[i]
        x[i] = opt[x[i]]
    return x
    
def get_max_hp(x):
    return x[0]
    
def get_damage(x):
    return x[1]
    
def get_hp_rest(x):
    return x[2]
    
def get_bullet_speed(x):
    return x[3]
    
