import random as r
import pygame
from pygame.locals import *

pygame.init()

# ----------------------------------------------Variables

# ---------------------------------------------General Variables
w = 800
h = w
fps = 60
clock = pygame.time.Clock()
speed = w // 100
score = 0
# ---------------------------------------------General Variables

# ---------------------------------------------Line Variables
line_col_1 = (0, 0, 0)
line_x_start_1 = r.randint(0, w / 2)
line_x_end_1 = r.randint(0, w / 2)
line_y = h
line_col = (0, 0, 0)
line_x_start = r.randint(w // 2, w)
line_x_end = r.randint(w // 2, w)
# ---------------------------------------------General Variables

# ---------------------------------------------Player's variables
player_w = 40/500 * w
player_h = player_w
player_x = w // 2 - player_w // 2
player_y = h // 8
player_col = (255, 0, 0)
# ---------------------------------------------Player's variables

# ---------------------------------------------Variables
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Abhinav\'s PROGRAM')
win.fill((255, 255, 255))
pygame.display.update()
player = pygame.draw.rect(win, player_col, (player_x, player_y, player_w, player_h))


def escape():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        exit()


def player_block():
    global win, player, player_x, player_y, player_w, player_h
    player = pygame.draw.rect(win, player_col, (player_x, player_y, player_w, player_h))
    keys = pygame.key.get_pressed()
    if player_x <= w - player_w:
        if keys[K_RIGHT] or keys[K_a]:
            player_x += speed
    if player_x >= 0:
        if keys[K_LEFT] or keys[K_d]:
            player_x -= speed


def obstcal_1():
    global line_col_1, score, line_y, player, line_x_start_1, line_x_end_1, line_x_start, line_x_end
    pygame.draw.line(win, line_col_1, (line_x_start_1, line_y), (line_x_end_1, line_y), 2)
    line_y -= speed
    if line_y <= 0:
        line_y = h
        line_x_start_1 = r.randint(0, w // 2)
        line_x_end_1 = r.randint(0, w // 2)
        line_x_start = r.randint(w // 2, w)
        line_x_end = r.randint(w // 2, w)
    for jx in range(line_x_start_1, line_x_end_1):
        if player.collidepoint(jx, line_y):
            line_y += speed


def obstcal():
    global line_col, line_y, player, line_x_start, line_x_end
    pygame.draw.line(win, line_col, (line_x_start, line_y), (line_x_end, line_y), 2)
    for jy in range(line_x_start, line_x_end):
        if player.collidepoint(jy, line_y):
            line_y += 1


while True:
    win.fill((255, 255, 255))
    obstcal()
    obstcal_1()
    player_block()
    escape()
    pygame.display.update()
    clock.tick(fps)
