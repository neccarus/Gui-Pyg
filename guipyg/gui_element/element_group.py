from .element import Element
import json
import pygame


class ElementGroup(Element):
    # ElementGroup can be a group of any Element(s) or ElementGroup(s)

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element Group", color=(255, 255, 255), style="default",
                 elements=[], **_):
        self.width = width
        self.height = height
        self.name = name
        self.color = color
        self.style = style
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(width, height, pos_x, pos_y, name, color, style)
        self.elements = elements
        self.class_name = self.my_name()

    def blit_elements(self):
        for element in self.elements:
            self.blit(element, (element.pos_x, element.pos_y))

    def fill_elements(self):
        for index, element in enumerate(self.elements):
            if hasattr(self.elements[index], "elements"):
                element.fill_elements()
            element.fill(element.color, element.rect)

    def setup(self):
        # run this after initializing the object or anytime a change is made in element positions
        self.blit_elements()

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # adjusts the position of the mouse within the ElementGroup
        adj_mouse_pos_x, adj_mouse_pos_y = mouse_pos
        adj_mouse_pos_x -= self.pos_x
        adj_mouse_pos_y -= self.pos_y

        return adj_mouse_pos_x, adj_mouse_pos_y

    def click(self, mouse_pos=(0, 0)):
        for element in self.elements:
            element.click(element.get_mouse_pos((self.get_mouse_pos(mouse_pos))))
