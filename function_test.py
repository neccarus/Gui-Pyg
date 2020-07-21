from guipyg.gui_element.element import Element
import pygame
pygame.init()


def test(x, y, z=0):

    return x + y - z


ele = Element()
ele.function = ele.StoredFunction("", "__main__", "test", None, 4, 4, 5)
print(ele.function(2, 2, 3))
print(ele.function())
