import pygame
import json
from json import JSONEncoder
#from pygame.locals import *


class Element(pygame.Surface):

    @classmethod
    def my_name(cls_):
        return cls_.__name__

    def class_name(self):
        return self.__class__.__name__

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element", color=(255, 255, 255), style="default", **_):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name
        self.color = color
        self.style = style
        self.rect = pygame.Rect((self.pos_x, self.pos_y), (self.height, self.width))
        self.class_name = self.my_name()

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # for compatibility with ElementGroup
        return mouse_pos



class ElementEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


def encode_element(element):
    return json.dumps(element, cls=ElementEncoder, indent=4)


# def decode_element(element, cls=Element, class_types={}):
#     # need decode_element function for each type of element
#     # how can I make these work across different types without copypasta?
#     print(cls)
#     if type(element) != dict:
#         element_decode = json.loads(element)
#         element_obj = cls(**element_decode)
#     else:
#         element_obj = cls(**element)
#         if hasattr(element_obj, "elements"):
#             for index, element in enumerate(element_obj.elements):
#                 element_name = element["class_name"]
#                 obj = decode_element(element, class_types[element_name])
#                 element_obj.elements[index] = obj
#
#     return element_obj
