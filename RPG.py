import os
import random
import pygame
import sys
import math
import enemy
# Variables
# General Variables
x = 50
y = 400
window_height = 500
window_width = 480
fps = 16
red = (255,0,0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
gray = (211,211,211)
clock = pygame.time.Clock()

# Stamina Variables 
running = False
cant_run = False
stamina = 300
stamina_max = 300
stamina_half = 150
stamina_consum = 5
stamina_regen = 2
speed = 5.5
speed_run = 8

# Health Variables
hp = 100
maxhp = 100
regenhp = 25

#Character Variables
hngr = 0
hngr_max = 100
hngr_reduce = 15
hngr_damage = 0.5 # Damage to the player if hngr is max
hngr_rise = 0.05 # How fast player gets hungry
thrst = 0
thrst_max = 100
thrst_reduce = 25
thrst_damage = 0.4 # Damage to the player if thrst is max
thrst_rise = 0.07 # How fast player gets thirsty
mlt = 6
double_damage = 0.7 # Double Damage from Lack of food and water

# Sprites
pygame.display.set_caption("Survivle RPG")
char = pygame.image.load('sprites/D1.png')
#Stamina Sprite
sbar = [pygame.image.load('sprites/stamina1.png'), pygame.image.load('sprites/stamina2.png'), pygame.image.load('sprites/stamina3.png'), pygame.image.load('sprites/stamina4.png'), pygame.image.load('sprites/stamina5.png'), pygame.image.load('sprites/stamina6.png'), pygame.image.load('sprites/stamina7.png'), pygame.image.load('sprites/stamina8.png')]
#Health Sprite
hbar = [pygame.image.load('sprites/health1.png'), pygame.image.load('sprites/health2.png'), pygame.image.load('sprites/health3.png'), pygame.image.load('sprites/health4.png'), pygame.image.load('sprites/health5.png'), pygame.image.load('sprites/health6.png'), pygame.image.load('sprites/health7.png'), pygame.image.load('sprites/health8.png')]
#Hunger Sprite
hngrbar = [pygame.image.load('sprites/health1.png'), pygame.image.load('sprites/health2.png'), pygame.image.load('sprites/health3.png'), pygame.image.load('sprites/health4.png'), pygame.image.load('sprites/health5.png'), pygame.image.load('sprites/health6.png'), pygame.image.load('sprites/health7.png'), pygame.image.load('sprites/health8.png')]
#Thirst Sprite
tbar = [pygame.image.load('sprites/health1.png'), pygame.image.load('sprites/health2.png'), pygame.image.load('sprites/health3.png'), pygame.image.load('sprites/health4.png'), pygame.image.load('sprites/health5.png'), pygame.image.load('sprites/health6.png'), pygame.image.load('sprites/health7.png'), pygame.image.load('sprites/health8.png')]



# Player Main Class
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player, self).__init__()
        #adding all images to sprite array
        self.imagesDown = []
        self.imagesUp = []
        self.imagesLeft = []
        self.imagesRight = []
        self.imagesChar = []
        # Down
        self.imagesDown.append(pygame.image.load('sprites/D1.png'))
        self.imagesDown.append(pygame.image.load('sprites/D2.png'))
        self.imagesDown.append(pygame.image.load('sprites/D3.png'))
        self.imagesDown.append(pygame.image.load('sprites/D4.png'))
            
        # Up
        self.imagesUp.append(pygame.image.load('sprites/U1.png'))
        self.imagesUp.append(pygame.image.load('sprites/U2.png'))
        self.imagesUp.append(pygame.image.load('sprites/U3.png'))
        self.imagesUp.append(pygame.image.load('sprites/U4.png'))
        # Left
        self.imagesLeft.append(pygame.image.load('sprites/L1.png'))
        self.imagesLeft.append(pygame.image.load('sprites/L2.png'))
        self.imagesLeft.append(pygame.image.load('sprites/L3.png'))
        self.imagesLeft.append(pygame.image.load('sprites/L4.png'))
        # Right
        self.imagesRight.append(pygame.image.load('sprites/R1.png'))
        self.imagesRight.append(pygame.image.load('sprites/R2.png'))
        self.imagesRight.append(pygame.image.load('sprites/R3.png'))
        self.imagesRight.append(pygame.image.load('sprites/R4.png'))

        self.imagesChar.append(pygame.image.load('sprites/D1.png'))

        #index value to get the image from the array
        self.index = 0

        self.image = self.imagesDown[self.index]
        self.rect = self.image.get_rect()
        self.hngr = hngr
        self.thrst = thrst
        self.hngr_max = hngr_max
        self.thrst_max = thrst_max

    def update(self):
        self.index += 1
        if key[pygame.K_s]:
            if self.index >= len(self.imagesDown):
                self.index = 0
            self.image = self.imagesDown[self.index]
        elif key[pygame.K_a]:
            if self.index >= len(self.imagesLeft):
                self.index = 0
            self.image = self.imagesLeft[self.index]
        elif key[pygame.K_d]:
            if self.index >= len(self.imagesRight):
                self.index = 0
            self.image = self.imagesRight[self.index]
        elif key[pygame.K_w]:
            if self.index >= len(self.imagesUp):
                self.index = 0
            self.image = self.imagesUp[self.index]
        else:
            if self.index >= len(self.imagesChar):
                self.index = 0
            self.image = self.imagesChar[self.index]
            
    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):

        global hngr
        global thrst
        global hp
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
        if pygame.sprite.collide_rect(player, food):
            food.rect.x = random.randint(20, 300)
            food.rect.y = random.randint(200, 400)
            hngr -= hngr_reduce
            if hngr < 0:
                hngr = 0
            print("You consumed food, your hunger level is now" + str(hngr))
        if pygame.sprite.collide_rect(player, water):
            water.rect.x = random.randint(20, 300)
            water.rect.y = random.randint(200, 400)
            thrst -= thrst_reduce
            if thrst < 0:
                thrst = 0
            print("You consumed water, your water level is now" + str(thrst))
        if pygame.sprite.collide_rect(player, medkit):
            medkit.rect.x = random.randint(20, 300)
            medkit.rect.y = random.randint(200, 400)
            hp += regenhp
            if hp > maxhp:
                hp = maxhp
                    

# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Enemy(object):
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.x = x
        self.rect.y = y
        self.vel = 3
                                
    def move_towards_player(self, player, speed=3):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist # Normalize vector
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
class Food(object):

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 16 ,16)

        self.rect.x = x
        self.rect.y = y


class Water(object):

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 16 ,16)

        self.rect.x = x
        self.rect.y = y

class Medkit(object):

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 16 ,16)

        self.rect.x = x
        self.rect.y = y
        
    
# Initialise pygame
pygame.display.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#Initialize window and background
win = pygame.display.set_mode((window_height,window_width))
backdrop = pygame.image.load(os.path.join('sprites','bg.png')).convert()
backdropbox = win.get_rect()

walls = [] # List to hold the walls
player = Player() # Create the player
player.rect.x = 0
player.rect.y = 0
enemy = Enemy(150, 100) # Enemy Variable
food = Food(300, 100) # Food Variable
water = Water(100, 200) # Water Variable
medkit = Medkit(150, 400) # Medkit Variable
player_list = pygame.sprite.Group(player)
level = [
"              WWWWWWWWWWWWWWWW",
"             WW              W",
"W         WWWWWW             W",
"W   WWWW       W             W",
"W   WWWW       W             W",
"W   WWWW       W             W",
"W   WWWW       W             W",
"W   WWWW       W             W",
"W   WWWW       W             W",
"W   WWWW       W             W",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        x += 16
    y += 16
    x = 0

#Animations
def redrawGameWindow():

    # Stamina UI Animation   
    
    if stamina >= 300:
        win.blit(sbar[0], (120,10))
        
    elif stamina < 300 and stamina >= 250:
        win.blit(sbar[1], (120,10))
        
    elif stamina < 250 and stamina >= 200:
        win.blit(sbar[2], (120,10))

    elif stamina < 200 and stamina >= 150:
        win.blit(sbar[3], (120,10))

    elif stamina < 150 and stamina >= 100:
        win.blit(sbar[4], (120,10))

    elif stamina < 100 and stamina >= 50:
        win.blit(sbar[5], (120,10))

    elif stamina < 50 and stamina > 10:
        win.blit(sbar[6], (120,10))
    else:
        win.blit(sbar[7], (120,10))

    def animateUI(var, spr, pos):    

        if var >= 100:
            win.blit(spr[0], (pos,10))
            
        elif var < 100 and var >= 85:
            win.blit(spr[1], (pos,10))
            
        elif var < 85 and var >= 70:
            win.blit(spr[2], (pos,10))
            
        elif var < 70 and var >= 55:
            win.blit(spr[3], (pos,10))

        elif var < 55 and var >= 40:
            win.blit(spr[4], (pos,10))

        elif var < 40 and var >= 25:
            win.blit(spr[5], (pos,10))

        elif var < 25 and var > 10:
            win.blit(spr[6], (pos,10))
        else:
            win.blit(spr[7], (pos,10))

    # Health UI Animation
    
    animateUI(hp, hbar, 20)

    # Hunger UI Animation

    animateUI(hngr, hngrbar, 220)

    # Thirst UI Animation

    animateUI(thrst,tbar, 320)

    pygame.display.update()
    
run = True
while run:

    clock.tick(fps)
    if stamina >= stamina_max:
        cant_run = False
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            run = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and key[pygame.K_LSHIFT] and stamina >= 1 and cant_run == False:#run left
        player.move(-speed_run, 0)
        stamina -= stamina_consum
        running = True
    elif key[pygame.K_d] and key[pygame.K_LSHIFT] and stamina >= 1 and cant_run == False:#run right
        player.move(speed_run, 0)
        stamina -= stamina_consum
        running = True
    elif key[pygame.K_w] and key[pygame.K_LSHIFT] and stamina >= 1 and cant_run == False:#run up
        player.move(0, -speed_run)
        stamina -= stamina_consum
        running = True
    elif key[pygame.K_s] and key[pygame.K_LSHIFT] and stamina >= 1 and cant_run == False:#run down
        player.move(0, speed_run)
        stamina -= stamina_consum
        running = True
    elif key[pygame.K_a]:#walk left 
        player.move(-speed, 0)
        running = False
        if stamina < stamina_max and running == False:
            stamina += stamina_regen
            if stamina <= stamina_half:
                cant_run = True
            else:
                cant_run = False
    elif key[pygame.K_d]:#walk right
        player.move(speed, 0)
        running = False
        if stamina < stamina_max and running == False:
            stamina += stamina_regen
            if stamina <= stamina_half:
                cant_run = True
            else:
                cant_run = False
    elif key[pygame.K_w]:#walk up
        player.move(0, -speed)
        running = False
        if stamina < stamina_max and running == False:
            stamina += stamina_regen
            if stamina <= stamina_half:
                cant_run = True
            else:
                cant_run = False
    elif key[pygame.K_s]:#walk down
        player.move(0, speed)
        if stamina < stamina_max and running == False:
            stamina += stamina_regen
            if stamina <= stamina_half:
                cant_run = True
            else:
                cant_run = False
    else:
        if stamina < stamina_max:
            stamina += 5
    
    # Hunger Bar
    if hngr < hngr_max:
        hngr+=hngr_rise
        if running == True:
            hngr+=hngr_rise*mlt
    elif hngr > hngr_max:
        hngr = hngr_max
    # Thirst Bar
    if thrst < thrst_max:
        thrst+=thrst_rise
        if running == True:
            thrst+=thrst_rise*mlt
    elif thrst > thrst_max:
        thrst = thrst_max
    #Health Bar
    if thrst == thrst_max:
        hp-=thrst_damage
    elif hngr == hngr_max:
        hp-=hngr_damage
    elif hngr == hngr_max and thrst == thrst_max:
        hp-=double_damage
    
    # Draw the scene
    player_list.update() 
    player_list.draw(win) #draw the player
    #pygame.draw.rect(win, black, enemy)
    for wall in walls:
        pygame.draw.rect(win, gray , wall.rect)
    pygame.draw.rect(win, green, food) # Draw Food
    pygame.draw.rect(win, blue, water) # Draw Water
    pygame.draw.rect(win, red, medkit) # Draw Medkit
    redrawGameWindow()
    pygame.display.flip()
    win.blit(backdrop, backdropbox)
    

pygame.quit()   
