import pygame
from pygame.locals import *

w = 50
rows = w // 10
h = 1
for i in range(1, rows + 1):
    h = h * 2
win = pygame.display.set_mode((w, h))

win.fill((255, 255, 255))


class Block:
    def __init__(self, s):
        self.amount = s
        self.size = s * 2

    def display(self):
        pygame.draw.rect(win, (0, 0, 0), [((self.amount - 1) * w // rows), h - self.size, w // rows, self.size, ], 1)
        pygame.display.update()


blocks = [Block(i) for i in range(1, rows + 1)]

for i in blocks:
    i.display()

while True:
    pass
