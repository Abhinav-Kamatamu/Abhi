import pygame, random, time
from pygame.locals import *
pygame.init()

#--variables--
pcol = input('Enter color[Yellow,Green,Blue,LightBlue,Red,Black]  ')
if pcol == 'Yellow':
    pcol = (255,255,0)
    
elif pcol == 'Green':
    pcol=(0,255,0)
elif pcol == 'Blue':
    pcol = (0,0,255)
elif pcol == 'LightBlue':
    pcol = (0,255,255)
elif pcol == 'Red':
    pcol = (255,0,0)
else:
    pcol = (0,0,0)
clock = pygame.time.Clock()
w = 300
fps = w//10
h = w
win = pygame.display.set_mode((w,h))
pygame.display.set_caption('Escape or die')
x = w//2-(w//10/2)
y = h+h//100-(h//10/2)-h//10
s = w//10
speed = w//200 + 7
score = 0
run = True
scorer = 0
timer = pygame.time.get_ticks()
ender = 120000
#----Block----
T = [pygame.time.get_ticks() for i in range(5)]
Bs = w//9
Bx = [random.randint(0, w - Bs) for _ in range(5)]
By = [-Bs for _ in range(5)]
S = [None for _ in range(5)]
C = [random.randint(1,15) for _ in range(5)]
bcol = (0,0,0)
#----Block----
#--variables--

def draw():
    global win, x, y,s, player, speed
    player = pygame.draw.rect(win,pcol,(x,y,s,s))
    pygame.draw.rect(win,(0,0,0),(x,y,s,s),1)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if x<= 0:
            pass
        else:
            x -= speed + 2
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if x +Bs >= w:
            pass
        else:
            x += speed + 2



def block(i):
    global S,T,Bx,By,w,win,Bs,C,speed,scorer, score
    S[i-1] = pygame.time.get_ticks()
    if S[i-1]-T[i-1] >= C[i-1]*1000:
        pygame.draw.rect(win,bcol,(Bx[i-1],By[i-1],Bs,Bs),1)
        pygame.display.update()
        By[i-1] += speed
        if By[i-1] > w + Bs:
            By[i-1] = -Bs
            Bx[i-1] = random.randint(0, w-Bs)
            scorer += 1
            scorer += 1
            scorer += 1
            scorer += 1
        key = pygame.key.get_pressed()

        if key[pygame.K_s] or key[pygame.K_DOWN]:
            pass
        else:
             for jx in range(Bx[i-1],Bx[i-1] + Bs):
                for jy in range (By[i-1],By[i-1] + Bs):
                    if player.collidepoint(jx,jy):
                        print(f'\n\n\n\n\n\n\n\nAbhinav\'s Game Says,\t\'Your score was {score}\'')
                        exit()
while run:
    if score > 100 and score < 200:
        win.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    else:
        win.fill((255,255,255))
    draw()
    block(1)
    block(2)
    block(3)
    block(4)
    block(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f'\n\n\n\n\n\n\n\nAbhinav\'s Game Says,\'Your score was {score}\'')
            exit()
    _type_=pygame.font.Font('freesansbold.ttf',(w*4)//100)
    text=_type_.render(f'Score:- {score}',True,(255,0,0))
    textrect=text.get_rect()
    textrect.topleft = (0,0)
    win.blit(text,textrect)
    pygame.display.update()
    now = pygame.time.get_ticks()
    if now - timer >= ender:
        for i in range(0,3):
            win.fill((0,0,0))
            pygame.display.update()
            pygame.time.delay(500)
            _type_=pygame.font.Font('freesansbold.ttf',(w*4)//45)
            text=_type_.render('TIME UP',True,(255,255,255))
            textrect=text.get_rect()
            textrect.center = (w//2,h//2)
            win.blit(text,textrect)
            pygame.display.update()
            time.sleep(1) 
        print(f'\n\n\n\n\n\nAbhinav\'s Game Says,\'Your score was {score}\'')
        break
    if scorer > 3:
        score += 1
        scorer = 0
    clock.tick(fps)