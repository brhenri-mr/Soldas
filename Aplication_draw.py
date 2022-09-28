from pyzwcad.types import APoint
from os import replace
from os.path import join
from time import sleep

class Draw_Solder:

    def __init__(self,zw, acad):

        self.acad = acad
        self.zw = zw

        #local dos blocos
        self.__local_dos_blocos = r'C:\Users\breno\Desktop\Projetos\Soldas\blocos'
        #Número padrão para o calculo da escala automatica
        self.__escala_padrao = 41.681469640756404
        #Escala automatica
        self.__escala_atual = (self.zw.doc.ActiveViewport.Height)/self.__escala_padrao
        #handle
        self.__handle = ''
    
    @property
    def local_dos_blocos(self):
        return self.__local_dos_blocos

    @property
    def escalas_padrao(self):
        return self.__escala_padrao

    @property
    def escala_atual(self):
        return self.__escala_atual

    @property
    def handle(self):
        return self.__handle

    @local_dos_blocos.setter
    def local_dos_blocos(self, novo_local):
        self.__local_dos_blocos = novo_local
        
    @escala_atual.setter
    def escala_atual(self,escala_nova):
        if isinstance(escala_nova,float):
             self.__escala_atual = escala_nova
        else:
            self.__escala_atual = float(escala_nova if ',' not in escala_nova else escala_nova.replace(',','.'))
    
    def inserir_bloco(self,tipo, *args):
        '''
        Insere o bloco do tipo especificado no autocad em exceção

        tipo = tipo da solda a ser inserida
        '''

        #Objeto block
        block = self.zw.doc.ActiveLayout.Block

        #definição do local dos blocos
        Path = join(self.__local_dos_blocos,tipo +'.dwg')
        
        #definição ponto de inserção
        ponto = self.zw.doc.Utility.GetPoint() if args[0] =='N_att' else args[0]
        ponto = APoint(ponto[0],ponto[1])

        #Inserção dos blocos
        block.InsertBlock(ponto,Path,self.__escala_atual,self.__escala_atual,1,0)
        
        self.__handle = block.Item(block.count-1).handle
        
    def descontinua(self,passo: int or list):
        '''
        Permite insere o passo passado pelo usuário a solda. Retorna a escrita no desenho 

        passo = infoirmacao dada pelo usuário para colocar no desenho
        '''
        Entity = self.acad.ActiveDocument.HandleToObject(self.__handle)
        passo = f'({passo})'
        
        for attr in Entity.GetAttributes():
            if '(' in attr.TagString or '-' in attr.TagString or 'PASSO' == attr.TagString:
                attr.TextString = str(passo)
                attr.Update()


    def espessura(self,exp: dict, *args):
        '''
        Insere o valor da solda no bloco desenhado no zwcad
        exp = dicionario com os valores de cada entrada do usuario que corresponde
        ao valor da solda
        exp: dict
        '''
        #Dados 
        i = -1
        j = -1

        #Instancia do ultimo objeto adcionado no documento
        Entity = self.acad.ActiveDocument.HandleToObject(args[0] if len(args) != 0 else self.__handle)

        #tratamento do exp
        #Modificação dos atributos do bloco
        for attr in Entity.GetAttributes():
            if attr.TagString in ["CORDAO","REF"]:
                if attr.TagString == 'REF':
                    j +=1
                    input = str(exp[attr.TagString])
                else:
                    i +=1
                    input = str(exp[attr.TagString][i])
                attr.TextString = input
                attr.Update()

    
    def apagar_bloco(self, handle):

        self.acad.ActiveDocument.HandleToObject(handle).Delete()

    def creat_solder(self,nome,unidade):
        '''
        Cadastra uma solda que não esta no banco de dados
        nome = nome do arquivo da solda, o mesmo possui todas as especificações da solda
        nome:str
        unidade = unidade escolhida pelo usuario: milimetros ou angulo. Usado para bisel
        unidade: Bool
        '''

        def inicializacao(zw):
            '''
            Inicializa o arquivo do template onde será escrita a solda 
            '''
            nome_arq = '.Template.dwg'

            local_path = join(self.__local_dos_blocos,'Interno',nome_arq)

            while zw.doc.Name != nome_arq:
                zw.doc.Open(local_path)
                sleep(1)

        def manipulat_txt_cad(zw,nome,unidade,acad=self.acad):
            '''
            Manipula o attribute txt do arquivo template original, o colocando no lugar
            e escolhendo a solda com a justificy mais adequada. Não abarca a manipualcao
            do texto especifico pasa reforco

            nome = string do nome da solda
            nome:str
            unidade = Valor boolenano que indica qual unidade será usada no desenho. Por
            padrão adota-se True para milimetros
            unidade:bool
            '''

            def criterio_de_desenho(nome,unidade):

                nomes = []
                saida_nomes = []
                ori_S = []
                subs = {
                    'filete':'esquerda',
                    'v_curvo':'meio',
                    '_v_':'meio',
                    'bisel':'meio',
                    'bisel_curvo':'',
                    'topo':'meio',
                    'descontinua':'descontinua',
                    'Reforco':'Reforco'
                }

                #criacao do vec nomes
                if '%' in nome:
                    pos_misto  = nome.index('%')
                    nomes.append(nome[:pos_misto])
                    if '#' in nome[pos_misto:]:
                        #dados aulixares
                        pos_ref = nome.index('#')
                        ref_sup = nome[:pos_ref]
                        ref_inf = nome[pos_misto:]
                        #criacao vec orientacao reforco
                        ori_S.append('Reforco' in ref_sup)
                        ori_S.append('Reforco' in ref_inf)
                        #criacao vec nomes 
                        nomes.append(ref_sup)
                        nomes.append(nome[pos_ref:])
                    else:
                        nomes.append(nome[pos_misto:])
                else:
                    nomes.append(nome)
                for key in subs.keys():
                    for n in nomes:
                        if key in n:
                            if key not in ['Reforco','descontinua']:
                                for _ in range(2 if 'amboslados' in n else 1):
                                    if key =='bisel' and unidade:
                                        saida_nomes.append('esquerda')
                                    saida_nomes.append(subs[key])
                            else:
                                saida_nomes.append(subs[key])
                return saida_nomes, 'direita' in nome,ori_S

            #Dados base
            refoco_incremento = 0
            usado = []
            obj_existe_handle = {
                '39F':[],
                '370':[],
                '1B8':[],
                '3A1':[]
                }

            criterio,ori,ori_S = criterio_de_desenho(nome,unidade)

            #Posição do txt
            for cri in criterio:
                #condicao de amboslados
                if cri in usado:
                    amboslados = -1
                    incremento = -1.8
                else:
                    amboslados = 1
                    incremento = 0
                #condicao de reforco
                if len(ori_S)>0:
                    if refoco_incremento != 0: #significa que ja foi usada uma direcao
                        refoco_incremento= 1 if refoco_incremento == -0.8 else -0.8
                    else:
                        if ori_S[1]:
                            refoco_incremento = -0.8
                        elif ori_S[0]:
                            refoco_incremento = 1
                else:
                    refoco_incremento = 1
                #construcao dos pontos
                if 'meio' == cri:
                    if ori:
                         obj_existe_handle['370'].append(APoint(-0.2714,-6.1968*amboslados+incremento))
                    else:
                        obj_existe_handle['370'].append(APoint(-10.2714,-6.1968*amboslados+incremento))

                elif  'descontinua' == cri:
                    if ori:
                        obj_existe_handle['39F'].append(APoint(22.7385,0.8891,0))
                    else:
                        obj_existe_handle['39F'].append(APoint(-23.1849,0.8891,0))
                elif 'Reforco' == cri:
                    if ori:
                        obj_existe_handle['3A1'].append(APoint(5.8661,-7.4663*refoco_incremento,0))
                    else:
                        obj_existe_handle['3A1'].append(APoint(-10.6035,-10.1243*refoco_incremento,0))
                else:
                    if ori: #direita
                        obj_existe_handle['1B8'].append(APoint(-7.0816,-2.6215*amboslados+incremento))
                    else: #esquerda
                        obj_existe_handle['1B8'].append(APoint(-16.4891,-2.6215*amboslados+incremento))
                usado.append(cri)
            print(criterio)
            sleep(0.4)
            #movimentacao dos textos
            for obj in zw.iter_objects(['AcDbAttributeDefinition']):
                if obj.handle in obj_existe_handle.keys():
                    for ponto in obj_existe_handle[obj.handle]:
                        obj_par_manipulacao = obj.Copy()
                        while True:
                            obj_par_manipulacao.Move(APoint(obj_par_manipulacao.InsertionPoint),ponto)
                            sleep(0.4)
                            if obj.InsertionPoint != obj_par_manipulacao.InsertionPoint: 
                                print('sucesso')
                                break
                            else: 
                                print('erro ao mover')
                                pass
            #[acad.ActiveDocument.HandleToObject(j).Delete() for j in obj_par_manipulacao.keys()]
            
        def base(zw,nome_base):
            '''
            Desenha a solda base
            nome_base = nome da solda
            nome_base:str
            '''

            if 'direita' in nome_base:
                i = 1
            else:
                i = -1

            if 'amboslados' in nome_base or '%' in nome_base:
                vezes = [1,-1]
                if '%' in nome_base:
                    pos_barra = nome_base.index('%')
                    nome_base_parte_2 =nome_base[pos_barra+1:] 
                    nome_base = nome_base[:pos_barra+1]
            else:
                vezes = [1]

            for vez in vezes:
                if 'filete' in nome_base:
                    #traço reto 
                    p1 = APoint(-10,0,0)*i
                    p2 = APoint(0,0,0)
                    zw.model.AddLine(p1,p2)

                    #traço vertical
                    p1 = APoint(-5,0,0)*i
                    p2 = APoint(-5*i,-3.25*vez,0)
                    zw.model.AddLine(p1,p2)

                    #traço inclinado
                    p1 = APoint(-5*i,-3.25*vez,0)
                    p2 = APoint(-1.75*i,0,0)
                    zw.model.AddLine(p1,p2)

                    #Alterar nome_base (caso seja o misto)
                    if '%' in nome_base:
                        nome_base = nome_base_parte_2
                
                elif 'bisel_curvo' in nome_base:
                    #traço reto 
                    p1 = APoint(-10,0,0)*i
                    p2 = APoint(0,0,0)
                    zw.model.AddLine(p1,p2)

                    #traço vertical
                    p1 = APoint(-5,0,0)*i
                    p2 = APoint(-5*i,-3.25,0)
                    zw.model.AddLine(p1,p2)

                    #arco
                    c = APoint(-1.7500000000000036, -1.7694179454963432e-16, 0.0)
                    r = 3.0
                    end = 4.71238898038469
                    start = 3.141592653589793
                    zw.model.AddArc(c,r,start,end)

                    #Alterar nome_base (caso seja o misto)
                    if '%' in nome_base:
                        nome_base = nome_base_parte_2

                elif 'bisel' in nome_base:
                    #traço reto 
                    p1 = APoint(-10,0,0)*i
                    p2 = APoint(0,0,0)
                    zw.model.AddLine(p1,p2)

                    #traço vertical
                    p1 = APoint(-5,0,0)*i
                    p2 = APoint(-5*i,-3*vez,0)
                    zw.model.AddLine(p1,p2)

                    #traço inclinado
                    p1 = APoint(-2*i,-3*vez,0)
                    p2 = APoint(-5,0,0)*i
                    zw.model.AddLine(p1,p2)

                    #Alterar nome_base (caso seja o misto)
                    if '%' in nome_base:
                        nome_base = nome_base_parte_2

                elif 'topo' in nome_base:
                    #traço reto 
                    p1 = APoint(-10,0,0)*i
                    p2 = APoint(0,0,0)
                    zw.model.AddLine(p1,p2)

                    #traço vertical
                    p1 = APoint(-4.0611,0,0)*i
                    p2 = APoint(-4.0611*i,-3*vez,0)
                    zw.model.AddLine(p1,p2)

                    #traço vertical
                    p1 = APoint(-5.9389*i,-3*vez,0)
                    p2 = APoint(-5.9389*i,0,0)
                    zw.model.AddLine(p1,p2)


                    #Alterar nome_base (caso seja o misto)
                    if '%' in nome_base:
                        nome_base = nome_base_parte_2

                elif 'v_curvo' in nome_base:
                    #traço reto 
                    p1 = APoint(-10,0,0)*i
                    p2 = APoint(0,0,0)
                    zw.model.AddLine(p1,p2)

                    #arco
                    p1 = APoint(-7.5577,-0.442,0)*i #centro
                    zw.model.AddArc(p1,2.5956400303711344,4.675345394956241,0.1711208686509456)

                    #arco
                    p1 = APoint(-1.8456,-0.442,0)*i #centro
                    zw.model.AddArc(p1,2.5956400303711344,2.9704717849388476,4.749432565813137)

                    #Alterar nome_base (caso seja o misto)
                    if '%' in nome_base:
                        nome_base = nome_base_parte_2

                elif 'v' in nome_base:
                    #traço reto 
                    p1 = APoint(-10,0,0)*i
                    p2 = APoint(0,0,0)*i
                    zw.model.AddLine(p1,p2)

                    #traço inclinado
                    p1 = APoint(-5,0,0)*i
                    p2 = APoint(-6.7485*i,-3*vez,0)
                    zw.model.AddLine(p1,p2)

                    #traço inclinado
                    p1 = APoint(-3.2471*i,-3*vez,0)
                    p2 = APoint(-5,0,0)*i
                    zw.model.AddLine(p1,p2)

                    #Alterar nome_base (caso seja o misto)
                    if '%' in nome_base:
                        nome_base = nome_base_parte_2

                elif 'u' in nome_base:
                    pass
               
                #Acabamentos 
                if 'reto' in nome_base:
                    #linha reta
                    p1 = APoint((-5+1.5)*i,-3.27*vez,0)
                    p2 = APoint((-5-1.5)*i,-3.27*vez,0)
                    zw.model.AddLine(p1,p2)

                elif 'convexo' in nome_base:
                    c = APoint(-4.977110378108507, -0.11062264899499308, 0.0)
                    r = 3.5526110509915334
                    end = 5.242397665338469
                    start = 4.18238029543091
                    zw.model.AddArc(c,r,start,end)
                    
                elif 'sem_acabamento' in nome_base:
                    pass

        def acabamentos(zw,nome_acabamento):
            '''
            Desenha os acabamentos da solda
            nome_acabamento = String do nome da solda
            nome_acabamento:str
            '''
            #Orientação
            if 'direita' in nome_acabamento:
                ori = True
                i = 1
            else:
                ori = False
                i = -1
            #Propriedades
            if 'contorno' in nome_acabamento:

                p1 = APoint(0,0,0)
                zw.model.AddCircle(p1,0.5517)

                for obj in zw.iter_objects(['Circle']):
                    obj.Color = 1
                
            if 'campo' in nome_acabamento:
                block = zw.doc.ActiveLayout.Block

                #definição do local dos blocos
                Path = join(self.__local_dos_blocos,'Interno\Solda_0_(obra)_direita.dwg' if ori else 'Interno\Solda_0_(obra)_esquerda.dwg')
                
                #definição ponto de inserção
                ponto = APoint(0,0,0)

                #Inserção dos blocos
                block.InsertBlock(ponto,Path,0.6,0.6,1,0)
            
            if 'descontinua' in nome_acabamento:
                #traço reto 
                p1 = APoint(-10,0,0)*i
                p2 = APoint(-24.2425,0,0)*i
                zw.model.AddLine(p1,p2)

                
            if 'tipico' in nome_acabamento:
                block = zw.doc.ActiveLayout.Block

                #definição do local dos blocos
                Path = join(self.__local_dos_blocos,'Interno\Tipico_direita.dwg' if ori else 'Interno\Tipico_esquerda.dwg')

                #definição ponto de inserção
                if 'descontinua' in nome_acabamento:
                    ponto = APoint(-14.2425-10 if ori else 10+14.2425,0,0)
                else:
                    ponto = APoint(-10*i,0,0)

                #Inserção dos blocos
                block.InsertBlock(ponto,Path,0.1,0.1,0.1,0)
            
            if 'Reforco' in nome_acabamento:

                if '#' in nome_acabamento:
                    vec = [1,-1]
                else:
                    if '%' in nome_acabamento or 'superior' in nome_acabamento:
                        vec = [-1]
                    else:
                        vec = [1]

                for j in vec:
                    #traço reto 
                    p1 = APoint(-5*i,0,0)
                    p2 = APoint(-5*i,-10.8139*j,0)
                    zw.model.AddLine(p1,p2)

                    #traço inclinado 
                    p1 = APoint(-5*i,-10.8139*j,0)
                    p2 = APoint(-1.75*i,-7.5572*j,0)
                    zw.model.AddLine(p1,p2)

                    #traço horizontal
                    p1 = APoint(-5*i,-7.5572*j,0)
                    p2 = APoint(-1.75*i,-7.5572*j,0)
                    zw.model.AddLine(p1,p2)

            else:
                self.acad.ActiveDocument.HandleToObject('3A1').Delete()


            for obj in zw.iter_objects(['Line','Arc']):
                    obj.Color = 1

            return 1

        def finalizacao(zw, nome):
            '''
            Finaliza a operação de criação da solda,isto é, sava o arquivo como outro nome
            nome = nome que a solda ira receber em seu arquivo
            nome:str
            '''
            zw.doc.SaveAs(nome+'.dwg')
            path = zw.doc.Path
            zw.doc.Close()
            if path != self.__local_dos_blocos:
                replace(join(path,nome+'.dwg'),join(self.__local_dos_blocos,nome+'.dwg'))

            return 0


        inicializacao(self.zw)
        base(self.zw,nome)
        acabamentos(self.zw,nome)
        manipulat_txt_cad(self.zw,nome,unidade)
        finalizacao(self.zw,nome)

class Solder():

    def __init__(self) -> None:
        pass

    def tipo(self,v) -> str:
        '''
        Faz a codificação do nome da solda pelo tipo de dados inserido pelo usuário.Retorna
        uma str com o nome da solda
        values = dicionario dos valores inseridos no gui
        valeus: dict
        '''
        #dados
        base = ['-FILETE-','-TOPO-','-V-','-V_CURVO-','-BISEL-','-BISEL_CURVO-','-J-','-COMI-','-COMS-']
        ori = ['-OESQ-','-ODIR-']
        prop = ['-CAMPO5-','-CAMPO1-','-CAMPO3-','-CAMPO4-','-CAMPO6-','-COMICHECKREF-','-COMSCHECKREF-','-CAMPO7-','-CAMPO2-']
        acabamento = ['-IRETO-','-ICONV-','-ISA-']

        subs = {
            '-FILETE-':'Solda_filete',
            '-TOPO-':'Solda_topo',
            '-V-':'Solda_v',
            '-V_CURVO-':'Solda_v_curvo',
            '-BISEL-':'Solda_bisel',
            '-BISEL_CURVO-':'Solda_bisel_curvo',
            '-J-':'Solda_j',
            '-COMI-':f"Solda_{v['-COMI-'].lower()}%",
            '-COMS-':f"{v['-COMS-'].lower()}",
            '-OESQ-':'esquerda',
            '-ODIR-':'direita',
            '-CAMPO1-':'campo',
            '-CAMPO3-':'amboslados',
            '-CAMPO4-':'inter',
            '-CAMPO5-':'contorno',
            '-CAMPO6-':'Reforco',
            '-COMSCHECKREF-':'Reforco#',
            '-COMICHECKREF-':'Reforco',
            '-CAMPO7-':'tipico',
            '-CAMPO2-':'descontinua',
            '-IRETO-':'reto',
            '-ICONV-':'convexo',
            '-ISA-':''
        }

        #incremento
        solda_block = ''

        for dado in [base,ori,prop,acabamento]:
            for parametro in dado:
                if v[parametro]:
                    if parametro in acabamento and 'filete' in solda_block:
                        break
                    elif parametro == '-ISA-':
                        pass
                    else:
                        solda_block = solda_block + subs[parametro]+('_' if parametro not in ['-COMI-','-COMICHECKREF-'] else '')
                    if parametro not in parametro:
                        break
        return solda_block
    
    def solda_desenhada(self,nome)->dict:

        '''
        Desenha a solda do autocad no programa.Retorna um id contendo valores boleanos para 
        cada caracteristica da solda. Essa informacao é usada para pre-configurar a janela 
        do duplo click.Exemplo: se for filete, no id tera um filete True

        nome = Nome da solda gerada pelo programa
        nome:str
        '''
        nomes = []
        id = {
            'filete':False,
            'Misto':False,
            'contorno':False,
            'amboslados':False,
            'campo':False,
            'direita':False,
            'esquerda':False,
            'bisel':False,
            'reto':False,
            'convexo':False,
            'inter':False,
            'topo':False,
            'tipico':False,
            'Reforco':False,
            'Reforco#':False,
            'descontinua':False
            }

        if '%' in nome or '#' in nome:
            id['Misto'] =True

        for key in id.keys():
  
            if key in nome:
                if '#' in nome:
                    pos  = nome.index('#')
                    nomes.append(nome[:pos])
                    if '%' in nome:
                        pos_base = nome.index('%')
                        nomes.append(nome[pos_base:])
                        nomes.append(nome[:pos_base])
                    else:
                        nomes.append(nome[pos:])
                    for parte in nomes:
                        if 'Reforco#' in parte:
                                id['Reforco#'] =True
                        elif key in parte:
                            if id[key]:
                                id['amboslados'] = True
                            else:
                                id[key] = True
                else:
                    id[key] =True
        return id
