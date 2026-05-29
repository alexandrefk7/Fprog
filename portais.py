from math import sqrt
from graphics import *


# par de portais que teleporta a bola entre dois pontos da janela
class PortalPair:

    def __init__(self, janela, centro_portal1, normal_portal1, centro_portal2, normal_portal2, largura_portal,
                 cor_portal1="blue", cor_portal2="orange"):

        self.janela        = janela
        self.largura_portal = largura_portal
        self.cor_portal1   = cor_portal1
        self.cor_portal2   = cor_portal2
        # cria os dois portais e guarda dados geométricos e segmento visual de cada um
        self.dados_portal1, self.segmento_portal1 = self._create(janela, centro_portal1, normal_portal1, largura_portal, cor_portal1)
        self.dados_portal2, self.segmento_portal2 = self._create(janela, centro_portal2, normal_portal2, largura_portal, cor_portal2)

    def _create(self, janela, centro_portal, normal_portal, largura_portal, cor_linha):
        centro_x, centro_y = centro_portal.getX(), centro_portal.getY()
        # normaliza o vetor normal para garantir comprimento unitário
        norma_vetor = sqrt(normal_portal[0]**2 + normal_portal[1]**2)
        normal_x, normal_y = normal_portal[0] / norma_vetor, normal_portal[1] / norma_vetor
        tangente_x, tangente_y = -normal_y, normal_x          # tangent perpendicular to normal
        metade_largura = largura_portal / 2
        # constrói e desenha o segmento visual do portal na janela
        segmento_visual = Line(Point(centro_x - tangente_x*metade_largura, centro_y - tangente_y*metade_largura),
                               Point(centro_x + tangente_x*metade_largura, centro_y + tangente_y*metade_largura))
        segmento_visual.setFill(cor_linha)
        segmento_visual.setWidth(4)
        segmento_visual.draw(janela)
        # devolve dados geométricos e segmento desenhado para uso posterior
        return (centro_x, centro_y, normal_x, normal_y, tangente_x, tangente_y), segmento_visual

    def move_p1(self, deslocamento_x, deslocamento_y):
        centro_x, centro_y, normal_x, normal_y, tangente_x, tangente_y = self.dados_portal1
        centro_x += deslocamento_x
        centro_y += deslocamento_y
        # apaga o segmento antigo e redesenha na nova posição
        self.segmento_portal1.undraw()
        metade_largura = self.largura_portal / 2
        self.segmento_portal1 = Line(Point(centro_x - tangente_x*metade_largura, centro_y - tangente_y*metade_largura),
                                     Point(centro_x + tangente_x*metade_largura, centro_y + tangente_y*metade_largura))
        self.segmento_portal1.setFill(self.cor_portal1)
        self.segmento_portal1.setWidth(4)
        self.segmento_portal1.draw(self.janela)
        # atualiza os dados geométricos do portal com o novo centro
        self.dados_portal1 = (centro_x, centro_y, normal_x, normal_y, tangente_x, tangente_y)

    def move_p2(self, deslocamento_x, deslocamento_y):
        centro_x, centro_y, normal_x, normal_y, tangente_x, tangente_y = self.dados_portal2
        centro_x += deslocamento_x
        centro_y += deslocamento_y
        # apaga o segmento antigo e redesenha na nova posição
        self.segmento_portal2.undraw()
        metade_largura = self.largura_portal / 2
        self.segmento_portal2 = Line(Point(centro_x - tangente_x*metade_largura, centro_y - tangente_y*metade_largura),
                                     Point(centro_x + tangente_x*metade_largura, centro_y + tangente_y*metade_largura))
        self.segmento_portal2.setFill(self.cor_portal2)
        self.segmento_portal2.setWidth(4)
        self.segmento_portal2.draw(self.janela)
        # atualiza os dados geométricos do portal com o novo centro
        self.dados_portal2 = (centro_x, centro_y, normal_x, normal_y, tangente_x, tangente_y)

    def _in_zone(self, bola, raio_bola, dados_portal):
        centro_x, centro_y, normal_x, normal_y, tangente_x, tangente_y = dados_portal
        diferenca_x = bola.getx() - centro_x
        diferenca_y = bola.gety() - centro_y
        distancia_normal     = abs(diferenca_x*normal_x   + diferenca_y*normal_y)    # perpendicular distance to portal
        distancia_tangencial = abs(diferenca_x*tangente_x + diferenca_y*tangente_y)  # distance along portal
        # bola na zona se próxima o suficiente em ambas as direções
        return distancia_normal <= raio_bola and distancia_tangencial <= self.largura_portal / 2

    def _teleport(self, bola, raio_bola, portal_entrada, portal_saida):
        _, _, normal_entrada_x, normal_entrada_y, tangente_entrada_x, tangente_entrada_y = portal_entrada
        centro_saida_x, centro_saida_y, normal_saida_x, normal_saida_y, tangente_saida_x, tangente_saida_y = portal_saida


        velocidade_normal      = bola.xvel * normal_entrada_x   + bola.yvel * normal_entrada_y    # normal component
        velocidade_tangencial  = bola.xvel * tangente_entrada_x + bola.yvel * tangente_entrada_y  # tangential component

        # preserva modulo da velocidad quando sai do segundo portal
        bola.xvel = velocidade_normal * normal_saida_x   + velocidade_tangencial * tangente_saida_x
        bola.yvel = velocidade_normal * normal_saida_y   + velocidade_tangencial * tangente_saida_y

        # posiciona a bola na saída do segundo portal
        bola.xpos = centro_saida_x + normal_saida_x * (raio_bola + 0.5)
        bola.ypos = centro_saida_y + normal_saida_y * (raio_bola + 0.5)

    def apply(self, bola, raio_bola):
        # verifica entrada no portal 1: produto escalar positivo significa movimento na direção da normal
        _, _, normal1_x, normal1_y, _, _ = self.dados_portal1
        if self._in_zone(bola, raio_bola, self.dados_portal1):
            if bola.xvel * normal1_x + bola.yvel * normal1_y > 0:  # ball entering p1
                self._teleport(bola, raio_bola, self.dados_portal1, self.dados_portal2)
                return True

        # verifica entrada no portal 2
        #_, para ignorar as variáveis que não sao necessarias
        _, _, normal2_x, normal2_y, _, _ = self.dados_portal2
        if self._in_zone(bola, raio_bola, self.dados_portal2):
            if bola.xvel * normal2_x + bola.yvel * normal2_y > 0:  # ball entering p2
                self._teleport(bola, raio_bola, self.dados_portal2, self.dados_portal1)
                return True

        # nenhum portal ativado neste passo
        return False
