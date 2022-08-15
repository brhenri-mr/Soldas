import threading
import os
from Aplication_eventos import verificar_duplo_click, evento_duplo_click


def inicia_programa(nome_arquivo):
    os.system('{}'.format(nome_arquivo))
    # Ex: os.system('py -3.7 x.py')




if __name__ == "__main__":

    arquivos = [r'C:\Users\breno\Desktop\Projetos\Soldas\aplication_gui_basic.py',
                r'C:\Users\breno\Desktop\Projetos\Soldas\aplication_gui_event.py']

    processos = []
    for arquivo in arquivos:
        processos.append(threading.Thread(target=inicia_programa, args=(arquivo,)))
        # Ex: adicionar o porcesso `threading.Thread(target=inicia_programa, args=('x.py',))`
    
    #for processo in processos:
        #processo.start()


    processos[0].start()
    while True:

        if verificar_duplo_click():
            evento_duplo_click()
            processos[1].start()
            processos[0]._stop

        elif processos[1].is_alive():
            pass

        elif processos[0].is_alive() and processos[1].is_alive():
            break
        else:
            if processos[0].is_alive():
                pass

            else:
                processos[0].start()


