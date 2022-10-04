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
    self.game_board = [ #here, each piece is being represented as a list of all its properties
      [["br","black","rook",(0,0)], ["bn","black","knight",(1,0)], ["bb","black","bishop",(2,0)], ["bq","black","queen",(3,0)], ["bk","black","king",(4,0)],["bb","black","bishop",(5,0)],["bn","black","knight",(6,0)],["br","black","rook",(7,0)]],
      [["bp","black","pawn",(0,1)],["bp","black","pawn",(1,1)],["bp","black","pawn",(2,1)],["bp","black","pawn",(3,1)],["bp","black","pawn",(4,1)],["bp","black","pawn",(5,1)],["bp","black","pawn",(6,1)],["bp","black","pawn",(7,1)]],
      [None,None,None,None,None,None,None,None],
      [None,None,None,None,None,None,None,None],
      [None,None,None,None,None,None,None,None],
      [None,None,None,None,None,None,None,None],
      [None,None,None,None,None,None,None,None],
      [["br","black","rook",(0,0)], ["bn","black","knight",(1,0)], ["bb","black","bishop",(2,0)], ["bq","black","queen",(3,0)], ["bk","black","king",(4,0)],["bb","black","bishop",(5,0)],["bn","black","knight",(6,0)],["br","black","rook",(7,0)]],

# Main Loop
While True:
  for event in pygame.event.get_pressed():
    if evnt.type == QUIT:
      exit()
