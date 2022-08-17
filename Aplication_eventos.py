
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
    

ok = ZwCADEvents(win32com.client.Dispatch('ZwCAD.Application'))


def evento_duplo_click():
    from pyautogui import press
    visual = Visualizar_att()
    while True:
        try:
            if visual.verificar(r'C:\Users\breno\Desktop\Projetos\Soldas\blocos') and ok.ok:
                handle, ponto, escala, name = visual.bloco_selecionado()
                ponto_um,ponto_dois = ponto[0],ponto[1]
                with open("log.txt",'w') as arquivo:
                    arquivo.write(f"{handle},{ponto_um},{ponto_dois},{escala},{name}")
                print('\033[92mBloco obtido com sucesso!!!\033[92m')
                press('esc')
                press('esc')
    
                break
        except:
            pass

def verificar_duplo_click():

    visual = Visualizar_att()
    try:
        return visual.verificar(r'C:\Users\breno\Desktop\Projetos\Soldas\blocos') and ok.ok 
    except:
        pass

evento_duplo_click()