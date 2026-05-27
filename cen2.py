from graphics import *
from Projectiles import *
from entities import *
import time
from gravar_trajetoria import *


def cen2():
    win2 = GraphWin(title="Title", width=500, height=500, autoflush=False)
    win2.setCoords(-15, -5, 15, 20)
    left_limit = -12
    parabola(left_limit, win2)

    message = None
    tracker = None
    quit_button = None
    quit_button = Button(win2, Point(0, 18), 3, 2, "QUIT")
    while tracker is None:

        droppoint = win2.checkMouse()

        if droppoint is not None:
            yvalue = parabola(droppoint.getX(), win2, draw=False)
            if left_limit < droppoint.getX() < -left_limit and droppoint.getY() > yvalue:

                xpos = droppoint.getX()
                ypos = droppoint.getY()
                tracker = ShotTracker1(xpoint=xpos, ypoint=ypos, win=win2, color="red", outline="black", r=1,
                                       scalar=0.1134, yoffset=1.05)
                quit_button.activate()
            else:
                if message is not None:
                    message.undraw()
                message = Text(Point(0, 15), "Can't launch the ball outside of trajectory.")
                message.draw(win2)

        time.sleep(0.05)

    # inicializa a gravação da trajetória antes do loop principal
    data_hora_inicio, tempo_atual, trajetoria_t, trajetoria_x, trajetoria_y = start_trajectory()

    while win2.isOpen():
        point = win2.checkMouse()
        if point is not None:
            if quit_button.clicked(point):
                quit_button.deactivate()
                win2.update()
                time.sleep(0.3)

                # apresenta a opção de gravar a trajetória antes de fechar
                aviso_gravar = Text(Point(0, 7), "Press 'G' to save or any other key to continue")
                aviso_gravar.setTextColor("red")
                aviso_gravar.setStyle("bold")
                aviso_gravar.draw(win2)

                tecla_pressionada = win2.getKey()
                aviso_gravar.undraw()

                if tecla_pressionada in ["G", "g"]:
                    save_trajectory(win2, trajetoria_t, trajetoria_x, trajetoria_y, data_hora_inicio, 500, 500)

                win2.close()
                break

        tracker.update_tracker(0.05)
        # regista a posição atual da bola na trajetória
        tempo_atual = record_point(trajetoria_t, trajetoria_x, trajetoria_y, tempo_atual, tracker.getx(), tracker.gety())
        time.sleep(0.05)
# cen2()
