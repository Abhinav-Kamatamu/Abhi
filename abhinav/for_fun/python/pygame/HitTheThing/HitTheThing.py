import random
import time
import pygame

pygame.init()
count = 0

width = 600
height = 650

win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

background = pygame.image.load('Board.png')
thing = pygame.image.load('Thing.png')

winer = pygame.mixer.Sound('beep1.ogg')


class Board:
    def __init__(self):
        self.layout = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def getPositon(self):
        for i in range(3):
            for j in range(3):
                if self.layout[i][j] == 1:
                    return 37 + j * 200, 66 + i * 200
        else:
            return False

    def display(self):
        win.fill((255, 206, 104))
        win.blit(background, (0, 50))
        if self.getPositon() != False:
            win.blit(thing, (self.getPositon()))
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(f'Live Score :- {item.score}',0,(255,0,0))
        win.blit(text, (5, 10))
        pygame.display.update()


    def layouter(self):
        return self.layout

    def reset(self):
        self.layout = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]


class Thing:
    def __init__(self):
        self.thing = thing.get_rect()
        self.score = 0
        self.tempScore = 0
        self.y = random.randint(0, 2)
        self.x = random.randint(0, 2)


    def get_random_board(self):
        global count
        count += 1
        board.reset()
        pre_x = self.x
        pre_y = self.y
        while (pre_x, pre_y) == (self.x,self.y):
            self.y = random.randint(0, 2)
            self.x = random.randint(0, 2)
        board.layouter()[self.y][self.x] = 1
        board.display()

    def click(self):
        start = time.time()
        while True:
            for i in range(3):
                for j in range(3):
                    if board.layout[i][j] == 1:
                        if inputs() == i * 3 + j + 1:
                            self.tempScore += 1

            end = time.time()
            if random.randint(700, 1100) < (end - start) * 1000 < random.randint(700, 1100):
                break
        if self.tempScore > 0:
            winer.play()
            self.score += 1
            self.tempScore = 0

def intro():
    global board
    intro = pygame.image.load('Intro.png')
    win.blit(intro, (0, 0))
    pygame.display.update()
    time.sleep(1)
    win.fill((255, 206, 104))
    win.blit(background, (0, 50))
    for alpha in range(300,0,-4):
        intro.set_alpha(alpha)
        win.fill((255, 206, 104))
        win.blit(background, (0, 50))
        win.blit(intro, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
def inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_7]:
        return 1
    if keys[pygame.K_KP_8]:
        return 2
    if keys[pygame.K_KP_9]:
        return 3
    if keys[pygame.K_KP_4]:
        return 4
    if keys[pygame.K_KP_5]:
        return 5
    if keys[pygame.K_KP_6]:
        return 6
    if keys[pygame.K_KP_1]:
        return 7
    if keys[pygame.K_KP_2]:
        return 8
    if keys[pygame.K_KP_3]:
        return 9

board = Board()
item = Thing()
intro()
starter = time.time()
while True:
    item.get_random_board()
    item.click()
    ender =time.time()
    if ender-starter >= 120:
        exit()
