import PySimpleGUI as sg
from Aplication_draw import Draw_Solder
from Aplication_graph import Pre_visualizacao
from pyzwcad import ZwCAD
from win32com.client import Dispatch
from datetime import datetime


def main_test(filete=False,campo=False, contorno=False,direita=False,esquerda=False,amboslados=False):
    #Criterio para ativação das propriedades
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
                            [sg.Checkbox(text="Solda em todo contorno", size=(10,1), default=False, key='-CAMPO5-', enable_events=True)],
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



    #sg.theme('DarkRed1')
    layout = [  [sg.Text('Tipo de solda', justification='center')],
            [sg.Column([[
                sg.Radio('Filete','Prop.',enable_events=True, key='-FILETE-', default=filete),
                sg.Radio('Topo','Prop.',enable_events=True, key='-TOPO-'), 
                sg.Radio('V','Prop.' ,enable_events=True, key='-V-'),
                sg.Radio('V Curvo','Prop.' ,enable_events=True, key='-V CURVO-'),
                sg.Radio('Bisel','Prop.' ,enable_events=True, key='-BISEL-'),
                sg.Radio('U','Prop.' ,enable_events=True, key='-U-'),
                sg.Radio('J','Prop.' ,enable_events=True, key='-J-')]])],
            [
                sg.Column([
                        [sg.Text('Espessura(mm)')],
                        [sg.Text('a='),sg.InputText('',key='-ESP_A-',size=(20), enable_events=True)],
                        [sg.Text('b='),sg.InputText('', key='-ESP_B-',size=(20),  enable_events=True)]
                        ], 
                        element_justification='l'),
                sg.Column([
                        [sg.Image(r'C:\\Users\\breno\\Desktop\\Projetos\\Soldas\\Imagem1.png', size=(200,102))]
                         ],expand_x=True, element_justification='r') #para o element justificante funcionar precisa do expand element true
                                                    ],
            [sg.Column(layout =filete_propriedades,key="Propriedades"),graph_elem],
            [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Reset')]]

    return sg.Window('Solda duplo click',layout, finalize=True,)

def ler_log():
        with open("log.txt",'r') as arquivo:
            linha = arquivo.readlines()[-1][:-2].split(',')
        return({'handle':linha[0],'ponto':[float(linha[1]),float(linha[2])],'escala':float(linha[3]),'nome':linha[4], 'time':datetime.strptime(linha[5],"%m/%d/%Y %H:%M:%S:%f")})


 

def solda_desenhada(nome):

        '''
        Desenha a solda do autocad no programa
        '''
        id = {'filete':False,'contorno':False,'amboslados':False,'campo':False,'direita':False,'esquerda':False}

        if 'd' == nome[0]:
            id['direita']=True
            if 'filete' in nome:
                id['filete']=True
            elif 'bisel' in nome:
                pass
            if 'contorno' in nome:
                id['contorno']=True
            if 'amboslados' in nome:
                id['amboslados']=True
            if 'campo' in nome:
                id['campo']=True

        elif 'e' == nome[0]:
            id['esquerda']=True
            if 'filete' in nome:
                id['filete']=True
            elif 'bisel' in nome:
                pass
            if 'contorno' in nome:
                id['contorno']=True
            if 'amboslados' in nome:
                id['amboslados']=True
            if 'campo' in nome:
                id['campo']=True

        return id


zw = ZwCAD()
acad = Dispatch("ZwCAD.Application")
bloco_cad = Draw_Solder(zw,acad)
tempo_utilizado = '' 
bloco_obtido = True
base = 'FILETE'
id = {'Base':'','solda_em_campo':'','ambos_os_lados':'','contorno':'','acabamento':'','intercalado':'','expB':''}



#fazer marca o campo qunado a janela abre
#for campo in zip(''[f'-CAMPO{i}-' for i in range(1,6)]):
    #if 
    #janela_um.Element(campo).Update(value=True)



while True:

    while bloco_obtido:
        #estou verificando que a ultima vez que o log foi utilizado se foi recente para que possa aparecer a janela de modificação

            parametros = ler_log()
            if (datetime.now()-parametros['time']).total_seconds() <=0.4 :
                if parametros['time'] != tempo_utilizado:
                    #inicializando a janela
                    codigo = solda_desenhada(parametros['nome'])
                    janela_um = main_test(
                        filete=codigo['filete'],
                        campo=codigo['campo'], 
                        contorno=codigo['contorno'],
                        direita=codigo['direita'],
                        esquerda=codigo['esquerda'],
                        amboslados=codigo['amboslados']
                    )
                    
                    grafico = Pre_visualizacao(janela_um.Element("-GRAPH-"))
                    #parametros
                    sid = grafico.solda_desenhada(parametros['nome'])
                    tempo_utilizado =  parametros['time']
                    bloco_obtido = False
                    break
            else:
                pass

      
        


    print(bloco_cad.handle)
    window,event, values = sg.read_all_windows()
    '''
    toda a vez que um evento é disparado o while roda
    '''
    #-------------------Tipo dinamicos-----------------------------
    #bloco_cad = Draw_Solder()
    window['-ESCX-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
    window['-ESCY-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
    #--------------------------------------------------------------

    print(event)
    if event == sg.WIN_CLOSED:
        window.close()
        bloco_obtido = True

    #----------------------evento ok-------------------------------
    elif event == "Ok":
        #---------------------------ATT----------------------------

        ponto,escala, nome =  parametros['ponto'], parametros['escala'], parametros['nome']
   
        handle = parametros['handle']


        print(handle,ponto,escala,nome)
        #---------------------------ESCALA-----------------------------

        if values['-AUTO-']:
            bloco_cad.escala_atual = escala
        else:
            bloco_cad.escala_atual = values['-ESCX-']

        #----------------------------INSERIR-------------------------------

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
                    if values['-ODIR-']:
                        if values['-CAMPO5-'] : #contorno
                            if values['-CAMPO1-'] and values['-CAMPO3-']: 
                                solda_block = 'dSolda_bisel_contorno_convexo_em_campo_amboslados'
                            elif values['-CAMPO1-']: 
                                solda_block = 'dSolda_bisel_contorno_convexo_em_campo'
                            elif values['-CAMPO3-']: 
                                solda_block = 'dSolda_bisel_convexo_em_campo_amboslados'
                            else:
                                solda_block = 'dSolda_bisel_contorno_convexo' 

        bloco_cad.apagar_bloco(handle)
        bloco_cad.inserir_bloco(solda_block, ponto)
        bloco_cad.espessura(values['-ESP_B-'],bloco_cad.handle)
        #finalizar a janela
        window.close()
        bloco_obtido = True
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
        [window[campos].Update(value=False) for campos in ['-CAMPO1-', '-CAMPO2-', '-CAMPO3-', '-CAMPO4-', '-CAMPO5-']]
        grafico.deletar()
        if values['-FILETE-']:
            id['Base'] = grafico.filete()

    elif event == '-OESQ-':
        [window[campos].Update(value=False) for campos in ['-CAMPO1-', '-CAMPO2-', '-CAMPO3-', '-CAMPO4-', '-CAMPO5-']]
        grafico.deletar()
        if values['-FILETE-']:
            id['Base'] = grafico.filete()
 
    #-------------------------Desenho---------------------------

    elif event == '-FILETE-':

        grafico.deletar()
        id['Base'] = grafico.filete()
        base = 'FILETE'
            
  
    elif event == '-BISEL-':

        grafico.deletar()
        grafico.bisel()
        base = 'BISEL'

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


    elif event == '-IRETO-' and base == 'BISEL':
        print(values['-CAMPO3-'])
        id['acabamento'] = grafico.acabamento_reto(values['-CAMPO3-'])

    elif event == '-ICONV-' and base == 'BISEL':

        id['acabamento'] = grafico.acabamento_convexo(values['-CAMPO3-'])
   
    elif event == '-ISA-' and base == 'BISEL':

        pass
   

   
 
    else:

        '''
        Mudanças das propriedades por escolha do tipo de solda
        '''
        ...