import PySimpleGUI as sg
import keyboard
from Aplication_draw import Draw_Solder
from pyzwcad import ZwCAD
from win32com.client import Dispatch
from Aplication_graph import Pre_visualizacao


def main_segundo_plano():
    sg.theme('SystemDefaultForReal')
    graph_elem = sg.Graph(canvas_size=(300, 300),
                                graph_bottom_left=(0, 0),
                                graph_top_right=(400, 400),
                                enable_events=True,
                                key='-GRAPH-',
                                background_color='lightblue')

    layout = [
        [sg.Text('Status:'),sg.Text('OFF', key='-STATUS-', text_color='red', font='bold')],
        [graph_elem]
        ]
    
    return sg.Window('',finalize=True,layout=layout, location=(1919-350,0),keep_on_top=True)

def decodificar(teclas):

    teclas = list(set(teclas))

    teclas_codigo = {
        'f':'Solda_filete_',
        't':'Solda_topo_',
        'b':'Solda_bisel_',
        'd':'direita_',
        'e':'esquerda_',
        'c':'contorno_',
        'o':'campo_',
        'a':'amboslados_',
        'r+f':'Reforc_',
        'r':'reto_',
        'c+v':'convexo_'
        }

    saida = ''

    for t in teclas_codigo.keys():
        if t in teclas:
            saida = saida + teclas_codigo[t]
    
    return saida

teclas_codigo = {
    'F':'Solda_filete_',
    'D':'direita_',
    'E':'esquerda_',
    'T':'Solda_topo_',
    'A':'amboslados_',
    'O':'campo_',
    'C':'contorno_'
    }

teclas_clicadas = []

janela = main_segundo_plano()

while True:
    try:
        zw = ZwCAD()
        acad = Dispatch("ZwCAD.Application")
        break
    except:
        print('erro')

blocos = Draw_Solder(zw,acad)
print('inicializando')

grafico = Pre_visualizacao(janela['-GRAPH-'])


while True:
    event, values = janela.Read(timeout=1)
    if keyboard.is_pressed('shift'):
        print('sucesso')
        if 'shift' in teclas_clicadas:
            teclas_clicadas.clear()
            grafico.deletar()
        else:
            pass
        janela['-STATUS-'].Update(value='ON', text_color='green')
        teclas_clicadas.append('shift')

    elif keyboard.is_pressed('b'):
        print('sucesso')
        if 'b' in teclas_clicadas:
            pass
        else:
            grafico.bisel()
            teclas_clicadas.append('b')

    elif keyboard.is_pressed('t'):
        print('sucesso')
        if 't' in teclas_clicadas:
            pass
        else:
            grafico.topo()
            teclas_clicadas.append('t')

    elif keyboard.is_pressed('v'):
        print('sucesso')
        if 'v' in teclas_clicadas:
            pass
        else:
            grafico.v()
            teclas_clicadas.append('t')

    elif keyboard.is_pressed('f'):
        print('sucesso')
        if 'f' in teclas_clicadas:
            pass
        else:
            grafico.filete()
            teclas_clicadas.append('f')

#------------------ORIENTACAO-----------------
    elif keyboard.is_pressed('d'):
        print('sucesso')
        if 'd' in teclas_clicadas:
            pass
        else:
            teclas_clicadas.append('d')
            ori = True

    elif keyboard.is_pressed('e'):
        print('sucesso')
        if 'e' in teclas_clicadas:
            pass
        else:
            teclas_clicadas.append('e')
            ori = False

#--------------Acabamentos------------------

    elif keyboard.is_pressed('r') and 'b' in teclas_clicadas:
        print('sucesso')
        if 'r' in teclas_clicadas:
            pass
        else:
            grafico.acabamento_reto(False,'BISEL')
            teclas_clicadas.append('r')

    elif keyboard.is_pressed('a'):
        print('sucesso')
        if 'a' in teclas_clicadas:
            pass
        else:
            teclas_clicadas.append('a')
    
    elif keyboard.is_pressed('c'):
        print('sucesso')
        if 'c' in teclas_clicadas:
            pass
        else:
            grafico.contorno(ori)
            teclas_clicadas.append('c')

    elif keyboard.is_pressed('o'):
        print('sucesso')
        if 'o' in teclas_clicadas:
            pass
        else:
            grafico.solda_em_campo(ori)
            teclas_clicadas.append('o')
    
#---------------------ESC----------------
    elif keyboard.is_pressed('esc'):
        print('limpar')
        janela['-STATUS-'].Update(value='OFF',text_color='red')
        teclas_clicadas.clear()
        grafico.deletar()
#--------------------OK-------------------

    elif keyboard.is_pressed('tab'):
        if 'shift' in teclas_clicadas:
            nome = decodificar(teclas_clicadas)
            print(nome)
            try:
                blocos.inserir_bloco(nome,'N_att')
            except:
                sg.popup('Solda não disponível')

    if event == sg.WIN_CLOSED:
        break
