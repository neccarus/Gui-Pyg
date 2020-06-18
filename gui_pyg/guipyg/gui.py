import pygame
import json
from json import JSONEncoder
from .gui_element.button import Button
from .gui_element.element import Element
from .gui_element.toggleable_element import ToggleableElement
from .gui_element.popup import Popup
from .gui_element.element_group import ElementGroup
from .gui_element.menu import Menu

class_types = {"Element": Element, "Button": Button, "Popup": Popup, "ToggleableElement": ToggleableElement,
               "ElementGroup": ElementGroup, "Menu": Menu}


class GUI(pygame.Surface):

    def __init__(self, surface="default", length=0, height=0, pos_x=0, pos_y=0, elements=[], *_):
        self.length = length
        self.height = height
        super().__init__((length, height))
        self.surface = surface  # passed in as a string as json doesn't want to encode pygame.Surface objects
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.elements = elements


class GUIEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


def encode_gui(gui):
    return json.dumps(gui, cls=GUIEncoder, indent=4)


def decode_element(element, cls=Element, class_types={}):

    if type(element) != dict:
        element_decode = json.loads(element)
        element_obj = cls(**element_decode)
    else:
        element_obj = cls(**element)
        if hasattr(element_obj, "elements"):
            for index, element in enumerate(element_obj.elements):
                element_name = element["class_name"]
                obj = decode_element(element, class_types[element_name])
                element_obj.elements[index] = obj

    return element_obj


def decode_gui(gui):
    gui_decoded = json.loads(gui)
    gui_obj = GUI(**gui_decoded)

    for index, element in enumerate(gui_obj.elements):
        element_name = element["class_name"]
        obj = decode_element(element, class_types[element_name], class_types)
        gui_obj.elements[index] = obj
    #print(gui_obj)
    return gui_obj
