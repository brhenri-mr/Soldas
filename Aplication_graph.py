
class Pre_visualizacao():
    """
    Controla todos os desenhos/imagens que serão disponibilizadas no gui
    """

    def __init__(self, janela) -> None:

        self.janela = janela
        janela.draw_image(filename='background2.png', location=(0,400))

    def filete(self,reg=True):
        '''
        Desenha uma solda filete básica 

        reg = Parametro que permite alterar a posição da solda: cima ou em baixo, por padrão é em cima 
        reg: bool

        '''

        if reg:
            i = 1
        else:
            i= -1

        return self.janela.draw_lines([(100,200),(280,200),(190,200),(190,200-48.5*i),(190,200-48.5*i),(248.5,200)],color='red')
    
    def bisel(self, reg=True):
        '''
        Desenha uma solda bisel básica
        reg = Parametro que permite alterar a posição da solda: cima ou em baixo, por padrão é em cima 
        reg: bool
        '''

        if reg:
            i = 1
        else:
            i = -1

        return self.janela.draw_lines([(100,200),(280,200),(190,200),(190,200-48.5*i),(190,200),(190+48.5,200-48.5*i)], color='red')
    
    def bisel_curvo(self, reg=True):
        '''
        Desenha uma solda bisel curava básica
        reg = Parametro que permite alterar a posição da solda: cima ou em baixo, por padrão é em cima 
        reg: bool
        '''
        if reg:
            i = 1
        else:
            i = -1

        id1 = self.janela.draw_lines([(100,200),(280,200),(190,200),(190,200 - 48.5*i)], color='red')
        id3 =  self.janela.draw_lines([(190,200),(190,200 - 48.5*i)], color='red')
        id2 = self.janela.draw_arc((195,250),(295,147),90 if reg else -90,180,style ='arc' ,arc_color='red')
        return [id1,id2,id3]

    def v(self, reg=True):
        '''
        Desenha uma solda v basica
        reg = Parametro que permite alterar a posição da solda: cima ou em baixo, por padrão é em cima 
        reg: bool
        '''

        if reg:
            i = 1
        else:
            i = -1

        return self.janela.draw_lines([  
                                    (100,200),(280,200),
                                    (190,200),(190+48.5,200-48.5*i),
                                    (190,200),(190-48.5,200-48.5*i)], color='red')

    def v_curvo(self,reg=True):
        '''
        Desenha uma solda v curva basica
        reg = Parametro que permite alterar a posição da solda: cima ou em baixo, por padrão é em cima 
        reg: bool
        '''

        id1 = self.janela.draw_arc((195,247),(295,147),90 if reg else-90,180,style ='arc' ,arc_color='red')
        id2 = self.janela.draw_arc((85,250),(185,150),-90 if reg else 90 ,0,style ='arc' ,arc_color='red')
        id3 = self.janela.draw_lines([(100,200),(280,200)], color='red')

        return [id1,id2,id3]
    
    def topo(self,reg=True):
        '''
        Desenha uma solda topo básica
        '''
        if reg:
            i = 1
        else:
            i = -1

        id1 = self.janela.draw_lines([(100,200),(280,200),(175,200),(175,200-48.5*i)],color='red')
        id2 = self.janela.draw_line((205,200),(205,200-48.5*i),color='red')
    
        return [id1,id2]

    def j(self):

        id1 = self.janela.draw_lines([(100,200),(280,200),(190,200),(190,150)], color='red')
        id2 = self.janela.draw_arc((150,190),(230,110),90,0,style ='arc' ,arc_color='red')

        return [id1,id2]

    def acabamento_reto(self,cri,tipo):
        '''
        Desenha o acabamento de tipo reto para soldas bisel

        cri = criterio que especifica se a solda é ambos os lados, True significa
        solda ambos os lados
        cri: bool
        tipo = Variavel indica o tipo da solda que vai receber o acabamento
        tipo: str

        '''
        if tipo == 'BISEL':
            if cri:
                id1 = self.janela.draw_lines([(185,250.5),(195+48.5,250.5)],color='red')
            else:
                id1= ''
            id2 = self.janela.draw_lines([(185,148.5),(195+48.5,148.5)],color='red')
        elif tipo == 'TOPO':
            if cri:
                id1 = self.janela.draw_lines([(162.5,250.5),(172.5+48.5,250.5)],color='red')
            else:
                id1= ''
            id2 = self.janela.draw_lines([(162.5,148.5),(172.5+48.5,148.5)],color='red')
        return [id1,id2]

    def acabamento_convexo(self,cri,tipo):
        '''
        Desenha o acabamento de tipo Convexo para soldas bisel

        cri = criterio que especifica se a solda é ambos os lados
        cri: bool
        tipo = Variavel indica o tipo da solda que vai receber o acabamento
        tipo: str
        '''
        if tipo == "BISEL":
            if cri:
                id1 = self.janela.draw_arc((135,259),(225+48.5,151),70,50,style='arc',arc_color='red')
            else:
                id1 = ''
            id2 = self.janela.draw_arc((135,195),(225+48.5,143.5),70,245,style='arc',arc_color='red')
        elif tipo == 'TOPO':
            if cri:
                id1 = self.janela.draw_arc((115,259),(215+48.5,143.5),80,55,style='arc',arc_color='red')
            else:
                id1 = ''
            id2 = self.janela.draw_arc((115,195),(205+48.5,143.5),80,235,style='arc',arc_color='red')


        return [id1,id2]

    def solda_em_campo(self, orientacao):
        '''
        orientacao = orientação dos detalhes no desenho, por padrão se adota que
        orientação verdadeira é direita
        orientacao: bool
        '''

        if orientacao:
            
            #traço vertical
            id_1 = self.janela.draw_line((280,200),(280,263),color='red')
            #bandeira
            id_2 = self.janela.draw_polygon([(280,263),(253,254.93),(280,246.86)],fill_color='red',line_color='red')
        else:
            
            #traço vertical
            id_1 = self.janela.draw_line((100,200),(100,263),color='red')
            #bandeira
            id_2 = self.janela.draw_polygon([(100,263),(126,254.93),(100,246.86)],fill_color='red',line_color='red')


        return [id_1,id_2]
    
    def reforco(self,direcao=True):
        '''
        Desenha o detalhe de reforco tipo cordao
        direcao = controla a direção para que vai estar o desenho, cima ou embaixo
        direcao:Bool
        '''
        if direcao:
            i = 1
        else:
            i = -1

        return self.janela.draw_lines([(190,200),(190,200-126*i),(190+48.5,200-126*i+48.5*i),(190,200-126*i+48.5*i)],color='red')

    def solda_ambos_os_lados(self,nome):

        '''
        Desenha o tipo ambos os lados para solda

        nome = nome do tipo base da solda
        nome: str
        '''

        if nome == 'FILETE':
            return  self.janela.draw_lines([(190,200),(190,248.5),(190,248.5),(248.5,200)], color='red')
        elif nome == 'BISEL':
            return  self.janela.draw_lines([(190,200),(190,248.5),(190,200),(190+48.5,248.5)], color='red')
        elif nome == 'TOPO':
            id1 = self.janela.draw_line((175,200),(175,248.5),color='red')
            id2 = self.janela.draw_line((205,200),(205,248.5),color='red')
            return [id1,id2]
        elif nome =='V':
            return self.janela.draw_lines([(190,200),(190+48.5,248.5),(190,200),(190-48.5,248.5)], color='red')
        elif nome == 'BISEL_CURVO':
            id1 = self.janela.draw_line((190,200),(190,248.5),color='red')
            id2 = self.janela.draw_arc((195,250),(295,147),90,90,style ='arc' ,arc_color='red')
            return [id1,id2]
        elif nome  == 'V_CURVO':
            id1 = self.janela.draw_arc((195,247),(295,147),90,90,style ='arc' ,arc_color='red')
            id2 = self.janela.draw_arc((85,250),(185,150),-90,90,style ='arc' ,arc_color='red') 
            return [id1,id2]
    
    def tipico(self,ori=True):
        '''
        Desenha a indicação de detalhe típico 

        ori = orientação do detalhe. por padrão é para direita
        ori:Bool
        '''

        if ori:
            id1 = self.janela.draw_lines([(100,200),(70,230),(100,200),(70,170)], color='red')
            id2 = self.janela.draw_text('(TÍP.)',(60,200), color='yellow',font=2.5)
        else:
            id1 = self.janela.draw_lines([(280,200),(310,230),(280,200),(310,170)], color='red')
            id2 = self.janela.draw_text('(TÍP.)',(320,200), color='yellow',font=2.5)
        return [id1,id2]
        
    def descontinuo(self,passo,ori=True):
        '''
        Desenha a informação adicional típica na prévisuzalição
        retorno -> um desenho 

        passo = valor a ser escrito no desenho
        passo:str
        ori = orientação do detalhe. por padrão é para direita
        ori:Bool
        '''
        if ori:
            id = self.janela.draw_text('('+passo+')',(130,215), color='yellow',font=1.5)
        else:
            id = self.janela.draw_text('('+passo+')',(270,215), color='yellow',font=1.5)
        return id

    def intercalado(self,id_old):
        '''
        Desenha solda com intercalada

        id_old = id da antiga solda base do desenho
        id_old: str
        '''

        self.apagar(id_old)

        return self.janela.draw_lines([(100,200),(280,200),
                  (165,200),(165,151.5),
                  (165,151.5),(222.5,200),
                  (190,200),(190,248.5),
                  (190,248.5),(248.5,200)
                  ], color='red')

    def contorno(self, orientacao):
        '''
        orientacao = orientação dos detalhes no desenho, por padrão se adota que
        orientação verdadeira é direita

        orientacao = direção que ira se aplicar todo o contorno, direita ou esquerda
        orientação: bool
        '''
        if orientacao:
            c = (280,200)
        else:
            c = (100,200)

        return self.janela.draw_circle(c, 17.5 ,line_color='red')

    def espessura(self,exps,base,unidade,direcao=True,*args,**kwargs):
        '''
        Insere no desenho de pré-visualização as espessuras de solda, há dois tipos de funcionamento:
        inserção da base como criterio, quando se clica em ambos os lados.
        
        exps = espessura que ira se usar nas soldas 
        exps: int or list

        base = Desenho base no qual se pretender colocar a espessura(bisel, filete)
        base: str

        unidade = Parametro que indica se a solda é milimetro ou angulo. Por padrão é milimetro
        unidade: bool

        direcao = Orientcao do txt da espessura, cima ou embaixo.Por padrao é para baixo, ou seja,
        True

        *args = Parametro adicional da solda, caso preciso
        *args:tuple
        '''

        if direcao:
            correcao_direcao = 1
        else:
            correcao_direcao = 2.92

        if base =='Amboslados':
            if len(args)>0:
                base = args[0]
                if args[0] == 'BISEL':
                    if unidade:
                        pontos = [(212-(len(exps[0])-1)*2,130),(170-(len(exps[1])-1)*2,175.75),(212-(len(exps[0])-1)*2,270),(170-(len(exps[1])-1)*2,224.25)]
                        exps = exps*2
                    else:
                        pontos = [(212-(len(exps[1])-1)*2,130),(212-(len(exps[1])-1)*2,270)]
                        exps = [exps[0],exps[0]]
                elif base == 'TOPO':
                    pontos = [(185.5-(len(exps[1])-1)*2,130),((185.5-(len(exps[1])-1)*2,270))]
                    exps = [exps[0],exps[0]]
                elif base == 'FILETE':
                    pontos = [(170-(len(exps[0])-1)*2,175.75),(170-(len(exps[0])-1)*2,224.25)]
                elif base =='V':
                    pontos = [(190.5-(len(exps[1])-1)*2,130),((190.5-(len(exps[1])-1)*2,270))]
                    exps = [exps[0],exps[0]]
                else:
                    return ''

        else:
            # base continua sendo base

            if base=='Intercalado':
                pontos = [(155 - (len(exps[0])-1),175.75),(178- (len(exps[1])-1)*2,224.25)]

            elif base in ['FILETE','J']:
                pontos = [(170-(len(exps[0])-1)*2,175.75*correcao_direcao)]

            elif base == 'TOPO':
                pontos = [(190.5-(len(exps[1])-1)*2,130*correcao_direcao)]

            elif base == 'V':
                pontos = [(190.5-(len(exps[1])-1)*2,130*correcao_direcao)]

            elif base == 'V CURVO':
                return ''
            
            elif base =='BISEL':
                if unidade:
                    pontos = [(212-(len(exps[0])-1)*2,130),(170-(len(exps[1])-1)*2,175.75)*correcao_direcao]
                    exps = exps*2
                else:
                    pontos = [(212-(len(exps[1])-1)*2,130)*correcao_direcao]
                    exps = exps
            elif base == 'Reforco':
                pontos = [(170-(len(exps[0])-1)*2,102.5*correcao_direcao)]
            else:
                return ''

        return [self.janela.draw_text(exp if unidade else str(exp+'°' if exp!= '' else ''),ponto, color='yellow',font=2.5) for exp,ponto in zip(exps,pontos)]

    def apagar(self,id):
        '''
        deleta uma figura/elemento do grafico
        '''
        [self.janela.delete_figure(i) for i in id] if isinstance(id,list) else self.janela.delete_figure(id)
        
    def deletar(self):
        '''
        Deleta toda a imagem que já foi gerada
        '''
        self.janela.erase()
        self.janela.draw_image(filename='background2.png', location=(0,400))
    
    def solda_desenhada(self,nome, *args):

        '''
        Desenha a solda completa (base e acabamentos), a função pode ser usada para transportar a solda do autocad para o programa
        (no caso do uso do gui_events) ou usada no programa main (gui_basic). A logica da função é deletar previamente todas as imagens
        deixando um id 'fantasma', isto é, com valores que presentam figuras ja deletas, mas se estão ali, é porque era para estar de
        senhando.
        Na primeira opção, a entrada vai ser um dicionario contendo os parametros da solda, de tipo True ou False, retornando um 
        id total do desenho.
        Na segunda opção,se usa os args para dar à função o tipo de solda desenhada. Usa-se essa função para preservar parametros do 
        desenho quando mudada alguma propriedade da base, como de filete para bisel e não perder os acabamentos. Essa opção retorna o
        id disponibilizado (nome) para a função, atualizando os valores dos ids

        nome = parametros da solda
        nome: dict
        '''

        id = {
        'Base':'',
        'solda_em_campo':'',
        'ambos_os_lados':'',
        'contorno':'',
        'acabamento':'',
        'intercalado':'', 
        'expA':'',
        'expB':'',
        'Reforco':'',
        'tipico':'',
        'Base_m_i':'',
        'Base_m_s':'',
        'm_reforco_s':'',
        'm_reforco_i':'',
        'Descontinuo':''
        }
        
        if len(args) >0:
            #por padrão é para direita
            ori = args[0]
            base = args[1]

            if 'MISTO' in base:
                lista_bases = base.split('_')[1:]
                for i in range(len(lista_bases)):
                    lista_bases[i] = lista_bases[i].replace(' ','_') 

                cri = True
            else:
                lista_bases = [base]
                cri = False
            print(lista_bases)
            for i,b in enumerate(lista_bases):

                if cri:
                    temp = 'Base_m_i' if i == 0 else 'Base_m_s'
                else:
                    temp = 'Base'
                if b =='FILETE':
                    nome[temp] = self.filete(reg=False if i == 1 else True)
                elif b == 'BISEL':
                    nome[temp] = self.bisel(reg=False if i == 1 else True)
                elif b == 'BISEL_CURVO':
                    nome[temp] = self.bisel_curvo(reg=False if i == 1 else True)
                elif b == 'V':
                    nome[temp] = self.v(reg=False if i == 1 else True)
                elif b == 'V_CURVO':
                    nome[temp] = self.v_curvo(reg=False if i == 1 else True)
                elif b == 'TOPO':
                    nome[temp] = self.topo(reg=False if i == 1 else True)
                elif b == 'J':
                    nome[temp] = self.j()
            
            if nome['contorno']!= '':
                nome['contorno'] = self.contorno(ori)
            if nome['ambos_os_lados'] != '':
                nome['ambos_os_lados'] = self.solda_ambos_os_lados(base)
            if nome['solda_em_campo']!= '':
                nome['solda_em_campo'] = self.solda_em_campo(ori)
            if nome['tipico'] !='':
                nome['tipico'] = self.tipico(ori)
            if nome['m_reforco_s'] !='':
                nome['m_reforco_s'] = self.reforco(direcao=False)
            if nome['m_reforco_i'] !='':
                nome['m_reforco_i'] = self.reforco()
            if nome['Descontinuo'] !='':
                nome['Descontinuo'] = self.descontinuo('PASSO',ori=ori)
            return nome

        else:
            if nome['direita']:
                ori = True
            elif nome['esquerda']:
                ori=False

            if nome['filete']:
                id['Base'] = self.filete()
                b= 'FILETE'
            elif nome['bisel']:
                id['Base'] = self.bisel()
                b='BISEL'
            if nome['contorno']:
                id['contorno'] = self.contorno(ori)
            if nome['amboslados']:
                id['amboslados'] = self.solda_ambos_os_lados(b)
            if nome['campo']:
                id['solda_em_campo'] = self.solda_em_campo(ori)
        