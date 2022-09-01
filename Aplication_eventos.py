
from win32com.client import getevents,Dispatch
from Aplication_Att import Visualizar_att
from pyautogui import press


class ZwCADEvents(getevents("ZwCAD.Application")):
    
    def OnBeginCommand(self, cmdName):

        print ("Beginning command " + str(cmdName) + "...")

        #fechar a aba automatica do zwcad
        if cmdName == "EATTEDIT":
            #propriedade que controla o q ta acontecendo
            self.ok = True
            press('esc')
        else:
            self.ok = False
    

ok = ZwCADEvents(Dispatch('ZwCAD.Application'))

def verificar_duplo_click():
    visual = Visualizar_att()
    try:
        if visual.verificar(r'C:\Users\breno\Desktop\Projetos\Soldas\blocos') and ok.ok:
            ok.ok = False
            return True
        return False
    except:
        return False