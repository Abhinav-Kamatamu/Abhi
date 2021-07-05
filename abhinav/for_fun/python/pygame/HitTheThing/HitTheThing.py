import random
import time
import pygame

pygame.init()

width = 600
height = 650
timespan = (700, 1100)
rounds = 150
rounds_passed = 0

win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

background = pygame.image.load('Board.png')
thing = pygame.image.load('Thing.png')
intro = pygame.image.load('Intro.png')
difficulty = pygame.image.load('Diffficulty.png')

winner = pygame.mixer.Sound('beep1.ogg')


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
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render(f'Live Score :- {item.score}', 1, (255, 0, 0))
        win.blit(text, (20, 15))
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
        board.reset()
        board.display()
        pre_x = self.x
        pre_y = self.y
        while (pre_x, pre_y) == (self.x, self.y):
            self.y = random.randint(0, 2)
            self.x = random.randint(0, 2)
        board.layouter()[self.y][self.x] = 1
        board.display()

    def click(self):
        global rounds_passed
        start = time.time()
        while True:
            for i in range(3):
                for j in range(3):
                    if board.layout[i][j] == 1:
                        if inputs() == i * 3 + j + 1:
                            self.tempScore += 1

            end = time.time()
            if random.randint(timespan[0], timespan[1]) < (end - start) * 1000 < random.randint(timespan[0],
                                                                                                timespan[1]):
                rounds_passed += 1
                break
        if self.tempScore > 0:
            winner.play()
            self.score += 1
            self.tempScore = 0


def introSlide():
    global board, timespan
    notgiven = True
    win.blit(intro, (0, 0))
    pygame.display.update()
    time.sleep(1)
    win.fill((255, 206, 104))
    win.blit(background, (0, 50))
    for alpha in range(300, 0, -4):
        intro.set_alpha(alpha)
        win.blit(difficulty, (0, 0))
        win.blit(intro, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
    while notgiven:
        win.blit(difficulty, (0, 0))
        pygame.display.update()
        if inputs() == 1:
            timespan = (1250, 1750)
            notgiven = False
        elif inputs() == 2:
            notgiven = False
        elif inputs() == 3:
            timespan = (400, 800)
            notgiven = False
    win.blit(difficulty, (0, 0))
    pygame.display.update()
    win.fill((255, 206, 104))
    win.blit(background, (0, 50))
    for alpha in range(300, 0, -4):
        difficulty.set_alpha(alpha)
        win.fill((255, 206, 104))
        win.blit(background, (0, 50))
        win.blit(difficulty, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()


def inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
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
    if keys[pygame.K_1]:
        return 1
    if keys[pygame.K_2]:
        return 2
    if keys[pygame.K_3]:
        return 3


def ending():
    for i in range(0, 3):
        win.fill((0, 0, 0))
        pygame.display.update()
        pygame.time.delay(500)
        text_font = pygame.font.Font('freesansbold.ttf', (width * 4) // 45)
        text_2 = text_font.render('TIME UP', True, (255, 255, 255))
        textrect = text_2.get_rect()
        textrect.center = (width // 2, height // 2)
        win.blit(text_2, textrect)
        pygame.display.update()
        time.sleep(1)
    win.fill((0, 0, 0))
    pygame.display.update()
    text_font = pygame.font.Font('freesansbold.ttf', 32)
    text_3 = text_font.render(f'Your final score was:-  {item.score}', True, (255, 255, 255))
    textrect = text_3.get_rect()
    textrect.center = (width // 2, height // 2)
    win.blit(text_3, textrect)
    pygame.display.update()
    time.sleep(2)
    exit()


board = Board()
item = Thing()
introSlide()
while True:
    item.get_random_board()
    item.click()
    if rounds_passed >= rounds:
        ending()
