
import win32com.client
from Aplication_Att import Visualizar_att

class ZwCADEvents(win32com.client.getevents("ZwCAD.Application")):

    def OnBeginCommand(self, cmdName):
        from pyautogui import press

        print ("Beginning command " + str(cmdName) + "...")

        #fechar a aba automatica do zwcad
        if cmdName == "EATTEDIT":
            #propriedade que controla o q ta acontecendo
            self.ok = True
            press('esc')
        else:
            self.ok = False
    

ok = ZwCADEvents(win32com.client.Dispatch('ZwCAD.Application'))

def verificar_duplo_click():

    visual = Visualizar_att()
    try:
        condicao = visual.verificar(r'C:\Users\breno\Desktop\Projetos\Soldas\blocos') and ok.ok
        if condicao:
            ok.ok = False
            return True
        return False
    except:
        return False