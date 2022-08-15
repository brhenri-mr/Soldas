def ler_log():
    with open("log.txt") as arquivo:
        linha = arquivo.readlines()[0].split(',')
    return({'handle':linha[0],'ponto':(linha[1],linha[2]),'escala':linha[3],'nome':linha[4]})

print(ler_log())