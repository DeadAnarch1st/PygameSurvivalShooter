import os
import random
import pygame

#Initialize a Window
win = pygame.display.set_mode((500,480))
pygame.display.set_caption("Survivle RPG")
walkRight = [pygame.image.load('sprites/R1.png'), pygame.image.load('sprites/R2.png'), pygame.image.load('sprites/R3.png'), pygame.image.load('sprites/R4.png')]
walkLeft = [pygame.image.load('sprites/L1.png'), pygame.image.load('sprites/L2.png'), pygame.image.load('sprites/L3.png'), pygame.image.load('sprites/L4.png')]
walkUp = [pygame.image.load('sprites/U1.png'), pygame.image.load('sprites/U2.png'), pygame.image.load('sprites/U3.png'), pygame.image.load('sprites/U4.png')]
walkDown = [pygame.image.load('sprites/D1.png'), pygame.image.load('sprites/D2.png'), pygame.image.load('sprites/D3.png'), pygame.image.load('sprites/D4.png')]
bg = pygame.image.load('sprites/bg.png')
char = pygame.image.load('sprites/D1.png')
sbar = [pygame.image.load('sprites/stamina1.png'), pygame.image.load('sprites/stamina2.png'), pygame.image.load('sprites/stamina3.png'), pygame.image.load('sprites/stamina4.png'), pygame.image.load('sprites/stamina5.png'), pygame.image.load('sprites/stamina6.png'), pygame.image.load('sprites/stamina7.png'), pygame.image.load('sprites/stamina8.png')]

# Variables
x = 50
y = 400
width = 92
height = 92
vel = 5
boost = 1.5
up = False
down = False
left = False
right = False
shift = False
walkcount = 0
stamina = 24
clock = pygame.time.Clock()

#Animations
def redrawGameWindow():
    global walkcount

    win.blit(bg,(0,0))

    if walkcount + 1 >= 16:
        walkcount = 0
        
    #Walking Animation
    if left:
        win.blit(walkLeft[walkcount//4], (x,y))
        walkcount += 1
    elif right:
        win.blit(walkRight[walkcount//4], (x,y))
        walkcount += 1
    elif up:
        win.blit(walkUp[walkcount//4], (x,y))
        walkcount += 1
    elif down:
        win.blit(walkDown[walkcount//4], (x,y))
        walkcount += 1
    else:
        win.blit(char, (x,y))
        walkcount = 0

    #Stamina Animation
    if stamina == 24:
        win.blit(sbar[0], (25,10))

    elif stamina < 24 and stamina >= 20:
        win.blit(sbar[1], (25,10))
        
    elif stamina < 20 and stamina >= 16:
        win.blit(sbar[2], (25,10))

    elif stamina < 16 and stamina >= 12:
        win.blit(sbar[3], (25,10))

    elif stamina < 12 and stamina >= 8:
        win.blit(sbar[4], (25,10))

    elif stamina < 8 and stamina >= 4:
        win.blit(sbar[5], (25,10))

    elif stamina < 4 and stamina > 0:
        win.blit(sbar[6], (25,10))
    else:
        win.blit(sbar[7], (25,10))

    pygame.display.update()
    
#Player's Movement
run = True
while run:
    #Refresh speed
    clock.tick(16)
    #Close the game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    #Keyboard keys
    if keys[pygame.K_w] and keys[pygame.K_LSHIFT]:
        if stamina >= 1:
            y -= vel*boost 
            stamina -= 1
        left = False
        right = False
        up = True
        down = False
    elif keys[pygame.K_s] and keys[pygame.K_LSHIFT]:
        if stamina >= 1:
            y += vel*boost
            stamina -= 1
        left = False
        right = False
        up = False
        down = True
    elif keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
        if stamina >= 1:
            x -= vel*boost 
            stamina -= 1
        left = True
        right = False
        up = False
        down = False
    elif keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
        if stamina >= 1:
            x += vel*boost 
            stamina -= 1
        left = False
        right = True
        up = False
        down = False
    elif keys[pygame.K_a]: 
        x -= vel
        left = True
        right = False
        up = False
        down = False
        shift = True
        #Regenerate Stamina
        if stamina < 24:
            stamina += .5
    elif keys[pygame.K_d]: 
        x += vel
        left = False
        right = True
        up = False
        down = False
        if stamina < 24:
            stamina += .5
    elif keys[pygame.K_w]:
        y -= vel
        left = False
        right = False
        up = True
        down = False
        if stamina < 24:
            stamina += .5
    elif keys[pygame.K_s]:
        y += vel
        left = False 
        right = False
        up = False
        down = True
        if stamina < 24:
            stamina += .5
    
    else:
        left = False 
        right = False
        up = False
        down = False
        walkcount = 0
        if stamina < 24:
            stamina += .5
    
    redrawGameWindow()
#end code
pygame.quit()
