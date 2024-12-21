import pygame, time
import copy
from pygame.locals import *

pygame.init()

# Defining Variables
WIDTH = HEIGHT = 800  # set the width and height of our display
piece_size = (WIDTH // 8, HEIGHT // 8)  # size of each square on the board
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # makes a screen of given size
pygame.display.set_caption('PLAY CHESS')  # sets a caption to the window

# If I work on something, then it has to be a version of this game only!
# Defining Classes


class GameBoard:  # contains all the things that a game should be able to do
    def __init__(self):
        self.game_board = [  # here, each piece is being represented as a list of all its properties
            [["br", "black", "rook", (0, 0), True], ["bn", "black", "knight", (1, 0)], ["bb", "black", "bishop", (2, 0)], ["bq", "black", "queen", (3, 0)], ["bk", "black", "king", (4, 0), True], ["bb", "black", "bishop", (5, 0)], ["bn", "black", "knight", (6, 0)], ["br", "black", "rook", (7, 0), True]],
            [["bp", "black", "pawn", (0, 1), True], ["bp", "black", "pawn", (1, 1), True], ["bp", "black", "pawn", (2, 1), True], ["bp", "black", "pawn", (3, 1), True], ["bp", "black", "pawn", (4, 1), True], ["bp", "black", "pawn", (5, 1), True], ["bp", "black", "pawn", (6, 1), True], ["bp", "black", "pawn", (7, 1), True]],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [["wp", "white", "pawn", (0, 6), True], ["wp", "white", "pawn", (1, 6), True], ["wp", "white", "pawn", (2, 6), True], ["wp", "white", "pawn", (3, 6), True], ["wp", "white", "pawn", (4, 6), True], ["wp", "white", "pawn", (5, 6), True], ["wp", "white", "pawn", (6, 6), True], ["wp", "white", "pawn", (7, 6), True]],
            [["wr", "white", "rook", (0, 7), True], ["wn", "white", "knight", (1, 7)], ["wb", "white", "bishop", (2, 7)], ["wq", "white", "queen", (3, 7)], ["wk", "white", "king", (4, 7), True], ["wb", "white", "bishop", (5, 7)], ["wn", "white", "knight", (6, 7)], ["wr", "white", "rook", (7, 7), True]]
        ]

        self.isWhiteTurn = True  # This is to check if it is white's turn
        self.turn_dict = {True: 'white', False: 'black'}  # This will be used to determine a str value of who's turn it is based on value of self.isWhiteTurn

        self.change_side = False  # Enable in case you want to change the side of the board with every turn
        self.turn_dict_change_side = {True: 0, False: 1}
        self.draw_white_side = 0  # 0 means true in this case. Black side would mean 1

        self.images = self.image_import()  # This is a dictionary of the following format {'wr' : corresponding image}

        self.king_pos = {"white": (4, 7), "black": (4, 0)}  # stores the kings position
        self.fake_board = None  # This is a fake board that is being used to check if the king is in a check

        self.possible_moves = []  # this is the list of possible moves

        self.selected_piece = (None, None)  # stores the coordinates of the selected piece
        self.move_loc = (None, None)  # coordinates of the point you want the selected piece to move to

        self.previous_board = None  # This stores the state of the previous board in case you want to take back
        self.latest_move = None  # Stores the latest move made
        self.draw_game_board()  # draws the game board

    def image_import(self):
        """
            For each of the images, it will import a scaled version of that image and define it in a dictionary
            It will also return that dictionary
        """
        images = {'board': pygame.transform.scale(pygame.image.load('Board.png'), (WIDTH, HEIGHT)), 'movable': pygame.transform.scale(pygame.image.load('movable.png'), (piece_size[0], piece_size[1]))}
        for piece in ['br', 'bn', 'bb', 'bn', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wn', 'wq', 'wk', 'wp']:
            images[piece] = pygame.transform.scale(pygame.image.load(f'{piece}.png'), (piece_size[0], piece_size[1]))
        return images

    def draw_pieces(self):
        """
        Draws the pieces on the board in respective positions
        """
        for y in range(8):
            for x in range(8):
                if self.game_board[y][x] is not None:  # If there is a piece on a square
                    screen.blit(self.images[f'{self.game_board[y][x][0]}'], (abs(7 * self.draw_white_side - x) * piece_size[0], abs(7 * self.draw_white_side - y) * piece_size[1]))  # Displays the piece images based on self.draw_white_side

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

    def draw_possibilities(self, possibilities):
        """
        Highlights possible moves on the board.
        """
        self.draw_game_board()
        for move in possibilities:
            x, y = move
            screen.blit(self.images['movable'], (abs(7 * self.draw_white_side - x) * piece_size[0], abs(7 * self.draw_white_side - y) * piece_size[1]))
            pygame.display.update()

    def select_piece(self, mouse_pos):
        """
        With the input of where the mouse clicked, it will decide if a piece is selected, to be moved or to be unselected
        """
        x, y = (mouse_pos[0] // piece_size[0], mouse_pos[1] // piece_size[1])  # Obtains the coordinates of the square that has been selected

        if self.selected_piece == (None, None) and self.move_loc == (None, None):  # If a piece has not been previously selected...
            if self.game_board[y][x] is not None:  # And if there is a piece on the currently selected square...
                if self.game_board[y][x][1] == self.turn_dict[self.isWhiteTurn]:  # If it is the turn of the colour of the piece that has been selected
                    self.selected_piece = (x, y)  # Then store the value of the selected piece
                    self.possible_moves = self.get_piece_possibility()
                    self.draw_possibilities(self.possible_moves)

        elif self.selected_piece != (None, None) and self.move_loc == (None, None):  # If a piece has already been selected but not moved yet...
            if self.game_board[y][x] is not None:  # If the square clicked on just now is not empty...
                if self.game_board[y][x][1] == self.turn_dict[self.isWhiteTurn]:  # And the new piece selected is of the colour of the turn...
                    if self.selected_piece == (x,y):  # If you have selected the same piece again...
                        self.selected_piece = (None, None)  # Deselect the piece
                        self.possible_moves = self.get_piece_possibility()
                        self.draw_possibilities(self.possible_moves)  # Remove the drawn dots
                    else:
                        self.selected_piece = (x, y)  # Change this to be the new selected piece
                        self.possible_moves = self.get_piece_possibility()
                        self.draw_possibilities(self.possible_moves)
                else:
                    self.move_loc = (x, y)
                    if self.move_loc in self.possible_moves:
                        self.previous_board = self.move_piece(self.game_board, self.selected_piece, self.move_loc, True)
                        self.move_loc = self.selected_piece = (None, None)
                        self.possible_moves = []
                    self.move_loc = (None, None)
            else:
                self.move_loc = (x, y)
                if self.move_loc in self.possible_moves:
                    self.previous_board = self.move_piece(self.game_board, self.selected_piece, self.move_loc, True)
                    self.move_loc = self.selected_piece = (None, None)
                    self.possible_moves = []
                self.move_loc = (None, None)

    def get_piece_possibility(self):
        if self.selected_piece == (None, None):
            return []
        x, y = self.selected_piece
        piece = self.game_board[y][x]
        if not piece:
            return []

        piece_type = piece[2]
        color = piece[1]
        moves = []

        if piece_type == 'pawn':
            direction = -1 if color == 'white' else 1
            # Forward move
            if 0 <= y + direction < 8 and self.game_board[y + direction][x] is None:
                moves.append((x, y + direction))
                # Double move from starting position
                if piece[4] and 0 <= y + 2 * direction < 8 and self.game_board[y + 2 * direction][x] is None:
                    moves.append((x, y + 2 * direction))
            # Capture moves
            for dx in [-1, 1]:
                if 0 <= x + dx < 8 and 0 <= y + direction < 8:
                    target = self.game_board[y + direction][x + dx]
                    if target and target[1] != color:
                        moves.append((x + dx, y + direction))

        elif piece_type in ['rook', 'bishop', 'queen']:
            directions = []
            if piece_type in ['rook', 'queen']:
                directions += [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if piece_type in ['bishop', 'queen']:
                directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    target = self.game_board[ny][nx]
                    if target is None:
                        moves.append((nx, ny))
                    else:
                        if target[1] != color:
                            moves.append((nx, ny))
                        break
                    nx += dx
                    ny += dy

        elif piece_type == 'knight':
            for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = self.game_board[ny][nx]
                    if target is None or target[1] != color:
                        moves.append((nx, ny))

        elif piece_type == 'king':
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = self.game_board[ny][nx]
                    if target is None or target[1] != color:
                        moves.append((nx, ny))

        return moves

    def move_piece(self, chess_board, start, end, want_duplicate):
        """
        Moves a piece to a new location

        Input : Takes the game board, the start position of the piece to be moved, the end position, if we want a duplicate of the game board
        Output : Duplicate_board / Game board (output depends on if we want and output or not)
        """
        ((start_x, start_y), (end_x, end_y)) = (start, end)  # Extracts the x and y coordinates from start and end
        duplicate = copy.deepcopy(chess_board)  # Creates a duplicate version of the board in case you want to take back
        chess_board[end_y][end_x] = chess_board[start_y][start_x]  # Creates a duplicate of the piece you want to move in the end position
        chess_board[end_y][end_x][3] = end  # Sets the coordinates of the new duplicate piece to update

        # Update the 'True' flag for a pawn that moves two steps
        if chess_board[end_y][end_x][2] == 'pawn' and chess_board[end_y][end_x][4]:
            chess_board[end_y][end_x][4] = False

        chess_board[start_y][start_x] = None  # Erases the original piece from the board

        # Update the king's position
        if chess_board[end_y][end_x][2] == 'king':
            self.king_pos[chess_board[end_y][end_x][1]] = end

        # Check for pawn promotion
        if chess_board[end_y][end_x][2] == 'pawn':
            # For white pawns reaching y=0 and black pawns reaching y=7
            if (chess_board[end_y][end_x][1] == 'white' and end_y == 0) or \
                    (chess_board[end_y][end_x][1] == 'black' and end_y == 7):
                self.promotion_handler(end_x, end_y)

        # Update latest move
        self.latest_move = [start, end]

        self.after_move()  # Runs a set of commands that need to run after a move has been made

        if want_duplicate:  # If you want a duplicate version of the board...
            return duplicate  # Return the duplicate
        else:
            return chess_board  # Return the chessboard

    def after_move(self):
        """
            This contains the code that has to be run after a move is made
        """
        if self.change_side:  # If change_side is enabled, then it will change the draw side every time a move is made
            self.draw_white_side = (self.draw_white_side * -1) + 1  # This will change draw_white_side to the opposite
        self.draw_game_board()  # The display needs to be updated after every move
        self.isWhiteTurn = not self.isWhiteTurn  # Changes the turn

    def take_back(self):
        self.game_board = self.previous_board
        self.isWhiteTurn = not self.isWhiteTurn
        if self.change_side:
            self.draw_white_side = (self.draw_white_side * -1) + 1
        self.draw_game_board()

    def promotion_handler(self, x, y):
        """
        Handles pawn promotion by displaying a dropdown menu with promotion options as icons.
        Ensures the dropdown is visible within the screen boundaries.
        """
        promotion = True
        selected_piece = None
        options = ['queen', 'rook', 'bishop', 'knight']

        # Determine the color prefix based on the current turn
        color_prefix = 'w' if self.isWhiteTurn else 'b'

        # Mapping from option to piece code
        option_to_piece = {
            'queen': f'{color_prefix}q',
            'rook': f'{color_prefix}r',
            'bishop': f'{color_prefix}b',
            'knight': f'{color_prefix}n'
        }

        # Convert board coordinates to screen coordinates
        screen_x = abs(7 * self.draw_white_side - x) * piece_size[0]
        screen_y = abs(7 * self.draw_white_side - y) * piece_size[1]

        # Determine dropdown position based on promotion direction
        if self.isWhiteTurn:
            # White pawn promotes to the top (y=0), place dropdown below the square
            dropdown_y = screen_y + piece_size[1]
            # If dropdown exceeds screen, place it above
            if dropdown_y + 4 * piece_size[1] > HEIGHT:
                dropdown_y = screen_y - 4 * piece_size[1]
        else:
            # Black pawn promotes to the bottom (y=7), place dropdown above the square
            dropdown_y = screen_y - 4 * piece_size[1]
            # If dropdown exceeds screen, place it below
            if dropdown_y < 0:
                dropdown_y = screen_y + piece_size[1]

        dropdown_x = screen_x

        # Preload the promotion piece images
        promotion_images = [self.images[option_to_piece[option]] for option in options]

        while promotion:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for idx, image in enumerate(promotion_images):
                        rect = pygame.Rect(dropdown_x, dropdown_y + idx * piece_size[1], piece_size[0], piece_size[1])
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected_piece = options[idx]
                            promotion = False

            # Draw the dropdown background (semi-transparent)
            s = pygame.Surface((piece_size[0], piece_size[1] * len(options)))  # Width x (Height * number of options)
            s.set_alpha(200)  # Alpha level for transparency
            s.fill((200, 200, 200))  # Grey background
            screen.blit(s, (dropdown_x, dropdown_y))

            # Draw each promotion option
            for idx, piece_code in enumerate(option_to_piece.values()):
                piece_image = self.images[piece_code]
                piece_rect = piece_image.get_rect(topleft=(dropdown_x, dropdown_y + idx * piece_size[1]))
                screen.blit(piece_image, piece_rect)

            pygame.display.update()

        # Replace the pawn with the selected piece
        selected_piece_code = option_to_piece[selected_piece]
        self.game_board[y][x] = [
            selected_piece_code,
            'white' if self.isWhiteTurn else 'black',
            selected_piece,
            (x, y),
            False
        ]
        self.draw_game_board()

board = GameBoard()


# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if board.draw_white_side == 1:
                board.select_piece((WIDTH - event.pos[0], HEIGHT - event.pos[1]))
            else:
                board.select_piece(event.pos)

        if event.type == KEYDOWN:
            if event.key == K_b:
                board.take_back()
            if event.key == K_c:
                board.change_side = not board.change_side
                board.draw_white_side = board.turn_dict_change_side[board.isWhiteTurn]
                board.draw_game_board()

    keys = pygame.key.get_pressed()