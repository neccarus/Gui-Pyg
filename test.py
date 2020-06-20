import pygame
import sys
import json
from guipyg import gui
from guipyg import create_gui
from guipyg.gui_element.button import Button
from guipyg.gui_element.menu import Menu

pygame.init()


def clicker(mouse_pos):
    print("Click! " + str(mouse_pos))


button_one = Button(150, 50, 10, 50, function=clicker, name="Button One", color=(150, 150, 150))
button_two = Button(150, 50, 10, 110, function=clicker, name="Button Two", color=(150, 150, 150))
gui.functions["clicker"] = clicker
my_menu = Menu(400, 400, 50, 50, "Menu One", color=(50, 50, 50), elements=[button_one, button_two], is_visible=False)
button_three = Button(150, 50, 10, 30, my_menu.toggle_visibility, "Button 3", (150, 150, 150))
my_menu_two = Menu(250, 200, 500, 50, "Menu Two", color=(50, 50, 50), elements=[button_three])
my_menu.font_color = (250, 250, 250)
my_menu_two.font_color = (250, 250, 250)
screen = pygame.display.set_mode((800, 600), 0, 32)
my_gui = create_gui(800, 600, 0, 0, elements=[])
my_gui.elements.append(my_menu)
my_gui.elements.append(my_menu_two)
gui.functions["toggle_visibility"] = gui.match_element_name(my_gui, "Menu One").toggle_visibility
pygame.display.set_caption("Testing")

gui_json = gui.encode_gui(my_gui)
with open('gui_file.json', 'w') as w:
    json.dump(gui_json, w)

del my_gui

with open('gui_file.json', 'r') as r:
    gui_json = json.load(r)
my_gui = gui.decode_gui(gui_json)
#print((gui.match_element_name(my_gui, "Menu One")).__dict__)
gui.functions["toggle_visibility"] = gui.match_element_name(my_gui, "Menu One").toggle_visibility
print(gui.functions)
gui.update_element_functions(my_gui, gui.functions)
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
    screen.fill((80, 80, 80))
