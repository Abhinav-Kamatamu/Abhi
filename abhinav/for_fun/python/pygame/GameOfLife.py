import pygame
w = 500
h = w

win = pygame.display.set_mode((w,h))

size = 10
cell_state = []


def createGrid(number):
    for i in range(1, number):
        cell_state.append([])
        for j in range(number):
            cell_state[i - 1].append(0)


createGrid(size)

cell_state[0][1] = 1
cell_state[1][2] = 1
cell_state[2][1] = 1
cell_state[2][2] = 1
cell_state[2][0] = 1
cell_state_2 = cell_state
print(cell_state)


def getCordinates(a, b):
    for i in range(size - 1):
        if a == i:
            x = i * size
        if b == i:
            y = i * size
    return x, y


def show(a, b):
    x, y = getCordinates(a, b)
    if cell_state[a][b] == 1:
        pygame.draw.rect(win, (0,0,0), [x, y, w // size, h // size])
        pygame.draw.rect(win, (255,255,255), [x, y, w // size, h // size],1)
    else:
        pygame.draw.rect(win, (0,0,0), [x, y, w // size, h // size], 1)


def display():

    for i in range(size - 1):
        for j in range(size - 1):
            show(i, j)

    pygame.display.update()
    win.fill((255,255,255))



def surroundingBlocks(a, b):
    count = 0
    try:
        if cell_state[a][b + 1] == 1:
            count += 1
    except IndexError:
        pass
    try:
        if cell_state[a + 1][b + 1] == 1:
            count += 1
    except IndexError:
        pass
    try:
        if cell_state[a + 1][b] == 1:
            count += 1
    except IndexError:
        pass
    try:
        if cell_state[a - 1][b] == 1:
            count += 1
    except IndexError:
        pass
    try:
        if cell_state[a - 1][b - 1] == 1:
            count += 1
    except IndexError:
        pass
    try:
        if cell_state[a][b - 1] == 1:
            count += 1
    except IndexError:
        pass
    try:
        if cell_state[a + 1][b - 1] == 1:
            count += 1
    except IndexError:
        pass
    try:
        if cell_state[a - 1][b + 1] == 1:
            count += 1
    except IndexError:
        pass
    return count


def update(block):
    for i in range(block - 1):
        for j in range(block - 1):
            if surroundingBlocks(i, j) < 2:
                cell_state_2[i][j] = 0
            if surroundingBlocks(i, j) == 2 and cell_state[i][j] == 1:
                cell_state_2[i][j] = 1
            if surroundingBlocks(i, j) == 3 and cell_state[i][j] == 1:
                cell_state_2[i][j] = 1
            if surroundingBlocks(i, j) > 3:
                cell_state_2[i][j] = 0
            if surroundingBlocks(i, j) == 3 and cell_state[i][j] == 0:
                cell_state_2[i][j] = 1

g = 0
while True:
    update(size)
    display()
    cell_state = cell_state_2
    if g == 0 or g == 1:
        print(cell_state)
        g += 1
print(cell_state)
