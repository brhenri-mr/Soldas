import multiprocessing
import time

def task():
    while True:
        print('Sleeping')
    

p= []

if __name__ == "__main__": 

    p.append(multiprocessing.Process(target = task))
    p[-1].start()
    time.sleep(2)
    p[-1].terminate()
    p.append(multiprocessing.Process(target = task))
    for i in range(3):
        print('to rodando')
    p[-1].start()
    time.sleep(1)
    p[-1].terminate()