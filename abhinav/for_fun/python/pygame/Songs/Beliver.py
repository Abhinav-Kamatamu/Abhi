import pygame
file = 'Song.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
  pygame.time.Clock().tick(1)
print('done')
