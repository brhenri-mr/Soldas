
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

    def solda_ambos_os_lados(self):
   
        id = self.janela.draw_lines([(190,200),(190,248.5),(190,248.5),(248.5,200)], color='red')

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
        id = self.janela.draw_circle(c, 10 ,line_color='red')
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

        if 'd' == nome[0]:
            if 'filete' in nome:
                self.filete()
            elif 'bisel' in nome:
                pass
            if 'contorno' in nome:
                self.contorno(True)
            if 'amboslados' in nome:
                self.solda_ambos_os_lados()
            if 'campo' in nome:
                self.solda_em_campo(True)

        elif 'e' == nome[0]:
            if 'filete' in nome:
                self.filete()
            elif 'bisel' in nome:
                pass
            if 'contorno' in nome:
                self.contorno(False)
            if 'amboslados' in nome:
                self.solda_ambos_os_lados()
            if 'campo' in nome:
                self.solda_em_campo(False)
    