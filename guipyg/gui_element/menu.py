import json

from .element_group import ElementGroup


class Menu(ElementGroup):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Menu", color=(255, 255, 255), style="default",
                 elements=[], **_):
        super().__init__(width, height, pos_x, pos_y, name, color, style, elements)
        self.class_name = self.my_name()
