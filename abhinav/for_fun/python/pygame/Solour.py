import pygame
from time import sleep

win = pygame.display.set_mode((300, 300))
win.fill((255, 255, 255))
x = 25
y  = 25
r = 0
g = 0
s20 = [i * 20 for i in range(0, 260 // 20)]
b = 0
for j in range(1, 256):
    s20 = [i*20+j for i in range(0, 260 // 20)]
    for i in range(1, 256):
        pygame.draw.rect(win, (r, g, b), (x, y, 1, 1))
        x += 1
        b += 1
        print(s20)
        if b in s20:
            g +=19
            r += 19
    b = 0
    y += 1
    x = 25
    r =0
    pygame.display.update()
    g = 0
sleep(10)
