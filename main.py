from graphics import *
from Projectiles import Projectile, ShotTracker
from entities import *
from button import Button
import time
import trajetoria

<<<<<<< HEAD
#define um valor placeholder para as variáveis
angle, vel0, h0, interval=20, 40, 48, 0.1
win=GraphWin("Basketball Game", 400, 400, autoflush=False)
win.setCoords(-10, -10, 210, 155)
#cria a linha de base
marked_distance_line=Static(center=Point(100, 0), shape="line", color="black", outline="black", window=win)


#cria o cesto
basket=Static(center=Point(160, 100), shape="basket", radius=3, color="slategrey", outline="black", window=win, offset=40)
#posição da bola
stickman_hand_height=48
stickman_right_disloc=23
#cria o contador
scoreboard=ScoreBoard(win)

#cria o jogador 
player = StickMan(win)
#cria uma janela para inputar os valores
while win.isOpen():
=======
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

def abre_cenario(num):
    w = GraphWin("Cenario {}".format(num), 600, 450)
    w.setBackground("lightblue")
    try:
        w.getMouse()
        w.close()
    except GraphicsError:
        pass
>>>>>>> fdbbda5fd04bb35a666cccee24234c93d1cef227

# --- Menu ---
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
<<<<<<< HEAD
    elif option=="Fire!":
        angle, vel0=v_window.collect_values()
       
        tracker = ShotTracker1(xpoint=stickman_right_disloc, win=win, color="orange", outline="black", r=6, ypoint=stickman_hand_height, angle=angle, vel0=vel0)
        player.shoot(win)

        marcou_ponto=False
        while 0<=tracker.gety() and -10<=tracker.getx()<=220:
            tracker.update_tracker(1/10)
            #verifica se marca ponto
            if not marcou_ponto and 163 < tracker.getx() < 197 and 95 <= tracker.gety() <= 105:
                
                    scoreboard.update_score()
                    marcou_ponto=True
                    scoreboard.message.undraw()
                    scoreboard.unecessary_cheers(win)

            win.update()
            update(20)
        tracker.destroy()
        player.clear_arms()
        player.create_arms(win)
        win.update()


#win.update()
    if win.checkMouse():
        win.close()
=======
    x, y = p.getX(), p.getY()
    if (x - 3.0)**2 + (y - 5.0)**2 <= 0.81:
        if sel is not None:
            menu.close()
            if sel == 1:
                cenario1()
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
>>>>>>> fdbbda5fd04bb35a666cccee24234c93d1cef227
