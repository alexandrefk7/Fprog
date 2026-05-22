from graphics import *
from Projectiles import Projectile, ShotTracker
from entities import *
from button import Button
from math import cos, sin, atan, sqrt
import time
import trajetoria

# ─── Cenário 2: Física do Rolamento (baseado no trabalho do colega) ────────────
SCALAR = 0.1  # parábola: y = SCALAR * x^2

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
    R = 0.6  # raio da bola

    def _centro(self):
        # Desloca o centro da bola pelo raio na direção da normal à parábola
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


# ─── Cenário 1 ────────────────────────────────────────────────────────────────
def cenario1():
    angle, vel0, h0 = 20, 40, 48
    win = GraphWin("Basketball Game", 400, 400, autoflush=False)
    win.setCoords(-10, -10, 210, 155)
    win.master.geometry("+50+100")
    create_line(win)
    create_basket(win)
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
        data_inicio = time.ctime()
        tempos, xs, ys = [], [], []
        t = 0
        tracker = ShotTracker(angle, vel0, h0, win)
        player.shoot(win)
        marcou_ponto = False
        while 0 <= tracker.gety() and -10 <= tracker.getx() <= 220:
            tempos.append(round(t, 1))
            xs.append(round(tracker.getx(), 2))
            ys.append(round(tracker.gety(), 2))
            tracker.update_tracker(0.1)
            if not marcou_ponto and 160 < tracker.getx() < 200 and 90 <= tracker.gety() <= 110:
                scoreboard.update_score()
                marcou_ponto = True
            t += 0.1
            update(25)
        tracker.destroy()
        trajetoria.janela_gravar(data_inicio, tempos, xs, ys)
    if win.isOpen():
        win.close()


# ─── Cenário 2 ────────────────────────────────────────────────────────────────
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

        # Altura inicial a partir do clique (limitada para a bola não sair do ecrã)
        h = max(p.getY(), 0.5)
        h = min(h, 14.0)
        x_start = -(h / SCALAR) ** 0.5  # começa no lado esquerdo

        data_inicio = time.ctime()
        tempos, xs, ys = [], [], []
        t = 0

        tracker = RollerTracker(x_start, win)
        prev_xpos = x_start
        a_correr = True
        sair = False

        while a_correr and win.isOpen():
            tempos.append(round(t, 2))
            xs.append(round(tracker.getx(), 2))
            ys.append(round(tracker.gety(), 2))

            prev_xpos = tracker.getx()
            tracker.update_tracker(0.05)
            curr_xpos = tracker.getx()

            # Perda de 20% de energia a cada meio ciclo (na passagem pelo fundo)
            if prev_xpos * curr_xpos < 0:
                tracker.tan_vel *= sqrt(0.8)

            # Parar quando a energia for negligenciável (bola imobilizada no fundo)
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
        trajetoria.janela_gravar(data_inicio, tempos, xs, ys)
        if sair:
            break
        msg.setText("Clique para nova simulacao")

    if win.isOpen():
        win.close()


# ─── Cenários em desenvolvimento ──────────────────────────────────────────────
def abre_cenario(num):
    w = GraphWin("Cenario {}".format(num), 600, 450)
    w.setBackground("lightblue")
    try:
        w.getMouse()
        w.close()
    except GraphicsError:
        pass


# ─── Menu ─────────────────────────────────────────────────────────────────────
menu = GraphWin("Simulacao de Fisica", 300, 400)
menu.setCoords(0, 0, 6, 8)
menu.setBackground("slategray")

grid = Rectangle(Point(0.5, 2.5), Point(5.5, 7.5))
grid.setFill("white")
grid.draw(menu)
Line(Point(0.5, 5.0), Point(5.5, 5.0)).draw(menu)
Line(Point(3.0, 2.5), Point(3.0, 7.5)).draw(menu)

nums = []
for i, (x, y) in enumerate([(1.75, 6.25), (4.25, 6.25), (1.75, 3.75), (4.25, 3.75)]):
    t = Text(Point(x, y), str(i + 1))
    t.setSize(18)
    t.setStyle("bold")
    t.draw(menu)
    nums.append(t)

start = Circle(Point(3.0, 5.0), 0.9)
start.setFill("red3")
start.setOutline("darkred")
start.setWidth(3)
start.draw(menu)
txt = Text(Point(3.0, 5.0), "START")
txt.setFill("white")
txt.setStyle("bold")
txt.setSize(13)
txt.draw(menu)

btn = Button(menu, Point(3.0, 1.25), 4.0, 0.8, "QUIT")
btn.activate()

sel = None
while True:
    try:
        p = menu.getMouse()
    except GraphicsError:
        break
    x, y = p.getX(), p.getY()
    if (x - 3.0)**2 + (y - 5.0)**2 <= 0.81:
        if sel is not None:
            menu.close()
            if sel == 1:
                cenario1()
            elif sel == 2:
                cenario2()
            else:
                abre_cenario(sel)
            break
    elif btn.clicked(p):
        menu.close()
        break
    elif 0.5 <= x <= 5.5 and 2.5 <= y <= 7.5:
        if x <= 3.0 and y >= 5.0: num = 1
        elif x >= 3.0 and y >= 5.0: num = 2
        elif x <= 3.0: num = 3
        else: num = 4
        for t in nums:
            t.setFill("black")
            t.setSize(18)
        nums[num - 1].setFill("red")
        nums[num - 1].setSize(28)
        sel = num
