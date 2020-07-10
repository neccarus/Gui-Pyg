import pygame
import json
from json import JSONEncoder
from guipyg.gui_style.style_item import style_dict
from functools import wraps


class Element(pygame.Surface):
    id_ = 0
    element_dict = {}  # dict structure {id: element}
    active_elements = []  # list all active elements

    # functions is a list of dictionaries meant to store all functions belonging to each Element
    # function: stores the function,
    # arguments: stores any static arguments if the Element has one purpose,
    # origin: the Element this function belongs to specified by the Element's name attribute,
    # target: if the function is affecting another Element that is stored here, specified by name.
    # functions = [
    #     {
    #         'function': None,
    #         'arguments': None,
    #         'origin': None,
    #         'target': None
    #     }
    # ]
    #
    # @classmethod
    # def add_function(cls, function, arguments=None, origin=None, target=None):
    #     cls.functions.append(
    #         {'function': function,
    #          'arguments': arguments,
    #          'origin': origin,
    #          'target': target}
    #     )

    @classmethod
    def my_name(cls):
        return cls.__name__

    @classmethod
    def new_id(cls, element):
        element.id_ = cls.id_
        cls.id_ += 1

    @classmethod
    def new_element(cls, element):
        cls.element_dict[element.id_] = element

    @classmethod
    def activate_element(cls, element):
        cls.active_elements.append(element)

    @classmethod
    def deactivate_element(cls, element):
        cls.active_elements.remove(element)

    def class_name(self):
        return self.__class__.__name__

    def set_style(self):
        for style in style_dict:
            if self.style == style_dict[style].style_name:
                style_dict[style].style_element(self)

    def set_drop_shadow(self):
        self.drop_shadow_thickness = (max(self.drop_shadow_left, self.drop_shadow_right,
                                          self.drop_shadow_top, self.drop_shadow_bottom)
                                      + self.corner_rounding)
        self.drop_shadow_rect = pygame.Rect(0,
                                            0,
                                            self.width + self.drop_shadow_right + self.drop_shadow_left,
                                            self.height + self.drop_shadow_bottom + self.drop_shadow_top)
        # self.drop_shadow_rect.center = self.pos_x + (self.width // 2), self.pos_y + (self.height // 2)
        self.drop_shadow_rect.center = self.rect.center

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element", color=(255, 255, 255), style="default",
                 is_visible=True, font_color=(10, 10, 10), **_):
        super().__init__((width, height), pygame.HWSURFACE)
        Element.new_id(self)
        Element.new_element(self)
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name
        self.color = color
        self.style = style
        self.is_visible = is_visible
        self.border_thickness = 1
        self.border_color = (1, 1, 1)
        self.corner_rounding = None
        self.margin_top = 0
        self.margin_bottom = 0
        self.margin_left = 0
        self.margin_right = 0
        self.rect = self.get_rect()
        self.rect.width -= abs((self.border_thickness % 2) - 1)
        self.rect.height -= abs((self.border_thickness % 2) - 1)
        self.content_rect = pygame.Rect((self.margin_left,
                                         self.margin_top),
                                        (self.width - self.margin_right - self.border_thickness,
                                         self.height - self.margin_bottom - self.border_thickness))
        self.content_surface = pygame.Surface((abs(self.content_rect.width), abs(self.content_rect.height)))
        self.content_surface.set_colorkey(self.color)  # elements exhibit a weird behaviour without this
        self.class_name = self.my_name()
        self.font = pygame.font.SysFont("times new roman", 22)
        self.font_pos_x = 10
        self.font_pos_y = 0
        self.font_color = font_color
        self.text_obj = self.font.render(self.name, True, self.font_color)
        self.text_rect = self.text_obj.get_rect()
        self.text_rect.topleft = (self.font_pos_x, self.font_pos_y)
        self.set_colorkey((0, 0, 0))
        self.fill((0, 0, 0),
                  self.rect)  # colorkey and fill to prevent weird behaviour on corners when there is corner rounding
        self.has_border = True
        self.is_draggable = False
        self.drag_toggle = False
        self.set_style()
        self.need_update = True  # hopefully will reduce calls to blit and fill
        self.has_drop_shadow = False
        self.drop_shadow_right = 0
        self.drop_shadow_left = 0
        self.drop_shadow_top = 0
        self.drop_shadow_bottom = 0
        self.drop_shadow_thickness = 0
        self.drop_shadow_alpha = 255
        self.drop_shadow_color = (0, 0, 0, self.drop_shadow_alpha)
        self.drop_shadow_rect = pygame.Rect(self.pos_x - self.drop_shadow_left,
                                            self.pos_y - self.drop_shadow_top,
                                            self.width + self.drop_shadow_right,
                                            self.height + self.drop_shadow_bottom)
        self.drop_shadow_position = self.rect.center
        self.set_drop_shadow()
        self.is_active = True
        Element.activate_element(self)
        # print(f"{self.my_name()}: {self.id_}")

    def __str__(self):
        return f"{self.my_name()}, {self.id_}"

    # @property
    # def arguments(self):
    #     return self.arguments
    #
    # @arguments.setter
    # def arguments(self, *args, **kwargs):
    #     self.arguments = {'args': args,
    #                       'kwargs': kwargs
    #                       }
    #
    # @property
    # def function(self):
    #     return self.function
    #
    # @function.setter
    # def function(self, function, arguments=None, target=None):
    #     self.function = function
    #     self.arguments = arguments
    #     if issubclass(target, Element):
    #         Element.add_function(function, arguments, self.name, target)
    #     else:
    #         Element.add_function(function, arguments, self.name)

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # for compatibility with ElementGroup
        return mouse_pos

    def toggle_visibility(self, *_, **__):
        self.is_visible = not self.is_visible

    def fill_elements(self, surface):
        if self.need_update:
            if not self.corner_rounding:
                self.fill(self.color, self.rect)
                self.content_surface.fill(self.color, self.content_rect)

            elif self.corner_rounding:
                pygame.draw.rect(self, self.color, self.rect, border_radius=self.corner_rounding)
                pygame.draw.rect(self.content_surface, self.color, self.content_rect,
                                 border_radius=self.corner_rounding)

    def blit_elements(self):
        if self.need_update:
            self.blit(self.content_surface, self.content_rect.topleft)
            self.need_update = False

    def draw_element_border(self):
        if self.need_update:
            pygame.draw.rect(self, self.border_color,
                             (0, 0, self.width - abs((self.border_thickness % 2) - 1),
                              self.height - abs((self.border_thickness % 2) - 1)),
                             self.border_thickness, border_radius=self.corner_rounding)

    def draw_text_to_elements(self):
        if self.need_update:
            self.draw_text(self.content_surface)

    def draw_text(self, surface):
        surface.blit(self.text_obj, self.text_rect)

    def drag_element(self, mouse_pos=(0, 0)):
        mouse_pos_start = mouse_pos
        element_pos_x = self.pos_x
        element_pos_y = self.pos_y

        while self.drag_toggle:
            current_mouse_pos = pygame.mouse.get_pos()
            mouse_pos_delta = (current_mouse_pos[0] - mouse_pos_start[0], current_mouse_pos[1] - mouse_pos_start[1])
            element_pos_delta_x, element_pos_delta_y = (element_pos_x + mouse_pos_delta[0],
                                                        element_pos_y + mouse_pos_delta[1])
            yield element_pos_delta_x, element_pos_delta_y
        yield None


# class ElementFunction(object):

# def __init__(self, function=None, target=None):
#     self.function = function
#     self.target = target
#
# def __call__(self, *args, **kwargs):
#     return self.function(*args, **kwargs)

# decorator probably won't work as I need to be able to make several instances of a button
# def element_function(function):
#     @wraps(function)
#     def wrapper(*args, **kwargs):
#         result = function(*args, **kwargs)
#
#         return result()
#
#     return wrapper


class ElementEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, "_id"):
            del o._id
        return o.__dict__


def encode_element(element):
    return json.dumps(element, cls=ElementEncoder, indent=1)
