import pygame

pygame.init()
win = pygame.display.set_mode((1000, 100))
win.fill((255, 255, 255))
pygame.display.update()
pygame.time.delay(2000)
fade = pygame.Surface((1000, 100))
fade.fill((0, 0, 255))
for i in range(0, 50):
    fade.set_alpha(i)
    win.blit(fade, (0, 0))
    pygame.display.update()
    pygame.time.delay(30)
win.fill((0,0,255))
pygame.time.delay(100)
pygame.display.update()