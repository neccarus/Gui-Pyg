# this module contains classes and functions to help with styling GUI objects


class Style(object):

    def __init__(self):
        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0
        self.has_border = False
        self.background_color = (255, 255, 255)
        self.alpha = 0
        self.border_thickness = 0
        self.border_color = (0, 0, 0)
        self.corner_rounding = 0
        self.has_drop_shadow = False
        self.drop_shadow_top = 0
        self.drop_shadow_bottom = 0
        self.drop_shadow_left = 0
        self.drop_shadow_right = 0
        self.drop_shadow_color = (0, 0, 0)
        self.drop_shadow_alpha = 0


class FontStyle(Style):

    def __init__(self):
        super().__init__()
        self.font = "arial black"
        self.font_size = 14
        self.font_italic = False
        self.font_bold = False
        self.font_underline = False
        self.text_wrapping = True


def style_element(element, style):
    element.margin_left, element.margin_right = style.margin_left, style.margin_right
    element.margin_top, element.margin_bottom = style.margin_top, style.margin_bottom
    element.has_border = style.has_border
    element.color = style.background_color
    element.set_alpha(style.alpha)  # pygame.Surface method set_alpha()
    element.border_thickness = style.border_thickness
    element.border_color = style.border_color
    element.corner_rounding = style.corner_rounding
    element.has_drop_shadow = style.has_drop_shadow
    element.drop_shadow_top = style.drop_shadow_top
    element.drop_shadow_bottom = style.drop_shadow_bottom
    element.drop_shadow_left = style.drop_shadow_left
    element.drop_shadow_right = style.drop_shadow_right
    element.drop_shadow_color = style.drop_shadow_color
    element.drop_shadow_alpha = style.drop_shadow_alpha


def style_text(element, style):
    # style_element(element, style)
    element.font = style.font
    element.font_size = style.font_size
    element.font_italic = style.font_italic
    element.font_bold = style.font_bold
    element.font_underline = style.font_underline
    element.text_wrapping = style.text_wrapping
