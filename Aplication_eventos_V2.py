import win32com
from Aplication_Att import Visualizar_att
from pyautogui import press
from pythoncom import PumpWaitingMessages

'''
Do nada para de funcionar sem o menor motivo, e quando escreve mais linhas
como alternativas para o funcionamento da funciona e se retorna ao padrão originalmente
problemático, o erro e solucinado.
Verificar isso aqui
'''
ok = False
class ZwCADEvents:
    
    def OnBeginCommand(self, cmdName):

        print ("Beginning command " + str(cmdName) + "...")
        global ok
        #fechar a aba automatica do zwcad
        if cmdName == "EATTEDIT":
            #propriedade que controla o q ta acontecendo
            ok = True
            press('esc')
        else:
            ok = False
    
class session_event_class:
    def BeginClose(self):
        print ('catched')


def verificar_duplo_click():
    global ok
    visual = Visualizar_att()
    if visual.verificar() and ok:
        ok = False
        return True
    return False

acad = win32com.client.DispatchWithEvents('ZwCAD.Application',ZwCADEvents)
active_session = acad.ActiveDocument
active_session_events =  win32com.client.WithEvents(active_session,session_event_class)
