from .element_group import ElementGroup


class Menu(ElementGroup): # TODO: this class needs to be fleshed out more, currently it does nothing more than its parent class

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Menu", msg="", color=(255, 255, 255), style=None,
                 is_visible=True, elements=None, font_color=(10, 10, 10), **kwargs):
        super().__init__(width, height, pos_x, pos_y, name, msg, color, style, is_visible, elements, font_color=font_color, **kwargs)
        self.class_name = self.my_name()
