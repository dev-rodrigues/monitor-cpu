import pygame
import random

### Windows Config. ###

width_window = 800
height_window = 600

window = pygame.display.set_mode((width_window, height_window))
pygame.display.set_caption("ATQ08.0")
pygame.display.init()

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 20)

### Colors ###
yellow = (255, 170, 0)
blue = (10, 10, 100)
grey = (45, 45, 45)
light_grey_1 = (70, 70, 70)
light_grey_2 = (155, 155, 155)
black = (0, 0, 0)
red = (200,0,0)

### Surface ###
s = pygame.surface.Surface((width_window, height_window))

### Atributes ###

class Square:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.side = 50
        self.color = yellow

class Circle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.height = 0
        self.color = grey

def make_square():
    square = Square()
    square.x = random.randint(0, 750)
    square.y = random.randint(0, 550)
    return square

def make_circle():
    circle = Circle()
    circle.x = 400
    circle.y = 300
    circle.radius = 50
    return circle

### Display ###
text_1 = "Clique"
text_1_render = font.render(text_1, 10, black)
s.blit(text_1_render, (10, 10))

square = make_square()
circle = make_circle()

collision = False

clock = pygame.time.Clock()
cont = 60
close = False

while not close:

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if button_1.collidepoint((pos[0], pos[1])):
                square = make_square()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                square = make_square()
            if (event.key == pygame.K_w):
                circle.y -= 10
            if (event.key == pygame.K_s):
                circle.y += 10
            if (event.key == pygame.K_a):
                circle.x -= 10
            if (event.key == pygame.K_d):
                circle.x += 10
                                                                    
        if event.type == pygame.QUIT:
            close = True

    s.fill(grey)        

    if not collision:
        pygame.draw.rect(s, square.color, (square.x, square.y, square.side, square.side))
    
    button_1 = pygame.draw.circle(s, light_grey_2, [circle.x, circle.y], circle.radius)
    s.blit(text_1_render, ((circle.x - 30), (circle.y - 6)))

    window.blit(s, (0, 0))
    
    if button_1.collidepoint((square.x, square.y)):
        collision = True
    elif button_1.collidepoint(((square.x + square.side), (square.y + square.side))):
        collision = True
    elif button_1.collidepoint(((square.x + square.side), square.y)):
        collision = True
    elif button_1.collidepoint((square.x, (square.y + square.side))):
        collision = True

    pygame.display.update()
    clock.tick(60)
    
pygame.display.quit()