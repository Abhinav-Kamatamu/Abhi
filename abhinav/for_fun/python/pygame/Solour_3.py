import pygame
from time import sleep

win = pygame.display.set_mode((300, 300))
win.fill((255, 255, 255))
x = 25
y = 25
r = 0
g = 0
s20 = [i * 20 for i in range(0, 260 // 20)]
b = 0


def quit():
    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                exit()
        if i.type == pygame.QUIT:
            exit()


for j in range(1, 256):
    s20 = [i * 20 - j for i in range(0, 260 // 20)]
    for i in range(1, 256):
        pygame.draw.rect(win, (r, g, b), (x, y, 1, 1))
        b += 1
        x += 1
        if b in s20:
            r += 19
            g += 19
    y += 1
    r = 0
    g = 0
    x = 25
    b = 0
    quit()
print(s20)
pygame.display.update()
while True:
    quit()
sleep(100)
