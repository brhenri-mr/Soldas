import PySimpleGUI as sg

layout = [
    [
        sg.Graph(
            canvas_size=(400, 400),
            graph_bottom_left=(0, 0),
            graph_top_right=(400, 400),
            key="graph"
        )
    ]
]

window = sg.Window("rect on image", layout)
window.Finalize()

graph = window.Element("graph")
graph.draw_line((100,200),(280,200), color='red')
graph.draw_line((190,200),(190,151.5), color='red')
graph.draw_line((190,151.5),(248.5,200), color='red')
graph.draw_circle((275,200), 15 ,line_color='red')
graph.draw_line((280,200),(280,263), color='red')
i = graph.draw_polygon([(280,263),(307,254.93),(280,246.86)],fill_color='red',line_color='red')
graph.draw_line((190,200),(190,248.5), color='red')
graph.draw_line((190,248.5),(248.5,200), color='red')
graph.delete_figure(i)
while True:
    event, values = window.Read()
    if event is None:
        break