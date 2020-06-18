import pygame
import sys
from guipyg.gui import GUI
from guipyg import create_gui
from guipyg.gui_element.button import Button
from guipyg.gui_element.menu import Menu
pygame.init()


def clicker(mousepos):
    print("Click!" + str(mousepos))


button_one = Button(250, 100, 50, 50, function=clicker, color=(0, 50, 200))
button_two = Button(200, 100, 50, 250, function=clicker, color=(200, 0, 150))
my_menu = Menu(400, 400, 50, 50, color=(200, 200, 0), elements=[button_one, button_two])
screen = pygame.display.set_mode((500, 500), 0, 32)
my_gui = create_gui(screen, 500, 500, 0, 0, elements=[])
my_gui.elements.append(my_menu)
pygame.display.set_caption("Testing")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in my_gui.elements:
                element.click(pygame.mouse.get_pos())

    my_gui.fill_elements()
    my_gui.fill((150, 150, 150))
    my_gui.blit_elements()
    screen.blit(my_gui, (0, 0))
    pygame.display.update()
    screen.fill((0, 0, 0))
