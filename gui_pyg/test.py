import pygame, sys
from gui import GUI
from . import create_gui
import gui_element
pygame.init()


def clicker():
    print("Click!")


my_gui = create_gui(pygame.Surface((200, 200)))
button_one = gui_element.button.Button(40, 10, 50, 50, clicker, color=(0, 50, 200))
my_gui.elements.append(button_one)
my_gui.blit_elements()

screen = pygame.display.set_mode((200, 200))
screen.set_caption("Testing")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        my_gui.blit_elements()
        screen.blit(my_gui)
