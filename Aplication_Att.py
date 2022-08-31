"""
Preve perceber se o úsuario pretende atualizar algum bloco
"""
import os
from pyzwcad import ZwCAD
import win32com.client
from pyautogui import press
from datetime import datetime

class Visualizar_att():

    def __init__(self) -> None:

        self.zw = ZwCAD()

    def verificar(self,local_blocos,*args):


        #Lista de blocos que pertecem ao programa
        blocos_possiveis = os.listdir(local_blocos)
        #Verificando a necessidade de atualização
        for t in range(1):
            for entity in args[0] if len(args)>0 else self.zw.doc.PickfirstSelectionSet:
                if (entity.Name+'.dwg') in blocos_possiveis:
                    return True
        return False

    def bloco_selecionado(self,*args):
        '''
        Devolve as propriedades de um objeto que sera deletado
        para que o programa possa fazer a devida atualização
        '''
        #so esta se selecionando uma
        for entity in args[0] if len(args)>0 else self.zw.doc.PickfirstSelectionSet:
            return entity.Handle, entity.InsertionPoint, entity.XScaleFactor, entity.Name

    def deletar(self, handle: str):

        app = win32com.client.Dispatch("ZwCAD.Application")
        Entity = app.ActiveDocument.HandleToObject(handle)
        print(Entity.Erase())

    def evento_duplo_click(self):

        objeto = self.zw.doc.PickfirstSelectionSet
        v  = self.verificar(r'C:\Users\breno\Desktop\Projetos\Soldas\blocos', objeto)
        print(v)
        if v:
            handle, ponto, escala, name = self.bloco_selecionado(objeto)
            ponto_um,ponto_dois = ponto[0],ponto[1]
            with open("log.txt",'a') as arquivo:

                arquivo.write(f"{handle},{ponto_um},{ponto_dois},{escala},{name},{datetime.now().strftime('%m/%d/%Y %H:%M:%S:%f')}"+'\n')

            print('\033[92mBloco obtido com sucesso!!!\033[92m')
            press('esc')
            press('esc')
    


