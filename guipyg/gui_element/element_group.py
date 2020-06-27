from .element import Element
import pygame


class ElementGroup(Element):
    # ElementGroup can be a group of any Element(s) or ElementGroup(s)

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element Group", color=(255, 255, 255), style="default",
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

    def blit_elements(self):
        for element in self.elements:
            element.blit(element.content_surface, element.content_rect.topleft)
            self.blit(element, (element.pos_x, element.pos_y))

    def fill_elements(self):
        for index, element in enumerate(self.elements):
            if hasattr(self.elements[index], "elements"):
                element.fill_elements()
            if not element.corner_rounding:
                element.fill(element.color, element.rect)
                element.content_surface.fill(element.color)

            elif element.corner_rounding:
                pygame.draw.rect(element, element.color, element.get_rect(), border_radius=element.corner_rounding)
                pygame.draw.rect(element.content_surface, element.color, element.content_rect, border_radius=element.corner_rounding)

    def draw_element_border(self):
        for index, element in enumerate(self.elements):
            if element.has_border:
                if hasattr(self.elements[index], "elements"):
                    element.draw_element_border()
                pygame.draw.rect(element, (1, 1, 1),
                                 (0, 0, element.width - abs((element.border_thickness % 2) - 1),
                                  element.height - abs((element.border_thickness % 2) - 1)),
                                 element.border_thickness, border_radius=element.corner_rounding)

    def draw_text_to_elements(self):
        for index, element in enumerate(self.elements):
            if hasattr(self.elements[index], "elements"):
                element.draw_text_to_elements(element)
            element.draw_text(element.content_surface)

    def setup(self):
        # run this after initializing the object or anytime a change is made in element positions
        self.blit_elements()

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # adjusts the position of the mouse within the ElementGroup
        adj_mouse_pos_x, adj_mouse_pos_y = mouse_pos
        adj_mouse_pos_x -= self.pos_x
        adj_mouse_pos_y -= self.pos_y

        return adj_mouse_pos_x, adj_mouse_pos_y

    def click(self, mouse_pos=(0, 0), *args, **kwargs):
        for element in self.elements:
            element.click(element.get_mouse_pos((self.get_mouse_pos(mouse_pos))), *args, **kwargs)
