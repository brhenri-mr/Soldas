import PySimpleGUI as sg
from Aplication_draw import Draw_Solder
from Aplication_Att import Visualizar_att



def main_test():
    #Criterio para ativação das propriedades
    graph_elem = sg.Graph((200,150), (0, 200), (300, 0),
                                enable_events=True,
                                key='-GRAPH-',
                                background_color='lightblue',
                                visible=False)
                                
    filete_propriedades = [ [sg.Text('Orientação')],
                            [sg.Checkbox(text='Direita', key='-ODIR-'), sg.Checkbox(text='Esquerda', key='-OESQ-')],
                            [sg.Text('Acabamentos')],
                            [sg.Checkbox(text= "Solda em campo", size=(10, 1), default=False, key='-CAMPO1-', enable_events=True),sg.Checkbox(text="Solda Continua", size=(10,1), default=False, key='-CAMPO2-')],
                            [sg.Checkbox(text="Ambos os lados", size=(10, 1), default=False, key='-CAMPO3-'),sg.Checkbox(text="Intercalado", size=(10,1), default=False, key='-CAMPO4-')],
                            [sg.Checkbox(text="Solda em todo contorno", size=(10,1), default=False, key='-CAMPO5-', enable_events=True), sg.Checkbox(text="Solda em todo contorno", size=(10,1), default=False, key='-CAMPO6-', enable_events=True)],
                            [sg.Checkbox(text="Filete", size=(10, 1), default=False, key='-CAMPO7-'),sg.Checkbox(text="Solda Continua", size=(10,1), default=False, key='-CAMPO8-')],
                            [sg.Text(text='Informações adicionais')],
                            [sg.Radio('Reto','Inf.', key='-IRETO-'),sg.Radio('Convexo','Inf.',key='-ICONV-'),sg.Radio('Sem Acabamento', 'Inf.',key='-ISA-')]
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
            [sg.Column(layout =filete_propriedades,key="Propriedades", visible=False),graph_elem],
            [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Reset')]]

    return sg.Window('Soldas',layout, finalize=True)

class Pre_visualizacao():
    """
    Controla todos os desenhos/imagens que serão disponibilizadas no gui
    """

    def __init__(self, janela) -> None:

        self.janela = janela


    def solda_em_campo(self):
        pass
    def solda_continua(self):
        pass
    def solda_ambos_os_lados(self):
        pass
    def intercalado(self):
        pass
    def contorno(self):
        pass
    def solda_continua(self):
        pass


#dados
keys_propriedades = ["-CAMPO"+str(i)+'-' for i in range(1,8)]
text_filete = ['S. Campo','Continua','Ambos Lados','Intercalado','Todo Contorno','Filete','Continua']
text_bisel = ['Maria', 'Jose','Adamastor','Cleusa','Todo Contorno','Douglas','Lemos']


janela_um = main_test()
while True:
    

    window,event, values = sg.read_all_windows()
    '''
    toda a vez que um evento é disparado o while roda
    '''
    print(event)
    if event == sg.WIN_CLOSED:
        break


    #----------------------evento ok-------------------------------
    elif event == "Ok":
        #---------------------------ATT----------------------------
        att = Visualizar_att()
        if att.verificar(r'C:\Users\breno\Desktop\Projetos\Soldas\blocos'):
            handle, ponto = att.bloco_selecionado()
            att.deletar(handle)
        else:
            handle, ponto = 'N_att', 'N_att'

        #--------------------------------------------------------------

        bloco_cad = Draw_Solder()
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
    #------------------------------------------------------
    else:
        if event in ['-FILETE-','-BISEL-','-TOPO-','-V-','-V CURVO-','-U-','-J-']:
            if event == '-FILETE-':
                cri = '-FILETE-'
                texto = text_filete.copy()
                window['-GRAPH-'].draw_line((75,150),(225,150))
                window['-GRAPH-'].draw_line((150,150),(150,170))
                window['-GRAPH-'].draw_line((150,170),(170,150))

        
            elif event == '-BISEL-':
                texto = text_bisel.copy()

            elif event == 'Tipo 3':
                ...

            for nomes, keys  in zip(texto,keys_propriedades):
                window[keys].Update(text = nomes, value = False)
            window['Propriedades'].Update(visible = True)
            window['-GRAPH-'].Update(visible = True)
            [window[i].Update(disabled = event ==i) for i in ['-FILETE-','-BISEL-','-TOPO-','-V-','-V CURVO-','-U-','-J-']]

        if cri == '-FILETE-':
            if event == '-CAMPO5-':
                window['-GRAPH-'].draw_circle((225,150), radius=10)
                pass
        if event == 'Cancel':
            window['-GRAPH-'].erase()
