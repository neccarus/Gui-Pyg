from guipyg import create_gui
from guipyg import gui as gu
import json


gui = create_gui()
gui_json = gu.encode_gui(gui)
with open('gui_file.json', 'w') as w:
    json.dump(gui_json, w)
print(gui_json)
with open('gui_file.json', 'r') as r:
    gui_json = json.load(r)
gui_obj = gu.decode_gui(gui_json)
#print(gui_obj.elements.__dict__)
del gui_json
gui_json = gu.encode_gui(gui_obj)
with open('gui_file2.json', 'w') as w:
    json.dump(gui_json, w)
with open('gui_file2.json', 'r') as r:
    gui_json = json.load(r)
gui_obj = gu.decode_gui(gui_json)
#print(dir(gui_obj))
#gui_json_2 = gu.encode_gui(gui_obj)
#print(gui_json_2)
print(gui_obj.pos_x, gui_obj.pos_y, gui_obj.elements[0].elements[0].pos_x)

if __name__ == '__main__':
    print('end')
