import pygame
import copy
from pygame.locals import *

pygame.init()

# Defining Variables
WIDTH = HEIGHT = 800  # set the width and height of our display
piece_size = (WIDTH // 8, HEIGHT // 8)  # size of each square on the board
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # makes a screen of given size
pygame.display.set_caption('PLAY CHESS')  # sets a caption to the window


# Defining Classes
class GameBoard:  # contains all the things that a game should be able to do
    def __init__(self):
        self.game_board = [  # here, each piece is being represented as a list of all its properties
            [["br", "black", "rook", (0, 0)], ["bn", "black", "knight", (1, 0)], ["bb", "black", "bishop", (2, 0)], ["bq", "black", "queen", (3, 0)], ["bk", "black", "king", (4, 0)], ["bb", "black", "bishop", (5, 0)], ["bn", "black", "knight", (6, 0)], ["br", "black", "rook", (7, 0)]],
            [["bp", "black", "pawn", (0, 1), True], ["bp", "black", "pawn", (1, 1), True], ["bp", "black", "pawn", (2, 1), True], ["bp", "black", "pawn", (3, 1), True], ["bp", "black", "pawn", (4, 1), True], ["bp", "black", "pawn", (5, 1), True], ["bp", "black", "pawn", (6, 1), True], ["bp", "black", "pawn", (7, 1), True]],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],  # -                 This true stands for pawn eligible for 2 jump
            [["wp", "white", "pawn", (0, 6), True], ["wp", "white", "pawn", (1, 6), True], ["wp", "white", (2, 6), True], ["wp", "white", "pawn", (3, 6), True], ["wp", "white", "pawn", (4, 6), True], ["wp", "white", "pawn", (5, 6), True], ["wp", "white", "pawn", (6, 6), True], ["wp", "white", "pawn", (7, 6), True]],
            [["wr", "white", "rook", (0, 7)], ["wn", "white", "knight", (1, 7)], ["wb", "white", "bishop", (2, 7)], ["wq", "white", "queen", (3, 7)], ["wk", "white", "king", (4, 7)], ["wb", "white", "bishop", (5, 7)], ["wn", "white", "knight", (6, 7)], ["wr", "white", "rook", (7, 7)]]
        ]
        self.isWhiteTurn = True  # This is to check if it is white's turn
        self.turn_dict = {True: 'white', False: 'black'}  # This will be used to determine who's turn it is

        self.draw_white_side = 1  # 1 means true in this case. Black turn would mean -1
        self.images = self.image_import()  # This is a dictionary of the following format {'wr' : corresponding image}

        self.king_pos = {"white": (4, 7), "black": (4, 0)}  # stores the kings position
        self.possible_moves = []  # this is the list of possible moves
        self.fake_board = None  # This is a fake board that is being used to check if the king is in a check
        self.selected_piece = (None, None)  # stores the coordinates of the selected piece
        self.move_loc = (None, None)  # coordinates of the point you want the selected piece to move to
        self.previous_board = None  # This stores the state of the previous board in case you want to take back
        self.change_side = False  # Enable in case you want to change the side of the board with every turn
        self.draw_game_board()  # draws the game board

    def image_import(self):
        """
            For each of the images, it will import a scaled version of that image and define it in a dictionary
            It will also return that dictionary
        """
        images = {'board': pygame.transform.scale(pygame.image.load('Board.png'), (WIDTH, HEIGHT))}
        pieces = ['br', 'bn', 'bb', 'bn', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wn', 'wq', 'wk', 'wp']
        for piece in pieces:
            images[piece] = pygame.transform.scale(pygame.image.load(f'{piece}.png'), (piece_size[0], piece_size[1]))
        return images

    def after_move(self):
        """
            This contains the code that has to be run after a move is made
        """
        if self.change_side:  # If change_side is enabled, then it will change the draw side every time a move is made
            self.draw_white_side *= -1  # This will change draw_white_side to the opposite
        self.draw_game_board()  # The display needs to be updated after every move
        self.isWhiteTurn = not self.isWhiteTurn  # Changes the turn
        pygame.display.set_caption(f'it is {}')

    def draw_game_board(self):
        """
            Draws the game board in the following sequence
            1) Draw image of board
            2) Colour the grid to indicate which piece was moved
            3) Draw all the possible moves
            4) Draw all the pieces
        """
        screen.blit(self.images['board'], (0, 0))  # Draws the board image
        self.draw_pieces()  # Draws the images of the pieces
        pygame.display.update()  # Updates the display

    def move_piece(self, chess_board, start, end, want_duplicate):
        ((start_x, start_y), (end_x, end_y)) = (start, end)
        duplicate = copy.deepcopy(chess_board)
        chess_board[end_y][end_x] = chess_board[start_y][start_x]
        chess_board[end_y][end_x][3] = end
        chess_board[start_y][start_x] = None
        if chess_board[end_y][end_x][2] == 'king':
            self.king_pos[chess_board[end_y][end_x][1]] = end
        self.after_move()
        if want_duplicate:
            return duplicate
        else:
            return chess_board

    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                if self.game_board[y][x] is not None:
                    if self.draw_white_side == -1:
                        screen.blit(self.images[f'{self.game_board[y][x][0]}'],
                                    (WIDTH - (x + 1) * piece_size[0], HEIGHT - (y + 1) * piece_size[1]))
                    if self.draw_white_side == 1:
                        screen.blit(self.images[f'{self.game_board[y][x][0]}'], (x * piece_size[0], y * piece_size[1]))

    def select_piece(self, mouse_pos):
        x, y = (mouse_pos[0] // piece_size[0], mouse_pos[1] // piece_size[1])
        if self.selected_piece == (None, None) and self.move_loc == (None, None):
            if self.game_board[y][x] is not None:
                if self.game_board[y][x][1] == self.turn_dict[self.isWhiteTurn]:
                    self.selected_piece = (x, y)
                    # show poasibility
        if self.selected_piece != (None, None) and self.move_loc == (None, None):
            if self.game_board[y][x] is not None:
                if self.game_board[y][x][1] == self.turn_dict[self.isWhiteTurn]:
                    self.selected_piece = (x, y)
                    # show poasibiliy
                else:
                    self.move_loc = (x, y)
                    self.previous_board = self.move_piece(self.game_board, self.selected_piece, self.move_loc, True)
                    self.move_loc = self.selected_piece = (None, None)
            else:
                self.move_loc = (x, y)
                self.previous_board = self.move_piece(self.game_board, self.selected_piece, self.move_loc, True)
                self.move_loc = self.selected_piece = (None, None)

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
