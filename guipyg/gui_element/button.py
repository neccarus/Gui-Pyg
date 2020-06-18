from .toggleable_element import ToggleableElement


# A single GUI element with a function attached
class Button(ToggleableElement):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, function=None, name="Button", color=(255, 255, 255), style="default", **_):
        self.function = function
        super().__init__(width, height, pos_x, pos_y, name=name, color=color, style=style)

    def toggle_click(self):
        self.toggle = not self.toggle

    def get_click(self, mouse_pos=(0, 0)):
        #mouse_pos_x, mouse_pos_y = mouse_pos[0], mouse_pos[1]
        mouse_pos_x, mouse_pos_y = self.get_mouse_pos(mouse_pos)
        if self.pos_x <= mouse_pos_x <= (self.pos_x + self.width) and \
                self.pos_y <= mouse_pos_y <= (self.pos_y + self.height):
            self.toggle_click()

    def click(self, mouse_pos=(0, 0)):
        self.get_click(mouse_pos)
        if self.toggle:
            self.toggle_click()
            return self.function()
