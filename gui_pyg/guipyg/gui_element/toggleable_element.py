from .element import Element


class ToggleableElement(Element):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element", color=(255, 255, 255), style="default", **_):
        self.toggle = False
        super().__init__(width, height, pos_x, pos_y, name, color=color, style=style)

        self.class_name = self.my_name()
