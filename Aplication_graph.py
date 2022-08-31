
class Pre_visualizacao():
    """
    Controla todos os desenhos/imagens que serão disponibilizadas no gui
    """

    def __init__(self, janela) -> None:

        self.janela = janela

    def filete(self):
        '''
        desenha uma solda filete básica 

        '''
        id = self.janela.draw_lines([(100,200),(280,200),(190,200),(190,151.5),(190,151.5),(248.5,200)],color='red')
        
        return id
    
    def bisel(self):
        id = self.janela.draw_lines([(100,200),(280,200),(190,200),(190,151.5),(190,200),(190+48.5,151.5)], color='red')
        return id
    
    def acabamento_reto(self,cri):
        

        if cri:
            id1 = self.janela.draw_lines([(185,250.5),(195+48.5,250.5)],color='red')
        else:
            id1= ''
        id2 = self.janela.draw_lines([(185,148.5),(195+48.5,148.5)],color='red')

        return [id1,id2]

    def acabamento_convexo(self,cri):
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

    def solda_continua(self, orientacao):
        pass

    def solda_ambos_os_lados(self,cri):
        
        if cri == 'FILETE':
            id = self.janela.draw_lines([(190,200),(190,248.5),(190,248.5),(248.5,200)], color='red')
        elif cri == 'BISEL':
            id = self.janela.draw_lines([(190,200),(190,248.5),(190,200),(190+48.5,248.5)], color='red')

        return id
      
    def intercalado(self):
        pass

    def contorno(self, orientacao):
        '''
        orientacao = orientação dos detalhes no desenho, por padrão se adota que
        orientação verdadeira é direita
        '''
        if orientacao:
            c = (280,200)
        else:
            c = (100,200)
        id = self.janela.draw_circle(c, 17.5 ,line_color='red')
        return id

    def solda_continua(self, orientacao):
        pass

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
    
    def solda_desenhada(self,nome):

        '''
        Desenha a solda do autocad no programa
        '''
        id = {'filete':[],'contorno':[],'amboslados':[],'campo':[]}

        if 'd' == nome[0]:
            if 'filete' in nome:
                id['filete'].append(self.filete())
                b= 'FILETE'
            elif 'bisel' in nome:
                pass
            if 'contorno' in nome:
                id['contorno'].append(self.contorno(True))
            if 'amboslados' in nome:
                id['amboslados'].append(self.solda_ambos_os_lados(b))
            if 'campo' in nome:
                id['campo'].append(self.solda_em_campo(True))

        elif 'e' == nome[0]:
            if 'filete' in nome:
                id['filete'].append(self.filete())
                b= 'FILETE'
            elif 'bisel' in nome:
                pass
            if 'contorno' in nome:
                id['contorno'].append(self.contorno(False))
            if 'amboslados' in nome:
                id['amboslados'].append(self.solda_ambos_os_lados(b))
            if 'campo' in nome:
                id['campo'].append(self.solda_em_campo(False))

        return id
    