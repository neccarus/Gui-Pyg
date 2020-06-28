from guipyg.gui_style import style

style_dict = {}
theme_dict = {}

default = style.Style()
style_dict[default.style_name] = default

my_first_style = style.Style()
my_first_style.style_name = "my_first_style"
my_first_style.corner_rounding = 4
my_first_style.margin_top = 5
my_first_style.margin_left = 10
my_first_style.border_thickness = 4
my_first_style.background_color = (150, 150, 150)
my_first_style.has_border = True
my_first_style.border_color = (1, 1, 1)
my_first_style.has_drop_shadow = True
my_first_style.drop_shadow_bottom = 4
my_first_style.drop_shadow_color = (1, 1, 1)
my_first_style.drop_shadow_alpha = 125
style_dict[my_first_style.style_name] = my_first_style
# theme_dict["element_group"] = my_first_style

my_button_style = style.Style()
my_button_style.style_name = "my_button_style"
my_button_style.border_color = (1, 1, 1)
my_button_style.border_thickness = 2
my_button_style.corner_rounding = 10
my_button_style.has_border = True
my_button_style.background_color = (100, 100, 100)
style_dict[my_button_style.style_name] = my_button_style
# theme_dict["element"] = my_button_style

my_theme = style.Theme("my_theme", my_first_style, my_button_style)
theme_dict[my_theme.theme_name] = my_theme
