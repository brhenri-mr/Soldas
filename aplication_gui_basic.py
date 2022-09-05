from optparse import Values
import PySimpleGUI as sg
from Aplication_draw import Draw_Solder, Solder
from Aplication_Att import Visualizar_att
from Aplication_graph import Pre_visualizacao
from pyzwcad import ZwCAD
from win32com.client import Dispatch

def main_test():
    #Criterio para ativação das propriedades
    sg.theme('SystemDefaultForReal')
    graph_elem = sg.Graph(canvas_size=(300, 300),
                                graph_bottom_left=(0, 0),
                                graph_top_right=(400, 400),
                                enable_events=True,
                                key='-GRAPH-',
                                background_color='lightblue')
                                
    filete_propriedades = [ [sg.Text('Orientação')],
                            [sg.Radio('Direita','Ori.', key='-ODIR-', default=True, enable_events=True), sg.Radio('Esquerda','Ori.', key='-OESQ-',enable_events=True)],
                            [sg.Text('Acabamentos')],
                            [sg.Checkbox(text= "Solda em campo", size=(15, 1), default=False, key='-CAMPO1-', enable_events=True),sg.Checkbox(text="Solda Continua", size=(15,1), default=False, key='-CAMPO2-')],
                            [sg.Checkbox(text="Ambos os lados", size=(15, 1), default=False, key='-CAMPO3-', enable_events=True),sg.Checkbox(text="Intercalado", size=(15,1), default=False, key='-CAMPO4-', enable_events=True)],
                            [sg.Checkbox(text="Solda em todo contorno", size=(15,1), default=False, key='-CAMPO5-', enable_events=True),sg.Checkbox(text="Reforço", size=(10,1), default=False, key='-CAMPO6-', enable_events=True)],
                            [sg.Checkbox(text="DEFINIR", size=(15,1), default=False, key='-CAMPO7-', enable_events=True),sg.Text('Ref=',key='-TREF-',visible=False),sg.InputText('',key='-REF-',size=(5), enable_events=True, visible=False)],
                            [sg.Column([[sg.Text(text='Informações adicionais')],
                                        [sg.Radio('Reto','Inf.', key='-IRETO-', enable_events=True),
                                        sg.Radio('Convexo','Inf.',key='-ICONV-', enable_events=True),
                                        sg.Radio('Sem Acabamento', 'Inf.',key='-ISA-', enable_events=True)]])],
                                        
                            [sg.Column([[sg.Text(text='Escala')],
                                        [sg.Radio('Manual', 'ESC',enable_events=True, key='-MANUAL-'),sg.Radio('Automatico','ESC',enable_events=True,key='-AUTO-',default=True)],
                                        [sg.Text(text='x'), sg.InputText('',key='-ESCX-',size=(5), disabled=True)],
                                        [sg.Text(text='y'), sg.InputText('',key='-ESCY-',size=(5), disabled=True)]
                                        ])]
                            ]


    layout = [  [sg.Text('Tipo de solda', justification='center')],
            [sg.Column([[
                sg.Radio('Filete','Prop.',enable_events=True, key='-FILETE-'),
                sg.Radio('Topo','Prop.',enable_events=True, key='-TOPO-'), 
                sg.Radio('V','Prop.' ,enable_events=True, key='-V-'),
                sg.Radio('V Curvo','Prop.' ,enable_events=True, key='-V_CURVO-'),
                sg.Radio('Bisel','Prop.' ,enable_events=True, key='-BISEL-'),
                sg.Radio('Bisel Curvo','Prop.' ,enable_events=True, key='-BISEL_CURVO-'),
                sg.Radio('J','Prop.' ,enable_events=True, key='-J-')]])],
            [
                sg.Column([
                        [sg.Text('Espessura(mm)')],
                        [sg.Text('a='),sg.InputText('',key='-ESP_A-',size=(20), enable_events=True)],
                        [sg.Text('b='),sg.InputText('', key='-ESP_B-',size=(20), enable_events=True)]
                        ], 
                        element_justification='l'),
                sg.Column([
                        [sg.Image(r'C:\\Users\\breno\\Desktop\\Projetos\\Soldas\\Imagem1.png', size=(200,102))]
                         ],expand_x=True, element_justification='r') #para o element justificante funcionar precisa do expand element true
                                                    ],
            [sg.Column(layout =filete_propriedades,key="Propriedades"),graph_elem],
            [sg.Button('Ok'), sg.Button('Reset'), sg.Button('Cancel')]]
    return sg.Window('Soldas',layout, finalize=True, icon=r'C:\Users\breno\Desktop\Projetos\Soldas\soldering_iron-48_46707.ico', titlebar_icon='soldering_iron-48_46707.ico')


#dados
id = {'Base':'','solda_em_campo':'','ambos_os_lados':'','contorno':'','acabamento':'','intercalado':'', 'expA':'','expB':'','Reforco':''}


#Tipo estaticos
base = 'FILETE' #variavel para auxiliar no desenho
janela_um = main_test()
zw = ZwCAD()
acad = Dispatch("ZwCAD.Application")
arquivo_nome = Solder()
grafico = Pre_visualizacao(janela_um['-GRAPH-'])

while True:

    window,event, values = sg.read_all_windows()
    print(arquivo_nome.tipo(values))
    
    '''
    toda a vez que um evento é disparado o while roda
    '''
    #-------------------Tipo dinamicos-----------------------------
    try:
        bloco_cad = Draw_Solder(zw,acad)

    except:
        sg.Popup('Erro ao tentar encontrar um ZwCAD')
        break
    
    window['-ESCX-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
    window['-ESCY-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
    #--------------------------------------------------------------

    if event == sg.WIN_CLOSED:
        break
    #----------------------RESET-----------------------------------

    elif event == 'Reset':
        [window[i].Update(value=False) for i in [f'-CAMPO{j}-' for j in range(1,8,1)]]

        for key,item in id.items():
            if key not in ['Base','expA','expB']:
                grafico.apagar(item)


    #----------------------evento ok-------------------------------
    elif event == "Ok":
        bloco_arquivo = arquivo_nome.tipo(values)
        #---------------------------ATT----------------------------
        att = Visualizar_att()
        if att.verificar():
            handle, ponto, escala, name = att.bloco_selecionado()
            att.deletar(handle)
        else:
            handle, ponto,escala = 'N_att', 'N_att', values['-ESCX-']

        #---------------------------ESCALA-----------------------------

        if values['-AUTO-']:
            bloco_cad.escala_atual = escala
        else:
            bloco_cad.escala_atual = values['-ESCX-']

        #---------------------------INSERIR---------------------------
        if att.verificar_arquivo(bloco_arquivo):
            bloco_cad.inserir_bloco(bloco_arquivo, ponto)
            bloco_cad.espessura([values['-REF-'],values['-ESP_B-'],values['-ESP_A-']])
        else:
            sg.popup('Bloco Não Disponível')
        
    #-------------------------EScala---------------------------
    
        #deixou o programa lento essa historia de pegar o valor da escala atual
    
    elif event =='-MANUAL-':
        window['-ESCX-'].Update(disabled=False, value='')
        window['-ESCY-'].Update(disabled=False, value='')
    elif event == '-AUTO-':
        window['-ESCX-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
        window['-ESCY-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))

    #--------------------------Orientação----------------------

    elif event == '-ODIR-':
        [window[campos].Update(value=False) for campos in ['-CAMPO1-', '-CAMPO2-', '-CAMPO3-', '-CAMPO4-', '-CAMPO5-']]
        grafico.deletar()
        if values['-FILETE-']:
            id['Base'] = grafico.filete()

    elif event == '-OESQ-':
        [window[campos].Update(value=False) for campos in ['-CAMPO1-', '-CAMPO2-', '-CAMPO3-', '-CAMPO4-', '-CAMPO5-']]
        grafico.deletar()
        if values['-FILETE-']:
            id['Base'] = grafico.filete()
 
    #-------------------------Reforço---------------------------

    elif event == '-CAMPO6-':
        if values['-CAMPO6-']:
            ref = True
            id['Reforco'] = grafico.reforco()
        else:
            ref = False
            grafico.apagar(id['Reforco'])
            pass
        window['-TREF-'].Update(visible=ref)
        window['-REF-'].Update(visible=ref)

    #-------------------------Desenho---------------------------


    elif event == '-FILETE-':
        if id['Base'] != '':
            grafico.apagar(id['Base'])
        else:
            grafico.deletar()
        id['Base'] = grafico.filete()
        base = 'FILETE'
  
    elif event == '-BISEL-':

        if id['Base'] != '':
            grafico.apagar(id['Base'])
        else:
            grafico.deletar()
        grafico.bisel()
        base = 'BISEL'

    elif event == '-BISEL_CURVO-':
        if id['Base'] != '':
            grafico.apagar(id['Base'])
        else:
            grafico.deletar()
        grafico.bisel_curvo()
        base = 'BISEL_CURVO'
    
    elif event == '-V-':
        if id['Base'] != '':
            grafico.apagar(id['Base'])
        else:
            grafico.deletar()
        id['Base'] = grafico.v()
        base = 'V'

    elif event == '-V_CURVO-':
        if id['Base'] != '':
            grafico.apagar(id['Base'])
        else:
            grafico.deletar()
        id['Base'] = grafico.v_curvo()
        base = 'V_CURVO'

    elif event == '-TOPO-':
        if id['Base'] != '':
            grafico.apagar(id['Base'])
        else:
            grafico.deletar()
        id['Base'] = grafico.topo()
        base = 'TOPO'

    elif event == '-ESP_B-' or event=='-ESP_A-':
        grafico.apagar(id['expB'])
        if values['-CAMPO4-']: #intercalador
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Intercalado')
        elif values['-CAMPO3-']: #anbos os lados
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Amboslados')
        else:
            id['expB'] = grafico.espessura([values['-ESP_B-']],'Filete')

    elif event == '-CAMPO1-':
        if values['-CAMPO1-']:
            id['solda_em_campo'] = grafico.solda_em_campo(values['-ODIR-'])
        else:
            grafico.apagar(id['solda_em_campo'])
            pass
    elif event == '-CAMPO2-':
        pass
    elif event == '-CAMPO3-':
        if values['-CAMPO3-']:
            id['ambos_os_lados'] = grafico.solda_ambos_os_lados(base)
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Amboslados')
        else:
            grafico.apagar(id['ambos_os_lados'])
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-']],'Filete')

    elif event == '-CAMPO4-':
        if values['-CAMPO4-']:
            id['intercalado'] = grafico.intercalado(id['Base'])
            #redesenhar as espessuras
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Intercalado')
        else:
            #aparemente não existe bisel intercalado
            grafico.apagar(id['intercalado'])
            id['Base'] = grafico.filete()
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Filete')

    elif event == '-CAMPO5-':
        if values['-CAMPO5-']:
           id['contorno'] = grafico.contorno(values['-ODIR-'])
        else:
            grafico.apagar(id['contorno'])
    elif event == '-CAMPO6-':
        pass
    elif event == '-CAMPO7-':
        pass


    elif event == '-IRETO-' and (base == 'BISEL'or base =='TOPO'):
        grafico.apagar(id['acabamento'])
        id['acabamento'] = grafico.acabamento_reto(values['-CAMPO3-'])

    elif event == '-ICONV-' and (base == 'BISEL'or base =='TOPO'):
        grafico.apagar(id['acabamento'])
        id['acabamento'] = grafico.acabamento_convexo(values['-CAMPO3-'])
   
    elif event == '-ISA-' and (base == 'BISEL'or base =='TOPO'):
        grafico.apagar(id['acabamento'])
    
    #------------------------grafico--------------------------
    elif event == '-GRAPH-':
        pass
    else:

        '''
        Mudanças das propriedades por escolha do tipo de solda
        '''
        ...
    
