
from cx_Freeze import Executable


class Draw_Solder:


    def __init__(self) -> None:

        from pyzwcad import ZwCAD
        from pyzwcad.types import APoint
        import win32com.client
        
        self.zw = ZwCAD()
        self.local_dos_blocos = r'C:\Users\breno\Desktop\Projetos\Soldas\blocos'

        #ainda vou pensar como vou fazer isso
    
    
    def inserir_bloco(self,tipo: str, *args) -> Executable:
        '''
        Insere o bloco do tipo especificado no autocad em exceção

        tipo = tipo da solda a ser inserida
        '''
        from pyzwcad.types import APoint
        import os

        #Objeto block
        block = self.zw.doc.ActiveLayout.Block

        #definição do local dos blocos
    
        Path = os.path.join(self.local_dos_blocos,tipo +'.dwg')
        
        #definição ponto de inserção
        print(args[0])
        ponto = self.zw.doc.Utility.GetPoint() if args[0] =='N_att' else args[0]

        #Inserção dos blocos
        block.InsertBlock(APoint(ponto),Path,1,1,1,0)
        #self.zw.app.Update

    def espessura(self,exp: int, *args) -> Executable:

        import win32com.client
        acad = win32com.client.Dispatch("ZwCAD.Application")

        #lista do handle (nomes) do ultimo documento adicionado
    
        elemento_add_handle = list(self.zw.iter_objects('block'))[-1].handle 

        #Instancia do ultimo objeto adcionado no documento
        Entity = acad.ActiveDocument.HandleToObject(elemento_add_handle)

        #Modificação dos atributos do bloco
        for attr in Entity.GetAttributes():
            if attr.TagString == "CORDAO":
                attr.TextString = str(exp)
                attr.Update()
        
            
                

