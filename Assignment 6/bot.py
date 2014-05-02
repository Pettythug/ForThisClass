

################### CONTROLLER #############################

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE
from common import *

class Controller():
    def __init__(self, m):
        self.m = m
        pygame.init()
    
    def poll(self):
        cmd = ''
        for event in pygame.event.get(): # inputs
            if event.type == QUIT:
                cmd = 'quit'
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    cmd = 'quit'
            
        if (cmd != 'quit'):
            cmd = choice(['up', 'down', 'left', 'right'])
                
        if cmd:
            self.m.do_cmd(cmd)

################### VIEW #############################

class View():
    count = 50
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        
    def display(self):
        if (v.count > 50):
            screen = self.screen
            borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
            pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
            b = self.m.mybox
            myrect = pygame.Rect(b[0], b[1], b[2], b[3])
            screen.fill((0, 0, 64))  # dark blue
            pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
            [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
            [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
            
            pygame.display.update()
            v.count = 0
        v.count += 1
    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)



       

        
while not model.game_over:

    sleep(0.02)
    c.poll()
    model.update()
    v.display()
