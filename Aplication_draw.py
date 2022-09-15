
from pyzwcad.types import APoint
from os.path import join

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

        print(ponto)
        #Inserção dos blocos
 
        block.InsertBlock(ponto,Path,self.__escala_atual,self.__escala_atual,1,0)
        
        self.__handle = block.Item(block.count-1).handle
        

    
        #self.zw.app.Update

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

    def creat_solder(self,nome):
        '''
        Cadastra uma solda que não esta no banco de dados
        nome = nome do arquivo da solda, o mesmo possui todas as especificações da solda
        nome:str
        '''
        def inserir_txt(self,tipo):

            block = self.zw.doc.ActiveLayout.Block

            #definição do local dos blocos
        
            Path = join(self.__local_dos_blocos,'.txt_'+tipo +'.dwg')
            
            #definição ponto de inserção
            
            ponto = APoint(-16.4891,-2.6215,0) if tipo == 'esquerda' else APoint(-11.7967,-6.1968,0)

            #Inserção dos blocos
    
            block.InsertBlock(ponto,Path,1,1,1,0)
            
            return block.Item(block.count-1).handle

        def base(nome_base):
            txt_base_handle = '1B8'
            txt_base_posicao = APoint(-16.489137675168433, -2.6215451766809816, 0.0)
            if 'filete' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)
                p2 = APoint(0,0,0)
                self.zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-5,0,0)
                p2 = APoint(-5,-3.25,0)
                self.zw.model.AddLine(p1,p2)

                #traço inclinado
                p1 = APoint(-5,-3.25,0)
                p2 = APoint(-1.75,0,0)
                self.zw.model.AddLine(p1,p2)

            elif 'bisel' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)
                p2 = APoint(0,0,0)
                self.zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-5,0,0)
                p2 = APoint(-5,-3,0)
                self.zw.model.AddLine(p1,p2)

                #traço inclinado
                p1 = APoint(-2,-3,0)
                p2 = APoint(-5,0,0)
                self.zw.model.AddLine(p1,p2)

            elif 'topo' in nome_base:
                #traço reto 
                p1 = APoint(-10,0,0)
                p2 = APoint(0,0,0)
                self.zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-4.0611,0,0)
                p2 = APoint(-4.0611,-3,0)
                self.zw.model.AddLine(p1,p2)

                #traço vertical
                p1 = APoint(-5.9389,-3,0)
                p2 = APoint(-5.9389,0,0)
                self.zw.model.AddLine(p1,p2)

                #Correção da texto
                Entity  = self.acad.ActiveDocument.HandleToObject(txt_base_handle)
                Entity.TextAlignmentPoint = APoint(-0.46443757968666793, -0.24396846570668096, 0.0)

            elif 'v_curvo' in nome_base:
                pass
            elif 'v' in nome_base:
                pass
            elif 'u' in nome_base:
                pass
            for obj in self.zw.iter_objects(['Line']):
                    obj.Color = 1
            return 1

        def acabamentos(self,nome_acabamento):
            #Orientação
            if 'direita' in nome_acabamento:
                ori = True
            else:
                ori = False
            #Propriedades
            if 'contorno' in nome_acabamento:
                pass
            if 'campo' in nome_acabamento:
                pass
            if 'amboslados' in nome_acabamento:
                pass
            if 'intercalado' in nome_acabamento:
                pass
            #Acabamentos 
            if 'reto' in nome_acabamento:
                pass
            elif 'convexo' in nome_acabamento:
                pass
            elif 'sem_acabamento' in  nome_acabamento:
                pass
            return 1


        acabamentos(nome)
        base(nome )


    
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
            '-BISEL_CURVO-':'Solda_biel_curvo',
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
                    else:
                        solda_block = solda_block + subs[parametro]+'_'
                    if parametro not in parametro:
                        break
        return solda_block
    
