import PySimpleGUI as sg
from Aplication_draw import Draw_Solder
from Aplication_Att import Visualizar_att
from Aplication_graph import Pre_visualizacao

def main_test():
    #Criterio para ativação das propriedades
    graph_elem = sg.Graph(canvas_size=(400, 400),
                                graph_bottom_left=(0, 0),
                                graph_top_right=(400, 400),
                                enable_events=True,
                                key='-GRAPH-',
                                background_color='lightblue')
                                
    filete_propriedades = [ [sg.Text('Orientação')],
                            [sg.Radio('Direita','Ori.', key='-ODIR-', default=True, enable_events=True), sg.Radio('Esquerda','Ori.', key='-OESQ-',enable_events=True)],
                            [sg.Text('Acabamentos')],
                            [sg.Checkbox(text= "Solda em campo", size=(10, 1), default=False, key='-CAMPO1-', enable_events=True),sg.Checkbox(text="Solda Continua", size=(10,1), default=False, key='-CAMPO2-')],
                            [sg.Checkbox(text="Ambos os lados", size=(10, 1), default=False, key='-CAMPO3-', enable_events=True),sg.Checkbox(text="Intercalado", size=(10,1), default=False, key='-CAMPO4-')],
                            [sg.Checkbox(text="Solda em todo contorno", size=(10,1), default=False, key='-CAMPO5-', enable_events=True), sg.Checkbox(text="Solda em todo contorno", size=(10,1), default=False, key='-CAMPO6-', enable_events=True)],
                            [sg.Checkbox(text="Filete", size=(10, 1), default=False, key='-CAMPO7-'),sg.Checkbox(text="Solda Continua", size=(10,1), default=False, key='-CAMPO8-')],
                            [sg.Column([[sg.Text(text='Informações adicionais')],
                                        [sg.Radio('Reto','Inf.', key='-IRETO-'),
                                        sg.Radio('Convexo','Inf.',key='-ICONV-'),
                                        sg.Radio('Sem Acabamento', 'Inf.',key='-ISA-')]])
                                        ,
                            sg.Column([[sg.Text(text='Escala')],
                                        [sg.Radio('Manual', 'ESC',enable_events=True, key='-MANUAL-'),sg.Radio('Automatico','ESC',enable_events=True,key='-AUTO-',default=True)],
                                        [sg.Text(text='x'), sg.InputText('',key='-ESCX-',size=(5), disabled=True)],
                                        [sg.Text(text='y'), sg.InputText('',key='-ESCY-',size=(5), disabled=True)]
                                        ])]
                            ]


    #sg.theme('DarkRed1')
    layout = [  [sg.Text('Tipo de solda', justification='center')],
            [sg.Column([[
                sg.Radio('Filete','Prop.',enable_events=True, key='-FILETE-'),
                sg.Radio('Topo','Prop.',enable_events=True, key='-TOPO-'), 
                sg.Radio('V','Prop.' ,enable_events=True, key='-V-'),
                sg.Radio('V Curvo','Prop.' ,enable_events=True, key='-V CURVO-'),
                sg.Radio('Bisel','Prop.' ,enable_events=True, key='-BISEL-'),
                sg.Radio('U','Prop.' ,enable_events=True, key='-U-'),
                sg.Radio('J','Prop.' ,enable_events=True, key='-J-')]])],
            [
                sg.Column([
                        [sg.Text('Espessura(mm)')],
                        [sg.Text('a='),sg.InputText('',key='-ESP_A-',size=(20))],
                        [sg.Text('b='),sg.InputText('', key='-ESP_B-',size=(20))]
                        ], 
                        element_justification='l'),
                sg.Column([
                        [sg.Image(r'C:\\Users\\breno\\Desktop\\Projetos\\Soldas\\Imagem1.png', size=(200,102))]
                         ],expand_x=True, element_justification='r') #para o element justificante funcionar precisa do expand element true
                                                    ],
            [sg.Column(layout =filete_propriedades,key="Propriedades"),graph_elem],
            [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Reset')]]

    return sg.Window('Soldas',layout, finalize=True)


#dados
id = {'solda_em_campo':'','ambos_os_lados':'','contorno':''}


#Tipo estaticos
janela_um = main_test()


while True:

    window,event, values = sg.read_all_windows()
    '''
    toda a vez que um evento é disparado o while roda
    '''
    #-------------------Tipo dinamicos-----------------------------
    bloco_cad = Draw_Solder()
    grafico = Pre_visualizacao(window['-GRAPH-'])
    window['-ESCX-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
    window['-ESCY-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
    #--------------------------------------------------------------

    if event == sg.WIN_CLOSED:
        break

    #----------------------evento ok-------------------------------
    elif event == "Ok":
        #---------------------------ATT----------------------------
        att = Visualizar_att()
        if att.verificar(r'C:\Users\breno\Desktop\Projetos\Soldas\blocos'):
            handle, ponto, escala, name = att.bloco_selecionado()
            att.deletar(handle)
        else:
            handle, ponto,escala = 'N_att', 'N_att', values['-ESCX-']

        #---------------------------ESCALA-----------------------------

        if values['-AUTO-']:
            bloco_cad.escala_atual = escala
        else:
            bloco_cad.escala_atual = values['-ESCX-']

        #--------------------------------------------------------------

        if values['-OESQ-']:
            if values['-FILETE-']:

                if values['-CAMPO5-']: #solda contorno
                    if values['-CAMPO1-']: #acabamento em campo
                        if values['-CAMPO3-']:
                            solda_block = 'eSolda_filete_contorno_em_campo_amboslados'
                        else:
                            solda_block = 'eSolda_filete_contorno_em_campo'
                    elif values['-CAMPO3-']: # ambos os lados
                        solda_block = 'eSolda_filete_contorno_amboslados'
                    else:
                        #somente contorno
                        solda_block = 'eSolda_filete_contorno'


                elif values['-CAMPO1-']:
                    if False:
                        pass
                    elif values['-CAMPO3-']:
                        solda_block = 'eSolda_filete_em_campo__amboslados'
                    else:
                        #so acabamento em campo
                        solda_block = 'eSolda_filete_em_campo'
        


            elif values['-BISEL-']:
                if values['-IRETO-']:
                    if values['-CAMPO5-']:
                        solda_block = 'Solda_bisel_contorno_reto'
                elif values['-ICONV-']:
                    if values['-CAMPO5-']:
                        solda_block = 'Solda_bisel_contorno_convexo' 
                elif values['-ISA-']:
                    if values['-CAMPO5-']:
                        solda_block = 'Solda_bisel_contorno_semacabamento' 

        elif values['-ODIR-']:
            if values['-FILETE-']:
                if values['-CAMPO5-']: #solda contorno
                    if values['-CAMPO1-']: #acabamento em campo
                        if values['-CAMPO3-']:
                            solda_block = 'dSolda_filete_contorno_em_campo_amboslados'
                        else:
                            solda_block = 'dSolda_filete_contorno_em_campo'
                    elif values['-CAMPO3-']: # ambos os lados
                        solda_block = 'dSolda_filete_contorno_amboslados'
                    else:
                        #somente contorno
                        solda_block = 'dSolda_filete_contorno'


                elif values['-CAMPO1-']:
                    if False:
                        pass
                    elif values['-CAMPO3-']:
                        solda_block = 'dSolda_filete_em_campo__amboslados'
                    else:
                        #so acabamento em campo
                        solda_block = 'dSolda_filete_em_campo'
        


            elif values['-BISEL-']:
                if values['-IRETO-']:
                    if values['-CAMPO5-']:
                        solda_block = 'Solda_bisel_contorno_reto'
                elif values['-ICONV-']:
                    if values['-CAMPO5-']:
                        solda_block = 'Solda_bisel_contorno_convexo' 
                elif values['-ISA-']:
                    if values['-CAMPO5-']:
                        solda_block = 'Solda_bisel_contorno_semacabamento' 

        bloco_cad.inserir_bloco(solda_block, ponto)
        bloco_cad.espessura(values['-ESP_B-'])
        '''
    elif False:
        #jogar a janela para frente
        #remarcar os campos e deletar o ultimo campo adicionada
        pass
        '''
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
        [window[campos].Update(value=False) for campos in ['-CAMPO1-', '-CAMPO2-', '-CAMPO3-', '-CAMPO4-', '-CAMPO5-', '-CAMPO6-', '-CAMPO7-']]
        grafico.deletar()
        if values['-FILETE-']:
            grafico.filete()

    elif event == '-OESQ-':
        [window[campos].Update(value=False) for campos in ['-CAMPO1-', '-CAMPO2-', '-CAMPO3-', '-CAMPO4-', '-CAMPO5-', '-CAMPO6-', '-CAMPO7-']]
        grafico.deletar()
        if values['-FILETE-']:
            grafico.filete()
 
    #-------------------------Desenho---------------------------

    elif event == '-FILETE-':
        grafico.filete()
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
             id['ambos_os_lados'] = grafico.solda_ambos_os_lados()
        else:
            grafico.apagar(id['ambos_os_lados'])
    elif event == '-CAMPO4-':
        pass
    elif event == '-CAMPO5-':
        if values['-CAMPO5-']:
           id['contorno'] = grafico.contorno(values['-ODIR-'])
        else:
            grafico.apagar(id['contorno'])
    elif event == '-CAMPO6-':
        pass
    elif event == '-CAMPO7-':
        pass
 
    else:

        '''
        Mudanças das propriedades por escolha do tipo de solda
        '''
        ...
    
