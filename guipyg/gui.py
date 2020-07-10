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
                # print(theme)
                if self.theme == theme_dict[theme].theme_name:
                    print(f"found theme {theme}")
                    theme_dict[theme].style_gui(self)
                    self.elements_to_update = self.elements
                    for element in self.elements:
                        element.need_update = True
                        if hasattr(element, "elements"):
                            for inner_element in element.elements:
                                inner_element.need_update = True
                    break

    def bring_element_to_front(self, element):
        for index, elements in enumerate(self.elements):
            if elements == element:
                self.elements += [self.elements.pop(index)]

    def fill_elements(self, surface):
        for element in self.elements_to_update:
            element.fill_elements(surface)

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
        if self.need_update and self.is_active:
            self.fill((0, 0, 0))
            self.set_clip_area()
            # self.draw_drop_shadows()
            self.fill_elements(screen)
            self.draw_text_to_elements()
            self.draw_element_border()
            self.blit_elements()
        screen.blit(self, (0, 0))
        self.need_update = False

    def select_element(self, mouse_pos):
        if not self.selected_element:
            reversed_elements = self.elements[::-1]
            for index, element in enumerate(reversed_elements):
                if element.is_visible and element.is_draggable and \
                        element.rect.collidepoint(element.get_mouse_pos(mouse_pos)):
                    element.drag_toggle = True
                    self.selected_element = element  # .drag_element(mouse_pos, datetime.now())
                    # if element.is_draggable:
                    self.dragging = self.selected_element.drag_element(mouse_pos)
                    self.bring_element_to_front(element)
                    break

    def drag_selected(self):
        if self.selected_element:
            self.selected_element.pos_x, self.selected_element.pos_y = next(self.dragging)
            if self.selected_element.pos_x < 0:
                self.selected_element.pos_x = 0
            elif self.selected_element.pos_x + self.selected_element.width > self.width:
                self.selected_element.pos_x = self.width - self.selected_element.width
            if self.selected_element.pos_y < 0:
                self.selected_element.pos_y = 0
            elif self.selected_element.pos_y + self.selected_element.height > self.height:
                self.selected_element.pos_y = self.height - self.selected_element.height
            self.need_update = True

    def let_go(self):
        if self.selected_element:
            self.selected_element.drag_toggle = False
            next(self.dragging)
            self.selected_element = None
            self.dragging = None

    def activate_selected(self, mouse_pos, *args, **kwargs):
        if self.selected_element:
            self.selected_element.click(mouse_pos, *args, **kwargs)
            self.need_update = True


class GUIEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, "function"):
            o.function = o.function.__name__
        if hasattr(o, "elements_to_update"):
            # o.elements_to_update = None
            del o.elements_to_update
        if hasattr(o, "__dict__"):
            return o.__dict__
        else:
            pass


def encode_gui(gui):
    return json.dumps(gui, skipkeys=True, cls=GUIEncoder, indent=4)


def save_gui(gui, file):
    with open(file, 'w') as w:
        json.dump(encode_gui(gui), w)


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


def load_gui(file):
    with open(file, 'r') as r:
        gui_json = json.load(r)
    gui = decode_gui(gui_json)
    gui.apply_theme()
    return gui


def match_element_name(gui, name):
    if hasattr(gui, "elements"):
        for index, element in enumerate(gui.elements):
            if hasattr(element, "elements"):
                match_element_name(element.elements, name)
            if element.name == name:
                return element


def match_gui_name(gui, name):
    if gui.name == name:
        print(f'Found a GUI called {name} here')
        return gui


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
