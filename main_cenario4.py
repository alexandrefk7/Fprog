from graphics import *
from Projectiles import Projectile, ShotTracker1
from entities import *
from button import Button, BotaoCircular
from math import cos, sin, atan, sqrt
import trajetoria2
import colisoes
from portais import ParDePortais


# ─── Cenário 1 com Colisões ───────────────────────────────────────────────────
def cenario1() :
    BALL_R = 6
    ARO_R  = 3
    WALL_X = 205

    angle, vel0, h0 = 20, 40, 48
    win = GraphWin("Basketball Game", 400, 400, autoflush=False)
    win.setCoords(-10, -10, 210, 155)
    win.master.geometry("+50+100")
    create_line(win)
    create_basket(win)
    Line(Point(WALL_X, -10), Point(WALL_X, 155)).draw(win)
    scoreboard = ScoreBoard(win)
    player = StickMan(win)

    while win.isOpen():
        v_window = InputDialog(angle, vel0)
        option = v_window.interaction()
        v_window.close()
        win.master.deiconify()
        win.master.lift()
        if option == "Quit":
            break
        elif option == "Fire!":
            angle, vel0 = v_window.collect_values()

        data_inicio, tempos, xs, ys, t = trajetoria2.iniciar()
        tracker = ShotTracker(angle, vel0, h0, win)
        player.shoot(win)
        marcou_ponto = False

        while win.isOpen():
            trajetoria2.registar(tempos, xs, ys, t, tracker)
            tracker.update_tracker(0.1)

            colisoes.colisao_chao(tracker, BALL_R)
            colisoes.colisao_parede(tracker, BALL_R, WALL_X)
            colisoes.colisao_circulo(tracker, BALL_R, 160, 100, ARO_R)
            colisoes.colisao_circulo(tracker, BALL_R, 200, 100, ARO_R)

            if not marcou_ponto and 160 < tracker.getx() < 200 and 90 <= tracker.gety() <= 110:
                scoreboard.update_score()
                marcou_ponto = True

            t += 0.1
            update(25)

            if tracker.getx() < -10:
                break
            if tracker.xvel**2 + tracker.yvel**2 < 0.25:
                break

        tracker.destroy()
        trajetoria2.janela_gravar(data_inicio, tempos, xs, ys)

    if win.isOpen():
        win.close()


# ─── Cenário 2 ────────────────────────────────────────────────────────────────
SCALAR = 0.1

def desenha_parabola(win, x_max=12):
    x = -x_max
    while x < x_max:
        x2 = x + 0.2
        Line(Point(x, SCALAR*x**2), Point(x2, SCALAR*x2**2)).draw(win)
        x += 0.2

class Roller:
    def __init__(self, xpos):
        self.xpos = xpos
        self.ypos = SCALAR * xpos**2
        self.tan_vel = 0
        self.xvel = 0

    def update(self, interval):
        slope = 2 * SCALAR * self.xpos
        angle = atan(slope)
        tan_accer = -9.8 * sin(angle)
        self.tan_vel += tan_accer * interval
        self.xvel = self.tan_vel * cos(angle)
        self.xpos += interval * self.xvel
        self.ypos = SCALAR * self.xpos**2

    def getx(self):
        return self.xpos

    def gety(self):
        return self.ypos

class RollerTracker(Roller):
    R = 0.6

    def _centro(self):
        slope = 2 * SCALAR * self.xpos
        length = sqrt(1 + slope**2)
        cx = self.xpos - self.R * slope / length
        cy = self.ypos + self.R / length
        return cx, cy

    def __init__(self, xpos, win):
        super().__init__(xpos)
        cx, cy = self._centro()
        self.marker = Circle(Point(cx, cy), self.R)
        self.marker.setFill("orange")
        self.marker.setOutline("black")
        self.marker.draw(win)

    def update_tracker(self, interval):
        self.update(interval)
        cx, cy = self._centro()
        center = self.marker.getCenter()
        self.marker.move(cx - center.getX(), cy - center.getY())

    def destroy(self):
        self.marker.undraw()

def cenario2():
    win = GraphWin("Cenario 2 - Rolamento", 500, 500, autoflush=False)
    win.setCoords(-15, -2, 15, 20)
    win.master.geometry("+50+100")
    desenha_parabola(win)
    btn_quit = Button(win, Point(0, 18.5), 5, 1.2, "QUIT")
    btn_quit.activate()
    msg = Text(Point(0, 17), "Clique para escolher a altura inicial")
    msg.draw(win)

    while win.isOpen():
        try:
            p = win.getMouse()
        except GraphicsError:
            break
        if btn_quit.clicked(p):
            break

        h = max(p.getY(), 0.5)
        h = min(h, 14.0)
        x_start = -(h / SCALAR) ** 0.5

        data_inicio, tempos, xs, ys, t = trajetoria2.iniciar()
        tracker = RollerTracker(x_start, win)
        prev_xpos = x_start
        a_correr = True
        sair = False

        while a_correr and win.isOpen():
            trajetoria2.registar(tempos, xs, ys, t, tracker, casas_t=2)

            prev_xpos = tracker.getx()
            tracker.update_tracker(0.05)
            curr_xpos = tracker.getx()

            if prev_xpos * curr_xpos < 0:
                tracker.tan_vel *= sqrt(0.8)

            energy_h = tracker.gety() + tracker.tan_vel**2 / (2 * 9.8)
            if energy_h < 0.02:
                a_correr = False

            t += 0.05
            update(25)

            chk = win.checkMouse()
            if chk and btn_quit.clicked(chk):
                a_correr = False
                sair = True

        tracker.destroy()
        trajetoria2.janela_gravar(data_inicio, tempos, xs, ys)
        if sair:
            break
        msg.setText("Clique para nova simulacao")

    if win.isOpen():
        win.close()


# ─── Cenário 4 ────────────────────────────────────────────────────────────────
def atualiza_parede_meio(win, parede_x, p1_cy, meia, linha_baixo, linha_cima):
    """Função auxiliar para apagar e redesenhar o muro do portal azul sem repetir código"""
    if linha_baixo is not None:
        linha_baixo.undraw()
        linha_cima.undraw()
    nova_linha_baixo = Line(Point(parede_x, -10), Point(parede_x, p1_cy - meia))
    nova_linha_cima = Line(Point(parede_x, p1_cy + meia), Point(parede_x, 155))
    nova_linha_baixo.draw(win)
    nova_linha_cima.draw(win)
    return nova_linha_baixo, nova_linha_cima


def cenario4():
    BALL_R = 6
    ARO_R = 3
    WALL_X = 205
    PAREDE_X = 100
    PORTAL_LARG = 20
    PASSO = 5

    p1_cy = 50
    p2_cx, p2_cy = 130, 85

    angle, vel0, h0 = 35, 40, 48
    win = GraphWin("Basketball Game - Portais", 400, 400, autoflush=False)
    win.setCoords(-10, -10, 210, 155)

    create_line(win)
    create_basket(win)
    Line(Point(WALL_X, -10), Point(WALL_X, 155)).draw(win)

    # Desenho inicial do muro usando a função auxiliar
    meia = PORTAL_LARG / 2
    linha_muro_baixo, linha_muro_cima = atualiza_parede_meio(win, PAREDE_X, p1_cy, meia, None, None)

    # Painel de controlo via botões gráficos
    btn_p1_up = Button(win, Point(30, 145), 35, 8, "Azul Cima")
    btn_p1_dn = Button(win, Point(30, 135), 35, 8, "Azul Baixo")

    btn_p2_esq = Button(win, Point(180, 145), 35, 8, "Lar Esq")
    btn_p2_dir = Button(win, Point(180, 135), 35, 8, "Lar Dir")

    btn_fire = Button(win, Point(105, -2), 40, 8, "ATIRAR")

    for b in [btn_p1_up, btn_p1_dn, btn_p2_esq, btn_p2_dir, btn_fire]:
        b.activate()

    portais = ParDePortais(
        win,
        Point(PAREDE_X, p1_cy), (1, 0),
        Point(p2_cx, p2_cy), (1, 1),
        largura=PORTAL_LARG
    )

    scoreboard = ScoreBoard(win)
    player = StickMan(win)

    while win.isOpen():

        # --- 1. FASE DE AJUSTE DOS PORTAIS (Via Cliques) ---
        msg = Text(Point(105, 10), "Use os botões para ajustar os portais e Atirar")
        msg.setFill("blue")
        msg.draw(win)

        while win.isOpen():
            p = win.getMouse()

            if btn_p1_up.clicked(p) and p1_cy + PASSO <= 143:
                portais.mover_p1(0, PASSO)
                p1_cy += PASSO
                linha_muro_baixo, linha_muro_cima = atualiza_parede_meio(win, PAREDE_X, p1_cy, meia, linha_muro_baixo,
                                                                         linha_muro_cima)
            elif btn_p1_dn.clicked(p) and p1_cy - PASSO >= 12:
                portais.mover_p1(0, -PASSO)
                p1_cy -= PASSO
                linha_muro_baixo, linha_muro_cima = atualiza_parede_meio(win, PAREDE_X, p1_cy, meia, linha_muro_baixo,
                                                                         linha_muro_cima)
            elif btn_p2_esq.clicked(p) and p2_cx - PASSO >= PAREDE_X + 20:
                portais.mover_p2(-PASSO, 0)
                p2_cx -= PASSO
            elif btn_p2_dir.clicked(p) and p2_cx + PASSO <= WALL_X - 15:
                portais.mover_p2(PASSO, 0)
                p2_cx += PASSO
            elif btn_fire.clicked(p):
                break

            update(25)

        msg.undraw()

        # --- 2. FASE DO INPUT DIALOG ---
        v_window = InputDialog(angle, vel0)
        option = v_window.interaction()
        v_window.close()

        if option == "Quit":
            break
        elif option == "Fire!":
            angle, vel0 = v_window.collect_values()

        # --- 3. FASE DO VOO
        data_inicio, tempos, xs, ys, t = trajetoria2.iniciar()

        tracker = ShotTracker1(0, win, "orange", "black", BALL_R, h0, angle, vel0)

        player.shoot(win)
        marcou_ponto = False

        while win.isOpen():
            trajetoria2.registar(tempos, xs, ys, t, tracker)
            tracker.update_tracker(0.1)

            if not portais.aplicar(tracker, BALL_R):
                na_zona_portal = (p1_cy - meia <= tracker.gety() <= p1_cy + meia)
                pela_esquerda = tracker.getx() <= PAREDE_X + BALL_R
                if not na_zona_portal and pela_esquerda:
                    colisoes.colisao_parede(tracker, BALL_R, PAREDE_X)

            colisoes.colisao_chao(tracker, BALL_R)
            colisoes.colisao_parede(tracker, BALL_R, WALL_X)

            colisoes.colisao_circulo(tracker, BALL_R, 160, 100, ARO_R)
            colisoes.colisao_circulo(tracker, BALL_R, 200, 100, ARO_R)

            if not marcou_ponto and 160 < tracker.getx() < 200 and 90 <= tracker.gety() <= 110:
                scoreboard.update_score()
                marcou_ponto = True

            # Movimentação dos portais por clique durante o tempo de voo
            p_voo = win.checkMouse()
            if p_voo:
                if btn_p1_up.clicked(p_voo) and p1_cy + PASSO <= 143:
                    portais.mover_p1(0, PASSO)
                    p1_cy += PASSO
                    linha_muro_baixo, linha_muro_cima = atualiza_parede_meio(win, PAREDE_X, p1_cy, meia,
                                                                             linha_muro_baixo, linha_muro_cima)
                elif btn_p1_dn.clicked(p_voo) and p1_cy - PASSO >= 12:
                    portais.mover_p1(0, -PASSO)
                    p1_cy -= PASSO
                    linha_muro_baixo, linha_muro_cima = atualiza_parede_meio(win, PAREDE_X, p1_cy, meia,
                                                                             linha_muro_baixo, linha_muro_cima)
                elif btn_p2_esq.clicked(p_voo) and p2_cx - PASSO >= PAREDE_X + 20:
                    portais.mover_p2(-PASSO, 0)
                    p2_cx -= PASSO
                elif btn_p2_dir.clicked(p_voo) and p2_cx + PASSO <= WALL_X - 15:
                    portais.mover_p2(PASSO, 0)
                    p2_cx += PASSO

            t += 0.1
            update(25)

            # Término do lançamento se a bola sair pela esquerda ou atingir o limite de 10 segundos
            if tracker.getx() < -10 or t >= 10.0:
                break
            if tracker.xvel ** 2 + tracker.yvel ** 2 < 0.25:
                break

        tracker.destroy()
        trajetoria2.janela_gravar(data_inicio, tempos, xs, ys)

    if win.isOpen():
        win.close()
# ─── Cenário 3 (placeholder) ──────────────────────────────────────────────────



# ─── Menu ─────────────────────────────────────────────────────────────────────
menu = GraphWin("Simulacao de Fisica", 300, 400)
menu.setCoords(0, 0, 6, 8)
menu.setBackground("slategray")

posicoes = [(1.75, 6.25), (4.25, 6.25), (1.75, 3.75), (4.25, 3.75)]
btns_cen = []
for i in range(4):
    x, y = posicoes[i]
    b = Button(menu, Point(x, y), 2.5, 2.5, str(i + 1))
    b.label.setSize(18)
    b.label.setStyle("bold")
    b.activate()
    btns_cen.append(b)

btn_start = BotaoCircular(menu, Point(3.0, 5.0), 0.9, "START")

btn_quit = Button(menu, Point(3.0, 1.25), 4.0, 0.8, "QUIT")
btn_quit.activate()

sel = None
while True:
    try:
        p = menu.getMouse()
    except GraphicsError:
        break
    if btn_start.clicked(p):
        if sel is not None:
            menu.close()
            if sel == 1:
                cenario1()
            elif sel == 2:
                cenario2()
            elif sel == 4:
                cenario4()
            else:
                abre_cenario(sel)
            break
    elif btn_quit.clicked(p):
        menu.close()
        break
    else:
        for i in range(4):
            if btns_cen[i].clicked(p):
                for b in btns_cen:
                    b.rect.setFill("lightgray")
                btns_cen[i].rect.setFill("lightyellow")
                sel = i + 1
                break
