from .element_group import ElementGroup
from .element import Element
from .text_elements import Label
from pygame import Vector2
import pygame


class Graph(ElementGroup):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class GraphElement(Element):

    def __init__(self, low_value=0, high_value=0, current_value=0,
                 empty_color=(0, 0, 0), related_object=None,
                 low_position=Vector2(0, 0), high_position=Vector2(0, 0),
                 angle=0, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.low_value = low_value
        self.high_value = high_value
        self.current_value = current_value
        self.empty_color = empty_color
        self.related_object = related_object
        self.low_position = low_position
        self.high_position = high_position
        self.current_high_position = high_position
        self.ratio = self.current_value / self.high_value
        self.angle = angle

    def add_to_graph(self, graph):

        self.parent = graph
        self.parent.elements.append(self)

    def update(self, *args, **kwargs):

        self.ratio = self.current_value / self.high_value

    def update_low(self, new_low):
        self.low_value = new_low

    def update_high(self, new_high):
        self.high_value = new_high


class BarElement(GraphElement):

    def __init__(self, thickness=1,  *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.thickness = thickness
        pygame.draw.rect(self, self.color, (self.low_position, self.current_high_position))
        self.original = self.copy()
        self.width, self.height = self.high_position

    def update(self, *args, **kwargs):

        super().update(*args, **kwargs)
        self.current_high_position = Vector2((self.high_position[0] * self.ratio, self.high_position[1]))

        self.draw()

    def draw(self):
        pygame.draw.rect(self.content_surface, self.color, (self.low_position, self.current_high_position))
        self.content_surface = pygame.transform.rotate(self.original, self.angle)
