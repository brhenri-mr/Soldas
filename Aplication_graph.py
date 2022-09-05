
class Pre_visualizacao():
    """
    Controla todos os desenhos/imagens que serão disponibilizadas no gui
    """

    def __init__(self, janela) -> None:

        self.janela = janela
        janela.draw_image(filename='background2.png', location=(0,400))

    def filete(self):
        '''
        Desenha uma solda filete básica 

        '''
        return self.janela.draw_lines([(100,200),(280,200),(190,200),(190,151.5),(190,151.5),(248.5,200)],color='red')
    
    def bisel(self):

        return self.janela.draw_lines([(100,200),(280,200),(190,200),(190,151.5),(190,200),(190+48.5,151.5)], color='red')
    
    def bisel_curvo(self):
        '''
        Desenha uma solda bisel curava básica
        '''
        id1 = self.janela.draw_lines([(100,200),(280,200),(190,200),(190,151.5)], color='red')
        id3 =  self.janela.draw_lines([(190,200),(190,151.5)], color='red')
        id2 = self.janela.draw_arc((195,250),(295,147),90,180,style ='arc' ,arc_color='red')
        return [id1,id2,id3]

    def v(self):
        '''
        Desenha uma solda v basica
        '''

        return self.janela.draw_lines([  
                                    (100,200),(280,200),
                                    (190,200),(190+48.5,151.5),
                                    (190,200),(190-48.5,151.5)], color='red')


    def v_curvo(self):
        '''
        Desenha uma solda v curva basica
        '''
        
        id1 = self.janela.draw_arc((195,247),(295,147),90,180,style ='arc' ,arc_color='red')
        id2 = self.janela.draw_arc((85,250),(185,150),-90,0,style ='arc' ,arc_color='red')
        id3 = self.janela.draw_lines([(100,200),(280,200)], color='red')

        return [id1,id2,id3]
    
    def topo(self):
        '''
        Desenha uma solda topo básica
        '''


        id1 = self.janela.draw_lines([(100,200),(280,200),(175,200),(175,151.5)],color='red')
        id2 = self.janela.draw_line((205,200),(205,151.5),color='red')
    
        return [id1,id2]

    def acabamento_reto(self,cri):
        '''
        Desenha o acabamento de tipo reto para soldas bisel

        cri = criterio que especifica se a solda é ambos os lados
        cri: bool
        '''

        if cri:
            id1 = self.janela.draw_lines([(185,250.5),(195+48.5,250.5)],color='red')
        else:
            id1= ''
        id2 = self.janela.draw_lines([(185,148.5),(195+48.5,148.5)],color='red')

        return [id1,id2]

    def acabamento_convexo(self,cri):
        '''
        Desenha o acabamento de tipo Convexo para soldas bisel

        cri = criterio que especifica se a solda é ambos os lados
        cri: bool
        '''
        if cri:
           id1 = self.janela.draw_arc((135,259),(225+48.5,151),70,50,style='arc',arc_color='red')
        else:
            id1 = ''
        id2 = self.janela.draw_arc((135,195),(225+48.5,143.5),70,245,style='arc',arc_color='red')

        return [id1,id2]

    def solda_em_campo(self, orientacao):
        '''
        orientacao = orientação dos detalhes no desenho, por padrão se adota que
        orientação verdadeira é direita
        orientacao: bool
        '''

        if orientacao:
            x = 280
            x_flag = 307
        else:
            x = 100
            x_flag = 73

        #traço vertical
        id_1 = self.janela.draw_line((x,200),(x,263),color='red')
        #bandeira
        id_2 = self.janela.draw_polygon([(x,263),(x_flag,254.93),(x,246.86)],fill_color='red',line_color='red')

        return [id_1,id_2]
    
    def reforco(self):
        '''
        Desenha o detalhe de reforco tipo cordao
        '''
        return self.janela.draw_lines([(190,200),(190,74),(190+48.5,74+48.5),(190,74+48.5)],color='red')

    def solda_continua(self, orientacao):
        pass

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

    def solda_continua(self, orientacao):
        pass

    def espessura(self,exps,base):
        '''
        Insere no desenho de pré-visualização as espessuras de solda
        
        exps = espessura que ira se usar nas soldas 
        exps: int or list

        base = Desenho base no qual se pretender colocar a espessura(bisel, filete)
        base: str
        '''

        if base=='Intercalado':

            pontos = [(155 - (len(exps[0])-1),175.75),(178- (len(exps[1])-1)*2,224.25)]

        elif base =='Amboslados':
            pontos = [(178-(len(exps[0])-1)*2,175.75),(178-(len(exps[1])-1)*2,224.25)]

        else:
            pontos = [(178-(len(exps[0])-1)*2,175.75)]

        return [self.janela.draw_text(exp,ponto, color='yellow',font=2.5) for exp,ponto in zip(exps,pontos)]

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
    
    def solda_desenhada(self,nome):

        '''
        Desenha a solda do autocad no programa

        nome = parametros da solda
        nome: dict
        '''
     
        if nome['direita']:
            ori = True
        elif nome['esquerda']:
            ori=False

        if nome['filete']:
            self.filete()
            b= 'FILETE'
        elif nome['bisel']:
            self.bisel()
            b='BISEL'
        if nome['contorno']:
            self.contorno(ori)
        if nome['amboslados']:
            self.solda_ambos_os_lados(b)
        if nome['campo']:
            self.solda_em_campo(ori)

    