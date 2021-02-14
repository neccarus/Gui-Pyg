import os
import pygame
import sys
import json

from guipyg import gui
from guipyg.gui_element.menu import Menu
from guipyg.gui_element.button import Button

if os.name == 'posix':
    os.environ['SDL_AUDIODRIVER'] = 'dsp'

screensize = (1280, 720)
pygame.init()
screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()

# build the GUI
gpe_window = gui.GUI(*screensize, name="GPEdit", theme="blue_theme")
gpe_menu = Menu(gpe_window.width, 20, 0, 0, "GPEdit_Menu", color=(130, 130, 145), hide_text=True)

# File Menu setup
file_button = Button(100, 20, 0, 0, name="File_Button", msg="File", color=(140, 140, 155))
file_menu = Menu(200, 500, file_button.rect.left, file_button.rect.bottom, name="File_Menu", color=(130, 130, 145), hide_text=True, is_visible=False)
file_button.function = file_menu.toggle_visibility
save_button = Button(file_menu.width, 20, 0, 0, name="Save_Button", msg="Save", color=(140, 140, 155))
save_as_button = Button(file_menu.width, 20, 0, 20, name="Save_As_Button", msg="Save As...", color=(140, 140, 155))
load_button = Button(file_menu.width, 20, 0, 40, name="Load_Button", msg="Load", color=(140, 140, 155))
file_menu.elements = [save_button, save_as_button, load_button]

# Edit Menu setup
edit_button = Button(100, 20, 100, 0, name="Edit_Button", msg="Edit", color=(140, 140, 155))

gpe_menu.elements = [file_button, edit_button]

gpe_window.elements += [gpe_menu, file_menu]
gpe_window.apply_theme()

if __name__ == "__main__":

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                current_mouse_pos = pygame.mouse.get_pos()
                gpe_window.select_element(current_mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                current_mouse_pos = pygame.mouse.get_pos()
                gpe_window.activate_selected(current_mouse_pos, gpe_window)
                gpe_window.let_go()

        gpe_window.update(screen)

        pygame.display.update()

        screen.fill((80, 80, 85))

        clock.tick()
