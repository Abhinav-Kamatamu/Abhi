import random
import time
import pygame

pygame.init()

# ---------------------------variables-----------------------

# ------------------------------Changeables----------------

pcol = (0, 255, 255)  # Player color
w = 300  # Window Width
fps = w // 10  # FPS of the game
duration = 2  # Time for which the program will run
bcol = (255, 255, 0)  # Color of block
score_give = 3  # Point at which the score increases

# ------------------------------Changeables----------------

clock = pygame.time.Clock()
h = w  # Window Height
win = pygame.display.set_mode((w, h))  # Screen of the game
pygame.display.set_caption('Escape or die')
x = w // 2 - (w // 10 / 2)  # X coordinate of the player
y = h + h // 100 - (w // 10 / 2) - h // 10  # Y coordinate of the player
s = 300 // 10  # Size of Player
speed = w // 200 + 4  # Speed of the game
score = 0  # Score of the player
run = True  # States whether the code is running
scorer = 0  # If decrease the chance of getting a score
timer = pygame.time.get_ticks()  # Counts the time for which the game has been running
ender = duration * (60 * 1000)  # Makes the time limit into minutes

# --------------------------------Block-------------------

no_blocks = w // 60  # No of obstacles
T = [pygame.time.get_ticks() for i in range(no_blocks)]  # Different spawn time for each block
Bs = 300 // 9  # Block size
Bx = [random.randint(0, w - Bs) for _ in range(no_blocks)]  # Different x coordinate of each obstacle
By = [-Bs for _ in range(no_blocks)]  # Different y coordinate of each obstacle
S = [None for _ in range(no_blocks)]  # Allows the block to follow the time of spawning
C = [random.randint(1, 15) for _ in range(no_blocks)]  # range of variations in block spawn time


# --------------------------------Block--------------------
# ---------------------------variables-----------------------


# Function to display the player
def draw():
    global win, x, y, s, player, speed
    player = pygame.draw.rect(win, pcol, (x, y, s, s))
    pygame.draw.rect(win, (0, 0, 0), (x, y, s, s), 1)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if x <= 5:
            pass
        else:
            x -= w // 200 + 6
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if x + Bs >= w:
            pass
        else:
            x += w // 200 + 6


# Function to display the blocks
def block(i):
    global S, T, Bx, By, h, win, Bs, C, speed, scorer, score
    S[i - 1] = pygame.time.get_ticks()
    if S[i - 1] - T[i - 1] >= C[i - 1] * 1000:
        pygame.draw.rect(win, bcol, (Bx[i - 1], By[i - 1], Bs, Bs))
        pygame.draw.rect(win, (0, 0, 0), (Bx[i - 1], By[i - 1], Bs, Bs), 1)
        pygame.display.update()
        By[i - 1] += speed
        if By[i - 1] > h + Bs:
            By[i - 1] = -Bs
            Bx[i - 1] = int(random.randint(0, w - Bs))
            scorer += 1
        key = pygame.key.get_pressed()

        if key[pygame.K_s] or key[pygame.K_DOWN]:
            pass
        else:
            for jx in range(Bx[i - 1], Bx[i - 1] + Bs):
                for jy in range(By[i - 1], By[i - 1] + Bs):
                    if player.collidepoint(jx, jy):
                        print('\n\n\nSystem Alert!!!\nYou Lost!\n\tSCORE:-', score)
                        exit()


while run:
    if 100 < score < 200:
        win.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    else:
        win.fill((255, 255, 255))
    draw()
    for i in range(no_blocks):
        block(i + 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('\n\n\nSystem Alert!!!\nYou Lost!\n\tSCORE:-', score)
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
        print('\n\n\nSystem Alert!!!\nYou Lost!\n\tSCORE:-', score)
        break
    if scorer >= score_give:
        score += 1
        scorer = 0
    if score == 30:
        speed = w // 200 + 5
    clock.tick(fps)
