import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.mixer_music.load("/home/abhinav/Desktop/Abhi/abhinav/for_fun/python/pygame/Songs/Song.mp3")
pygame.mixer_music.set_volume(0.8)
print(pygame.mixer_music.get_volume())
play_1 = pygame.mixer.music.play()
pygame.mixer.music.load("/Song.mp3")
while True:
    pass
