
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
        print(args[0])

        ponto = self.zw.doc.Utility.GetPoint() if args[0] =='N_att' else args[0]
        ponto = APoint(ponto[0],ponto[1])

        #Inserção dos blocos
        block.InsertBlock(ponto,Path,self.__escala_atual,self.__escala_atual,1,0)
        
        self.__handle = block.Item(block.count-1).handle
        

    def espessura(self,exp: int or list, *args):
        
        i = 0
        s = []

        #Instancia do ultimo objeto adcionado no documento
        Entity = self.acad.ActiveDocument.HandleToObject(args[0] if len(args) != 0 else self.__handle)
        print(exp)
        #tratamento do exp
        for elemento in exp:
            if elemento == '':
                pass
            else:
                s.append(elemento)
        
        print(s)
        #Modificação dos atributos do bloco
        for attr in Entity.GetAttributes():
            if attr.TagString in ["CORDAO","REF"]:
                print(attr.TagString)
                if len(s)>1:
                    input = s[i]
                elif len(s) == 0:
                    input = 0 
                else:
                    input = s[0]
                attr.TextString = str(input)
                attr.Update()
                i +=1
    
    def apagar_bloco(self, handle):

        self.acad.ActiveDocument.HandleToObject(handle).Delete()

    def creat_solder(self,nome,unidade):
        '''
        Cadastra uma solda que não esta no banco de dados
        nome = nome do arquivo da solda, o mesmo possui todas as especificações da solda
        nome:str
        '''

        def inicializacao(zw):
            '''
            Inicializa o arquivo do template onde será escrita a solda 
            '''
            nome_arq = '.Template.dwg'

            local_path = join(self.__local_dos_blocos,'Interno',nome_arq)
            print(local_path)

            while zw.doc.Name != nome_arq:
                zw.doc.Open(local_path)
                sleep(1)

        def manipulat_txt_cad(zw,criterio,ori,acad = self.acad):
            '''
            Manipula o attribute txt do arquivo template original, o colocando no lugar
            e escolhendo a solda com a justificy mais adequada
            criterio = criterio para esclja da justificy
            criterio:str
            ori = orientação do desenho
            '''
            
            apagar = []

            #Dados base
            if criterio == 'meio':
                txt_base_handle = '370'
                if ori == 1:
                    text_base_posi = APoint(-10.2714,-6.1968)
                else:
                    text_base_posi = APoint(3.3301,-6.1968)
            elif criterio == 'delete':
                txt_base_handle = ''
            else:
                txt_base_handle = '1B8'
                if ori == 1: #direita
                    text_base_posi = APoint(-16.4891,-2.6215)
                else: #esquerda
                    text_base_posi = APoint(-7.0816,-2.6215)
                


            for obj in zw.iter_objects(['AcDbAttributeDefinition']):
                if obj.handle == txt_base_handle:
                    antigo = obj.InsertionPoint
                    while True:
                        #Tenta mover o bloco, as vezes nao vai de primeira, por isso o While
                        obj.Move(APoint(obj.InsertionPoint),text_base_posi)
                        print(type(antigo))
                        print(obj.InsertionPoint)
                        if antigo[0] == obj.InsertionPoint[0]:
                            pass
                        else:
                            break
                else:
                    apagar.append(obj.handle)
            [acad.ActiveDocument.HandleToObject(j).Delete() for j in apagar]

        def base(zw,nome_base,unidade):
            '''
            Desenha a solda base
            nome_base = nome da solda
            nome_base:str
            unidade = ang ou milimetro, por padrão True é milimetro
            unidade:Bool
            '''

            if 'direita' in nome_base:
                i = 1
            else:
                i = -1
            print(f'i={i}',nome_base)
            if 'filete' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)*i
                p2 = APoint(0,0,0)
                zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-5,0,0)*i
                p2 = APoint(-5,-3.25,0)*i
                zw.model.AddLine(p1,p2)

                #traço inclinado
                p1 = APoint(-5,-3.25,0)*i
                p2 = APoint(-1.75,0,0)*i
                zw.model.AddLine(p1,p2)
                #txt
                manipulat_txt_cad(zw,'esquerda',i)
            
            elif 'bisel_curvo' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)*i
                p2 = APoint(0,0,0)
                zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-5,0,0)*i
                p2 = APoint(-5,-3.25,0)*i
                zw.model.AddLine(p1,p2)

                #arco
                c = APoint(-1.7500000000000036, -1.7694179454963432e-16, 0.0)
                r = 3.0
                end = 4.71238898038469
                start = 3.141592653589793
                zw.model.AddArc(c,r,start,end)

                #text
                manipulat_txt_cad(zw,'delete',i)

            elif 'bisel' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)*i
                p2 = APoint(0,0,0)
                zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-5,0,0)*i
                p2 = APoint(-5,-3,0)*i
                zw.model.AddLine(p1,p2)

                #traço inclinado
                p1 = APoint(-2,-3,0)*i
                p2 = APoint(-5,0,0)*i
                zw.model.AddLine(p1,p2)

                #texto
                if unidade:
                    manipulat_txt_cad(zw,'esquerda',i)

                manipulat_txt_cad(zw,'meio',i)


            elif 'topo' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)*i
                p2 = APoint(0,0,0)
                zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-4.0611,0,0)*i
                p2 = APoint(-4.0611*i,-3,0)
                zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-5.9389*i,-3,0)
                p2 = APoint(-5.9389*i,0,0)
                zw.model.AddLine(p1,p2)

                #Correção da texto
                #texto
                manipulat_txt_cad(zw,'meio',i)

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

                #texto
                manipulat_txt_cad(zw,'meio',i)

            elif 'v' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)*i
                p2 = APoint(0,0,0)*i
                zw.model.AddLine(p1,p2)

                #traço inclinado
                p1 = APoint(-5,0,0)*i
                p2 = APoint(-6.7485,-3,0)*i
                zw.model.AddLine(p1,p2)

                #traço inclinado
                p1 = APoint(-3.2471,-3,0)*i
                p2 = APoint(-5,0,0)*-i
                zw.model.AddLine(p1,p2)

                #texto
                manipulat_txt_cad(zw,'meio',i)

            elif 'u' in nome_base:
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
        
            if 'amboslados' in nome_acabamento:
                pass
            if 'intercalado' in nome_acabamento:
                pass
            #Acabamentos 
            if 'reto' in nome_acabamento:
                #linha reta
                p1 = APoint((-5+1.5)*i,-3.27,0)
                p2 = APoint((-5-1.5)*i,-3.27,0)
                zw.model.AddLine(p1,p2)

            elif 'convexo' in nome_acabamento:
                c = APoint(-4.977110378108507, -0.11062264899499308, 0.0)
                r = 3.5526110509915334
                end = 5.242397665338469
                start = 4.18238029543091
                zw.model.AddArc(c,r,start,end)
                
            elif 'sem_acabamento' in  nome_acabamento:
                pass

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
        base(self.zw,nome,unidade)
        acabamentos(self.zw,nome)
        finalizacao(self.zw,nome)

class Solder():

    def __init__(self) -> None:
        pass

    def tipo(self,v):
        '''
        Faz a codificação do nome da solda pelo tipo de dados inserido pelo usuário
        values = dicionario dos valores inseridos no gui
        valeus: dict
        '''
        #dados
        base = ['-FILETE-','-TOPO-','-V-','-V_CURVO-','-BISEL-','-BISEL_CURVO-','-J-']
        ori = ['-OESQ-','-ODIR-']
        prop = ['-CAMPO5-','-CAMPO1-','-CAMPO3-','-CAMPO4-','-CAMPO6-','-CAMPO7-','-CAMPO2-']
        acabamento = ['-IRETO-','-ICONV-','-ISA-']

        subs = {
            '-FILETE-':'Solda_filete',
            '-TOPO-':'Solda_topo',
            '-V-':'Solda_v',
            '-V_CURVO-':'Solda_v_curvo',
            '-BISEL-':'Solda_bisel',
            '-BISEL_CURVO-':'Solda_bisel_curvo',
            '-J-':'Solda_j',
            '-OESQ-':'esquerda',
            '-ODIR-':'direita',
            '-CAMPO1-':'campo',
            '-CAMPO3-':'amboslados',
            '-CAMPO4-':'inter',
            '-CAMPO5-':'contorno',
            '-CAMPO6-':'Reforco',
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
                        solda_block = solda_block + subs[parametro]+'_'
                    if parametro not in parametro:
                        break
        return solda_block
    
