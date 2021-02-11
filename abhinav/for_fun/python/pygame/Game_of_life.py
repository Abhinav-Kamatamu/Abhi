import pygame
from time import sleep

w = 500
h = w
r = 50
c = r


class Board:
    def __init__(self, wid, hei, row, col):
        self.width = wid
        self.height = hei
        self.rows = row
        self.columns = col
        self.win = None

    def adjust_size(self):
        if self.width % self.columns != 0:
            self.width -= self.width % self.columns

        if self.height % self.rows != 0:
            self.height -= self.height % self.rows

    def window(self):
        self.adjust_size()
        self.win = pygame.display.set_mode((self.width, self.height))
        self.win.fill((0, 0, 0))
        pygame.display.update()

    def update(self):
        pygame.display.update()
        self.win.fill((0, 0, 0))
        sleep(1)


board = Board(w, h, r, c)


class Cell:
    def __init__(self, x, y, attribute):
        global board
        self.x = x
        self.y = y
        self.activeNeighbours = 0
        self.sizex = board.width // board.columns
        self.sizey = board.height // board.rows
        self.listat = attribute
        if self.listat == 2 or self.listat == 53 or self.listat == 101 or self.listat == 102 or self.listat == 103:
            self.fake_state = 1
            self.state = 1
        else:
            self.fake_state = 0
            self.state = 0

    def neighbours(self):
        neighbours_list = []

        global board
        neighbours_list.append((self.x, self.y + self.sizey))
        neighbours_list.append((self.x, self.y - self.sizey))
        neighbours_list.append((self.x - self.sizex, self.y + self.sizey))
        neighbours_list.append((self.x + self.sizex, self.y - self.sizey))
        neighbours_list.append((self.x - self.sizex, self.y - self.sizey))
        neighbours_list.append((self.x + self.sizex, self.y + self.sizey))
        neighbours_list.append((self.x + self.sizex, self.y))
        neighbours_list.append((self.x - self.sizex, self.y))

        return neighbours_list

    def active_neighbours(self):
        global classList
        self.activeNeighbours = 0
        match = 0
        times = 0
        for i in classList:
            if (i.x, i.y) == self.neighbours()[times]:
                times += 1
                match += 1
                if i.state == 1:
                    self.activeNeighbours += 1
        return self.activeNeighbours

    def update(self):
        self.active_neighbours()
        print(self.activeNeighbours)
        if self.activeNeighbours < 2:
            self.fake_state = 0
        if self.activeNeighbours == 2 and self.state == 1:
            self.fake_state = 1
        if self.activeNeighbours == 3 and self.state == 1:
            self.fake_state = 1
        if self.activeNeighbours > 3:
            self.fake_state = 0
        if self.activeNeighbours == 3 and self.state == 0:
            self.fake_state = 1

    def show(self):
        if self.state == 1:
            pygame.draw.rect(board.win, (255, 255, 255), [self.x, self.y, self.sizex, self.sizey])
        if self.state == 0:
            pygame.draw.rect(board.win, (255, 255, 255), [self.x, self.y, self.sizex, self.sizey], 1)

    def change_board(self):
        self.state = self.fake_state


# ---- Variables ---- #
classList = []
at = 1
# ---- /Variables ---- #

for i in range(board.rows):
    for j in range(board.columns):
        x = (i) * board.width // board.columns
        y = j * board.height // board.rows
        classList.append(Cell(x, y, at))
        at += 1

# ---- Board ---- #
board.window()
# ---- Board ---- #
for i in classList:
    if i.listat == 2 or i.listat == 53 or i.listat == 101 or i.listat == 102 or i.listat == 103:
        i.fake_state = 1
        i.state = 1
while True:
    for i in classList:
        i.update()
    for i in classList:
        i.show()
        i.change_board()
    board.update()
