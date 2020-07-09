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
from guipyg.gui_style.style_item import theme_dict

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

SCREENSIZE = (1280, 720)

font = pygame.font.SysFont("times new roman", 22)
font_pos_x = 10
font_pos_y = 10
font_color = (0, 255, 0)


def clicker(*_, **__):
    mouse_pos = pygame.mouse.get_pos()
    print("Click! " + str(mouse_pos))


def display_fps(fps, surface):
    text_obj = font.render(fps, True, font_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (font_pos_x, font_pos_y)
    surface.blit(text_obj, text_rect)


def swap_theme(gui_obj, themes):
    for theme in themes:
        if theme != gui_obj.theme:
            gui_obj.theme = theme
            gui_obj.apply_theme()
            break


gui_create_timer_start = datetime.now()

button_one = Button(150, 50, 10, 50, function=clicker, name="Button One", color=(150, 150, 150))
button_two = Button(150, 50, 10, 110, function=clicker, name="Button Two", color=(150, 150, 150))
my_menu = Menu(400, 400, 50, 50, "Menu One", color=(50, 50, 50), elements=[button_one, button_two], is_visible=False)
button_three = Button(150, 50, 10, 30, my_menu.toggle_visibility, "Button 3", (150, 150, 150))
my_menu_two = Menu(250, 200, 500, 50, "Menu Two", color=(50, 50, 50), elements=[button_three])
button_four = Button(150, 50, 10, 50, function=swap_theme, name="Button 4", color=(150, 150, 150))
my_menu_three = Menu(200, 150, 400, 200, "Menu Three", (50, 50, 50), elements=[button_four])
my_gui = create_gui(1280, 720, 0, 0, theme="my_theme")
my_gui.elements.append(my_menu)
my_gui.elements.append(my_menu_two)
my_gui.elements.append(my_menu_three)
my_gui.apply_theme()
gui.functions["toggle_visibility"] = gui.match_element_name(my_gui, "Menu One").toggle_visibility
gui.functions["swap_theme"] = swap_theme
gui.functions["clicker"] = clicker

gui_create_timer_end = datetime.now()

print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to create the GUI.")

# screen = pygame.display.set_mode((848, 480), pygame.FULLSCREEN | pygame.SCALED)
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Testing")

gui_create_timer_start = datetime.now()

gui.save_gui(my_gui, 'gui_file.json')

gui_create_timer_end = datetime.now()

print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to save the GUI to a file.")

del my_gui

gui.functions["clicker"] = clicker
gui.functions["toggle_visibility"] = Element().toggle_visibility

gui_create_timer_start = datetime.now()

my_gui = gui.load_gui("gui_file.json")
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
                pygame.display.set_mode(SCREENSIZE, pygame.FULLSCREEN | pygame.SCALED)
            if event.key == ord('g'):
                # pygame.display.set_mode((848, 480), pygame.SCALED)
                pygame.display.set_mode(SCREENSIZE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            my_gui.select_element(current_mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            current_mouse_pos = pygame.mouse.get_pos()
            my_gui.activate_selected(current_mouse_pos, my_gui, theme_dict)
            my_gui.let_go()

    my_gui.drag_selected()

    my_gui.update(screen)
    display_fps(str(round(clock.get_fps(), 1)), screen)
    pygame.display.update(my_gui.clip_rect)
    screen.fill((80, 80, 80))
    clock.tick()

    # clock.tick(60)
