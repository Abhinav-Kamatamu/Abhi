import pygame
from pygame.locals import *

pygame.init()

win = pygame.display.set_mode((800, 800))

#   initial square
square_side_length = 500
square_colour = (255, 0, 0)
square_location = ((800 - square_side_length) // 2, (800 - square_side_length) // 2)
pygame.draw.rect(win, square_colour, [square_location[0], square_location[1], square_side_length, square_side_length])

# defifning parameteres for rotating square
rsquare_side_length = 500
rsquare_colour = (255, 0, 0)
rsquare_location = ((800 - rsquare_side_length) // 2, (800 - rsquare_side_length) // 2)
s = pygame.Surface((rsquare_side_length,rsquare_side_length))
for angle in range (0,91):
    s = pygame.transform.rotate(s, angle)
    pygame.draw.rect(win, rsquare_colour, s.get_rect(), 1)
    pygame.display.update()
pygame.display.update()

while True:
    pass