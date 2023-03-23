import pygame
from time import sleep
import math

pygame.init()

win = pygame.display.set_mode((800, 800))
win.fill((255, 255, 255))
rsquare_side_length = 500
rsquare_colour = (255, 0, 0)
rsquare_location = ((800 - rsquare_side_length) // 2, (800 - rsquare_side_length) // 2)

for angle in range(0, 91):
    s = pygame.Surface((int(rsquare_side_length * math.sin(angle) / math.cos(angle) * (math.sin(angle) + math.cos(angle))),
                        int(rsquare_side_length * math.sin(angle) / math.cos(angle) * (math.sin(angle) + math.cos(angle)))))
    win.blit(pygame.transform.rotate(s, angle), (100, 100))
    # rsquare = s.get_rect()
    # rsquare.center = (400,400)
    # pygame.draw.rect(win, rsquare_colour, rsquare, 1)
    pygame.display.update()
    win.fill((255, 255, 255))
    sleep(0.1)
