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
from datetime import datetime

class_types = {"Element": Element, "Button": Button, "Popup": Popup, "ToggleableElement": ToggleableElement,
               "ElementGroup": ElementGroup, "Menu": Menu}
functions = {}


class GUI(ElementGroup):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="GUI", elements=None, theme=None, *_, **__):
        if elements is None:
            elements = []
        self.width = width
        self.height = height
        super().__init__(width, height, pos_x, pos_y, name, elements=elements)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.set_colorkey((0, 0, 0))
        self.elements = elements
        self.elements_to_update = self.elements
        self.theme = theme  # receives a Theme object from style module, used to stylize all elements
        self.need_update = True
        self.selected_element = None
        self.dragging = None
        self.is_draggable = False
        self.clip_rect = None
        # self.set_clip_area()

    def apply_theme(self):
        if self.theme:
            for theme in theme_dict:
                print(theme)
                if self.theme == theme_dict[theme].theme_name:
                    print("found theme")
                    theme_dict[theme].style_gui(self)

    def fill_elements(self):
        for element in self.elements_to_update:
            element.fill_elements()

        self.elements_to_update = []

    def set_clip_area(self):
        left, top, right, bottom = 0, 0, self.width, self.height
        for element in self.elements:
            if element.rect.left < left:
                left = element.rect.left + element.pos_x
            if element.rect.top < top:
                top = element.rect.top + element.pos_y
            if element.rect.right > right:
                right = element.rect.right + element.pos_x
            if element.rect.bottom > bottom:
                bottom = element.rect.bottom + element.pos_y
        self.clip_rect = pygame.Rect(left, top, right - left, bottom - top)
        self.set_clip(self.clip_rect)

    def update(self, screen):
        # screen to blit to
        if self.need_update:
            self.fill((0, 0, 0))
            self.set_clip_area()
            self.fill_elements()
            self.draw_text_to_elements()
            self.draw_element_border()
            self.blit_elements()
        screen.blit(self, (0, 0))
        self.need_update = False

    def select_element(self, mouse_pos):
        if not self.selected_element:
            reversed_elements = self.elements[::-1]
            for element in reversed_elements:
                if element.is_visible and element.is_draggable and \
                        element.rect.collidepoint(element.get_mouse_pos(mouse_pos)):
                    element.drag_toggle = True
                    self.selected_element = element  # .drag_element(mouse_pos, datetime.now())
                    # if element.is_draggable:
                    self.dragging = self.selected_element.drag_element(mouse_pos)
                    break

    def drag_selected(self):
        if self.selected_element:
            self.selected_element.pos_x, self.selected_element.pos_y = next(self.dragging)
            self.need_update = True

    def let_go(self):
        if self.selected_element:
            self.selected_element.drag_toggle = False
            next(self.dragging)
            self.selected_element = None
            self.dragging = None


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
