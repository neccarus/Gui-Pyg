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
functions = {}


class GUI(pygame.Surface):

    def __init__(self, length=0, height=0, pos_x=0, pos_y=0, elements=[], *_):
        self.length = length
        self.height = height
        super().__init__((self.length, self.height))
        #self.surface = surface  # passed in as a string as json doesn't want to encode pygame.Surface objects
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.elements = elements

    #def toggle_element_visibility(self, element_name):

    def blit_elements(self):
        for index, element in enumerate(self.elements):
            if element.is_visible:
                if hasattr(self.elements[index], "elements"):
                    element.blit_elements()
                self.blit(element, (element.pos_x, element.pos_y))

    def fill_elements(self):
        for index, element in enumerate(self.elements):
            if hasattr(self.elements[index], "elements"):
                element.fill_elements()
            element.fill(element.color, element.rect)
            # element.blit(element, (0, 0))

    def draw_text_to_elements(self):
        for index, element in enumerate(self.elements):
            if hasattr(self.elements[index], "elements"):
                element.draw_text_to_elements()
            element.draw_text(element)

    def update(self, screen):
        # screen to blit to
        self.fill((0, 0, 0))
        self.set_colorkey((0, 0, 0))
        self.fill_elements()
        self.draw_text_to_elements()
        self.blit_elements()
        screen.blit(self, (0, 0))


class GUIEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, "function"):
            o.function = o.function.__name__
            print(o.function)
        #self.skipkeys = True
        if hasattr(o, "__dict__"):
            return o.__dict__
        else:
            pass
        # Let the base class default method raise the TypeError
        # return JSONEncoder.default(self, o)


def encode_gui(gui):
    return json.dumps(gui, skipkeys=True, cls=GUIEncoder, indent=4)


def decode_element(element, cls=Element, class_types={}):

    if type(element) != dict:
        element_decode = json.loads(element)
        element_obj = cls(**element_decode)
    else:
        element_obj = cls(**element)
        if hasattr(element_obj, "function"):
            element_obj.function = functions[element_obj.function]
        if hasattr(element_obj, "elements"):
            for index, element in enumerate(element_obj.elements):
                element_name = element["class_name"]
                obj = decode_element(element, class_types[element_name])
                element_obj.elements[index] = obj

    return element_obj


def match_element_name(gui, name):
    if hasattr(gui, "elements"):
        for index, element in enumerate(gui.elements):
            if hasattr(element, "elements"):
                match_element_name(element.elements, name)
            if element.name == name:
                return element


def update_element_functions(gui, functions):
    if hasattr(gui, "elements"):
        for index, element in enumerate(gui.elements):
            if hasattr(element, "elements"):
                update_element_functions(element, functions)
            if hasattr(element, "function"):
                element.function = functions[element.function.__name__]


def decode_gui(gui):
    gui_decoded = json.loads(gui)
    gui_obj = GUI(**gui_decoded)

    for index, element in enumerate(gui_obj.elements):
        element_name = element["class_name"]
        obj = decode_element(element, class_types[element_name], class_types)
        gui_obj.elements[index] = obj
    #print(gui_obj)
    return gui_obj
