from .element import Element
import pygame


class ElementGroup(Element):
    # ElementGroup can be a group of any Element(s) or ElementGroup(s)

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element Group", color=(255, 255, 255),
                 style="default",
                 is_visible=True, elements=None, font_color=(10, 10, 10), **_):
        if elements is None:
            elements = []
        self.width = width
        self.height = height
        self.name = name
        self.color = color
        self.style = style
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(width, height, pos_x, pos_y, name, color, style, is_visible, font_color)
        self.elements = elements
        self.class_name = self.my_name()
        self.is_draggable = True

    def fill_elements(self):
        for element in self.elements:
            # if hasattr(element, "elements"):
            element.fill_elements()
        super().fill_elements()

    def draw_element_border(self):
        for element in self.elements:
            if element.has_border:
                element.draw_element_border()
        super().draw_element_border()

    def draw_text_to_elements(self):
        for element in self.elements:
            element.draw_text_to_elements()
        self.draw_text(self)
        # super().draw_text_to_elements()

    def blit_elements(self, surface):
        for element in self.elements:
            element.blit_elements(self)
        surface.blit(self, (self.pos_x, self.pos_y))

    def setup(self):
        # run this after initializing the object or anytime a change is made in element positions
        self.blit_elements(self)

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # adjusts the position of the mouse within the ElementGroup
        adj_mouse_pos_x, adj_mouse_pos_y = mouse_pos
        adj_mouse_pos_x -= self.pos_x
        adj_mouse_pos_y -= self.pos_y

        return adj_mouse_pos_x, adj_mouse_pos_y

    def click(self, mouse_pos=(0, 0), *args, **kwargs):
        for element in self.elements:
            element.click(element.get_mouse_pos((self.get_mouse_pos(mouse_pos))), *args, **kwargs)
