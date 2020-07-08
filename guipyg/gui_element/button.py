from .toggleable_element import ToggleableElement


# A single GUI element with a function attached
class Button(ToggleableElement):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, function=None, name="Button", color=(255, 255, 255),
                 style="default", is_visible=True, **_):
        self.function = function
        super().__init__(width, height, pos_x, pos_y, name=name, color=color, style=style, is_visible=is_visible)
        self.font_pos_x, self.font_pos_y = self.rect.center

    def toggle_click(self):
        self.toggle = not self.toggle

    def get_click(self, mouse_pos=(0, 0)):
        mouse_pos_x, mouse_pos_y = self.get_mouse_pos(mouse_pos)
        if self.pos_x <= mouse_pos_x <= (self.pos_x + self.width) and \
                self.pos_y <= mouse_pos_y <= (self.pos_y + self.height):
            self.toggle_click()

    # def click(self, mouse_pos=(0, 0), *args, **kwargs):
    #     self.get_click(mouse_pos)
    #     if self.toggle:
    #         self.toggle_click()
    #         # return self.function(mouse_pos, *args, **kwargs)
    #         return self.function(*args, **kwargs)

    def click(self, mouse_pos=(0, 0), *args, **kwargs):
        self.get_click(mouse_pos)
        if self.toggle:
            self.toggle_click()
            # return self.function(mouse_pos, *args, **kwargs)
            return self.function(*args, **kwargs)

    def draw_text(self, surface):
        text_obj = self.font.render(self.name, 1, self.font_color)
        text_rect = text_obj.get_rect()
        text_rect.center = (self.font_pos_x, self.font_pos_y)
        surface.blit(text_obj, text_rect)
