from graphics import *
from entities import *
from engine import *
from gravar_trajetoria import *
from portais import PortalPair

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
    dt = 0.1

    win = GraphWin("Basketball Game - Portais", 400, 400, autoflush=False)
    win.setCoords(-10, -10, 210, 155)

    # Static
    marked_distance_line = Static(center=Point(100, 0), shape="metric", color="black", outline="black", window=win)
    basket = Static(center=Point(160, 100), shape="basket", radius=ARO_R, color="slategrey", outline="black",
                    window=win, offset=40)


    Line(Point(WALL_X, -10), Point(WALL_X, 155)).draw(win)

    # muro
    espessura = 8
    muro_estatico = Rectangle(Point(PAREDE_X, -10), Point(PAREDE_X + espessura, 155))
    muro_estatico.setFill("darkgray")
    muro_estatico.setOutline("black")
    muro_estatico.setWidth(1)
    muro_estatico.draw(win)

    meia = PORTAL_LARG / 2

    #painel de mover portais
    btn_p1_up = Button(win, Point(30, 140), 35, 8, "Azul Cima")
    btn_p1_dn = Button(win, Point(30, 130), 35, 8, "Azul Baixo")
    btn_p2_esq = Button(win, Point(180, 140), 35, 8, "Lar Esq")
    btn_p2_dir = Button(win, Point(180, 130), 35, 8, "Lar Dir")
    btn_fire = Button(win, Point(105, -2), 40, 8, "ATIRAR")
    quit_btn = Button(win, Point(185, 150), 35, 8, "QUIT")

    for b in [btn_p1_up, btn_p1_dn, btn_p2_esq, btn_p2_dir, btn_fire, quit_btn]:
        b.activate()

    #portais
    portais = PortalPair(
        win,
        Point(PAREDE_X - 1, p1_cy), (1, 0),
        Point(p2_cx, p2_cy), (0.5, 1),
        largura=PORTAL_LARG
    )

    #scoreboard e jogador
    scoreboard = ScoreBoard(Point(15, 150), Point(100, 140), win)
    player = StickMan(Point(5, 52), 0, "right", win)

    stickman_hand_height = 48
    stickman_right_disloc = 23

    data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

    while win.isOpen():


        msg = Text(Point(105, 10), "Use os botões para ajustar os portais e Atirar")
        msg.setFill("blue")
        msg.draw(win)

        while win.isOpen():
            p = win.getMouse()

            if btn_p1_up.clicked(p) and p1_cy + PASSO <= 143:
                portais.move_p1(0, PASSO)
                p1_cy += PASSO
            elif btn_p1_dn.clicked(p) and p1_cy - PASSO >= 12:
                portais.move_p1(0, -PASSO)
                p1_cy -= PASSO
            elif btn_p2_esq.clicked(p) and p2_cx - PASSO >= PAREDE_X + 20 + espessura:
                portais.move_p2(-PASSO, 0)
                p2_cx -= PASSO
            elif btn_p2_dir.clicked(p) and p2_cx + PASSO <= WALL_X - 15:
                portais.move_p2(PASSO, 0)
                p2_cx += PASSO
            elif btn_fire.clicked(p):
                break
            elif quit_btn.clicked(p):
                msg.undraw()
                aviso_gravar = Text(Point(100, 150), "Press 'G' to save or any other key to continue")
                aviso_gravar.setTextColor("red")
                aviso_gravar.setStyle("bold")
                aviso_gravar.draw(win)
                win.update()
                tecla_pressionada = win.getKey()
                aviso_gravar.undraw()
                if tecla_pressionada in ["G", "g"]:
                    save_trajectory(win, trajectory_t, trajectory_x, trajectory_y, data_hora_inicio, 400, 400)
                win.close()
                return

            win.update()
            update(25)

        msg.undraw()

        v_window = InputDialog(angle, vel0)
        option = v_window.interaction()

        if option == "Quit":
            v_window.close()
            break
        elif option == "Fire!":
            angle, vel0 = v_window.collect_values()


            v_window.close()

            win.master.lift()
            win.master.focus_force()
            win.update()
            win.bind_all("<Key>", win._onKey)

            # gravar trajet
            data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

            # gravar trajet
            data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

            tracker = ShotTracker1(
                xpoint=stickman_right_disloc,
                win=win,
                color="orange",
                outline="black",
                r=BALL_R,
                ypoint=stickman_hand_height,
                angle=angle,
                vel0=vel0,
                scalar=0
            )

            player.shoot(win)
            scored = False

            while 0 <= tracker.gety() and -10 <= tracker.getx() <= 220:
                tracker.update_tracker(dt)

                #registo de pontos
                tempo_atual = record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual, tracker.getx(),
                                           tracker.gety())

                # portais e colisoes
                if not portais.apply(tracker, BALL_R):
                    na_zona_portal = (p1_cy - meia <= tracker.gety() <= p1_cy + meia)
                    pela_esquerda = tracker.getx() <= PAREDE_X + BALL_R
                    if not na_zona_portal and pela_esquerda:
                        static_colision_detector(tracker, BALL_R, px=PAREDE_X, py=0, normx=-1, normy=0)

                static_colision_detector(tracker, BALL_R, px=0, py=0, normx=0, normy=1)
                static_colision_detector(tracker, BALL_R, px=WALL_X, py=0, normx=-1, normy=0)

                # colisao cesto
                static_colision_detector(tracker, BALL_R, cenx=160, ceny=100, cenr=ARO_R)
                static_colision_detector(tracker, BALL_R, cenx=200, ceny=100, cenr=ARO_R)


                if not scored and 163 < tracker.getx() < 197 and 95 <= tracker.gety() <= 105:
                    scoreboard.update_score()
                    scored = True
                    scoreboard.message.undraw()
                    scoreboard.unecessary_cheers(win)


                p_voo = win.checkMouse()
                if p_voo:
                    if btn_p1_up.clicked(p_voo) and p1_cy + PASSO <= 143:
                        portais.move_p1(0, PASSO)
                        p1_cy += PASSO
                    elif btn_p1_dn.clicked(p_voo) and p1_cy - PASSO >= 12:
                        portais.move_p1(0, -PASSO)
                        p1_cy -= PASSO
                    elif btn_p2_esq.clicked(p_voo) and p2_cx - PASSO >= PAREDE_X + 20 + espessura:
                        portais.move_p2(-PASSO, 0)
                        p2_cx -= PASSO
                    elif btn_p2_dir.clicked(p_voo) and p2_cx + PASSO <= WALL_X - 15:
                        portais.move_p2(PASSO, 0)
                        p2_cx += PASSO

                win.update()
                update(25)

                #evitar loops infinitos em ressaltos baixos
                if tracker.xvel ** 2 + tracker.yvel ** 2 < 0.25:
                    break

            tracker.destroy()

            # reset bracos
            player.clear_arms()
            player.create_arms(win)

            #mensagem de continuar
            aviso_gravar = Text(Point(100, 150), "Press 'G' to save or any other key to continue")
            aviso_gravar.setTextColor("red")
            aviso_gravar.setStyle("bold")
            aviso_gravar.draw(win)
            win.update()

            tecla_pressionada = win.getKey()
            aviso_gravar.undraw()
            win.update()

            if tecla_pressionada in ["G", "g"]:
                save_trajectory(win, trajectory_t, trajectory_x, trajectory_y, data_hora_inicio, 400, 400)

    if win.isOpen():
        win.close()