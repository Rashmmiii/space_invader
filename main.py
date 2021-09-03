import pygame
import random
import math
import time
import os
from pygame import mixer

#Dafont -site for downloading free font

#intialize the pygame
pygame.init()
pygame.mixer.init()

#create the screen
WIDTH, HEIGHT = 800, 600
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
screen=pygame.display.set_mode((800,600))

background=pygame.image.load("background.png")

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerimg=pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0
playerY_change=0

#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

#game over
overfont=pygame.font.Font('freesansbold.ttf',64)

def showscore(x,y):
    score=font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    overtxt=overfont.render("GAME OVER",True,(255,255,255))
    screen.blit(overtxt,(200,210))
    finalscore=score_value
    overtxt1=overfont.render("FINAL SCORE : "+str(finalscore),True,(255,255,255))
    screen.blit(overtxt1,(170,280))

lvlspeed=[0,7,10,14,17,21]
level=1
health=100
lives_label = font.render(f"Lives: {health}", 1, (255,255,255))
level_label = font.render(f"Level: {level}", 1, (255,255,255))


def showlvl():
    screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
    screen.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 20+level_label.get_height()))

#enemy
#Ready - you can't see the bullet
#fire - the bullet is currently in mootion
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
numenemies=6

for i in range(numenemies):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(6)
    enemyY_change.append(40)


#bullet
bulletimg=pygame.image.load('bullet.png')
bulletX=0
bulletY=playerY
bulletX_change=0
bulletY_change=10
bullet_state="ready"

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    if bullet_state=="fire":
        distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
        if distance < 27:
            return True
        else:
            return False


def isout(enemyX,enemyY,playerX,playerY):
    distance=math.sqrt((math.pow(enemyX-playerX,2))+(math.pow(enemyY-playerY,2)))
    if distance < 40:
        return True
    else:
        return False

global out

FPS=60
clock = pygame.time.Clock()

#game loop
running=True
while running:
    #RGB = red , green , blue
    clock.tick(FPS)
    screen.fill((0,0,0))

    #background image
    screen.blit(background,(0,0))

    #every event gets locked inside pygame.event.get()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #if keystroke is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-8
            if event.key==pygame.K_RIGHT:
                playerX_change=8
            if event.key==pygame.K_DOWN:
                playerY_change=5
            if event.key==pygame.K_UP:
                playerY_change=-5
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bulletsound=pygame.mixer.Sound('laser.wav')
                    bulletsound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,playerY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
            if event.key==pygame.K_DOWN or event.key==pygame.K_UP:
                playerY_change=0

    #player movement
    playerX+=playerX_change
    playerY+=playerY_change

    if playerX<=0:
        playerX=0
    if playerX>=736:
        playerX=736

    if playerY<=0:
        playerY=0
    if playerY>=536:
        playerY=536

    #enemy movement
    for i in range(numenemies):

        #game over
        out=isout(enemyX[i],enemyY[i],playerX,playerY)
        if out:
            for j in range(numenemies):
                enemyY[j]=20000
            game_over_text()
            break
        
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=lvlspeed[level]
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-lvlspeed[level]

            enemyY[i]+=enemyY_change[i]
        
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            expsound=pygame.mixer.Sound('explosion.wav')
            expsound.play()
            bulletY=playerY
            bullet_state="ready"
            score_value+=1
            if(score_value==10):
                level+=1
            elif(score_value==30):
                level+=1
            elif(score_value==50):
                level+=1
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)
            
        enemy(enemyX[i],enemyY[i],i)

    if out==True:
        game_over_text()
        pygame.display.update()
        time.sleep(3.5)    # Pause 5.5 seconds
        # score_value=0
        break  
    
    
    #bullet movement
    if bulletY<=0:
        bulletY=playerY
        bullet_state="ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    
    showscore(textX,textY)
    showlvl()
    
    player(playerX,playerY)
    # enemy(enemyX,enemyY)
    pygame.display.update()
    
