import pygame
from time import sleep

win = pygame.display.set_mode((255, 255))
win.fill((255, 255, 255))

pixelsFilled = 0

r = 255
g = 255
b = 255

x = 0
y = 0


def stop():
    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                exit()
        if i.type == pygame.QUIT:
            exit()


def fill():
    global pixelsFilled, r, g, b, x, y

    while pixelsFilled <= 65025:

        pygame.draw.rect(win, (r, g, b), (x, y, 1, 1))

        if x < 255:

            x += 1

            r -= (255 - y) / 255
            g -= (255 - y) / 255

        elif x <= 255:

            x = 0
            y += 1

            r = 255 - y
            g = 255 - y
            b = 255 - y

        pixelsFilled += 1


fill()

pygame.display.update()

while True:
    stop()