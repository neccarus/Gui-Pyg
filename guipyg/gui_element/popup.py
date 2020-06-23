from .element_group import ElementGroup


class Popup(ElementGroup):

    def __init__(self, elements=None, **_):
        super().__init__(elements)

        self.class_name = self.my_name()
