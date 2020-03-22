import pygame,sys,time
from pygame.locals import *
pygame.init()

fps = 60
clock = pygame.time.Clock()

width = 1200
height=1000
neg = 0
y = height - (height/10)
x = width/2
velcro = 5
side = 50

win = pygame.display.set_mode((width,height))
win.fill((255,255,255))
co = 0
pygame.display.set_caption(f'YOUR   SCORE   IS      :-  {co}')

# colours
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

def move_around_like_a_monster():
    global x,y
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        x += velcro
    if key[pygame.K_LEFT]:
        x -= velcro
    if key[pygame.K_DOWN]:
        y += velcro
    if key[pygame.K_UP]:
        y -= velcro
    if key[pygame.K_SPACE]:
        jump(50)
    
def redraw():
    global white, red,x,y,side
    win.fill(white)
    pygame.draw.rect(win,red,(x,y,side,side))
    pygame.display.update

def jump(height):
    global neg, y
    if neg < height:
            y += 1
            neg += 1
    if neg > height:
        neg = 0
         
def main():
    while True:
        clock.tick(fps)
        redraw()
        move_around_like_a_monster()       
        
main()        