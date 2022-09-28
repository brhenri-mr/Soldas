import PySimpleGUI as sg
from Aplication_draw import Draw_Solder, Solder
from Aplication_graph import Pre_visualizacao
from Aplication_Att import Visualizar_att
from pyzwcad import ZwCAD
from win32com.client import Dispatch
from datetime import datetime

def main_test(filete=False,campo=False, contorno=False,direita=True,esquerda=False,amboslados=False,inter=False,bisel=False,topo=False,
                misto=False,reforco=False,reforco_S=False,v=False,v_curvo=False,bisel_curvo=False,descontinua=False,tipico=False,reto=False,none=True,
                convexo=False):
    #Criterio para ativação das propriedades
    sg.theme('SystemDefaultForReal')
    graph_elem = sg.Graph(canvas_size=(300, 300),
                                graph_bottom_left=(0, 0),
                                graph_top_right=(400, 400),
                                enable_events=True,
                                key='-GRAPH-',
                                background_color='lightblue')
                                
    filete_propriedades = [ 
                            [sg.Text('Orientação')],
                            [sg.Radio('Direita','Ori.', key='-ODIR-', default=True, enable_events=True), sg.Radio('Esquerda','Ori.', key='-OESQ-',enable_events=True)],
                            [sg.Radio('Superior','Reg.', key='-SUP-', default=False, enable_events=True), sg.Radio('Inferior','Reg.', key='-INF-',enable_events=True, default=True)],
                            [sg.Text('Acabamentos')],
                            [sg.Radio('Reto','Inf.', key='-IRETO-', enable_events=True,default=reto),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\reto.png'),
                            sg.Radio('Convexo','Inf.',key='-ICONV-', enable_events=True,default=convexo),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\convexo.png'),
                            sg.Radio('None', 'Inf.',key='-ISA-', enable_events=True,default=none)],
                            [sg.Checkbox(text= "Solda em campo", size=(12, 1), default=campo, key='-CAMPO1-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\solda_campo.png'),sg.Checkbox(text="Ambos os lados", size=(12, 1), default=amboslados, key='-CAMPO3-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\amboslados.png')],
                            [sg.Checkbox(text="Intercalado",size=(12, 1), default=inter, key='-CAMPO4-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\intercalado.png'),sg.Checkbox(text="Todo contorno", size=(12,1), default=contorno, key='-CAMPO5-', enable_events=True),sg.Image(source=r'C:\Users\breno\Desktop\Projetos\Soldas\imagens\contorno.png'),],
                            [sg.Checkbox(text="Reforço", size=(10,1), default=reforco, key='-CAMPO6-', enable_events=True),sg.Text('espessura reforço=',key='-TREF-',visible=False),sg.InputText('',key='-REF-',size=(5), enable_events=True, visible=False)],
                            [sg.Column([[sg.Text(text='Informações adicionais')],
                                        [sg.Checkbox(text="Descontinua", size=(10,1), default=descontinua, key='-CAMPO2-',enable_events=True),sg.Text('Passo',key='-TXTCAMPO2-'),sg.InputText('',size =(15,1),key='-INPUTTXTCAMPO2-',enable_events = True, disabled=True)],
                                        [sg.Checkbox(text="Típico", size=(15,1), default=tipico, key='-CAMPO7-', enable_events=True)]])],
                                        
                            [sg.Column([[sg.Text(text='Escala')],
                                        [sg.Radio('Manual', 'ESC',enable_events=True, key='-MANUAL-'),sg.Radio('Automatico','ESC',enable_events=True,key='-AUTO-',default=True)],
                                        [sg.InputOptionMenu(('----','1:7.5', '1:10','1:12.5','1:25','1:50','1:100'), key='-OPESC-'),sg.Text(text='1:'), sg.InputText('',key='-ESCX-',size=(8), disabled=True)],
                                        ])]
                            ]

    layout = [  [sg.Text('Tipo de solda', justification='center')],
            [sg.Column([[
                sg.Radio('Filete','Prop.',enable_events=True, key='-FILETE-', default=filete),
                sg.Radio('Topo','Prop.',enable_events=True, key='-TOPO-',default=topo), 
                sg.Radio('V','Prop.' ,enable_events=True, key='-V-',default=v),
                sg.Radio('V Curvo','Prop.' ,enable_events=True, key='-V_CURVO-',default=v_curvo),
                sg.Radio('Bisel','Prop.' ,enable_events=True, key='-BISEL-', default=bisel),
                sg.Radio('Bisel Curvo','Prop.' ,enable_events=True, key='-BISEL_CURVO-',default=bisel_curvo),
                sg.Radio('J','Prop.' ,enable_events=True, key='-J-'),
                sg.Radio('Misto','Prop.' ,enable_events=True, key='-MISTO-', default=misto)]])],
            [
                sg.Column([
                        [sg.Text('Espessura(mm)',size=(25)),sg.Text('    '),sg.Text('Misto',justification='c')],
                        [sg.Radio('Milimetros','unid.',key='-MIM-',enable_events=True, default=True),sg.Radio('Angulo','unid.',key='-ANG-',enable_events=True),sg.Text('              '),
                        sg.InputCombo(('----','Filete', 'Bisel','Bisel Curvo','Topo','V','V Curvo'), key='-COMS-', enable_events=True, disabled=True),
                        sg.Checkbox('Reforço',key='-COMSCHECKREF-',enable_events=True,default=reforco_S),sg.InputText('',key='-COMSREF-',size=(5), enable_events=True, visible=False)],

                        [sg.Text('a=',key='-TEXTEXPA-'),sg.InputText('',key='-ESP_A-',size=(20), enable_events=True),sg.Text('            '),
                        sg.InputCombo(('----','Filete', 'Bisel','Bisel Curvo','Topo','V','V Curvo'), key='-COMI-', enable_events=True, disabled=True),
                        sg.Checkbox('Reforço',key='-COMICHECKREF-',enable_events=True,default=reforco),sg.InputText('',key='-COMIREF-',size=(5), enable_events=True, visible=False)],

                        [sg.Text('b=',key='-TEXTEXPB-'),sg.InputText('', key='-ESP_B-',size=(20), enable_events=True)]
                        ], 
                        element_justification='l')],
            [sg.Column(layout =filete_propriedades,key="Propriedades"),graph_elem],
            [sg.Button('Ok'), sg.Button('Reset'), sg.Button('Cancel')]]

    return sg.Window('Solda duplo click',layout, finalize=True,)

def ler_log():
        with open("log.txt",'r') as arquivo:
            linha = arquivo.readlines()[-1][:-2].split(',')
        return({'handle':linha[0],'ponto':[float(linha[1]),float(linha[2])],'escala':float(linha[3]),'nome':linha[4], 'time':datetime.strptime(linha[5],"%m/%d/%Y %H:%M:%S:%f")})


#Zwcad

acad = Dispatch("ZwCAD.Application")

#classes
zw = ZwCAD()
bloco_cad = Draw_Solder(zw,acad)
arquivo_nome  = Solder()
att = Visualizar_att()

#Parametro adicionais
tempo_utilizado = '' 
bloco_obtido = True
base = 'FILETE'
id = {
    'Base':'',
    'solda_em_campo':'',
    'ambos_os_lados':'',
    'contorno':'',
    'acabamento':'',
    'intercalado':'', 
    'expA':'','expB':'',
    'Reforco':'',
    'tipico':'',
    'Base_m_i':'',
    'Base_m_s':'',
    'm_reforco_s':'',
    'm_reforco_i':'',
    'Descontinuo':''
    }

while True:

    while bloco_obtido:
        #estou verificando que a ultima vez que o log foi utilizado se foi recente para que possa aparecer a janela de modificação
            parametros = ler_log()
            if (datetime.now()-parametros['time']).total_seconds() <=0.4 :
                if parametros['time'] != tempo_utilizado:
                    #inicializando a janela
                    codigo = arquivo_nome.solda_desenhada(parametros['nome'])
                    janela_um = main_test(
                        filete=codigo['filete'],
                        bisel=codigo['bisel'],
                        campo=codigo['campo'], 
                        contorno=codigo['contorno'],
                        direita=codigo['direita'],
                        esquerda=codigo['esquerda'],
                        amboslados=codigo['amboslados'],
                        inter=codigo['inter'],
                        descontinua=codigo['descontinua'],
                        reforco=codigo['Reforco'],
                        reforco_S=codigo['Reforco%']
                    )
                    grafico = Pre_visualizacao(janela_um.Element("-GRAPH-"))
                    #parametros
                    sid = grafico.solda_desenhada(codigo)
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
    #--------------------------------------------------------------

    print(event)
    if event == sg.WIN_CLOSED:
        window.close()
        bloco_obtido = True

    #----------------------RESET-----------------------------------

    elif event == 'Reset':
        [window[i].Update(value=False) for i in [f'-CAMPO{j}-' for j in range(1,8,1)]]

        for key,item in id.items():
            if key not in ['Base','expA','expB','Base_m_i','Base_m_s']:
                grafico.apagar(item)

    #----------------------evento ok-------------------------------
    elif event == "Ok":
        bloco_arquivo = arquivo_nome.tipo(values)
        #---------------------------ATT----------------------------

        ponto,escala, nome =  parametros['ponto'], parametros['escala'], parametros['nome']
   
        handle = parametros['handle']

        print(handle,ponto,escala,nome)
        #---------------------------ESCALA-----------------------------

        if values['-AUTO-']:
            if values['-OPESC-'] not in ['----','']:
                # tratamento do string escala
                bloco_cad.escala_atual = float(values['-OPESC-'][2:])
            else:
                bloco_cad.escala_atual = escala
        else:
            
            bloco_cad.escala_atual = values['-ESCX-']

        #----------------------------INSERIR-------------------------------
        if att.verificar_arquivo(bloco_arquivo):
            bloco_cad.apagar_bloco(handle)
            bloco_cad.inserir_bloco(bloco_arquivo, ponto)
            bloco_cad.espessura({'REF':values['-REF-'],'CORDAO':[values['-ESP_B-'],values['-ESP_A-']]},bloco_cad.handle)
            if values['-CAMPO2-']:
                bloco_cad.descontinua(values['-INPUTTXTCAMPO2-'])
                
            #finalizar a janela
            window.close()
            bloco_obtido = True
        else:
            sg.popup('Bloco Não Disponível')
       
        '''
    elif False:
        #jogar a janela para frente
        #remarcar os campos e deletar o ultimo campo adicionada
        pass
        '''
    #-------------------------EScala---------------------------
    

    
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
            id['Reforco'] = grafico.reforco(direcao=values['-INF-'])
        else:
            ref = False
            grafico.apagar(id['Reforco'])
            pass
        window['-TREF-'].Update(visible=ref)
        window['-REF-'].Update(visible=ref)

    elif event == '-REF-':
        grafico.apagar(id['expREF'])
        id['expREF'] = grafico.espessura([values['-REF-']],'Reforco',True,direcao=True)

    elif event == '-COMSCHECKREF-':
        if values['-COMSCHECKREF-']:
            ref = True
            id['m_reforco_s'] = grafico.reforco(direcao=False)
        else:
            ref = False
            grafico.apagar(id['m_reforco_s'])
        window['-COMSREF-'].Update(visible=ref)

    elif event == '-COMICHECKREF-':
        if values['-COMICHECKREF-']:
            ref = True
            id['m_reforco_i'] = grafico.reforco()
        else:
            ref = False
            grafico.apagar(id['m_reforco_i'])
            pass
        window['-COMIREF-'].Update(visible=ref)
    
    elif event == '-COMSREF-':
        grafico.apagar(id['expCOMS'])
        id['expCOMS'] = grafico.espessura([values['-COMSREF-']],'Reforco',True,direcao=False)

    elif event == '-COMIREF-':
        grafico.apagar(id['expCOMI'])
        id['expCOMI'] = grafico.espessura([values['-COMIREF-']],'Reforco',True,direcao=True)

    #-------------------------Desenho---------------------------

    elif event == '-FILETE-':
        window['-MIM-'].Update(disabled=False)
        window['-ANG-'].Update(disabled=True)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-CAMPO4-'].Update(disabled=False)
        window['-CAMPO6-'].Update(disabled=False, value = False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        window['-COMICHECKREF-'].Update(disabled=True)
        window['-COMSCHECKREF-'].Update(disabled=True)
        window['-COMIREF-'].Update(disabled=True)
        window['-COMSREF-'].Update(disabled=True)
        if isinstance(id['Base'],int) or isinstance(id['Base'],list):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
            if values['-CAMPO3-']:
                grafico.apagar(id['ambos_os_lados'])
                id['ambos_os_lados'] = grafico.solda_ambos_os_lados('FILETE')
        else:
            grafico.deletar()
        id['Base'] = grafico.filete(reg=values['-INF-'])
        base = 'FILETE'
  
    elif event == '-BISEL-':
        window['-MIM-'].Update(disabled=False, value=True)
        window['-ANG-'].Update(disabled=False)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-CAMPO4-'].Update(disabled=True)
        window['-CAMPO6-'].Update(disabled=False, value = False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        window['-COMICHECKREF-'].Update(disabled=True)
        window['-COMSCHECKREF-'].Update(disabled=True)
        window['-COMIREF-'].Update(disabled=True)
        window['-COMSREF-'].Update(disabled=True)
        if isinstance(id['Base'],int) or isinstance(id['Base'],list):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
            if values['-CAMPO3-']:
                grafico.apagar(id['ambos_os_lados'])
                id['ambos_os_lados'] = grafico.solda_ambos_os_lados('BISEL')
        else:
            grafico.deletar()
        id['Base'] = grafico.bisel(reg=values['-INF-'])
        base = 'BISEL'

    elif event == '-BISEL_CURVO-':
        window['-MIM-'].Update(disabled=True)
        window['-ANG-'].Update(disabled=True)
        window['-ESP_A-'].Update(disabled=True)
        window['-ESP_B-'].Update(disabled=True)
        window['-CAMPO3-'].Update(disabled=False)
        window['-CAMPO4-'].Update(disabled=True)
        window['-CAMPO6-'].Update(disabled=False, value = False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        window['-COMICHECKREF-'].Update(disabled=True)
        window['-COMSCHECKREF-'].Update(disabled=True)
        window['-COMIREF-'].Update(disabled=True)
        window['-COMSREF-'].Update(disabled=True)
        if isinstance(id['Base'],int) or isinstance(id['Base'],list):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
            if values['-CAMPO3-']:
                grafico.apagar(id['ambos_os_lados'])
                id['ambos_os_lados'] = grafico.solda_ambos_os_lados('BISEL_CURVO')
        else:
            grafico.deletar()
        id['Base'] = grafico.bisel_curvo()
        base = 'BISEL_CURVO'
    
    elif event == '-V-':
        window['-MIM-'].Update(disabled=True)
        window['-ANG-'].Update(disabled=False, value=True)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-CAMPO4-'].Update(disabled=True)
        window['-CAMPO6-'].Update(disabled=False, value = False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        window['-COMICHECKREF-'].Update(disabled=True)
        window['-COMSCHECKREF-'].Update(disabled=True)
        window['-COMIREF-'].Update(disabled=True)
        window['-COMSREF-'].Update(disabled=True)
        if isinstance(id['Base'],int) or isinstance(id['Base'],list):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
            if values['-CAMPO3-']:
                grafico.apagar(id['ambos_os_lados'])
                id['ambos_os_lados'] = grafico.solda_ambos_os_lados('V')
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
        window['-CAMPO4-'].Update(disabled=True)
        window['-CAMPO6-'].Update(disabled=False, value = False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        window['-COMICHECKREF-'].Update(disabled=True)
        window['-COMSCHECKREF-'].Update(disabled=True)
        window['-COMIREF-'].Update(disabled=True)
        window['-COMSREF-'].Update(disabled=True)
        if isinstance(id['Base'],int) or isinstance(id['Base'],list):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
            if values['-CAMPO3-']:
                grafico.apagar(id['ambos_os_lados'])
                id['ambos_os_lados'] = grafico.solda_ambos_os_lados('V_CURVO')
        else:
            grafico.deletar()
        id['Base'] = grafico.v_curvo()
        base = 'V_CURVO'

    elif event == '-TOPO-':
        window['-MIM-'].Update(disabled=True)
        window['-ANG-'].Update(disabled=False, value = True)
        window['-ESP_A-'].Update(disabled=False)
        window['-ESP_B-'].Update(disabled=False)
        window['-CAMPO3-'].Update(disabled=False)
        window['-CAMPO4-'].Update(disabled=True)
        window['-CAMPO6-'].Update(disabled=False, value = False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        window['-COMICHECKREF-'].Update(disabled=True)
        window['-COMSCHECKREF-'].Update(disabled=True)
        window['-COMIREF-'].Update(disabled=True)
        window['-COMSREF-'].Update(disabled=True)
        if isinstance(id['Base'],int) or isinstance(id['Base'],list):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
            if values['-CAMPO3-']:
                grafico.apagar(id['ambos_os_lados'])
                id['ambos_os_lados'] = grafico.solda_ambos_os_lados('TOPO')
        else:
            grafico.deletar()
        id['Base'] = grafico.topo()
        base = 'TOPO'
    
    elif event == '-J-':
        window['-CAMPO3-'].Update(disabled=False)
        window['-CAMPO6-'].Update(disabled=False, value = False)
        window['-COMI-'].Update(disabled=True)
        window['-COMS-'].Update(disabled=True)
        window['-COMICHECKREF-'].Update(disabled=True)
        window['-COMSCHECKREF-'].Update(disabled=True)
        window['-COMIREF-'].Update(disabled=True)
        window['-COMSREF-'].Update(disabled=True)
        if isinstance(id['Base'],int) or isinstance(id['Base'],list):
            [grafico.apagar(id[f'Base{i}']) for i in ['','_m_i','_m_s']]
            if values['-CAMPO3-']:
                grafico.apagar(id['ambos_os_lados'])
                id['ambos_os_lados'] = grafico.solda_ambos_os_lados('J')
        else:
            grafico.deletar()
        id['Base'] = grafico.j()
        base = 'J'

    elif event == '-MISTO-':
        window['-CAMPO6-'].Update(disabled=True, value = False)
        window['-COMI-'].Update(disabled=False)
        window['-COMS-'].Update(disabled=False)
        window['-COMICHECKREF-'].Update(disabled=False)
        window['-COMSCHECKREF-'].Update(disabled=False)
        window['-COMIREF-'].Update(disabled=False)
        window['-COMSREF-'].Update(disabled=False)
        [grafico.apagar(id[i]) for i in ['Base','ambos_os_lados']]
        id['Base']= window['-GRAPH-'].draw_lines([(100,200),(280,200)],color='red')

        window['-CAMPO3-'].Update(disabled=True)
 
    elif event == '-COMI-':
        if values['-MISTO-']:
            if isinstance(id['Base'],int) or isinstance(id['Base'],list):
                grafico.apagar(id['Base_m_i'])

            base = 'MISTO_'+values['-COMI-'].upper() + '_'+ (values['-COMS-'].upper() if values['-COMS-'] != '' else 'NULL')
            grafico.deletar()
            id = grafico.solda_desenhada(id,True,base)
        else:
            pass
            
    elif event == '-COMS-':
        if values['-MISTO-']:
            if isinstance(id['Base'],int) or isinstance(id['Base'],list):
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
        if values['-CAMPO2-']:
            window['-INPUTTXTCAMPO2-'].Update(disabled=False)
        else:
            window['-INPUTTXTCAMPO2-'].Update(disabled=True)

    elif event == '-INPUTTXTCAMPO2-':
        grafico.apagar(id['Descontinuo'])
        if len(values['-INPUTTXTCAMPO2-'])>1:
            if '-' in values['-INPUTTXTCAMPO2-']:
                pass
            else:
                window['-INPUTTXTCAMPO2-'].Update(value=f"{values['-INPUTTXTCAMPO2-']}-")

        id['Descontinuo'] =  grafico.descontinuo(values['-INPUTTXTCAMPO2-'],ori=values['-ODIR-'])
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
   
 
    else:

        '''
        Mudanças das propriedades por escolha do tipo de solda
        '''
        ...
