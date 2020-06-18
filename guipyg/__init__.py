import pygame
import json
import os
# from pygame.locals import *


def create_gui(surface=pygame.Surface((0, 0)), length=0, height=0, pos_x=0, pos_y=0, elements=[], config=os.path.join(os.getcwd(), "config")):

    from .gui_element.element import Element
    from .gui_element.element import encode_element
    from .gui_element.toggleable_element import ToggleableElement
    from .gui_element.element_group import ElementGroup
    from .gui_element.button import Button
    from .gui_element.popup import Popup
    from .gui_element.menu import Menu
    from .gui import GUI

    # button = Button(10, 10, 20, 20, name="Button 1")
    # button2 = Button(20, 20, 10, 10, name="Button 2")
    # button3 = Button(30, 30, 40, 40, name="Button 3")
    # menu = Menu(elements=[button, button2, button3])
    #button_enc = encode_element(button)
    gui = GUI(surface, length, height, pos_x, pos_y, elements=elements)

    #gui.get_elements(json.loads(os.path.join(config, "buttons.json")))
    #load_elements("buttons", json.loads(config.buttons))
    #load_elements("popups", json.loads(config.popups))
    #load_elements("menus", json.loads(config.menus))

    return gui
