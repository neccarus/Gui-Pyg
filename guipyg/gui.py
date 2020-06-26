import pygame
import json
from json import JSONEncoder
from .gui_element.button import Button
from .gui_element.element import Element
from .gui_element.toggleable_element import ToggleableElement
from .gui_element.popup import Popup
from .gui_element.element_group import ElementGroup
from .gui_element.menu import Menu
from .gui_style.style_item import theme_dict

class_types = {"Element": Element, "Button": Button, "Popup": Popup, "ToggleableElement": ToggleableElement,
               "ElementGroup": ElementGroup, "Menu": Menu}
functions = {}


class GUI(pygame.Surface):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, elements=None, theme="default", *_, **__):
        if elements is None:
            elements = []
        self.width = width
        self.height = height
        super().__init__((self.width, self.height))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.set_colorkey((0, 0, 0))
        self.elements = elements
        self.elements_to_update = self.elements
        self.theme = theme  # receives a Theme object from style module, used to stylize all elements
        self.need_update = True
        # self.set_clip_area()

    def apply_theme(self):
        for theme in theme_dict:
            print(theme)
            if self.theme == theme_dict[theme].theme_name:
                print("found theme")
                theme_dict[theme].style_gui(self)

    def blit_elements(self, element, index):
        if element.is_visible:
            element.blit(element.content_surface, element.content_rect.topleft)
            if hasattr(self.elements[index], "elements"):
                element.blit_elements()
            self.blit(element, (element.pos_x, element.pos_y))

    def fill_elements(self):
        for index, element in enumerate(self.elements_to_update):
            if hasattr(self.elements_to_update[index], "elements"):
                element.fill_elements()
            element.fill(element.color, element.rect)
            element.content_surface.fill(element.color)
        self.elements_to_update = []

    def draw_element_border(self, element, index):
        if element.has_border:
            if hasattr(self.elements[index], "elements"):
                element.draw_element_border()
            pygame.draw.rect(element, (1, 1, 1), (0, 0, element.width - abs((element.border_thickness % 2) - 1),
                                                  element.height - abs((element.border_thickness % 2) - 1)),
                             element.border_thickness)

    def draw_text_to_elements(self, element, index):
        if hasattr(self.elements[index], "elements"):
            element.draw_text_to_elements()

        element.draw_text(element.content_surface)

    def set_clip_area(self):
        left, top, right, bottom = self.width, self.height, 0, 0
        for element in self.elements:
            if element.rect.left < left:
                left = element.rect.left
            if element.rect.top < top:
                top = element.rect.top
            if element.rect.right > right:
                right = element.rect.right
            if element.rect.bottom > bottom:
                bottom = element.rect.bottom

    def update(self, screen):
        # screen to blit to
        if self.need_update:
            self.fill((0, 0, 0))
            self.set_clip_area()
        self.set_colorkey((0, 0, 0))
        self.fill_elements()
        for index, element in enumerate(self.elements):
            self.draw_text_to_elements(element, index)
            self.draw_element_border(element, index)
            self.blit_elements(element, index)
        screen.blit(self, (0, 0))
        self.need_update = False


class GUIEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, "function"):
            o.function = o.function.__name__
        if hasattr(o, "elements_to_update"):
            o.elements_to_update = None
        if hasattr(o, "__dict__"):
            return o.__dict__
        else:
            pass


def encode_gui(gui):
    return json.dumps(gui, skipkeys=True, cls=GUIEncoder, indent=1)


def decode_element(element, cls=Element, class_types=None):
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


def update_element_functions(gui):
    if hasattr(gui, "elements"):
        for index, element in enumerate(gui.elements):
            if hasattr(element, "elements"):
                update_element_functions(element)
            if hasattr(element, "function"):
                element.function = functions[element.function.__name__]


def decode_gui(gui):
    gui_decoded = json.loads(gui)
    gui_obj = GUI(**gui_decoded)

    for index, element in enumerate(gui_obj.elements):
        element_name = element["class_name"]
        obj = decode_element(element, class_types[element_name], class_types)
        gui_obj.elements[index] = obj

    return gui_obj
