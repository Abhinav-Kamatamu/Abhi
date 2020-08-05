import random
import time
import pygame

pygame.init()

ask = input('Do you know the rules?[Yes, no]')
ask = ask.lower()

if ask == "no":
    print('''
----RULES----
    
    You will have 2 minutes to collect blocks
    If your score reaches -5 you die
    
----RUlES----
''')
    time.sleep(5)
# --variables--
clock = pygame.time.Clock()
w = 300
pcol = (0, 255, 255)
fps = w // 10
h = w
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Collect or die')
x = w // 2 - (w // 10 / 2)
y = h + 10 - (h // 10 / 2) - h // 10
s = 300 // 10
speed = w // 200 + 4
score = 0
no_blocks = w // 60
checker = False
timer = pygame.time.get_ticks()
ender = 120000
# ----Block----
T = [pygame.time.get_ticks() for i in range(no_blocks)]
bcol = (255, 255, 0)
Bs = 300 // 9
Bx = [random.randint(0, w - Bs) for _ in range(no_blocks)]
By = [-Bs for _ in range(no_blocks)]
S = [None for _ in range(no_blocks)]
C = [random.randint(1, 15) for _ in range(no_blocks)]


# ----Block----
# --variables--

def draw():
    global win, x, y, s, player, speed, pcol
    player = pygame.draw.rect(win, pcol, (x, y, s, s))
    pygame.draw.rect(win, (0, 0, 0), (x, y, s, s), 1)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if x <= 0:
            pass
        else:
            x -= w // 200 + 6
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if x + Bs >= w:
            pass
        else:
            x += w // 200 + 6


def block(i):
    global S, T, Bx, By, w, win, Bs, C, speed, score, checker, bcol
    S[i - 1] = pygame.time.get_ticks()
    if S[i - 1] - T[i - 1] >= C[i - 1] * 1000:
        pygame.draw.rect(win, bcol, (Bx[i - 1], By[i - 1], Bs, Bs))
        pygame.draw.rect(win, (0, 0, 0), (Bx[i - 1], By[i - 1], Bs, Bs), 1)
        pygame.display.update()
        By[i - 1] += speed
        if By[i - 1] > w + Bs:
            By[i - 1] = -Bs
            Bx[i - 1] = random.randint(0, w - Bs)
            score -= 1
        key = pygame.key.get_pressed()

        for jx in range(Bx[i - 1], Bx[i - 1] + Bs):
            for jy in range(By[i - 1], By[i - 1] + Bs):
                if player.collidepoint(jx, jy):
                    checker = True
                    By[i - 1] = -Bs
                    Bx[i - 1] = random.randint(0, w - Bs)
        if checker:
            score += 1
            checker = False


while True:
    if 50 < score < 100:
        win.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    else:
        win.fill((255, 255, 255))
    draw()
    for i in range(no_blocks):
        block(i + 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('\n\n\n\n\nAbhinav\'s Game Says,\'Your score was {}'.format(score))
            exit()
    _type_ = pygame.font.Font('freesansbold.ttf', (w * 4) // 100)
    text = _type_.render('Score:- {}'.format(score), True, (255, 0, 0))
    textrect = text.get_rect()
    textrect.topleft = (0, 0)
    win.blit(text, textrect)
    pygame.display.update()
    now = pygame.time.get_ticks()
    if now - timer >= ender:
        for i in range(0, 3):
            win.fill((0, 0, 0))
            pygame.display.update()
            pygame.time.delay(500)
            _type_ = pygame.font.Font('freesansbold.ttf', (w * 4) // 45)
            text = _type_.render('TIME UP', True, (255, 255, 255))
            textrect = text.get_rect()
            textrect.center = (w // 2, h // 2)
            win.blit(text, textrect)
            pygame.display.update()
            time.sleep(1)

        print('\n\n\n\n\n\nAbhinav\'s Game Says,\'Your score was {}\''.format(score))
        exit()
    if score == -5:
        print('\n\n\n\n\n\nAbhinav\'s Game Says,\'You died as your score was -5\'')
        exit()
    if score == 30:
        speed = w // 200 + 5
    elif score == 50:
        speed == w // 200 + 6
    elif score == 80:
        speed == w // 200 + 7
    elif score == 100:
        speed = w // 200 + 8
    clock.tick(fps)
