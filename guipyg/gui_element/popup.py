from .element_group import ElementGroup


class Popup(ElementGroup): # TODO: this class needs to be fleshed out

    def __init__(self, name="Popup", msg="", elements=None, **kwargs):
        super().__init__(name=name, msg=msg, elements=elements, **kwargs)

        self.class_name = self.my_name()
