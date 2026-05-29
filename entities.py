from graphics import *
import random
import time
from math import sqrt
from datetime import datetime
import tkinter as tk
import numpy as np


"""
Static — representa qualquer elemento fixo do jogo, como chão, parede ou cesto.
recebe um tipo de forma e desenha-a automaticamente na janela ao ser criado.
não se move nem reage a colisões — é apenas a estrutura do cenário.
"""
# Cria a linha com medições de distância (Cenário 1)
class Static:
    def __init__(self, center, shape, color, outline, window, offset=0, radius=0):
        self.center = center
        self.shape = shape
        self.radius = radius
        self.color = color
        self.outline = outline
        self.win = window
        self.offset = offset
        self.constructor()

    # desenha uma linha vertical na posição x definida
    def create_wall(self):
        line = Line(self.center, Point(self.center.getX(), self.center.getY() + self.offset))
        line.draw(self.win)

    # desenha uma linha horizontal na posição y definida
    def create_line(self):
        line = Line(self.center, Point(self.center.getX() + self.offset, self.center.getY()))
        line.draw(self.win)

    # desenha um círculo com a cor e raio definidos
    def create_balls(self):
        self.ball = Circle(self.center, self.radius)
        self.ball.setFill(self.color)
        self.ball.setOutline(self.outline)
        self.ball.draw(self.win)

    def create_metricline(self):
        big_line = Line(Point(0, self.center.getY()), Point(self.offset, self.center.getY()))
        big_line.draw(self.win)
        for val in range(0, int(self.offset), 50):
            line = Line(Point(val, 0), Point(val, 4))
            line.draw(self.win)
            mark = Text(Point(val, -5), f"{val}")
            mark.draw(self.win)

    # cria dois aros ligados por uma linha horizontal
    def create_basket(self):
        left_ball = Static(self.center, "circle", self.color, self.outline, self.win, radius=self.radius)
        right_ball = Static(Point(self.center.getX() + self.offset, self.center.getY()), "circle", self.color,
                            self.outline, self.win, radius=self.radius)
        left_ball.create_balls()
        right_ball.create_balls()
        line = Line(Point(self.center.getX(), self.center.getY() + self.radius),
                    Point(self.center.getX() + self.offset, self.center.getY() + self.radius))
        line.draw(self.win)

    def create_rectangle(self):
        Rectangle = Rectangle()

    # redireciona para o método de construção correto com base na forma escolhida
    def constructor(self):
        if self.shape == "circle" and self.radius > 0 and self.offset == 0:
            self.create_balls()
        elif self.shape == "metric" and self.radius == 0:
            self.create_metricline()
        elif self.shape == "basket" and self.radius > 0 and self.offset > 0:
            self.create_basket()
        elif self.shape == "line" and self.offset != 0:
            self.create_line()
        elif self.shape == "wall" and self.offset != 0:
            self.create_wall()


"""
parabola — traça a curva parabólica que serve de rampa no cenário 3.
calcula e desenha segmentos de reta consecutivos para aproximar a forma da parábola.
também devolve o valor y correspondente a um dado x, mesmo sem desenhar.
"""
def parabola(left_side_xcord, win, xoffset=0, yoffset=0, mirror_dif=0, scalar=0.1, draw=True):
    # ponto de espelho simétrico da parábola
    mirror = left_side_xcord * -1 - mirror_dif
    if draw == True:
        # avança x em pequenos passos, desenhando segmentos curtos
        while left_side_xcord < mirror:
            point = Point(left_side_xcord, scalar * (left_side_xcord - xoffset) ** 2 + yoffset)
            nextx_coord = left_side_xcord + 0.2
            next_point = Point(nextx_coord, scalar * (nextx_coord - xoffset) ** 2 + yoffset)
            line = Line(point, next_point)
            line.draw(win)
            left_side_xcord += 0.2
    return scalar * (left_side_xcord - xoffset) ** 2 + yoffset


"""
ScoreBoard — gere a pontuação e as vidas exibidas na janela de jogo.
mostra mensagens de incentivo ou crítica a cada jogada realizada.
pode funcionar como marcador de pontos ou como contador de vidas, conforme o cenário.
"""
# Classe que cria e atualiza uma determinada pontuação (Cenário 1 e 3)
class ScoreBoard:
    def __init__(self, pos, message_pos, win, number=0, subject="Score"):
        self.congratulations = ["Nice!", "You're Killing it!", "9/10 dentists recommend your plays!", "ON FIRE!",
                                "KOBE!"]
        self.depreciations = ["Oh well!", "Can't win them all", "The door is over there...",
                              "*crowd throws tomatoes at you..."]
        self.score_number = number
        self.lives = number

        self.message = Text(message_pos, "Test your skills!")
        self.message.setStyle("bold")
        self.message.draw(win)

        self.scoreboard = Text(Point(10, 10), "Ah")
        self.lifeboard = Text(Point(10, 10), "Ah")

        if subject == "Score":
            self.print_score(pos, win, subject)
        elif subject == "Lives":
            self.print_lives(pos, win, subject)

    def print_score(self, pos, win, subject):
        self.scoreboard = Text(pos, f"{subject}: {self.score_number}")
        self.scoreboard.draw(win)

    def print_lives(self, pos, win, subject):
        self.lifeboard = Text(pos, f"{subject}: {self.lives}")
        self.lifeboard.draw(win)

    # Atualiza o valor da pontuação
    def update_lives(self):
        self.lives -= 1
        self.lifeboard.setText(f"Lives: {self.lives}")

    # incrementa a pontuação em 2 e atualiza o texto no ecrã
    def update_score(self):

        self.score_number += 2
        self.scoreboard.setText(f"Score: {self.score_number}")

    # escolhe uma mensagem aleatória de encorajamento
    def unecessary_cheers(self, win):

        self.message.setText(f"{self.congratulations[random.randint(0, (len(self.congratulations) - 1))]}")
        self.message.undraw()
        self.message.draw(win)

    # escolhe uma mensagem aleatória de crítica
    def necessary_depreciations(self, win):
        self.message.setText(f"{self.depreciations[random.randint(0, (len(self.depreciations) - 1))]}")
        self.message.undraw()
        self.message.draw(win)

    # mostra o texto de fim de jogo no centro da janela
    def game_over(self, win):
        end_text = Text(Point(175, 100), "Game Over!")
        end_text.setSize(15)
        end_text.draw(win)


"""
Button — botão clicável com rótulo de texto na janela gráfica.
pode ser ativado ou desativado para controlar quando aceita cliques.
deteta se o utilizador clicou dentro dos seus limites e reage em conformidade.
"""
# cria a classe botão
class Button:
    def __init__(self, window, center, width, height, label):
        self.active = True

        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(window)
        self.label = Text(center, label)
        self.label.draw(window)
        self.deactivate()

        # ativa o botão

    def activate(self):
        self.label.setFill("black")
        self.rect.setWidth(2)
        self.active = True

    # impossibilita o uso do botão
    def deactivate(self):
        self.label.setFill("darkgrey")
        self.rect.setWidth(1)
        self.active = False

    # verifica se o botão foi pressionado
    def clicked(self, p):
        return self.active and \
            self.xmin <= p.getX() <= self.xmax and \
            self.ymin <= p.getY() <= self.ymax


"""
InputDialog — janela separada para o utilizador introduzir o ângulo e a velocidade.
valida os valores antes de os aceitar e devolve-os ao cenário que a criou.
fecha-se automaticamente após a confirmação ou cancelamento.
"""
# cria a janela que aceita os valores escolhidos pelo utilizador
class InputDialog:
    # inicializa uma nova janela onde vão ser colocados os valores
    def __init__(self):
        self.window = GraphWin("Valores Iniciais", 200, 300, autoflush=False)
        self.window.setCoords(0, 5, 4, 0.5)
        self.window.setBackground("grey")

        Text(Point(1, 2), "Angulo").draw(self.window)
        self.angle = Entry(Point(3, 2), 5)
        self.angle.draw(self.window)

        Text(Point(1, 3.5), "Velocidade").draw(self.window)
        self.vel = Entry(Point(3, 3.5), 5)
        self.vel.draw(self.window)

        self.shoot = Button(self.window, Point(1, 4.5), 1.25, .5, "Iniciar")
        self.shoot.activate()
        self.quit = Button(self.window, Point(3, 4.5), 1.25, .5, "Sair")
        self.quit.activate()

    # cria um utcome para cada botão possivelmente pressionado
    def interaction(self):
        while self.window.isOpen():
            pt = self.window.checkMouse()
            if pt is not None:
                if self.quit.clicked(pt):
                    self.quit.deactivate()
                    self.window.update()
                    time.sleep(0.3)
                    return "Quit"
                elif self.shoot.clicked(pt):
                    self.shoot.deactivate()
                    self.window.update()
                    time.sleep(0.3)
                    return "Fire!"
                self.window.update()

    def close(self):
        self.window.close()

    # aguarda o clique do utilizador e valida os valores introduzidos
    def collect_val(self):
        while self.window.isOpen():
            pt = self.window.getMouse()
            if self.quit.clicked(pt):
                self.window.close()
                return None, None
            elif self.shoot.clicked(pt):
                try:
                    angle = float(self.angle.getText())
                    vel0 = float(self.vel.getText())
                    if angle > 90 or angle < 0 or vel0 > 80 or vel0 < 0:
                        raise ValueError
                    self.window.close()
                    return angle, vel0
                except ValueError:
                    self.vel.setFill("red")
                    self.angle.setFill("red")

    def destroy(self):
        self = None


"""
StickMan — o jogador do jogo, desenhado como um boneco de palito.
segura uma bola laranja antes de disparar e muda de postura no momento do lançamento.
os seus braços são apagados e redesenhados a cada novo turno.
"""
class StickMan:
    def __init__(self, neck_point, ground_level, direction, win):
        self.direction = direction
        self.px = neck_point.getX()
        self.py = neck_point.getY()

        # Cabeça e tronco
        # point(5,60)
        self.head = Circle(Point(self.px, self.py + 8), 8)
        self.head.setWidth(2)
        self.head.draw(win)
        self.torso = Line(Point(self.px, self.py), Point(self.px, self.py - 22))
        self.torso.setWidth(2)
        self.torso.draw(win)
        # Pernas
        self.rleg = Line(Point(self.px, self.py - 22), Point(self.px + 9, ground_level))
        self.rleg.setWidth(2)
        self.rleg.draw(win)
        self.lleg = Line(Point(self.px, self.py - 22), Point(self.px - 9, ground_level))
        self.lleg.setWidth(2)
        self.lleg.draw(win)

        self.create_arms(win)

    # desenha os dois braços e a bola na posição de repouso
    def create_arms(self, win):
        if self.direction == "left":
            self.w = -1
        else:
            self.w = 1
        # Bola
        self.ball = Circle(Point(self.px + self.w * 18, self.py - 2), 6)
        self.ball.draw(win)
        self.ball.setFill("orange")
        self.ball.setOutline("black")

        self.larm1 = Line(Point(self.px, self.py), Point(self.px + self.w * 10, self.py - 10))
        self.larm1.setWidth(2)
        self.larm1.draw(win)
        self.larm2 = Line(Point(self.px + self.w * 10, self.py - 10), Point(self.px + self.w * 13, self.py))
        self.larm2.setWidth(2)
        self.larm2.draw(win)

        self.rarm1 = Line(Point(self.px, self.py), Point(self.px + self.w * 5, self.py - 15))
        self.rarm1.setWidth(2)
        self.rarm1.draw(win)
        self.rarm2 = Line(Point(self.px + self.w * 5, self.py - 15), Point(self.px + self.w * 20, self.py - 5))
        self.rarm2.setWidth(2)
        self.rarm2.draw(win)

    # devolve o ponto onde a mão está antes de disparar
    def hand_position(self):
        return Point(self.px + self.w * 20, self.py - 5)

    # apaga os braços e a bola para redesenhar
    def clear_arms(self):
        self.ball.undraw()
        self.rarm1.undraw()
        self.rarm2.undraw()
        self.larm1.undraw()
        self.larm2.undraw()

    # redesenha os braços em posição de lançamento
    def shoot(self, win):

        if self.direction == "left":
            self.w = -1
        else:
            self.w = 1
        self.clear_arms()

        self.larm1 = Line(Point(self.px, self.py), Point(self.px + self.w * 20, self.py + 5))
        self.larm1.setWidth(2)
        self.larm1.draw(win)
        self.larm2 = Line(Point(self.px + self.w * 20, self.py + 5), Point(self.px + self.w * 24, self.py + 14))
        self.larm2.setWidth(2)
        self.larm2.draw(win)

        # segundo braço(frente, direita)
        self.rarm1 = Line(Point(self.px, self.py), Point(self.px + self.w * 25, self.py + 8))
        self.rarm1.setWidth(2)
        self.rarm1.draw(win)
        self.rarm2 = Line(Point(self.px + self.w * 25, self.py + 8), Point(self.px + self.w * 40, self.py + 18))
        self.rarm2.setWidth(2)
        self.rarm2.draw(win)

"""
PortalPair — par de portais que teletransporta a bola entre duas posições da janela.
quando a bola entra num portal, sai imediatamente pelo outro com a velocidade redirecionada.
os portais podem ser movidos durante o jogo e desenhados em cores distintas.
"""
# par de portais que teleporta a bola entre dois pontos da janela
class PortalPair:

    def __init__(self, window, center1, normal1, center2, normal2, portal_width,
                 color1="blue", color2="orange"):

        self.window       = window
        self.portal_width = portal_width
        self.color1       = color1
        self.color2       = color2
        # cria os dois portais e guarda dados geométricos e segmento visual de cada um
        self.data1, self.segment1 = self._create(window, center1, normal1, portal_width, color1)
        self.data2, self.segment2 = self._create(window, center2, normal2, portal_width, color2)

    def _create(self, window, center, normal, portal_width, color):
        cx, cy = center.getX(), center.getY()
        # normaliza o vetor normal para garantir comprimento unitário
        norm = sqrt(normal[0]**2 + normal[1]**2)
        nx, ny = normal[0] / norm, normal[1] / norm
        tx, ty = -ny, nx                        # tangent perpendicular to normal
        half_width = portal_width / 2
        # constrói e desenha o segmento visual do portal na janela
        segment = Line(Point(cx - tx*half_width, cy - ty*half_width),
                       Point(cx + tx*half_width, cy + ty*half_width))
        segment.setFill(color)
        segment.setWidth(4)
        segment.draw(window)
        # devolve dados geométricos e segmento desenhado para uso posterior
        return (cx, cy, nx, ny, tx, ty), segment

    def move_p1(self, dx, dy):
        cx, cy, nx, ny, tx, ty = self.data1
        cx += dx
        cy += dy
        # apaga o segmento antigo e redesenha na nova posição
        self.segment1.undraw()
        half_width = self.portal_width / 2
        self.segment1 = Line(Point(cx - tx*half_width, cy - ty*half_width),
                             Point(cx + tx*half_width, cy + ty*half_width))
        self.segment1.setFill(self.color1)
        self.segment1.setWidth(4)
        self.segment1.draw(self.window)
        # atualiza os dados geométricos do portal com o novo centro
        self.data1 = (cx, cy, nx, ny, tx, ty)

    def move_p2(self, dx, dy):
        cx, cy, nx, ny, tx, ty = self.data2
        cx += dx
        cy += dy
        # apaga o segmento antigo e redesenha na nova posição
        self.segment2.undraw()
        half_width = self.portal_width / 2
        self.segment2 = Line(Point(cx - tx*half_width, cy - ty*half_width),
                             Point(cx + tx*half_width, cy + ty*half_width))
        self.segment2.setFill(self.color2)
        self.segment2.setWidth(4)
        self.segment2.draw(self.window)
        # atualiza os dados geométricos do portal com o novo centro
        self.data2 = (cx, cy, nx, ny, tx, ty)

    def _in_zone(self, ball, ball_r, portal_data):
        cx, cy, nx, ny, tx, ty = portal_data
        dx = ball.getx() - cx
        dy = ball.gety() - cy
        normal_dist  = abs(dx*nx + dy*ny)    # perpendicular distance to portal
        tangent_dist = abs(dx*tx + dy*ty)    # distance along portal
        # bola na zona se próxima o suficiente em ambas as direções
        return normal_dist <= ball_r and tangent_dist <= self.portal_width / 2

    def _teleport(self, ball, ball_r, entry, exit_portal):
        _, _, entry_nx, entry_ny, entry_tx, entry_ty = entry
        exit_cx, exit_cy, exit_nx, exit_ny, exit_tx, exit_ty = exit_portal

        v_normal  = ball.xvel * entry_nx + ball.yvel * entry_ny    # normal component
        v_tangent = ball.xvel * entry_tx + ball.yvel * entry_ty    # tangential component

        # preserva modulo da velocidade quando sai do segundo portal
        ball.xvel = v_normal * exit_nx + v_tangent * exit_tx
        ball.yvel = v_normal * exit_ny + v_tangent * exit_ty

        # posiciona a bola na saída do segundo portal
        ball.xpos = exit_cx + exit_nx * (ball_r + 0.5)
        ball.ypos = exit_cy + exit_ny * (ball_r + 0.5)

    def apply(self, ball, ball_r):
        # verifica entrada no portal 1: produto escalar positivo significa movimento na direção da normal
        _, _, n1x, n1y, _, _ = self.data1
        if self._in_zone(ball, ball_r, self.data1):
            if ball.xvel * n1x + ball.yvel * n1y > 0:  # ball entering p1
                self._teleport(ball, ball_r, self.data1, self.data2)
                return True

        # verifica entrada no portal 2
        _, _, n2x, n2y, _, _ = self.data2
        if self._in_zone(ball, ball_r, self.data2):
            if ball.xvel * n2x + ball.yvel * n2y > 0:  # ball entering p2
                self._teleport(ball, ball_r, self.data2, self.data1)
                return True

        # nenhum portal ativado neste passo
        return False



from tkinter import filedialog
from graphics import *
from entities import Button


"""
Menu — ecrã inicial do simulador com os quatro cenários disponíveis.
o utilizador seleciona o cenário desejado numa grelha e clica em START para abrir.
também oferece um botão de saída para fechar o programa limpo.
"""
class Menu:
    def __init__(self, win):
        self.win = win
        self.sel = None
        self._draw_grid()
        self._draw_numbers()
        self._draw_start()
        self._draw_quit()

    # desenha a grelha de seleção dos quatro cenários
    def _draw_grid(self):
        grid = Rectangle(Point(0.5, 2.5), Point(5.5, 7.5))
        grid.setFill("white")
        grid.draw(self.win)
        Line(Point(0.5, 5.0), Point(5.5, 5.0)).draw(self.win)
        Line(Point(3.0, 2.5), Point(3.0, 7.5)).draw(self.win)

    # coloca os números 1 a 4 em cada célula da grelha
    def _draw_numbers(self):
        self.nums = []
        for i, (x, y) in enumerate([(1.75, 6.25), (4.25, 6.25), (1.75, 3.75), (4.25, 3.75)]):
            t = Text(Point(x, y), str(i + 1))
            t.setSize(18)
            t.setStyle("bold")
            t.draw(self.win)
            self.nums.append(t)

    # desenha o botão circular vermelho START no centro
    def _draw_start(self):
        start = Circle(Point(3.0, 5.0), 0.9)
        start.setFill("red3")
        start.setOutline("darkred")
        start.setWidth(3)
        start.draw(self.win)
        txt = Text(Point(3.0, 5.0), "START")
        txt.setFill("white")
        txt.setStyle("bold")
        txt.setSize(13)
        txt.draw(self.win)

    # cria o botão de saída na parte inferior
    def _draw_quit(self):
        self.btn = Button(self.win, Point(3.0, 1.25), 4.0, 0.8, "QUIT")
        self.btn.activate()

    # determina qual célula foi clicada e destaca o número selecionado
    def _select(self, x, y):
        if x <= 3.0 and y >= 5.0:
            num = 1
        elif x >= 3.0 and y >= 5.0:
            num = 2
        elif x <= 3.0:
            num = 3
        else:
            num = 4
        for t in self.nums:
            t.setFill("black")
            t.setSize(18)
        self.nums[num - 1].setFill("red")
        self.nums[num - 1].setSize(28)
        self.sel = num

    # placeholder substituído em modular.py para abrir o cenário real
    def _abre_cenario(self, num):
        w = GraphWin(f"Cenario {num}", 600, 450)
        w.setBackground("lightblue")
        try:
            w.getMouse()
            w.close()
        except GraphicsError:
            pass

    # loop principal do menu: detetar cliques e reagir conforme a área
    def run(self):
        while True:
            try:
                p = self.win.getMouse()
            except GraphicsError:
                break
            x, y = p.getX(), p.getY()
            if (x - 3.0) ** 2 + (y - 5.0) ** 2 <= 0.81:
                if self.sel is not None:
                    self._abre_cenario(self.sel)
            elif self.btn.clicked(p):
                self.win.close()
                break
            elif 0.5 <= x <= 5.5 and 2.5 <= y <= 7.5:
                self._select(x, y)


"""
start_trajectory — prepara um novo registo de trajetória antes de lançar a bola.
devolve a data/hora de início e listas vazias prontas a receber os pontos gravados.
deve ser chamada sempre que se inicia um novo lançamento.
"""
# inicializa a data/hora de início e as listas de pontos da trajetória
def start_trajectory():
    return datetime.now(), 0.0, [], [], []

"""
record_point — guarda a posição atual da bola (x, y) nas listas de trajetória.
acrescenta o instante de tempo atual e avança o contador em cada chamada.
é chamada em cada frame enquanto a bola está em voo.
"""
# acrescenta um novo ponto (t, x, y) às listas e avança o contador de tempo
def record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual, bola_x, bola_y):
    trajectory_t.append(round(tempo_atual, 4))
    trajectory_x.append(round(bola_x, 4))
    trajectory_y.append(round(bola_y, 4))
    tempo_atual = round(tempo_atual + 0.002, 4)
    return tempo_atual

"""
save_trajectory — exporta a trajetória gravada para um ficheiro de texto escolhido pelo utilizador.
abre uma janela de diálogo para selecionar o destino e formata os dados em quatro linhas.
escreve data, tempos e coordenadas x e y separadas por espaços.
"""
# guarda a trajetória num ficheiro de texto escolhido pelo utilizador
def save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio):
    # abre a janela de diálogo para selecionar o destino do ficheiro
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    nome_ficheiro = filedialog.asksaveasfilename(
         defaultextension=".txt",
         filetypes=[("Ficheiros de Texto", "*.txt"), ("Todos os Ficheiros", "*.*")],
         title="Guardar Trajetória",
         parent=root
    )

    if not nome_ficheiro:
        return

    # converte as listas em arrays numpy
    arr_t = np.array(trajectory_t)
    arr_x = np.array(trajectory_x)
    arr_y = np.array(trajectory_y)

    # formata cada conjunto de valores como uma string separada por espaços
    data_hora_str = data_hora_inicio.strftime("%c")
    tempos_str    = " ".join(str(t) for t in arr_t)
    xs_str        = " ".join(str(x) for x in arr_x)
    ys_str        = " ".join(str(y) for y in arr_y)

    # escreve data/hora, tempos e coordenadas x e y em linhas separadas
    with open(nome_ficheiro, "w") as f:
        f.write(data_hora_str + "\n")
        f.write(tempos_str    + "\n")
        f.write(xs_str        + "\n")
        f.write(ys_str        + "\n")
