import pygame
from pygame.locals import *

pygame.init()

# Defining Variables
WIDTH = HEIGHT = 800
piece_size = WIDTH//8
screen = pygame.display.set_mode((WIDTH,HEIGHT))


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
    self.isWhiteTurn = True
    self.turn_dict = {True: 'white', False: 'black'}
    self.draw_white_side = 1 # 1 means true in this case. Black turn would mean -1
    self.king_pos = {"white":(4,7), "black":(4,0)}
    self.possible_moves = []
    self.fake_board = None
    self.selected_piece = (None,None)
    self.images = self.image_import()
    self.previous_board = None
    self.isSelected = False
    self.move_loc = (None,None)
    self.draw_game_board()
  def image_import(self):
    images = {'board' : pygame.transform.scale(pygame.image.load('Board.png'),(WIDTH,HEIGHT))}
    pieces = ['br', 'bn', 'bb', 'bn' , 'bq', 'bk', 'bp','wr', 'wn', 'wb', 'wn' , 'wq', 'wk', 'wp']
    for piece in pieces:
      images[piece] = pygame.transform.scale(pygame.image.load(f'{piece}.png'), (piece_size,piece_size))
    return images
  def draw_game_board(self):
    screen.blit(self.images['board'],(0,0))
    self.draw_pieces()
    pygame.display.update()
  def move_piece(self, board, start, end):
      ((start_x,start_y), (end_x,end_y)) = (start,end)
      duplicate = board
      board[end_y][end_x] = board[start_y][start_x]
      board[end_y][end_x][3] = end
      board[start_y][start_x] = None
      if board[end_y][end_x][2] == 'king':
          self.king_pos[board[end_y][end_x][1]] = end
      #temp code
      self.draw_game_board()
      self.isWhiteTurn = not self.isWhiteTurn
      return board, duplicate
          
  def draw_pieces(self):
      for y in range(0,8,self.draw_white_side):
          for x in range(0,8,self.draw_white_side):
              if self.game_board[y][x] != None:
                  screen.blit(self.images[f'{self.game_board[y][x][0]}'], (x*piece_size, y* piece_size))
  def select_piece(self,mouse_pos):
      x,y = (mouse_pos[0]//piece_size,mouse_pos[1]//piece_size)
      if self.selected_piece == (None,None):
          if self.game_board[y][x] != None:
              if self.turn_dict[self.isWhiteTurn] == self.game_board[y][x][1]:
                  self.selected_piece = (x,y)
      elif self.selected_piece != (None,None) and self.move_loc == (None,None):
          if self.game_board[y][x] != None:
              if self.game_board[y][x][1] == self.turn_dict[self.isWhiteTurn]:
                  self.selected_piece = (None, None)
          else:
              self.move_loc = (x,y)
              self.game_board , self.previous_board = self.move_piece(self.game_board , self.selected_piece, self.move_loc)
      elif self.selected_piece != (None,None) and self.move_loc != (None, None):
          self.move_loc = (None,None)
          self.selected_piece = (None,None)
          if self.game_board[y][x] != None:
              if self.turn_dict[self.isWhiteTurn] == self.game_board[y][x][1]:
                  self.selected_piece = (x,y)
      
      print(self.selected_piece, self.move_loc)
          
          
          
    
board = GameBoard() 
# Main Loop
while True:
  for event in pygame.event.get():
    if event.type == QUIT: 
      exit()
    if event.type == MOUSEBUTTONDOWN:
        board.select_piece(event.pos)
