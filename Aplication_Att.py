"""
Preve perceber se o úsuario pretende atualizar algum bloco
"""

class Visualizar_att():

    def __init__(self) -> None:
        from pyzwcad import ZwCAD

        self.zw = ZwCAD()

    def verificar(self,local_blocos):
        import os
        from pyzwcad import ZwCAD

        #Lista de blocos que pertecem ao programa
        blocos_possiveis = os.listdir(local_blocos)
        #Verificando a necessidade de atualização
        for entity in self.zw.doc.PickfirstSelectionSet:
            if (entity.Name+'.dwg') in blocos_possiveis:
                return True
        return False

    def bloco_selecionado(self):
        '''
        Devolve as propriedades de um objeto que sera deletado
        para que o programa possa fazer a devida atualização
        '''
        #so esta se selecionando uma
        for entity in self.zw.doc.PickfirstSelectionSet:
            return entity.Handle, entity.InsertionPoint

    def deletar(self, handle: str):

        import win32com.client
        app = win32com.client.Dispatch("ZwCAD.Application")
        Entity = app.ActiveDocument.HandleToObject(handle)
        print(Entity.Erase())



            
                



        
        


