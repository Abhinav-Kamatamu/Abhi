import pygame,sys,random
from pygame.locals import *
pygame.init()
w=1280
h=700
a=700
b=700
obj=['rock.png','paper.jpg','scissors.jpg']
#w=int(input('enter the width'))
#h=int(input('enter the hight'))
wind=pygame.display.set_mode((w,h))

def background(image,w,h):
    surf= pygame.image.load(image)
    surf_1=pygame.transform.scale(surf,(w,h))
    s=wind.blit(surf_1,[0,0])
    pygame.display.update()

def test_background():
    background('wallpaper.png',w,h)

def image(image,w,h,x,y,x_1,x_2):
    lx=x/y*w
    ly=x_1/x_2*h
    surf= pygame.image.load(image)
    surf_1=pygame.transform.scale(surf,(w,h))
    s=wind.blit(surf_1,(lx,ly))
    pygame.display.update()
def test_image():
    image('rock.png',400,400,2,3,3,4)
def close():
    for i in pygame.event.get():
        if i.type==QUIT:
            pygame.quit()
            sys.exit()
def win_display():
    if win=='player':
        font=pygame.font.Font('freesansbold',32)
        text=font.render('the player has won',True,(0,0,255))
        textrect=text.get_rect()
        wind.blit(text,textrect)
        pygame.display.update()
        pygame.quit()
        exit()
    if win=='ai':
        font=pygame.font.Font('freesansbold',32)
        text=font.render('the computer has won',True,(0,0,255))
        textrect=text.get_rect()
        wind.blit(text,textrect)
        pygame.display.update()
        exit()
def set_caption(pers):
        pygame.display.set_caption(f' ai score is{b} and player score is{a}')
def get_check():
    ai_play = random.choice(obj)
    
    keys=pygame.key.get_pressed()
    if keys[pygame.K_r]:
        pl_play='rock'
        image(ai_play,400,400,1,5,3,4)
        image('rock.png',400,400,2,3,3,4)
    if keys[pygame.K_s]:
        pl_play='scissors'
        image(ai_play,400,400,1,5,3,4)
        image('scissor.png',400,400,2,3,3,4)
    if keys[pygame.K_p]:
        pl_play='paper'
        image(ai_play,400,400,1,5,3,4)
        image('paper.png',400,400,2,3,3,4)
    if ai_play=='rock' and pl_play=='paper':
        set_caption('player')
        a+=1
    if ai_play=='rock'and pl_play=='rock':
        set_caption('none')
    if ai_play=='rock'and pl_play=='scissors':
        set_caption('ai')
        b+=1
    if ai_play=='paper' and pl_play=='paper':
        set_caption('none')
    if ai_play=='paper'and pl_play=='rock':
        set_caption('ai')
        b+=1
    if ai_play=='paper'and pl_play=='scissors':
        set_caption('player')
        a+=1
    if ai_play=='scissors' and pl_play=='paper':
        set_caption('ai')
        b+=1
    if ai_play=='scissors'and pl_play=='rock':
        set_caption('player')
        a+=1
    if ai_play=='scissors'and pl_play=='scissors':
        set_caption('none')

while True:
    set_caption('po')
    get_check()
    if a==5:
        win='player'
        win_display()
    if b==5:
        win=='a1'
        win_display()
    close()
    
        
        
    