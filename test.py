import pygame
import sys
import json
from guipyg import gui
from datetime import datetime
# from guipyg import create_gui
from guipyg.gui import GUI
from guipyg.gui_element.button import Button
from guipyg.gui_element.menu import Menu
from guipyg.gui_element.textbox import TextBox
from guipyg.gui_element.element import Element
import os
from guipyg.gui_style.style_item import theme_dict
from guipyg.utils.utils import Instance

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


class Basic(Instance):

    def __init__(self, name):
        self.name = name
        super().add_instance()

    def instance_method(self, *_, **__):
        print("This method was called from a class outside of the Element inheritance")


basic = Basic('basic')

gui_create_timer_start = datetime.now()

button_one = Button(200, 50, 10, 50, name="Button One", msg="Click Me!", color=(150, 150, 150))
button_one.function = button_one.StoredFunction("", "__main__", "clicker", None, button_one)
button_two = Button(200, 50, 10, 110, name="Button Two", msg="Click Me!", color=(150, 150, 150))
button_two.function = button_two.StoredFunction("", "__main__", "instance_method", 'basic', button_two)
text_box = TextBox(200, 200, 10, 170, "Text")
my_menu = Menu(400, 400, 50, 50, "Menu One", color=(50, 50, 50), elements=[button_one, button_two, text_box], is_visible=False)
button_three = Button(200, 50, 10, 30, name="Button 3", msg="Toggle Visibility", color=(150, 150, 150))
button_three.function = button_three.StoredFunction("guipyg.gui_element", ".element", "toggle_visibility", "Menu One", button_three)
my_menu_two = Menu(250, 200, 500, 50, "Menu Two", color=(50, 50, 50), elements=[button_three])
button_four = Button(150, 50, 10, 50, name="Button 4", msg="Swap Theme", color=(150, 150, 150))
my_menu_three = Menu(200, 150, 400, 200, "Menu Three", (50, 50, 50), elements=[button_four])
my_gui = GUI(1280, 720, 0, 0, theme="my_theme", name="My Gui")
button_four.function = button_four.StoredFunction("", "__main__", "swap_theme", None, button_four)
my_gui.elements.extend([my_menu, my_menu_two, my_menu_three])
my_gui.apply_theme()

gui_create_timer_end = datetime.now()

print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to create the GUI.")

screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Testing")

gui_create_timer_start = datetime.now()

gui.save_gui(my_gui, 'gui_file.json')

gui_create_timer_end = datetime.now()

print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to save the GUI to a file.")
del my_gui
del button_one, button_two, button_three, button_four, my_menu, my_menu_two, my_menu_three, text_box

# gui.GUI.deactivate_element(my_gui)

gui_create_timer_start = datetime.now()

my_gui = gui.load_gui("gui_file.json")

gui_create_timer_end = datetime.now()


print(f"It took {(gui_create_timer_end - gui_create_timer_start).total_seconds()} seconds to load the GUI from a file.")

clock = pygame.time.Clock()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_f:
                pygame.display.set_mode(SCREENSIZE, pygame.FULLSCREEN | pygame.SCALED)
            if event.key == pygame.K_g:
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
    # pygame.display.update()
    screen.fill((80, 80, 80))
    clock.tick()

    # clock.tick(60)
