from graphics import *
from Projectiles import *
from entities import *
import time


"""
cen2 — cenário de bola rolando pela parábola: o utilizador clica na curva para posicionar a bola.
a bola desliza pela parábola seguindo a física do rolamento; pode ser reposicionada durante o percurso.
permite gravar a trajetória no final quando a bola perde toda a velocidade.
"""
def cen2():
    win2 = GraphWin(title="Title", width=500, height=500, autoflush=False)
    win2.setCoords(-15, -5, 15, 20)
    left_limit = -12
    parabola(left_limit, win2)

    message = None
    tracker = None
    quit_button = Button(win2, Point(0, 18), 3, 2, "QUIT")

    # aguarda o clique do utilizador para posicionar a bola na parábola
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

                if message is not None:
                    message.undraw()
                    message = None
            else:
                if message is not None:
                    message.undraw()
                message = Text(Point(0, 15), "Can't launch the ball outside of trajectory.")
                message.draw(win2)

        time.sleep(0.05)

    # inicia o registo da trajetória quando a bola está pronta
    data_hora_inicio, tempo_atual, trajetoria_t, trajetoria_x, trajetoria_y = start_trajectory()

    # loop principal: atualiza física, deteta cliques e verifica paragem
    while win2.isOpen():
        point = win2.checkMouse()

        if point is not None:
            # 1. Did they click quit?
            if quit_button.clicked(point):
                quit_button.deactivate()
                win2.update()
                time.sleep(0.3)
                aviso_gravar = Text(Point(0, 7), "Press 'G' to save or any other key to continue")
                aviso_gravar.setTextColor("red")
                aviso_gravar.setStyle("bold")
                aviso_gravar.draw(win2)
                win2.update()
                tecla_pressionada = win2.getKey()
                aviso_gravar.undraw()
                if tecla_pressionada in ["G", "g"]:
                    save_trajectory(trajetoria_t, trajetoria_x, trajetoria_y, data_hora_inicio)
                win2.close()
                break

            elif tracker.on_route and abs(tracker.xvel) < 5:
                yvalue = parabola(point.getX(), win2, draw=False)

                if left_limit < point.getX() < -left_limit and point.getY() > yvalue:

                    tracker.destroy()

                    tracker = ShotTracker1(xpoint=point.getX(), ypoint=point.getY(), win=win2, color="red",
                                           outline="black", r=1, scalar=0.1134, yoffset=1.05)


                else:
                    if message is not None:
                        message.undraw()
                    message = Text(Point(0, 15), "Can't launch the ball outside of trajectory.")
                    message.draw(win2)
        tracker.update_tracker(0.05)
        tempo_atual = record_point(trajetoria_t, trajetoria_x, trajetoria_y, tempo_atual, tracker.getx(), tracker.gety())

        # condição de paragem: velocidade abaixo do limiar
        if tracker.xvel ** 2 + tracker.yvel ** 2 < 0.1:
            aviso_gravar = Text(Point(0, 7), "Press 'G' to save or any other key to continue")
            aviso_gravar.setTextColor("red")
            aviso_gravar.setStyle("bold")
            aviso_gravar.draw(win2)
            win2.update()
            tecla_pressionada = win2.getKey()
            aviso_gravar.undraw()
            if tecla_pressionada in ["G", "g"]:
                save_trajectory(win2, trajetoria_t, trajetoria_x, trajetoria_y, data_hora_inicio, 500, 500)
            win2.close()
            break

        win2.update()
        time.sleep(0.05)


