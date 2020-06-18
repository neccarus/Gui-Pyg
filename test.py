import pygame
import sys
import json
from guipyg import gui
from guipyg.gui import GUI
from guipyg import create_gui
from guipyg.gui_element.button import Button
from guipyg.gui_element.menu import Menu
pygame.init()


def clicker(mouse_pos):
    print("Click! " + str(mouse_pos))


button_one = Button(150, 50, 10, 50, function=clicker, name="Button One", color=(0, 50, 200))
button_two = Button(150, 50, 10, 110, function=clicker, name="Button Two", color=(200, 0, 150))
my_menu = Menu(400, 400, 50, 50, color=(200, 150, 0), elements=[button_one, button_two], is_visible=False)
button_three = Button(150, 50, 10, 30, my_menu.toggle_visibility, "Button 3", (170, 170, 170))
my_menu_two = Menu(250, 200, 500, 500, color=(255, 255, 255), elements=[button_three])
screen = pygame.display.set_mode((800, 800), 0, 32)
my_gui = create_gui(800, 800, 0, 0, elements=[])
my_gui.elements.append(my_menu)
my_gui.elements.append(my_menu_two)
pygame.display.set_caption("Testing")

gui_json = gui.encode_gui(my_gui)
with open('gui_file.json', 'w') as w:
    json.dump(gui_json, w)

with open('gui_file.json', 'r') as r:
    gui_json = json.load(r)
my_gui = gui.decode_gui(gui_json)
print(gui_json)
print(my_gui.elements)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index, element in enumerate(my_gui.elements):
                if element.is_visible:
                    element.click(pygame.mouse.get_pos())

    my_gui.update(screen)
    pygame.display.update()
    screen.fill((0, 0, 0))

