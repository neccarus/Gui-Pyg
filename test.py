import pygame
import sys
import json
from guipyg import gui
from datetime import datetime
from guipyg import create_gui
from guipyg.gui_element.button import Button
from guipyg.gui_element.menu import Menu
from guipyg.gui_element.element import Element
from guipyg.gui_style.style_item import style_dict

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

button_one = Button(150, 50, 10, 50, function=clicker, name="Button One", color=(150, 150, 150), style="my_button_style")
button_two = Button(150, 50, 10, 110, function=clicker, name="Button Two", color=(150, 150, 150), style="my_button_style")
my_menu = Menu(400, 400, 50, 50, "Menu One", color=(50, 50, 50), elements=[button_one, button_two], is_visible=False, style="my_first_style")
button_three = Button(150, 50, 10, 30, my_menu.toggle_visibility, "Button 3", (150, 150, 150), style="my_button_style")
my_menu_two = Menu(250, 200, 500, 50, "Menu Two", color=(50, 50, 50), elements=[button_three], style="my_first_style")
button_four = Button(150, 50, 10, 50, function=clicker, name="Button Four", color=(150, 150, 150), style="my_button_style")
my_menu_three = Menu (200, 150, 400, 200, "Menu Three", (50, 50, 50), elements=[button_four], style="my_first_style")
my_menu.font_color = (250, 250, 250)
my_menu_two.font_color = (250, 250, 250)
my_menu_three.font_color = (250, 250, 250)
screen = pygame.display.set_mode((1280, 720), 0, 32)
pygame.display.toggle_fullscreen()
my_gui = create_gui(1280, 720, 0, 0)
my_gui.elements.append(my_menu)
my_gui.elements.append(my_menu_two)
my_gui.elements.append(my_menu_three)
gui.functions["toggle_visibility"] = gui.match_element_name(my_gui, "Menu One").toggle_visibility
gui.functions["clicker"] = clicker
pygame.display.set_caption("Testing")

gui_json = gui.encode_gui(my_gui)
with open('gui_file.json', 'w') as w:
    json.dump(gui_json, w)

del my_gui

gui.functions["clicker"] = clicker
gui.functions["toggle_visibility"] = Element().toggle_visibility

with open('gui_file.json', 'r') as r:
    gui_json = json.load(r)
my_gui = gui.decode_gui(gui_json)
gui.functions["toggle_visibility"] = gui.match_element_name(my_gui, "Menu One").toggle_visibility
gui.update_element_functions(my_gui)

clock = pygame.time.Clock()
while True:
    current_mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            reversed_elements = my_gui.elements[::-1]
            for element in reversed_elements:
                if element.is_visible and element.is_draggable:
                    if element.rect.collidepoint(element.get_mouse_pos(current_mouse_pos)):
                        element.drag_toggle = True
                        drag = element.drag_element(current_mouse_pos, datetime.now())
                        break
        if event.type == pygame.MOUSEBUTTONUP:
            reversed_elements = my_gui.elements[::-1]
            for element in reversed_elements:
                if element.is_visible:
                    element.click(mouse_pos=current_mouse_pos)
                    my_gui.need_update = True
                    element.drag_toggle = False
                    #element.drag_timer_start = 0

    for element in my_gui.elements:
        if element.is_visible and element.drag_toggle:
            element.pos_x, element.pos_y = next(drag)
            my_gui.need_update = True

    my_gui.update(screen)
    display_fps(str(round(clock.get_fps(), 1)), screen)
    pygame.display.update()
    screen.fill((80, 80, 80))
    clock.tick()

    # clock.tick(60)
