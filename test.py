import pygame
import sys
import json
from guipyg import gui
from datetime import datetime
from guipyg import create_gui
from guipyg.gui_element.button import Button
from guipyg.gui_element.menu import Menu
from guipyg.gui_element.element import Element
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

font = pygame.font.SysFont("times new roman", 22)
font_pos_x = 10
font_pos_y = 10
font_color = (0, 255, 0)


def clicker(mouse_pos):
    print("Click! " + str(mouse_pos))


def display_fps(fps, surface):
    text_obj = font.render(fps, True, font_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (font_pos_x, font_pos_y)
    surface.blit(text_obj, text_rect)


gui_create_timer_start = datetime.now()

button_one = Button(150, 50, 10, 50, function=clicker, name="Button One", color=(150, 150, 150))
button_two = Button(150, 50, 10, 110, function=clicker, name="Button Two", color=(150, 150, 150))
my_menu = Menu(400, 400, 50, 50, "Menu One", color=(50, 50, 50), elements=[button_one, button_two], is_visible=False)
button_three = Button(150, 50, 10, 30, my_menu.toggle_visibility, "Button 3", (150, 150, 150))
my_menu_two = Menu(250, 200, 500, 50, "Menu Two", color=(50, 50, 50), elements=[button_three])
button_four = Button(150, 50, 10, 50, function=clicker, name="Button Four", color=(150, 150, 150))
my_menu_three = Menu(200, 150, 400, 200, "Menu Three", (50, 50, 50), elements=[button_four])
my_gui = create_gui(848, 480, 0, 0, theme="my_theme")
my_gui.elements.append(my_menu)
my_gui.elements.append(my_menu_two)
my_gui.elements.append(my_menu_three)
my_gui.apply_theme()
gui.functions["toggle_visibility"] = gui.match_element_name(my_gui, "Menu One").toggle_visibility
gui.functions["clicker"] = clicker

gui_create_timer_end = datetime.now()

print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to create the GUI.")

screen = pygame.display.set_mode((848, 480), pygame.FULLSCREEN | pygame.SCALED)
# pygame.display.toggle_fullscreen()
pygame.display.set_caption("Testing")

gui_create_timer_start = datetime.now()

gui_json = gui.encode_gui(my_gui)
with open('gui_file.json', 'w') as w:
    json.dump(gui_json, w)

gui_create_timer_end = datetime.now()

print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to save the GUI to a file.")

del my_gui

gui.functions["clicker"] = clicker
gui.functions["toggle_visibility"] = Element().toggle_visibility

gui_create_timer_start = datetime.now()

with open('gui_file.json', 'r') as r:
    gui_json = json.load(r)
my_gui = gui.decode_gui(gui_json)
my_gui.apply_theme()
gui.functions["toggle_visibility"] = gui.match_element_name(my_gui, "Menu One").toggle_visibility
gui.update_element_functions(my_gui)

gui_create_timer_end = datetime.now()

print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to load the GUI from a file.")

clock = pygame.time.Clock()
drag = None
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                sys.exit()
            if event.key == ord('f'):
                pygame.display.set_mode((848, 480), pygame.FULLSCREEN | pygame.SCALED)
            if event.key == ord('g'):
                pygame.display.set_mode((848, 480), pygame.SCALED)

        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            my_gui.select_element(current_mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            current_mouse_pos = pygame.mouse.get_pos()
            my_gui.let_go()
            reversed_elements = my_gui.elements[::-1]
            for element in reversed_elements:
                if element.is_visible:
                    element.click(mouse_pos=current_mouse_pos)
                    my_gui.need_update = True

    my_gui.drag_selected()

    my_gui.update(screen)
    display_fps(str(round(clock.get_fps(), 1)), screen)
    # try:
    #     pygame.display.update()
    # finally:
    pygame.display.update()
    screen.fill((80, 80, 80))
    clock.tick()

    # clock.tick(60)
