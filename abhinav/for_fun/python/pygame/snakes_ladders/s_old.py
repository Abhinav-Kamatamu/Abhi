import random
import pygame,sys
from pygame.locals import *
pygame.init()
from time import sleep
name=input("enter first person's name:-  ")
name_2=input("enter second person name person's name:-  ")
print(name,'is red')
print(name_2,'is blue')
bg=pygame.image.load('Abhinav_18.jpg')
a=0
b=0
mx=0
my=0
h=400
x=15
y=15
care=4
go=True
w=400
bg=pygame.transform.scale(bg,(h,w))
win=pygame.display.set_mode((w,h))
pygame.display.set_caption('snakes and ladders')
def roling (pn):
    num=random.randint(1,6)
    if num==6:
        num=num+random.randint(1,6)
        if num==12:
            num=num+random.randint(1,6)
            if num==18:
                num==0

    return(num)
def position(p,p2):
    win.blit(bg,(0,0))
    c=p
    d=p2
    xpos={0:15,1:'45',2:'83',3:'113',4:'150',5:'182',6:'215',7:'248',8:'285',9:'317',10:'351',11:'351',12:'317',13:'285',14:'248',15:'215',16:182,17:150,18:113,19:83,20:45,21:45,22:85,23:113,24:147,25:182,26:215,27:248,28:285,29:317,30:351 ,31:351,32:317,33:285,34:248,35:215,36:182,37:150,38:113,39:83,40:45,41:45,42:85,43:113,44:147,45:182,46:215,47:248,48:285,49:317,50:351,51:351,52:317,53:285,54:248,55:215,56:182,57:150,58:113,59:83,60:45,61:45,62:85,63:113,64:147,65:182,66:215,67:248,68:285,69:317,70:351,71:351,72:317,73:285,74:248,75:215,76:182,77:150,78:113,79:83,80:45,81:45,82:85,83:113,84:147,85:182,86:215,87:248,88:285,89:317,90:351,91:351,92:317,93:285,94:248,95:215,96:182,97:150,98:113,99:83,100:45}
    ypos={0:355,1:355,2:355,3:355,4:355,5:355,6:355,8:355,7:355,10:355,9:355,11:320,12:320,13:320,14:320,15:320,16:320,17:320,18:320,19:320,20:320,21:285,22:285,23:285,24:285,25:285,26:285,27:285,28:285,29:285,30:285,31:248,32:248,33:248,34:248,35:248,36:248,37:248,38:248,39:248,40:248,41:215,42:215,43:215,44:215,45:215,46:215,47:215,48:215,49:215,50:215,51:182,52:182,53:180,54:182,55:182,56:182,57:182,58:182,59:182,60:182,61:147,62:147,63:147,64:147,65:147,66:147,67:147,68:147,69:147,70:147,71:113,72:113,73:113,74:113,75:113,76:113,77:113,78:113,79:113,80:113,81:83,82:83,83:83,84:83,85:83,86:83,87:83,88:83,89:83,90:83,91:45,92:45,93:45,94:45,95:45,96:45,97:45,98:45,99:45,100:45}

    xploc_p=int(xpos[c])
    yploc_p=int(ypos[c])
    xploc_p2=int(xpos.get(d))
    yploc_p2=int(ypos.get(d))
    pygame.draw.circle(win,(255,0,0),(xploc_p,yploc_p),x,y)
    pygame.draw.circle(win,(0,0,255),(xploc_p2,yploc_p2),x,y)
    pygame.display.update()


while go:
    p_a=a
    p_b=b
    sleep(3)
    pygame.time.delay(50)
    position(a,b)
    sleep(1)
    a+=roling(name)
    if a==100:
        position(a,b)
        sleep(2)
        pygame.font.init()
        p1_win=name,'has won'
        font=pygame.font.Font('freesansbold.ttf', 32)
        text=font.render('see! the game is won',True,(0,0,0),(255,255,255))
        textrect=text.get_rect()
        textrect.center=(w/2,h/2)
        win.blit(text,textrect)
        pygame.display.update()
        break
    if a>100:
        a=p_a
    position(a,b)
    if a==8:
        a= 26
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==19:
        a= 38
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==26:
        a= 53
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==21:
        a= 82
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==36:
        a= 57
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
        position(a,b)
    if a==50:
        a= 91
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==54:
        a= 88
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==61:
        a= 99
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==62:
        a= 96
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==66:
        a= 87
        print (name,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if a==46:
        a= 15
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)

    if a==48:
        a= 9
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)
    if a==52:
        a= 11
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)
    if a==59:
        a= 18
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)
    if a==64:
        a= 24
        print (name,' has been eaten by a snake')
        sleep(3)
    if a==68:
        a= 2
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)
    if a==69:
        a= 33
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)
    if a==83:
        a= 22
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)
    if a==93:
        a= 37
        print (name,' has been eaten by a snake')
        sleep(3)
        position(a,b)
    if a==98:
        a= 13
        print (name,' has been eaten by a snake')
        sleep(3)

    previous_b=b
    b=b+roling(name_2)
    sleep(3)
    if b==100:
        position(a,b)
        sleep(2)
        p2_win=(name_2,'has won')
        font=pygame.font.Font('freesansbold.ttf', 32)
        
        text=font.render('see! the game is won',True,(0,0,0),(255,255,255))
        textrect=text.get_rect()
        textrect.center=(w/2,h/2)
        win.blit(text,textrect)
        pygame.display.update()
        break
    if b>100:
        b=previous_b


    if b==8:
        b= 26
        print (name_2,' has climbed a ladder')
        sleep(3)

    if b==19:
        b= 38
        print (name_2,' has climbed a ladder')
        sleep(3)
    if b==28:
        b= 53
        print (name_2,' has climbed a ladder')
        sleep(3)
    if b==21:
        b= 82
        print (name_2,' has climbed a ladder')
        sleep(3)
        position(a,b)
    if b==36:
        b= 57
        print (name_2,' has climbed a ladder')
        sleep(3)
        position(a,b)


    if b==50:
        b= 91
        print (name_2,' has climbed a ladder')
        sleep(3)
    if b==54:
        b= 88
        print (name_2,' has climbed a ladder')
        sleep(3)
    if b==61:
        b= 99
        print (name_2,' has climbed a ladder')
        sleep(3)
    if b==62:
        b= 96
        print (name_2,' has climbed a ladder')
        sleep(3)
    if b==66:
        b= 87
        print (name_2,' has climbed a ladder')
        sleep(3)
    if b==46:
        b= 15
        print (name_2,' has been eaten by a snake')
        sleep(3)

    if b==48:
        b= 9
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==52:
        b= 11
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==59:
        b= 18
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==64:
        b= 24
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==68:
        b= 2
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==69:
        b= 33
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==83:
        b= 22
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==93:
        b= 37
        print (name_2,' has been eaten by a snake')
        sleep(3)
    if b==98:
        b= 13
        print (name,' has been eaten by a snake')
        sleep(3)
    for event in pygame.event.get():
        if event.type==QUIT:

            pygame.quit()
            go=False
sleep(5)
font_2=pygame.font.Font('freesansbold.ttf', 16)
great=font_2.render('Abhinav wrote the whole programe on his own',True,(0,0,0),(255,255,255))
greatrect=great.get_rect()
greatrect.center=(w/2,h/2)
win.blit(great,greatrect)
pygame.display.update()
sleep(3)
pygame.quit()
            
