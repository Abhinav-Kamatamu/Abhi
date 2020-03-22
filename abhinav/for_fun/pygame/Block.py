import pygame
from pygame.local import *

pygame.init()

window_width

start = pygame.time.get_ticks()
class Block():
    def __init__(self, color, breadth):
        self.color = color
        self.breadth = breadth
        self.x = random.randint(1,200)
        self.y = -self.breadth
        self.height = self.breadth
        self.speed = 5
        self.cooldown = random.randint(0, 8000)
        self.now = None
    def draw(self):
        win.fill((255,255,255))
        pygame.draw.rect(win,self.color,(self.x,self.y,self.breadth,self.height))
        pygame.display.update()
    def move(self):
        global start
        while:
            self.now = pygame.time.get_ticks()
            self.draw()
            if start - self.now >= self.cooldown:
                self.y += self.speed
                if self.y > window_width + self.breadth:
                    self.y = -self.breadth
    def ()
