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
      [["wp","white","pawn",(0,6)],["wp","white","pawn",(1,6)],["wp","black","white",(2,6)],["wp","white","pawn",(3,6)],["wp","white","pawn",(4,6)],["wp","white","pawn",(5,6)],["wp","white","pawn",(6,6)],["wp","white","pawn",(7,6)]],
      [["wr","white","rook",(0,7)], ["wn","white","knight",(1,7)], ["wb","white","bishop",(2,7)], ["wq","white","queen",(3,7)], ["wk","white",  "king",(4,7)],["wb","white","bishop",(5,7)],["wn","white","knight",(6,7)],["wr","white","rook",(7,7)]]
    ]
    self.isWhiteTrun = True
    self.draw_white_side = 1 # 1 means true in this case. Black turn would mean -1
    self.king_pos = {"white":(4,7), "black":(4,0)}
    self.possible_moves = []
    self.fake_board = None
    self.selected_piece = (None,None)
    self.images = self.imgae_import()
    self.previous_board = None

    
    
# Main Loop
While True:
  for event in pygame.event.get_pressed():
    if evnt.type == QUIT:
      exit()
