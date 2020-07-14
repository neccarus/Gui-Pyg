from .element_group import ElementGroup


class Popup(ElementGroup):

    def __init__(self, name="Popup", msg="", elements=None, **_):
        super().__init__(name=name, msg=msg, elements=elements)

        self.class_name = self.my_name()
