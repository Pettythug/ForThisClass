"""
Style: main and subroutines
Components: main program and subroutines
Connectors: procedure calls
Constraints: components can't communicate using shared memory (e.g. global 
variables) 
Gains: change the implementation of a subroutine without affecting the main 
program.  
"""

from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_w, K_s, K_a, K_d, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE


############################################################

def process_input(prev_direction): ############# Q2: Here is where i changed the control keys. 
    keep_going, direction, pause = True, prev_direction, True
    for event in pygame.event.get():
        if event.type == QUIT:
            keep_going = False
        if event.type == KEYDOWN:            
            key = event.key
        
            if key == K_ESCAPE:
                keep_going = False
            elif key == K_w:
                direction = (0, -1)
            elif key == K_s:
                direction = (0, 1)
            elif key == K_a:
                direction = (-1, 0)
            elif key == K_d:
                direction = (1, 0)
            if key == K_SPACE: ###################Q5: Here is where I entered pause feature. Also lets you exit the program while paused.
                event = pygame.event.wait() ## sets event to vaiable that pauses the program
                while pause: 
                    event = pygame.event.wait() ## sets event to vaiable that pauses the program

                    if event.type == KEYDOWN and event.key == K_SPACE: #if th it sets pause to false or true and keeps looping till it is pressed again.
                        pause = not pause
                    if event.type == QUIT: ## Lets you exit while paused. 
                        keep_going = False #Breaks the main loop 
                        pause = not pause
    return keep_going, direction

############################################################

def draw_everything(screen, mybox, pellets, borders): ####### Q1: Here is where I changed the colors to the pellets and box and screen and borders.#########
    screen.fill((64, 0, 64))  # dark blue
    pygame.draw.rect(screen, (255, 191, 0), mybox)  # Deep Sky Blue
    [pygame.draw.rect(screen, (203, 192, 255), p) for p in pellets]  # pink
    [pygame.draw.rect(screen, (255, 191, 0), b) for b in borders]  # red
    pygame.display.update()

############################################################

def create_box(dims):
    w, h = dims
    box = pygame.Rect(w / 2, h / 2, 10, 10)  # start in middle of the screen
    direction = 0, 1  # start direction: down
    return box, direction

############################################################

def collide(box, boxes):
    # return True if box collides with any entity in boxes
    return box.collidelist(boxes) != -1 ### Q3b:
    
############################################################

def move(box, direction ): 
    return box.move(direction[0] * 2, direction[1] * 2) #### Q3a: Speeds up the player without affecting the FPS

############################################################

def create_borders(dims, thickness=2):
    w, h = dims
    return [pygame.Rect(0, 0, thickness, h),
            pygame.Rect(0, 0, w, thickness),
            pygame.Rect(w - thickness, 0, thickness, h),
            pygame.Rect(0, h - thickness, w, thickness),
            pygame.Rect(w/2, h / 3, 100, thickness), # Q4: Changed here to add the two obstacles to the game. 
            pygame.Rect(w/3, h / 2, thickness, 100)]
    
############################################################

def create_pellet(dims, offset):
    w, h = dims
    return pygame.Rect(randint(offset, w - offset),
                       randint(offset, h - offset), 5, 5)

def create_pellets(dims, qty, offset=10): 
    # the only Pygame-independent subroutine
    return [create_pellet(dims, offset) for _ in range(qty)]
    
def eat_and_replace_colliding_pellet(box, pellets, dims, offset=10):
    p_index = box.collidelist(pellets) ## Q3b: 
    if p_index != -1:  # ate a pellet: grow, and replace a pellet
        pellets[p_index] = create_pellet(dims, offset)
        box.size = box.width * 1.2, box.height * 1.2
    return box, pellets
    
############################################################

pygame.init()
clock = pygame.time.Clock()

# display
dims = 400, 300
screen = pygame.display.set_mode(dims)

# game objects
borders = create_borders(dims)
pellets = create_pellets(dims, 4)
mybox, direction = create_box(dims)

# game loop
keep_going = True
while keep_going:

    keep_going, direction = process_input(direction)
    
    mybox = move(mybox, direction)
    if collide(mybox, borders):
        mybox, direction = create_box(dims)
    mybox, pellets = eat_and_replace_colliding_pellet(mybox, pellets, dims)
    
    draw_everything(screen, mybox, pellets, borders)
    
    clock.tick(50) # or sleep(.02) to have the loop Pygame-independent