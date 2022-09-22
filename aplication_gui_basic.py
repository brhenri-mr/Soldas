import PySimpleGUI as sg
from Aplication_draw import Draw_Solder, Solder
from Aplication_Att import Visualizar_att
from Aplication_graph import Pre_visualizacao
from pyzwcad import ZwCAD
from win32com.client import Dispatch
import os 

print(os.getcwd())

def main_test():
    #Criterio para ativação das propriedades
    sg.theme('SystemDefaultForReal')

    menu = [['Opções',['Favorito','configurações']]]

    graph_elem = sg.Graph(canvas_size=(300, 300),
                                graph_bottom_left=(0, 0),
                                graph_top_right=(400, 400),
                                enable_events=True,
                                key='-GRAPH-',
                                background_color='lightblue')
                                
    filete_propriedades = [ 
                            [sg.Text('Orientação')],
                            [sg.Radio('Direita','Ori.', key='-ODIR-', default=True, enable_events=True), sg.Radio('Esquerda','Ori.', key='-OESQ-',enable_events=True)],
                            [sg.Radio('Superior','Reg.', key='-SUP-', default=True, enable_events=True), sg.Radio('Inferior','Reg.', key='-INF-',enable_events=True)],
                            [sg.Text('Acabamentos')],
                            [sg.Checkbox(text= "Solda em campo", size=(12, 1), default=False, key='-CAMPO1-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\pixilart-drawing (3) (1).png'),sg.Checkbox(text="Descontinua", size=(15,1), default=False, key='-CAMPO2-')],
                            [sg.Checkbox(text="Ambos os lados", size=(12, 1), default=False, key='-CAMPO3-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\amboslados.png'),sg.Checkbox(text="Intercalado", default=False, key='-CAMPO4-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\intercalado.png')],
                            [sg.Checkbox(text="Todo contorno", size=(12,1), default=False, key='-CAMPO5-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\pixilart-drawing (4) (1) (2).png'),sg.Checkbox(text="Reforço", size=(10,1), default=False, key='-CAMPO6-', enable_events=True),],
                            [sg.Checkbox(text="Típico", size=(15,1), default=False, key='-CAMPO7-', enable_events=True),sg.Text('ESP=',key='-TREF-',visible=False),sg.InputText('',key='-REF-',size=(5), enable_events=True, visible=False)],
                            [sg.Column([[sg.Text(text='Informações adicionais')],
                                        [sg.Radio('Reto','Inf.', key='-IRETO-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\reto.png'),
                                        sg.Radio('Convexo','Inf.',key='-ICONV-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\convexo.png'),
                                        sg.Radio('Sem Acabamento', 'Inf.',key='-ISA-', enable_events=True)]])],
                                        
                            [sg.Column([[sg.Text(text='Escala')],
                                        [sg.Radio('Manual', 'ESC',enable_events=True, key='-MANUAL-'),sg.Radio('Automatico','ESC',enable_events=True,key='-AUTO-',default=True)],
                                        [sg.InputOptionMenu(('----','1:7.5', '1:10','1:12.5','1:25','1:50','1:100'), key='-OPESC-'),sg.Text(text='1:'), sg.InputText('',key='-ESCX-',size=(8), disabled=True)],
                                        ])]
                            ]


    layout = [ 
            [sg.Menu(menu)],
            [sg.Text('Tipo de solda', justification='l'),sg.Column([[sg.Image('star_off.png',key='-ESTRELA-',enable_events = True)]],element_justification = 'right',expand_x=True)],
            [sg.Column([[
                sg.Radio('Filete','Prop.',enable_events=True, key='-FILETE-'),
                sg.Radio('Topo','Prop.',enable_events=True, key='-TOPO-'), 
                sg.Radio('V','Prop.' ,enable_events=True, key='-V-'),
                sg.Radio('V Curvo','Prop.' ,enable_events=True, key='-V_CURVO-'),
                sg.Radio('Bisel','Prop.' ,enable_events=True, key='-BISEL-'),
                sg.Radio('Bisel Curvo','Prop.' ,enable_events=True, key='-BISEL_CURVO-'),
                sg.Radio('J','Prop.' ,enable_events=True, key='-J-'),
                sg.Radio('Misto','Prop.' ,enable_events=True, key='-MISTO-')]])],
            [
                sg.Column([
                        [sg.Text('Espessura(mm)',size=(25)),sg.Text('    '),sg.Text('Misto',justification='c')],
                        [sg.Radio('Milimetros','unid.',key='-MIM-',enable_events=True, default=True),sg.Radio('Angulo','unid.',key='-ANG-',enable_events=True),sg.Text('              '),sg.InputCombo(('----','Filete', 'Bisel','Bisel Curvo','Topo','V','V Curvo'), key='-COMI-', enable_events=True, disabled=True),sg.InputCombo(('----','Filete', 'Bisel','Bisel Curvo','Topo','V','V Curvo'), key='-COMS-', enable_events=True, disabled=True)],
                        [sg.Text('a=',key='-TEXTEXPA-'),sg.InputText('',key='-ESP_A-',size=(20), enable_events=True)],
                        [sg.Text('b=',key='-TEXTEXPB-'),sg.InputText('', key='-ESP_B-',size=(20), enable_events=True)]
                        ], 
                        element_justification='l')],
            [sg.Column(layout =filete_propriedades,key="Propriedades"),graph_elem],
            [sg.Button('Ok'), sg.Button('Reset'), sg.Button('Cancel')]]
    return sg.Window('Soldas',layout, finalize=True, icon=r'C:\Users\breno\Desktop\Projetos\Soldas\soldering_iron-48_46707.ico', titlebar_icon='soldering_iron-48_46707.ico')

def favoritos():
    sg.theme('SystemDefaultForReal')

    layout=[
        [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(50, 3), key='listbox')],
        [sg.Text('Nome'),sg.InputText('Insira o nome da solda')]
        ]
    return sg.Window('Favoritos',layout, finalize=True)

#dados
id = {'Base':'','solda_em_campo':'','ambos_os_lados':'','contorno':'','acabamento':'','intercalado':'', 'expA':'','expB':'','Reforco':'','tipico':'','Base_m_i':'','Base_m_s':''}


#Tipo estaticos
base = 'FILETE' #variavel para auxiliar no desenho
janela_um = main_test()
arquivo_nome = Solder()
grafico = Pre_visualizacao(janela_um['-GRAPH-'])

#tipo dinamico 
j = True #liga e desliga o 

while True:
    try:
        zw = ZwCAD()
        acad = Dispatch("ZwCAD.Application")
        break
    except:
        sg.Popup('Erro ao tentar encontrar um ZwCAD')



while True:

    window,event, values = sg.read_all_windows()
    bloco_arquivo = arquivo_nome.tipo(values)
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
    
    #--------------------------------------------------------------

    if event == sg.WIN_CLOSED:
        break
    #----------------------RESET-----------------------------------

    elif event == 'Reset':
        [window[i].Update(value=False) for i in [f'-CAMPO{j}-' for j in range(1,8,1)]]

        for key,item in id.items():
            if key not in ['Base','expA','expB','Base_m_i','Base_m_s']:
                grafico.apagar(item)


    #----------------------evento ok-------------------------------
    elif event == "Ok":

        #---------------------------ATT----------------------------
        att = Visualizar_att()
        if att.verificar():
            handle, ponto, escala, name = att.bloco_selecionado()
            att.deletar(handle)
        else:
            handle, ponto,escala = 'N_att', 'N_att', values['-ESCX-']

        #---------------------------ESCALA-----------------------------

        if values['-AUTO-']:
            if values['-OPESC-'] not in ['----','']:
                # tratamento do string escala
                bloco_cad.escala_atual = float(values['-OPESC-'][2:])
            else:
                bloco_cad.escala_atual = escala
        else:
            
            bloco_cad.escala_atual = values['-ESCX-']

        #---------------------------INSERIR---------------------------
        if att.verificar_arquivo(bloco_arquivo):
            bloco_cad.inserir_bloco(bloco_arquivo, ponto)
            bloco_cad.espessura([values['-REF-'],values['-ESP_B-'],values['-ESP_A-']])
        else:
            sg.popup('Bloco Não Disponível')
            bloco_cad.creat_solder(bloco_arquivo,values['-MIM-'])
            sg.popup('Bloco cadastradado com sucesso')
        
    #-------------------------EScala---------------------------
    
        #deixou o programa lento essa historia de pegar o valor da escala atual
    
    elif event =='-MANUAL-':
        window['-ESCX-'].Update(disabled=False, value='')
        
    elif event == '-AUTO-':
        if values['-OPESC-'] not in ['----','']:
            window['-ESCX-'].Update(disabled=True,value=int(values['-OPESC-'][-2:]) if len(values['-OPESC-']) == 4 else  int(values['-OPESC-'][-1]))
        else:
            window['-ESCX-'].Update(disabled=True,value=round(bloco_cad.escala_atual,1))
        

    #--------------------------Orientação----------------------

    elif event == '-ODIR-':
        
        grafico.deletar()
        id =grafico.solda_desenhada(id,True,base)

    elif event == '-OESQ-':

        grafico.deletar()
        id = grafico.solda_desenhada(id,False,base)
 
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
        window['-MIM-'].Update(disabled=False)
        window['-ANG-'].Update(disabled=True)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        if isinstance(id['Base'],int):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
        else:
            grafico.deletar()
        print(values['-INF-'])
        id['Base'] = grafico.filete(reg=values['-SUP-'])
        base = 'FILETE'
  
    elif event == '-BISEL-':
        window['-MIM-'].Update(disabled=False)
        window['-ANG-'].Update(disabled=False)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        if isinstance(id['Base'],int):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
        else:
            grafico.deletar()
        id['Base'] = grafico.bisel(reg=values['-SUP-'])
        base = 'BISEL'

    elif event == '-BISEL_CURVO-':
        window['-MIM-'].Update(disabled=True)
        window['-ANG-'].Update(disabled=True)
        window['-ESP_A-'].Update(disabled=True)
        window['-ESP_B-'].Update(disabled=True)
        window['-CAMPO3-'].Update(disabled=False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        if isinstance(id['Base'],int):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
        else:
            grafico.deletar()
        id['Base'] = grafico.bisel_curvo()
        base = 'BISEL_CURVO'
    
    elif event == '-V-':
        window['-MIM-'].Update(disabled=True)
        window['-ANG-'].Update(disabled=False)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        if isinstance(id['Base'],int):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
        else:
            grafico.deletar()
        id['Base'] = grafico.v()
        base = 'V'

    elif event == '-V_CURVO-':
        window['-MIM-'].Update(disabled=True)
        window['-ANG-'].Update(disabled=True)
        window['-ESP_A-'].Update(disabled=True)
        window['-ESP_B-'].Update(disabled=True)
        window['-CAMPO3-'].Update(disabled=False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        if isinstance(id['Base'],int):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
        else:
            grafico.deletar()
        id['Base'] = grafico.v_curvo()
        base = 'V_CURVO'

    elif event == '-TOPO-':
        window['-MIM-'].Update(disabled=True)
        window['-ANG-'].Update(disabled=False)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        if isinstance(id['Base'],int):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
        else:
            grafico.deletar()
        id['Base'] = grafico.topo()
        base = 'TOPO'
    
    elif event == '-J-':
        window['-CAMPO3-'].Update(disabled=False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        if isinstance(id['Base'],int):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
        else:
            grafico.deletar()
        id['Base'] = grafico.j()
        base = 'J'

    elif event == '-MISTO-':
        window['-COMI-'].Update(disabled=False)
        window['-COMS-'].Update(disabled=False)
        grafico.apagar(id['Base'])
        id['Base']= window['-GRAPH-'].draw_lines([(100,200),(280,200)],color='red')

        window['-CAMPO3-'].Update(disabled=True)
 
    elif event == '-COMI-':
        if values['-MISTO-']:

            if isinstance(id['Base_m_i'],int):
                grafico.apagar(id['Base_m_i'])

            base = 'MISTO_'+values['-COMI-'].upper() + '_'+ (values['-COMS-'].upper() if values['-COMS-'] != '' else 'NULL')
            grafico.deletar()
            id = grafico.solda_desenhada(id,True,base)
        else:
            pass
            
    elif event == '-COMS-':
        if values['-MISTO-']:
            if isinstance(id['Base_m_s'],int):
                grafico.apagar(id['Base_m_s'])
            base = 'MISTO_'+ (values['-COMI-'].upper() if values['-COMI-']!='' else 'NULL') + '_'+values['-COMS-'].upper()
            grafico.deletar()
            id = grafico.solda_desenhada(id,True,base)
        else:
            pass

        #---------------------TEXT-------------------------------
    elif event == '-ANG-':
        window['-ESP_A-'].Update(disabled=True, value='')
        window['-TEXTEXPA-'].Update(value='    ')
    elif event == '-MIM-':
        window['-ESP_A-'].Update(disabled=False)
        window['-TEXTEXPA-'].Update(value='a=')

    elif event == '-ESP_B-' or event=='-ESP_A-':
        grafico.apagar(id['expB'])
        if values['-CAMPO4-']: #intercalador
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Intercalado',values['-MIM-'])
        elif values['-CAMPO3-']: #anbos os lados
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Amboslados',values['-MIM-'],base)
        else:
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],base,values['-MIM-'])
        #---------------------------------------------------------

    elif event == '-CAMPO1-':
        if values['-CAMPO1-']:
            id['solda_em_campo'] = grafico.solda_em_campo(values['-ODIR-'])
        else:
            grafico.apagar(id['solda_em_campo'])
            id['solda_em_campo'] = ''
            
    elif event == '-CAMPO2-':
        pass
    elif event == '-CAMPO3-':
        if values['-CAMPO3-']:
            id['ambos_os_lados'] = grafico.solda_ambos_os_lados(base)
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Amboslados',values['-MIM-'],base)
        else:
            grafico.apagar(id['ambos_os_lados'])
            id['ambos_os_lados'] = ''
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-']],'Filete',values['-MIM-'])

    elif event == '-CAMPO4-':
        if values['-CAMPO4-']:
            id['intercalado'] = grafico.intercalado(id['Base'])
            #redesenhar as espessuras
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Intercalado',values['-MIM-'])
        else:
            #aparemente não existe bisel intercalado
            grafico.apagar(id['intercalado'])
            id['Base'] = grafico.filete()
            grafico.apagar(id['expB'])
            id['expB'] = grafico.espessura([values['-ESP_B-'],values['-ESP_A-']],'Filete',values['-MIM-'])

    elif event == '-CAMPO5-':
        if values['-CAMPO5-']:
           id['contorno'] = grafico.contorno(values['-ODIR-'])
        else:
            grafico.apagar(id['contorno'])
            id['contorno'] = ''

    elif event == '-CAMPO6-':
        pass

    elif event == '-CAMPO7-':
        if values['-CAMPO7-']:
            id['tipico'] = grafico.tipico(values['-ODIR-'])
        else:
            grafico.apagar(id['tipico'])
            id['tipico'] = ''

    #-------------------------ACABAMENTOS-------------------------
    elif event == '-IRETO-' and (base == 'BISEL'or base =='TOPO'):
        grafico.apagar(id['acabamento'])
        id['acabamento'] = grafico.acabamento_reto(values['-CAMPO3-'],base)

    elif event == '-ICONV-' and (base == 'BISEL'or base =='TOPO'):
        grafico.apagar(id['acabamento'])
        id['acabamento'] = grafico.acabamento_convexo(values['-CAMPO3-'],base)
   
    elif event == '-ISA-' and (base == 'BISEL'or base =='TOPO'):
        grafico.apagar(id['acabamento'])
    
    #------------------------grafico--------------------------
    elif event == '-GRAPH-':
        pass
    #------------------------Favorito_estrela--------------------------
    elif event == '-ESTRELA-':
        if j:
            window['-ESTRELA-'].update(source='star_on.png')
            j = False
        else:
            window['-ESTRELA-'].update(source='star_off.png')
            j = True
    #------------------------Favorito_TELA--------------------------
    if event == 'Favorito':
        janela_dois = favoritos()
    else:

        '''
        Mudanças das propriedades por escolha do tipo de solda
        '''
        ...
