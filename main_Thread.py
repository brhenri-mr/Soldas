
from threading import Thread
from subprocess import call
from sys import executable
from Aplication_Att import Visualizar_att
from Aplication_eventos import verificar_duplo_click

def inicia_programa(nome_arquivo):
    call([executable, f'{nome_arquivo}'])
    # Ex: os.system('py -3.7 x.py')

p = Visualizar_att()
d= False

if __name__ == "__main__":
    d= False

    arquivos = [r'C:\Users\breno\Desktop\Projetos\Soldas\aplication_gui_basic.py',
                r'C:\Users\breno\Desktop\Projetos\Soldas\aplication_gui_event.py']

    processos = []
    for arquivo in arquivos:
        if 'event' in arquivo:
            d = True
        processos.append(Thread(target=inicia_programa, args=(arquivo,), daemon=d))

    processos[0].start()
    processos[1].start()

    while True:
    
        if verificar_duplo_click():
            p.evento_duplo_click()

        if not processos[0].is_alive():
            break

