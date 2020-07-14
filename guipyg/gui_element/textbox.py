from .element import Element
import pygame


class TextBox(Element):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element", msg="", color=(245, 245, 245),
                 style="default", is_visible=True, font_color=(10, 10, 10), mutable=True, text="",
                 default_text="Please type here...", **_):
        super().__init__(width, height, pos_x, pos_y, name, msg, color, style, is_visible, font_color, **_)
        self.mutable = mutable
        self.default_text = default_text
        # self.text_gap = 2
        if text == "" and self.mutable:
            self.text = self.default_text
        elif text != "":
            self.text = text
        self.text_content = self.font.render(self.text, True, self.font_color)
        self.get_text_box()

    def get_text_box(self):
        self.text_rect = pygame.Rect((self.margin_left + self.border_thickness,
                                      self.margin_top + self.font.get_ascent() + self.border_thickness + 2),
                                     (self.width - (self.margin_right + self.margin_left + self.border_thickness + self.corner_rounding),
                                      self.height - self.margin_bottom - self.border_thickness - self.font.get_height()))
        self.text_surface = pygame.Surface((abs(self.text_rect.width), abs(self.text_rect.height)))

    def fill_elements(self, surface):
        if self.need_update:
            if not self.corner_rounding:
                self.fill(self.color, self.rect)
                self.content_surface.fill(self.color, self.content_rect)
                self.text_surface.fill((245, 245, 245), self.text_surface.get_rect())

            elif self.corner_rounding:
                pygame.draw.rect(self, self.color, self.rect, border_radius=self.corner_rounding)
                pygame.draw.rect(self.content_surface, self.color, self.content_rect,
                                 border_radius=self.corner_rounding)
                pygame.draw.rect(self.text_surface, (245, 245, 245), self.text_surface.get_rect(),
                                 border_radius=self.corner_rounding)

    def blit_elements(self):
        if self.need_update:
            self.content_surface.blit(self.text_surface, self.text_rect.topleft)
            self.blit(self.content_surface, self.content_rect.topleft)
            self.need_update = False

    def draw_text_to_elements(self):
        if self.need_update:
            self.draw_text(self.content_surface, self.text_obj)
            self.draw_text(self.text_surface, self.text_content)

    def draw_text(self, surface, text):
        surface.blit(text, self.rect)
