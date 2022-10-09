import pygame, copy
from pygame.locals import *

pygame.init()

# Defining Variables
WIDTH = HEIGHT = 800 # set the width and height of our display
piece_size = WIDTH//8 # size of each square on the board
screen = pygame.display.set_mode((WIDTH,HEIGHT)) # makes a screen of given size
pygame.display.set_caption('PLAY CHESS') # sets a caption to the window


# Defining Classes
class GameBoard: # contains all the things that a game should be able to do
  def __init__(self):
    self.game_board = [ #here, each piece is being represented as a list of all its properties
      [["br","black","rook",(0,0)], ["bn","black","knight",(1,0)], ["bb","black","bishop",(2,0)], ["bq","black","queen",(3,0)], ["bk","black","king",(4,0)],["bb","black","bishop",(5,0)],["bn","black","knight",(6,0)],["br","black","rook",(7,0)]],
      [["bp","black","pawn",(0,1),True],["bp","black","pawn",(1,1),True],["bp","black","pawn",(2,1),True],["bp","black","pawn",(3,1),True],["bp","black","pawn",(4,1),True],["bp","black","pawn",(5,1),True],["bp","black","pawn",(6,1),True],["bp","black","pawn",(7,1),True]],
      [None,None,None,None,None,None,None,None],
      [None,None,None,None,None,None,None,None],
      [None,None,None,None,None,None,None,None],
      [None,None,None,None,None,None,None,None],#                  This true stands for pawn eligible for 2 jump
      [["wp","white","pawn",(0,6),True],["wp","white","pawn",(1,6),True],["wp","white",(2,6),True],["wp","white","pawn",(3,6),True],["wp","white","pawn",(4,6),True],["wp","white","pawn",(5,6),True],["wp","white","pawn",(6,6),True],["wp","white","pawn",(7,6),True]],
      [["wr","white","rook",(0,7)], ["wn","white","knight",(1,7)], ["wb","white","bishop",(2,7)], ["wq","white","queen",(3,7)], ["wk","white",  "king",(4,7)],["wb","white","bishop",(5,7)],["wn","white","knight",(6,7)],["wr","white","rook",(7,7)]]
    ]
    self.isWhiteTurn = True # This is to check if it is white's turn
    self.turn_dict = {True: 'white', False: 'black'} # This will be used to determine who's turn it is
    self.draw_white_side = 1 # 1 means true in this case. Black turn would mean -1
    self.king_pos = {"white":(4,7), "black":(4,0)} # stores the kings position
    self.possible_moves = [] # this is the list of possible moves
    self.fake_board = None # This is a fake board that is being used 
    self.selected_piece = (None,None)
    self.images = self.image_import()
    self.previous_board = None
    self.change_side = False
    self.move_loc = (None,None)
    self.draw_game_board()
    
  def image_import(self):
    images = {'board' : pygame.transform.scale(pygame.image.load('Board.png'),(WIDTH,HEIGHT))}
    pieces = ['br', 'bn', 'bb', 'bn' , 'bq', 'bk', 'bp','wr', 'wn', 'wb', 'wn' , 'wq', 'wk', 'wp']
    for piece in pieces:
      images[piece] = pygame.transform.scale(pygame.image.load(f'{piece}.png'), (piece_size,piece_size))
    return images

  def after_move(self):
      if self.change_side:
          self.draw_white_side *= -1
      self.draw_game_board()
      self.isWhiteTurn = not self.isWhiteTurn
      

  def draw_game_board(self):
    screen.blit(self.images['board'],(0,0))
    self.draw_pieces()
    pygame.display.update()
    
  def move_piece(self, board, start, end , want_duplicate):
      ((start_x,start_y), (end_x,end_y)) = (start,end)
      duplicate = copy.deepcopy(board)
      board[end_y][end_x] = board[start_y][start_x]
      board[end_y][end_x][3] = end
      board[start_y][start_x] = None
      if board[end_y][end_x][2] == 'king':
          self.king_pos[board[end_y][end_x][1]] = end
      self.after_move()
      if want_duplicate:
          return duplicate
      else:
          return board
     
  def draw_pieces(self):
      for y in range(8):
          for x in range(8):
              if self.game_board[y][x] != None:
                  if self.draw_white_side == -1:
                      screen.blit(self.images[f'{self.game_board[y][x][0]}'], (WIDTH-(x+1)*piece_size, HEIGHT-(y+1)* piece_size))
                  if self.draw_white_side == 1:
                      screen.blit(self.images[f'{self.game_board[y][x][0]}'], (x*piece_size, y* piece_size))
                  
  def select_piece(self,mouse_pos):
      x,y = (mouse_pos[0]//piece_size,mouse_pos[1]//piece_size)
      if self.selected_piece == (None,None) and self.move_loc==(None, None):
          if self.game_board[y][x] != None:
              if self.game_board[y][x][1] == self.turn_dict[self.isWhiteTurn]:
                  self.selected_piece =(x,y)
                  #show poasibility
      if self.selected_piece!=(None,None) and self.move_loc==(None,None):
          if self.game_board[y][x] !=  None:
              if self.game_board[y][x][1] == self.turn_dict[self.isWhiteTurn]:
                  self.selected_piece =(x,y)
                  #show poasibiliy
              else:
                  self.move_loc = (x,y)
                  self.previous_board = self.move_piece(self.game_board, self.selected_piece, self.move_loc, True)
                  self.move_loc = self.selected_piece = (None,None)
          else:
              self.move_loc = (x,y)
              self.previous_board = self.move_piece(self.game_board, self.selected_piece, self.move_loc, True)
              self.move_loc = self.selected_piece = (None,None)
      
      print(self.selected_piece, self.move_loc)
          
  def take_back(self):  
    self.game_board = self.previous_board
    self.isWhiteTurn = not self.isWhiteTurn
    self.draw_game_board()
          
    
board = GameBoard() 
# Main Loop
while True:
  for event in pygame.event.get():
    if event.type == QUIT: 
      exit()
    if event.type == MOUSEBUTTONDOWN:
        if board.draw_white_side == -1:
            board.select_piece((WIDTH - event.pos[0], HEIGHT - event.pos[1]))
        else:
            board.select_piece(event.pos)
    if event.type == KEYDOWN:
        if event.key == K_b:
            board.take_back()
        if event.key == K_c:
            board.change_side = not board.change_side
  keys = pygame.key.get_pressed()
    
