import pygame
from pygame.locals import *

pygame.init()

# Defining Variables
WIDTH = HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
board = GameBoard()

# Defining Classes
class GameBoard:
  def __init__(self):
    self.game_board = [
      {"code": "br", "type":"rook", "color" : "black", "position" : (0,0)}

# Main Loop
While True:
  for event in pygame.event.get_pressed():
    if evnt.type == QUIT:
      exit()
