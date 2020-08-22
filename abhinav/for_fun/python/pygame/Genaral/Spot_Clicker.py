import pygame
#-------Init--------
pygame.init()
# -------Init--------

# -----Variables-----
w = 300
h = w
fps = 60
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Clicker')
x = int(0.1 * w)
y = int(0.9 * h)
cx = int(0.125 * w) + 4
cy = int(0.925 * h)
r = int(1 / 30 * w)
l = int(0.8 * w)
b = int(0.05 * h)
run = True
speed = 7
mx = 0
points = 0
touched = 0
click_disabled = False
click_time = 0
clock = pygame.time.Clock()


# -----Variables-----

# -----Functions-----
def pointing():
    global cx
    if (w / 2 > cx > w / 2 - int(0.017 * w)) or (w / 2 < cx < w / 2 + int(0.017 * w)):
        return 16
    if (w / 2 > cx > w / 3) or (w / 2 < cx < w / 3):
        return 4
    if (w / 3 > cx > w / 4) or (w / 3 < cx < w / 4):
        return 1
    else:
        return 0


def click():
    global points, w, y
    if play.collidepoint(w // 2, cy):
        points += pointing()
    else:
        points += pointing()


def in_loops():
    global run, click_time, click_disabled
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not click_disabled:
            click()
            click_time = 0
            click_disabled = True
        if click_disabled:
            click_time += 1
            if click_time == 10:
                click_disabled = False
                click_time = 0
    move()


def move():
    global cx, touched
    if cx >= x + l - r or cx <= x + r:
        touched += 1
    if touched % 2 == 1:
        cx += speed
    if touched % 2 == 0:
        cx -= speed


# -----Functions-----
while run:
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (255, 50, 50), (x, y, l, b))
    pygame.draw.line(win, (0, 255, 0), (w / 2, y), (w / 2, y + b), int(1 / 150 * w))
    play = pygame.draw.circle(win, (0, 0, 0), (cx, cy), r, int(1 / 150 * w))
    in_loops()
    _type_ = pygame.font.Font('freesansbold.ttf', 32)
    text = _type_.render('Score:- {}'.format(points), True, (0, 0, 255))
    textrect = text.get_rect()
    textrect.center = (w // 2, h // 2)
    win.blit(text, textrect)
    pygame.display.update()
    clock.tick(fps)
