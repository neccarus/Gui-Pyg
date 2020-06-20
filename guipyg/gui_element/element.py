import pygame
import json
from json import JSONEncoder
from guipyg import gui


class Element(pygame.Surface):

    @classmethod
    def my_name(cls_):
        return cls_.__name__

    def class_name(self):
        return self.__class__.__name__

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element", color=(255, 255, 255), style="default",
                 is_visible=True, font_color=(10, 10, 10), **_):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name
        self.color = color
        self.style = style
        self.is_visible = is_visible
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.class_name = self.my_name()
        self.font = pygame.font.SysFont("arial black", 18)
        self.font_color = font_color
        self.font_pos_x = 10
        self.font_pos_y = 0
        self.has_border = True
        self.border_thickness = 3

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # for compatibility with ElementGroup
        return mouse_pos

    def toggle_visibility(self, *_, **__):
        self.is_visible = not self.is_visible
        print(self.name)
        print("Toggle visibility: " + str(self.is_visible))

    def draw_text(self, surface):
        text_obj = self.font.render(self.name, 1, self.font_color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (self.font_pos_x, self.font_pos_y)
        surface.blit(text_obj, text_rect)


class ElementEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


def encode_element(element):
    return json.dumps(element, cls=ElementEncoder, indent=4)

