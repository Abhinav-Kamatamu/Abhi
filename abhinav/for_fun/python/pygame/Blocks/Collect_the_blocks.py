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

# ---------------------------variables-----------------------

# ------------------------------Changeables----------------

pcol = (0, 255, 255)  # Player color
w = 300  # Window Width
fps = w // 10  # FPS of the game
duration = 2  # Time for which the program will run
bcol = (255, 255, 0)  # Color of block

# ------------------------------Changeables----------------

clock = pygame.time.Clock()  # Clock of the game
h = w  # Window Height
win = pygame.display.set_mode((w, h))  # Screen of the game
pygame.display.set_caption('Collect or die')
x = w // 2 - (w // 10 / 2)  # X coordinate of the player
y = h + 10 - (h // 10 / 2) - h // 10  # Y coordinate of the player
s = 300 // 10  # Size of Player
speed = w // 200 + 4  # Speed of the game
score = 0  # Score of the player
checker = False  # If collided or not
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
    global win, x, y, s, player, speed, pcol
    player = pygame.draw.rect(win, pcol, (x, y, s, s))
    pygame.draw.rect(win, (0, 0, 0), (x, y, s, s), 1)
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


# Function to display the blocks
def block(i):
    global S, T, Bx, By, w, win, Bs, C, speed, score, checker, bcol
    S[i - 1] = pygame.time.get_ticks()
    if S[i - 1] - T[i - 1] >= C[i - 1] * 1000:
        pygame.draw.rect(win, bcol, (Bx[i - 1], By[i - 1], Bs, Bs))
        pygame.draw.rect(win, (0, 0, 0), (Bx[i - 1], By[i - 1], Bs, Bs), 1)
        By[i - 1] += speed
        if By[i - 1] > w + Bs:
            By[i - 1] = -Bs
            Bx[i - 1] = random.randint(0, w - Bs)
            keys = pygame.key.get_pressed()
            score -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                score += 1
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


def stop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('\n\n\n\n\nAbhinav\'s Game Says,\'Your score was {}'.format(score))
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print('\n\n\n\n\nAbhinav\'s Game Says,\'Your score was {}'.format(score))
                exit()


while True:
    if 50 < score < 100:
        win.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    else:
        win.fill((255, 255, 255))
    draw()
    for i in range(no_blocks):
        block(i + 1)
    stop()
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
    elif score == 100:
        speed = w // 200 + 8
    clock.tick(fps)
