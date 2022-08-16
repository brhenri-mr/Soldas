
class Draw_Solder:


    def __init__(self) -> None:

        from pyzwcad import ZwCAD
        
        self.zw = ZwCAD()

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
        self.__escala_atual = float(escala_nova)
    

    
    def inserir_bloco(self,tipo: str, *args):
        '''
        Insere o bloco do tipo especificado no autocad em exceção

        tipo = tipo da solda a ser inserida
        '''
        from pyzwcad.types import APoint
        from os.path import join

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

    
        #self.zw.app.Update

    def espessura(self,exp: int, *args):

        from win32com.client import Dispatch
        acad = Dispatch("ZwCAD.Application")


        #lista do handle (nomes) do ultimo documento adicionado
    
        self.__handle = list(self.zw.iter_objects('block'))[-1].handle 


        #Instancia do ultimo objeto adcionado no documento
        Entity = acad.ActiveDocument.HandleToObject(self.__handle)

        #Modificação dos atributos do bloco
        for attr in Entity.GetAttributes():
            if attr.TagString == "CORDAO":
                attr.TextString = str(exp)
                attr.Update()
    
    def apagar_bloco(self, handle):
        from win32com.client import Dispatch
        acad = Dispatch("ZwCAD.Application")
        acad.ActiveDocument.HandleToObject(handle).Delete()

            
                

