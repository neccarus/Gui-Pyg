from .element import Element


class ToggleableElement(Element):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element", msg="", color=(255, 255, 255), style="default",
                 is_visible=True, **_):
        self.toggle = False
        super().__init__(width, height, pos_x, pos_y, name, msg, color, style, is_visible)

        self.class_name = self.my_name()
