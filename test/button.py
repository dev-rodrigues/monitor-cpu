import pygame
import random

pygame.init()

pink = (255, 185, 185)
font_obj = pygame.font.Font('freesansbold.ttf', 20)
x = 100
y = 50
cor = (255, 233, 233)

def draw_button(button, screen):
    pygame.draw.circle(screen, cor, (150+x, 70+y), 60, 1)
    screen.blit(button['text'], (120+x, 50+y))


def create_button(w, h, text, callback):
    global x, y

    text_surf = font_obj.render(text, True, (0, 0, 0))

    button = {
        'rect': pygame.Rect(x+90, y, w-10, h),
        'text': text_surf,
        'color': (255, 0, 255),
        'callback': callback,
        }
    return button


def main():
    global x, y
    screen = pygame.display.set_mode((400, 400))
    done = False
    squares = []

    def addRect():
        randomsValues = [random.randint(0, 400), random.randint(0, 400)]
        newDraw = [screen, (255, 255, 0), (randomsValues[0], randomsValues[1], 50, 50)]
        testRect = False
        for i in range(len(squares)-1, -1, -1):
            auxSquare = pygame.draw.rect(squares[i][0], squares[i][1], squares[i][2])
            if auxSquare.collidepoint((randomsValues[0], randomsValues[1])):
                squares.pop(i)
                testRect = True
        if testRect == False:
            squares.append(newDraw)
        screen.fill(pink)

    button1 = create_button(135, 135, 'clique', addRect)
    screen.fill(pink)
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button1['rect'].collidepoint(event.pos):
                        button1['callback']()

            elif event.type == pygame.KEYDOWN:
                screen.fill(pink)
                if event.key == pygame.K_w:
                    y -= 10
                    button1 = create_button(135, 135, 'clique', addRect)

                if event.key == pygame.K_s:
                    y += 10
                    button1 = create_button(135, 135, 'clique', addRect)

                if event.key == pygame.K_a:
                    x -= 10
                    button1 = create_button(135, 135, 'clique', addRect)

                if event.key == pygame.K_d:
                    x += 10
                    button1 = create_button(135, 135, 'clique', addRect)
                for i in range(len(squares) - 1, -1, -1):
                    if button1['rect'].collidepoint(squares[i][2][0], squares[i][2][1]):
                        squares.pop(i)

        draw_button(button1, screen)

        for square in squares:
            pygame.draw.rect(square[0], square[1], square[2])
        pygame.display.update()


main()
pygame.quit()