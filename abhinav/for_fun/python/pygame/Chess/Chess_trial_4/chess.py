import pygame
import sys
import copy
from pygame.locals import *

# -----------------------------------------------------------------------
#                            CONSTANTS
# -----------------------------------------------------------------------
WIDTH = HEIGHT = 800
SQUARE_SIZE = WIDTH // 8  # Each square is 1/8 of the board dimension

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PLAY CHESS')


# -----------------------------------------------------------------------
#                          GAME STATE CLASS
# -----------------------------------------------------------------------
class GameState:
    """
    Holds all information about the current game:
    - Board with piece positions
    - Whose turn it is (white or black)
    - The positions of kings
    - Move history for take-backs
    - Info about check alerts, possible-move display toggles, side flips, etc.
    """

    def __init__(self):
        # The board is an 8x8 list of lists.
        # Each piece is [pieceCode, color, pieceName, (x, y), optionalBool...]
        # Or None if the square is empty.
        self.board = [
            [["br", "black", "rook", (0, 0), True],
             ["bn", "black", "knight", (1, 0)],
             ["bb", "black", "bishop", (2, 0)],
             ["bq", "black", "queen", (3, 0)],
             ["bk", "black", "king", (4, 0), True],
             ["bb", "black", "bishop", (5, 0)],
             ["bn", "black", "knight", (6, 0)],
             ["br", "black", "rook", (7, 0), True]],

            [["bp", "black", "pawn", (0, 1), True],
             ["bp", "black", "pawn", (1, 1), True],
             ["bp", "black", "pawn", (2, 1), True],
             ["bp", "black", "pawn", (3, 1), True],
             ["bp", "black", "pawn", (4, 1), True],
             ["bp", "black", "pawn", (5, 1), True],
             ["bp", "black", "pawn", (6, 1), True],
             ["bp", "black", "pawn", (7, 1), True]],

            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],

            [["wp", "white", "pawn", (0, 6), True],
             ["wp", "white", "pawn", (1, 6), True],
             ["wp", "white", "pawn", (2, 6), True],
             ["wp", "white", "pawn", (3, 6), True],
             ["wp", "white", "pawn", (4, 6), True],
             ["wp", "white", "pawn", (5, 6), True],
             ["wp", "white", "pawn", (6, 6), True],
             ["wp", "white", "pawn", (7, 6), True]],

            [["wr", "white", "rook", (0, 7), True],
             ["wn", "white", "knight", (1, 7)],
             ["wb", "white", "bishop", (2, 7)],
             ["wq", "white", "queen", (3, 7)],
             ["wk", "white", "king", (4, 7), True],
             ["wb", "white", "bishop", (5, 7)],
             ["wn", "white", "knight", (6, 7)],
             ["wr", "white", "rook", (7, 7), True]]
        ]

        # White goes first
        self.is_white_turn = True
        self.turn_dict = {True: 'white', False: 'black'}

        # Toggle for flipping the board every move
        self.change_side = False
        self.turn_dict_change_side = {True: 0, False: 1}
        self.draw_white_side = 0  # 0 means white side at bottom, 1 means black side at bottom

        # Load images for board and pieces
        self.images = self.import_images()

        # King positions
        self.king_pos = {"white": (4, 7), "black": (4, 0)}

        # For check alerts
        # draw_alert_box[0] = bool for whether to highlight king
        # draw_alert_box[1] = colour of king in check
        self.draw_alert_box = [False]

        # If "supports" is True, it means we show possible move squares
        self.supports = False

        # Possible moves for the currently selected piece
        self.possible_moves = []

        # The currently selected piece's coordinates
        self.selected_piece = (None, None)
        # The move location requested
        self.move_loc = (None, None)

        # For take-back
        self.previous_board = None
        # Latest move
        self.latest_move = None

    def import_images(self):
        """
        Loads and scales images (board, movable squares, and pieces).
        Uses the same filenames as your original code.
        """
        images = {}
        images['board'] = pygame.transform.scale(
            pygame.image.load('Board.png'), (WIDTH, HEIGHT)
        )
        images['movable'] = pygame.transform.scale(
            pygame.image.load('movable.png'), (SQUARE_SIZE, SQUARE_SIZE)
        )
        for piece in ['br', 'bn', 'bb', 'bq', 'bk', 'bp',
                      'wr', 'wn', 'wb', 'wq', 'wk', 'wp']:
            images[piece] = pygame.transform.scale(
                pygame.image.load(f'{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)
            )
        return images


# -----------------------------------------------------------------------
#                        MOVE LOGIC / VALIDATION CLASS
# -----------------------------------------------------------------------
class MoveManager:
    """
    Handles moves, generating possibilities, checking for check, checkmate, promotions, etc.
    Essentially, all the logic from your original code, but placed in a single class
    to keep it separate from display and input.
    """

    def __init__(self, game_state):
        self.gs = game_state  # Reference to the GameState object

    def select_piece(self, mouse_pos):
        """
        Exactly the same selection and move logic as your original code.
        """
        x, y = (mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE)

        # Adjust for board flip
        if self.gs.draw_white_side == 1:
            x = 7 - x
            y = 7 - y

        if (self.gs.selected_piece == (None, None)
                and self.gs.move_loc == (None, None)):
            # No piece was previously selected
            if self.gs.board[y][x] is not None:
                # There's a piece on the clicked square
                if self.gs.board[y][x][1] == self.gs.turn_dict[self.gs.is_white_turn]:
                    # The piece belongs to the player whose turn it is
                    self.gs.selected_piece = (x, y)
                    self.gs.possible_moves = self.get_piece_possibility()
                    # If supports is on, we highlight immediately
                else:
                    # Selected opponent's piece or empty square => no action
                    pass

        elif (self.gs.selected_piece != (None, None)
              and self.gs.move_loc == (None, None)):
            # We already selected a piece, now we're trying to move or re-select
            if self.gs.board[y][x] is not None:
                # The new clicked square has a piece
                if self.gs.board[y][x][1] == self.gs.turn_dict[self.gs.is_white_turn]:
                    # The new piece is of the same colour as the turn
                    if self.gs.selected_piece == (x, y):
                        # Re-click on the same piece => deselect
                        self.gs.selected_piece = (None, None)
                        self.gs.possible_moves = []
                    else:
                        # Switch selection to the new piece
                        self.gs.selected_piece = (x, y)
                        self.gs.possible_moves = self.get_piece_possibility()
                else:
                    # Possibly capturing
                    self.gs.move_loc = (x, y)
                    if self.gs.move_loc in self.gs.possible_moves:
                        self.gs.previous_board = copy.deepcopy(self.gs.board)
                        self.move_piece(self.gs.selected_piece, self.gs.move_loc, True)
                        self.after_move(self.gs.selected_piece, self.gs.move_loc)
                    # Reset selection
                    self.gs.move_loc = (None, None)
                    self.gs.selected_piece = (None, None)
                    self.gs.possible_moves = []
            else:
                # We clicked an empty square => could be a normal move
                self.gs.move_loc = (x, y)
                if self.gs.move_loc in self.gs.possible_moves:
                    self.gs.previous_board = copy.deepcopy(self.gs.board)
                    self.move_piece(self.gs.selected_piece, self.gs.move_loc, True)
                    self.after_move(self.gs.selected_piece, self.gs.move_loc)
                self.gs.move_loc = (None, None)
                self.gs.selected_piece = (None, None)
                self.gs.possible_moves = []

    def move_piece(self, start, end, want_duplicate):
        """
        Exactly as the old code: move a piece from start to end on the self.gs.board.
        If want_duplicate is True, store the old board state for undo.
        """
        start_x, start_y = start
        end_x, end_y = end

        # The piece we are moving
        piece_copy = self.gs.board[start_y][start_x].copy()

        duplicate = None
        if want_duplicate:
            duplicate = copy.deepcopy(self.gs.board)

        # Move the piece on the board
        self.gs.board[end_y][end_x] = piece_copy
        # Update its internal coordinates
        self.gs.board[end_y][end_x][3] = (end_x, end_y)
        # If it was a pawn that hasn't moved yet, set that to False
        if (self.gs.board[end_y][end_x][2] == 'pawn'
                and len(self.gs.board[end_y][end_x]) == 5
                and self.gs.board[end_y][end_x][4]):
            self.gs.board[end_y][end_x][4] = False

        # Clear old square
        self.gs.board[start_y][start_x] = None

        # Pawn promotion
        if piece_copy[2] == 'pawn':
            if (piece_copy[1] == 'white' and end_y == 0) or (piece_copy[1] == 'black' and end_y == 7):
                self.promotion_handler(end_x, end_y)

        return duplicate

    def promotion_handler(self, x, y):
        """
        Exactly as the old code: show a mini-GUI to choose piece type, or keep it simple.
        We'll keep the same dropdown approach that pops up over the board.
        """
        promotion = True
        selected_piece = None
        options = ['queen', 'rook', 'bishop', 'knight']
        color_prefix = 'w' if self.gs.is_white_turn else 'b'
        option_to_piece = {
            'queen': f'{color_prefix}q',
            'rook': f'{color_prefix}r',
            'bishop': f'{color_prefix}b',
            'knight': f'{color_prefix}n'
        }

        # Convert board coords to screen coords (take into account board flip)
        if self.gs.draw_white_side == 1:
            screen_x = (7 - x) * SQUARE_SIZE
            screen_y = (7 - y) * SQUARE_SIZE
        else:
            screen_x = x * SQUARE_SIZE
            screen_y = y * SQUARE_SIZE

        # Decide which side to show the dropdown
        if self.gs.is_white_turn:
            dropdown_y = screen_y + SQUARE_SIZE
            # If it doesn't fit, put it above
            if dropdown_y + 4 * SQUARE_SIZE > HEIGHT:
                dropdown_y = screen_y - 4 * SQUARE_SIZE
        else:
            dropdown_y = screen_y - 4 * SQUARE_SIZE
            if dropdown_y < 0:
                dropdown_y = screen_y + SQUARE_SIZE

        dropdown_x = screen_x
        promotion_images = [
            self.gs.images[option_to_piece[option]] for option in options
        ]

        while promotion:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Check which piece was chosen
                    for idx, img in enumerate(promotion_images):
                        rect = pygame.Rect(
                            dropdown_x, dropdown_y + idx * SQUARE_SIZE,
                            SQUARE_SIZE, SQUARE_SIZE
                        )
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected_piece = options[idx]
                            promotion = False

            # Draw the dropdown background
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE * len(options)))
            s.set_alpha(200)
            s.fill((200, 200, 200))
            screen.blit(s, (dropdown_x, dropdown_y))

            # Draw each option
            for idx, piece_code in enumerate(option_to_piece.values()):
                piece_img = self.gs.images[piece_code]
                piece_rect = piece_img.get_rect(
                    topleft=(dropdown_x, dropdown_y + idx * SQUARE_SIZE)
                )
                screen.blit(piece_img, piece_rect)

            pygame.display.update()

        # Replace the pawn
        selected_piece_code = option_to_piece[selected_piece]
        self.gs.board[y][x] = [
            selected_piece_code,
            'white' if self.gs.is_white_turn else 'black',
            selected_piece,
            (x, y),
            False
        ]

    def after_move(self, start, end):
        """
        Exactly as old code: runs after a move is completed.
        """
        end_x, end_y = end
        moved_piece = self.gs.board[end_y][end_x]
        # Update king pos if king moved
        if moved_piece[2] == 'king':
            self.gs.king_pos[moved_piece[1]] = (end_x, end_y)

        self.gs.latest_move = [start, end]

        # Check if opposing king is in check
        opposing_col = self.gs.turn_dict[not self.gs.is_white_turn]
        opposing_king = self.gs.king_pos[opposing_col]
        if self.verify_check(opposing_col, opposing_king):
            self.gs.draw_alert_box = [True, opposing_col]
            if self.is_checkmate(opposing_col):
                print(f"Checkmate! {self.gs.turn_dict[self.gs.is_white_turn].capitalize()} wins!")
                pygame.quit()
                sys.exit()
        else:
            self.gs.draw_alert_box = [False]

        # Flip side if enabled
        if self.gs.change_side:
            self.gs.draw_white_side = (self.gs.draw_white_side * -1) + 1

        # Switch turn
        self.gs.is_white_turn = not self.gs.is_white_turn

    def get_piece_possibility(self):
        """
        The same logic as your old get_piece_possibility.
        Returns a list of board coords (x, y) where the currently selected piece can move.
        """
        if self.gs.selected_piece == (None, None):
            return []
        x, y = self.gs.selected_piece
        piece = self.gs.board[y][x]
        if not piece:
            return []

        piece_type = piece[2]
        color = piece[1]

        if piece_type == 'pawn':
            return self.get_pawn_moves(x, y, color)
        elif piece_type in ['rook', 'bishop', 'queen', 'knight', 'king']:
            return self.get_sliding_moves(x, y, piece_type, color)
        return []

    def get_pawn_moves(self, x, y, color):
        """
        Same as old code's pawn logic (with is_legal_move checks).
        """
        direction = -1 if color == 'white' else 1
        moves = []

        # forward 1 step
        ny = y + direction
        if 0 <= ny < 8 and self.gs.board[ny][x] is None:
            if self.is_legal_move(color, (x, y), (x, ny)):
                moves.append((x, ny))
            # forward 2 steps if piece[4] is True
            if (self.gs.board[y][x][4]
                    and 0 <= (y + 2 * direction) < 8
                    and self.gs.board[y + 2 * direction][x] is None):
                if self.is_legal_move(color, (x, y), (x, y + 2 * direction)):
                    moves.append((x, y + 2 * direction))

        # captures
        for dx in [-1, 1]:
            nx = x + dx
            ny = y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = self.gs.board[ny][nx]
                if target and target[1] != color:
                    if self.is_legal_move(color, (x, y), (nx, ny)):
                        moves.append((nx, ny))

        # Return the final list
        return moves

    def get_sliding_moves(self, x, y, piece_type, color):
        """
        Rook, Bishop, Queen, Knight, King logic combined, just like your original code
        but split for each piece.
        """
        moves = []
        board = self.gs.board

        if piece_type == 'rook' or piece_type == 'queen':
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            moves += self.get_linear_moves(x, y, directions, piece_type, color)

        if piece_type == 'bishop' or piece_type == 'queen':
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            moves += self.get_linear_moves(x, y, directions, piece_type, color)

        if piece_type == 'knight':
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                            (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dx, dy in knight_moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[ny][nx]
                    if target is None or target[1] != color:
                        if self.is_legal_move(color, (x, y), (nx, ny)):
                            moves.append((nx, ny))

        if piece_type == 'king':
            king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                          (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in king_moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[ny][nx]
                    if target is None or target[1] != color:
                        if self.is_legal_move(color, (x, y), (nx, ny)):
                            moves.append((nx, ny))

        return moves

    def get_linear_moves(self, x, y, directions, piece_type, color):
        """
        Helper to retrieve sliding (rook/bishop/queen) moves line by line, with is_legal_move checks.
        """
        moves = []
        board = self.gs.board
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is None:
                    # Empty
                    if self.is_legal_move(color, (x, y), (nx, ny)):
                        moves.append((nx, ny))
                else:
                    if target[1] != color:
                        if self.is_legal_move(color, (x, y), (nx, ny)):
                            moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return moves

    def is_legal_move(self, color, start, end):
        """
        Your original is_legal_move logic:
        1) Duplicate the board
        2) Make the move on the duplicate
        3) Check if your own king is now in check
        4) Return not in_check
        """
        temp_board = copy.deepcopy(self.gs.board)

        sx, sy = start
        ex, ey = end
        piece = temp_board[sy][sx]
        temp_board[ey][ex] = piece.copy()
        temp_board[ey][ex][3] = (ex, ey)
        temp_board[sy][sx] = None

        # If we moved the king, update king position in our local copy
        temp_king_pos = None
        if piece[2] == 'king':
            temp_king_pos = (ex, ey)
        else:
            temp_king_pos = self.gs.king_pos[color]

        # But the actual king might be somewhere else if we didn't physically track it
        # We'll forcibly find the king in temp_board
        found_king = False
        for r in range(8):
            for c in range(8):
                if temp_board[r][c] and temp_board[r][c][2] == 'king' and temp_board[r][c][1] == color:
                    temp_king_pos = (c, r)
                    found_king = True
                    break
            if found_king:
                break

        # Check if king is in check
        return not self.verify_check_on_temp(temp_board, color, temp_king_pos)

    def verify_check_on_temp(self, board, color, king_pos):
        """
        Check if the 'color' king at king_pos is under attack in the 'board' snapshot.
        We replicate is_attack from your original code but pass in our 'board' reference.
        """
        return self.is_attack(king_pos, board, color)

    def is_attack(self, coords, board, player_col):
        """
        Same logic as your original 'is_attack'.
        """
        x, y = coords
        opponent_col = 'white' if player_col == 'black' else 'black'

        # 1) Diagonals for bishop/queen
        bishop_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in bishop_dirs:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                occ = board[ny][nx]
                if occ:
                    if (occ[1] == opponent_col and occ[2] in ['bishop', 'queen']):
                        return True
                    break
                nx += dx
                ny += dy

        # 2) Straights for rook/queen
        rook_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in rook_dirs:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                occ = board[ny][nx]
                if occ:
                    if (occ[1] == opponent_col and occ[2] in ['rook', 'queen']):
                        return True
                    break
                nx += dx
                ny += dy

        # 3) Knights
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in knight_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                occ = board[ny][nx]
                if occ and occ[1] == opponent_col and occ[2] == 'knight':
                    return True

        # 4) King
        king_moves = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dx, dy in king_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                occ = board[ny][nx]
                if occ and occ[1] == opponent_col and occ[2] == 'king':
                    return True

        # 5) Pawn captures
        if player_col == 'white':
            # Opponent is black => black pawns move downward => they attack from (x±1, y+1)
            check_positions = [(x - 1, y - 1), (x + 1, y - 1)]
        else:
            # Opponent is white => white pawns move upward => they attack from (x±1, y-1)
            check_positions = [(x - 1, y + 1), (x + 1, y + 1)]
        for nx, ny in check_positions:
            if 0 <= nx < 8 and 0 <= ny < 8:
                occ = board[ny][nx]
                if occ and occ[1] == opponent_col and occ[2] == 'pawn':
                    return True

        return False

    def verify_check(self, color, king_coords):
        """
        Check if king of 'color' at 'king_coords' in the real board is in check.
        """
        return self.is_attack(king_coords, self.gs.board, color)

    def is_checkmate(self, color):
        """
        If the king is in check, test if there's any move that can get out of check.
        If not, it's checkmate.
        """
        # If king not in check => not checkmate
        if not self.verify_check(color, self.gs.king_pos[color]):
            return False

        # Try every piece of 'color' to see if there's a legal move that resolves check
        for y in range(8):
            for x in range(8):
                piece = self.gs.board[y][x]
                if piece and piece[1] == color:
                    saved_sel = self.gs.selected_piece
                    self.gs.selected_piece = (x, y)
                    possible = self.get_piece_possibility()
                    self.gs.selected_piece = saved_sel
                    for mv in possible:
                        if self.is_legal_move(color, (x, y), mv):
                            return False
        return True

    def take_back(self):
        """
        If the user pressed 'b' for a take-back, restore the previous board if exists.
        """
        if self.gs.previous_board:
            self.gs.board = self.gs.previous_board
            self.gs.is_white_turn = not self.gs.is_white_turn
            self.gs.draw_alert_box = [False]
            if self.gs.change_side:
                self.gs.draw_white_side = (self.gs.draw_white_side * -1) + 1


# -----------------------------------------------------------------------
#                          RENDERER CLASS
# -----------------------------------------------------------------------
class Renderer:
    """
    Handles all drawing: the board background, the pieces, the check highlight,
    the possible moves, etc.
    """

    def __init__(self, game_state):
        self.gs = game_state

    def draw_game_board(self):
        """
        1) Draw the board image
        2) Draw the pieces
        3) Highlight check if needed
        4) If supports is True, draw possible moves
        5) Update the display
        """
        # Draw the background board image
        screen.blit(self.gs.images['board'], (0, 0))
        # Draw all pieces
        self.draw_pieces()
        # Draw possibilities
        self.draw_possibilities()
        # If king is in check and supports is True, highlight the king
        if self.gs.draw_alert_box[0] and self.gs.supports:
            color_in_check = self.gs.draw_alert_box[1]
            kx, ky = self.gs.king_pos[color_in_check]
            # Flip coords if needed
            rx = abs(7 * self.gs.draw_white_side - kx) * SQUARE_SIZE
            ry = abs(7 * self.gs.draw_white_side - ky) * SQUARE_SIZE
            rect = pygame.Rect(rx, ry, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, (255, 0, 0), rect, 3)
        pygame.display.update()

    def draw_pieces(self):
        """
        Loops through the board and draws each piece in its correct location,
        factoring in whether the board is flipped or not.
        """
        for y in range(8):
            for x in range(8):
                if self.gs.board[y][x] is not None:
                    piece_code = self.gs.board[y][x][0]  # e.g. 'br', 'wq'
                    # Flip coords if needed
                    rx = abs(7 * self.gs.draw_white_side - x) * SQUARE_SIZE
                    ry = abs(7 * self.gs.draw_white_side - y) * SQUARE_SIZE
                    screen.blit(self.gs.images[piece_code], (rx, ry))

    def draw_possibilities(self):
        """
        Draw the 'movable.png' markers on squares in self.gs.possible_moves,
        if self.gs.supports is True.
        """
        if not self.gs.supports:
            return
        for move in self.gs.possible_moves:
            mx, my = move
            rx = abs(7 * self.gs.draw_white_side - mx) * SQUARE_SIZE
            ry = abs(7 * self.gs.draw_white_side - my) * SQUARE_SIZE
            screen.blit(self.gs.images['movable'], (rx, ry))


# -----------------------------------------------------------------------
#                          INPUT HANDLER
# -----------------------------------------------------------------------
class InputHandler:
    """
    Manages keyboard and mouse events and calls appropriate logic from MoveManager.
    """

    def __init__(self, game_state, move_manager, renderer):
        self.gs = game_state
        self.mm = move_manager
        self.renderer = renderer

    def handle_events(self):
        """
        In the main loop, we call this every frame to process user input.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                self.mm.select_piece(event.pos)
                # After selecting or moving piece, draw possibilities
                self.renderer.draw_game_board()

            if event.type == KEYDOWN:
                if event.key == K_b:
                    # Undo
                    self.mm.take_back()
                    self.renderer.draw_game_board()
                elif event.key == K_c:
                    # Flip board side
                    self.gs.change_side = not self.gs.change_side
                    self.gs.draw_white_side = self.gs.turn_dict_change_side[self.gs.is_white_turn]
                    self.renderer.draw_game_board()
                elif event.key == K_s:
                    # Toggle supports
                    self.gs.supports = not self.gs.supports
                    self.renderer.draw_game_board()


# -----------------------------------------------------------------------
#                               MAIN
# -----------------------------------------------------------------------

# Create game components
game_state = GameState()
move_manager = MoveManager(game_state)
renderer = Renderer(game_state)
input_handler = InputHandler(game_state, move_manager, renderer)

# Initial board draw
renderer.draw_game_board()

while True:
    input_handler.handle_events()

    # We don't have a separate "update" step because
    # the old code logic draws immediately after input.
