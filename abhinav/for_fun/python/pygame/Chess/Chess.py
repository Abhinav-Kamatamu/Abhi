import pygame
from pygame.locals import *

pygame.init()
# ---------Important Variables --------
width = 800
height = 800
chesswidth = 600
chessheight = 600
piecesize = 75
boardStartPoint = (100, 100)
PAWN = 'PAWN'
ROOK = 'ROOK'
KNIGHT = 'KNIGHT'
BISHOP = 'BISHOP'
QUEEN = 'QUEEN'
KING = 'KING'
BLACK = 'BLACK'
WHITE = 'WHITE'
# ----------- Image Importing ---------
chessboard = pygame.image.load('Board.png')
wp = pygame.image.load('wp.png')
wr = pygame.image.load('wr.png')
wn = pygame.image.load('wn.png')
wb = pygame.image.load('wb.png')
wk = pygame.image.load('wk.png')
wq = pygame.image.load('wq.png')
bp = pygame.image.load('bp.png')
br = pygame.image.load('br.png')
bn = pygame.image.load('bn.png')
bb = pygame.image.load('bb.png')
bk = pygame.image.load('bk.png')
bq = pygame.image.load('bq.png')

chessboard = pygame.transform.scale(chessboard, (chesswidth, chessheight))
wp = pygame.transform.scale(wp, (piecesize, piecesize))
wr = pygame.transform.scale(wr, (piecesize, piecesize))
wn = pygame.transform.scale(wn, (piecesize, piecesize))
wb = pygame.transform.scale(wb, (piecesize, piecesize))
wk = pygame.transform.scale(wk, (piecesize, piecesize))
wq = pygame.transform.scale(wq, (piecesize, piecesize))
bp = pygame.transform.scale(bp, (piecesize, piecesize))
br = pygame.transform.scale(br, (piecesize, piecesize))
bn = pygame.transform.scale(bn, (piecesize, piecesize))
bb = pygame.transform.scale(bb, (piecesize, piecesize))
bk = pygame.transform.scale(bk, (piecesize, piecesize))
bq = pygame.transform.scale(bq, (piecesize, piecesize))


# -------------- Classes----------------

class Piece:
    def __init__(self):
        pass

    class Pawn:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.type = PAWN

    class Rook:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.type = ROOK

    class Knight:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.type = KNIGHT

    class Bishop:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.type = BISHOP

    class Queen:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.type = QUEEN

    class King:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.type = KING


class Board:
    def __init__(self, boardwidth, boardheight):
        self.width = boardwidth
        self.height = boardheight
        self.grid = [
            [Piece.Rook(BLACK, 1, 1), Piece.Knight(BLACK, 2, 1), Piece.Bishop(BLACK, 3, 1),
             Piece.Queen(BLACK, 4, 1), Piece.King(BLACK, 5, 1), Piece.Bishop(BLACK, 6, 1),
             Piece.Knight(BLACK, 7, 1), Piece.Rook(BLACK, 8, 1)],
            [Piece.Pawn(BLACK, 1, 2), Piece.Pawn(BLACK, 2, 2), Piece.Pawn(BLACK, 3, 2), Piece.Pawn(BLACK, 4, 2),
             Piece.Pawn(BLACK, 5, 2), Piece.Pawn(BLACK, 6, 2), Piece.Pawn(BLACK, 7, 2), Piece.Pawn(BLACK, 8, 2)],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [Piece.Pawn(WHITE, 1, 7), Piece.Pawn(WHITE, 2, 7), Piece.Pawn(WHITE, 3, 7),
             Piece.Pawn(WHITE, 4, 7), Piece.Pawn(WHITE, 5, 7), Piece.Pawn(WHITE, 6, 7),
             Piece.Pawn(WHITE, 7, 7), Piece.Pawn(WHITE, 8, 7)],
            [Piece.Rook(WHITE, 1, 8), Piece.Knight(WHITE, 2, 8), Piece.Bishop(WHITE, 3, 8), Piece.Queen(WHITE, 4, 8),
             Piece.King(WHITE, 5, 8), Piece.Bishop(WHITE, 6, 8), Piece.King(WHITE, 7, 8), Piece.Rook(WHITE, 8, 8)]

        ]
        self.blackDict = {
            PAWN: bp,
            ROOK: br,
            KNIGHT: bn,
            BISHOP: bb,
            QUEEN: bq,
            KING: bk
        }
        self.whiteDict = {
            PAWN: wp,
            ROOK: wr,
            KNIGHT: wn,
            BISHOP: wb,
            QUEEN: wq,
            KING: wk
        }
        self.win = None
        self.turn = WHITE
        self.clicx = 0
        self.clicky = 0

    def startup(self):
        self.win = pygame.display.set_mode((self.width, self.height))
        self.win.blit(chessboard, boardStartPoint)
        pygame.display.update()
        pygame.display.set_caption("CHESS")

    def renderDirectionA(self):
        self.win.blit(chessboard, boardStartPoint)
        for i in range(0, 8):
            for j in range(0, 8):
                if self.grid[i][j] != 0:
                    if self.grid[i][j].colour == WHITE:
                        self.win.blit(self.whiteDict[self.grid[i][j].type], (
                            (self.grid[i][j].position[0] - 1) * piecesize + boardStartPoint[0],
                            (self.grid[i][j].position[1] - 1) * piecesize + boardStartPoint[1]))
                    if self.grid[i][j].colour == BLACK:
                        self.win.blit(self.blackDict[self.grid[i][j].type], (
                            (self.grid[i][j].position[0] - 1) * piecesize + boardStartPoint[0],
                            (self.grid[i][j].position[1] - 1) * piecesize + boardStartPoint[1]))
        pygame.display.update()

    def detectClick(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                (self.clicx, self.clicky) = event.pos
                return self.clicx, self.clicky

    def getMoves(self, x, y, type, colour):
        if type == PAWN:
            if colour == WHITE:
                possible_moves = [(x - 1, y - 2), (x - 1, y - 3), (x, y - 2), (x - 2, y - 2)]
                if y != 7:
                    possible_moves.remove(possible_moves[1])
                for i in possible_moves:
                    if i[1] < 0:
                        possible_moves.remove(i)
                    if i[0] < 0:
                        possible_moves.remove(i)
                    if i[0] > 7:
                        possible_moves.remove(i)
                for i in possible_moves:
                    if self.grid[i[1]][i[0]] != 0:
                        if self.grid[i[1]][i[0]].colour == WHITE:
                            possible_moves.remove(i)
            if colour == BLACK:
                possible_moves = [(x - 1, y), (x - 1, y + 1), (x, y), (x - 2, y)]
                if y != 2:
                    possible_moves.remove(possible_moves[1])
                for i in possible_moves:
                    if i[1] > 7:
                        possible_moves.remove(i)
                    if i[0] < 0:
                        possible_moves.remove(i)
                    if i[0] > 7:
                        possible_moves.remove(i)
                for i in possible_moves:
                    if self.grid[i[1]][i[0]] != 0:
                        if self.grid[i[1]][i[0]].colour == BLACK:
                            possible_moves.remove(i)
        if type == BISHOP:
            possible_moves = []
            for j in range(0, 4):
                for i in range(1, 9):
                    if j == 0:
                        dealer = (x - 1 - i, y - 1 - i)
                    elif j == 1:
                        dealer = (x - 1 + i, y - 1 + i)
                    elif j == 2:
                        dealer = (x - 1 - i, y - 1 + i)
                    else:
                        dealer = (x - 1 + i, y - 1 - i)
                    if dealer[1] > 7 or dealer[1] < 0:
                        break
                    elif dealer[0] > 7 or dealer[0] < 0:
                        break
                    elif self.grid[dealer[1]][dealer[0]] != 0:
                        if self.grid[dealer[1]][dealer[0]].colour == colour:
                            break
                        else:
                            possible_moves.append(dealer)
                            break
                    else:
                        possible_moves.append(dealer)
        if type == ROOK:
            possible_moves = []
            for j in range(0, 4):
                for i in range(1, 9):
                    if j == 0:
                        dealer = (x - 1 - i, y - 1)
                    elif j == 1:
                        dealer = (x - 1 + i, y - 1)
                    elif j == 2:
                        dealer = (x - 1, y - 1 + i)
                    else:
                        dealer = (x - 1, y - 1 - i)
                    if dealer[1] > 7 or dealer[1] < 0:
                        break
                    elif dealer[0] > 7 or dealer[0] < 0:
                        break
                    elif self.grid[dealer[1]][dealer[0]] != 0:
                        if self.grid[dealer[1]][dealer[0]].colour == colour:
                            break
                        else:
                            possible_moves.append(dealer)
                            break
                    else:
                        possible_moves.append(dealer)
        if type == QUEEN:
            possible_moves = []
            for j in range(0, 8):
                for i in range(1, 9):
                    if j == 0:
                        dealer = (x - 1 - i, y - 1)
                    elif j == 1:
                        dealer = (x - 1 + i, y - 1)
                    elif j == 2:
                        dealer = (x - 1, y - 1 + i)
                    elif j == 3:
                        dealer = (x - 1, y - 1 - i)
                    if j == 4:
                        dealer = (x - 1 - i, y - 1)
                    elif j == 5:
                        dealer = (x - 1 + i, y - 1)
                    elif j == 6:
                        dealer = (x - 1, y - 1 + i)
                    else:
                        dealer = (x - 1, y - 1 - i)
                    if dealer[1] > 7 or dealer[1] < 0:
                        break
                    elif dealer[0] > 7 or dealer[0] < 0:
                        break
                    elif self.grid[dealer[1]][dealer[0]] != 0:
                        if self.grid[dealer[1]][dealer[0]].colour == colour:
                            break
                        else:
                            possible_moves.append(dealer)
                            break
                    else:
                        possible_moves.append(dealer)

board = Board(width, height)
board.startup()
board.renderDirectionA()
while True:
    pass
