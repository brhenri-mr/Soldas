
'''
import PySimpleGUI as sg
sg.theme('SystemDefaultForReal')
layout = [
    [sg.Menu([['File',['Open','Save']]]),
    [sg.Column([[sg.Button('',key='butao',image_filename='star_off.png')]],justification='r',element_justification = 'r')],
    [sg.Image('star_off.png',key='estrela',enable_events = True)],
        sg.Graph(
            canvas_size=(400, 400),
            graph_bottom_left=(0, 0),
            graph_top_right=(400, 400),
            key="graph"
        )
    ]
]


sg.Image()

sg.pin

window = sg.Window("rect on image", layout, icon="soldering_iron-48_46707.ico")
window.Finalize()

graph = window.Element("graph")
graph.draw_image(filename=b'background2.png', location=(0,400))
graph.draw_lines([(100,200),(280,200),(190,200),(190,151.5),(190,200),(190+48.5,151.5)], color='red')
graph.draw_lines([(190,200),(190,74),(190+48.5,74+48.5),(190,74+48.5)], color='red')

j = 0

while True:
    event, values = window.Read()
    if event is None:
        break
    elif event == 'butao':
        if j == 0:
            window['butao'].update(image_filename='star_on.png')
            j = 1
        else:
            window['butao'].update(image_filename='star_off.png')
            j =0
    elif event == 'estrela':
        if j == 0:
            window['estrela'].update(source='star_on.png')
            j = 1
        else:
            window['estrela'].update(source='star_off.png')
            j =0
'''


from pyzwcad import ZwCAD, APoint
from win32com.client import Dispatch
from os.path import join

zw = ZwCAD()
acad = Dispatch("ZwCAD.Application")

txt_base_handle_esquerda = '1B8'
text_base_posi_esquerda = APoint(-16.4891,-2.6215)

txt_base_handle_centro = '370'
text_base_posi_centro = APoint(-10.2714,-6.1968)

classname = 'Attribute Definition'


#Entity  = acad.ActiveDocument.HandleToObject('1B8')
Entity  = acad.ActiveDocument.HandleToObject('26E')


print(Entity.Radius)

c = (-1.7500000000000036, -1.7694179454963432e-16, 0.0)
r = 3.0
end = 4.71238898038469
start = 3.141592653589793

'''
for obj in zw.iter_objects(['Arc']):
    obj.EndPoint = APoint(-5,0,0)
    obj.StartPoint = APoint(-7.6539,-3.0359,0)


for obj in zw.iter_objects(['AcDbAttributeDefinition']):
    if obj.handle == txt_base_handle_centro:
        antigo = obj.InsertionPoint
        while True:
            obj.Move(APoint(obj.InsertionPoint),text_base_posi_centro)
            print(type(antigo))
            print(obj.InsertionPoint)
            if antigo[0] == obj.InsertionPoint[0]:
                pass
            else:
                break
    else:
        obj.Erase
'''