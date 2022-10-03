
from win32com.client import getevents, Dispatch
from Aplication_Att import Visualizar_att
from pyautogui import press
import pythoncom
from time import sleep

'''
Do nada para de funcionar sem o menor motivo, e quando escreve mais linhas
como alternativas para o funcionamento da funciona e se retorna ao padrão originalmente
problemático, o erro e solucinado.
Verificar isso aqui
'''

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
    

ok =    ZwCADEvents()
'''
ok = ZwCADEvents(Dispatch('ZwCAD.Application'))

def verificar_duplo_click():
    visual = Visualizar_att()
    try:
        if visual.verificar() and ok.ok:
            ok.ok = False
            return True
        return False
    except:
        return False
'''
while True:
    pythoncom.PumpWaitingMessages()
    sleep(0.1)
