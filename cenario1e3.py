from engine import *
from entities import *
from cen2 import cen2
from gravar_trajetoria import *
import time


def cen1():
    angle, vel0, h0, interval = 20, 40, 48, 0.1

    win = GraphWin("Basketball Game", 400, 400, autoflush=False)
    win.setCoords(-10, -10, 210, 155)

    Line(Point(205, -10), Point(205, 155)).draw(win)

    # cria a linha de base e o cesto
    marked_distance_line = Static(center=Point(100, 0), shape="metric", color="black", outline="black", window=win)
    basket = Static(center=Point(160, 100), shape="basket", radius=3, color="slategrey", outline="black", window=win,
                    offset=40)

    #botao quit
    btn_quit = Button(win, Point(180, 140), 30, 10, "QUIT")
    btn_quit.activate()

    # posição da bola e placar
    stickman_hand_height = 48
    stickman_right_disloc = 23
    dt = 0.1
    scoreboard = ScoreBoard(Point(15, 150), Point(100, 140), win)
    player = StickMan(Point(5, 52), 0, "right", win)


    while win.isOpen():
        win.update()


        v_window = InputDialog(angle, vel0)
        option = v_window.interaction()

        if option == "Quit":
            v_window.close()
            break
        elif option == "Fire!":
            angle, vel0 = v_window.collect_values()
            v_window.close()

            # focos da janela
            win.master.lift()
            win.master.focus_force()
            win.update()
            win.bind_all("<Key>", win._onKey)

            # inicializa a gravação da trajetória
            data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

            tracker = ShotTracker1(xpoint=stickman_right_disloc, win=win, color="orange", outline="black", r=6,
                                   ypoint=stickman_hand_height, angle=angle, vel0=vel0, scalar=0)
            player.shoot(win)
            scored = False


            while 0 <= tracker.gety() and -10 <= tracker.getx() <= 220:
                tracker.update_tracker(dt)

                static_colision_detector(tracker, 6, px=0, py=0, normx=0, normy=1)
                static_colision_detector(tracker, 6, px=205, py=0, normx=-1, normy=0)
                static_colision_detector(tracker, 6, cenx=160, ceny=100, cenr=3)
                static_colision_detector(tracker, 6, cenx=200, ceny=100, cenr=3)

                # evitar ressaltos muito pequenos
                if tracker.gety() <= 6.5:
                    tracker.xvel *= 0.85
                    if abs(tracker.yvel) < 3:
                        tracker.yvel = 0

                # regista a posição atual da bola
                tempo_atual = record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual, tracker.getx(),
                                           tracker.gety())

                # verifica se marca ponto
                if not scored and 163 < tracker.getx() < 197 and 95 <= tracker.gety() <= 105:
                    scoreboard.update_score()
                    scored = True
                    scoreboard.message.undraw()
                    scoreboard.unecessary_cheers(win)


                p_voo = win.checkMouse()
                if p_voo and btn_quit.clicked(p_voo):
                    tracker.destroy()
                    if win.isOpen():
                        win.close()
                    return

                win.update()
                update(20)

                #pos colisao
                if tracker.xvel ** 2 + tracker.yvel ** 2 < 0.25:
                    break

            tracker.destroy()
            player.clear_arms()
            player.create_arms(win)

            # opcao de gravar
            aviso_gravar = Text(Point(100, 120), "Press 'G' to save or any other key to continue")
            aviso_gravar.setTextColor("red")
            aviso_gravar.setStyle("bold")
            aviso_gravar.draw(win)
            win.update()

            tecla_pressionada = None
            while win.isOpen():
                tecla_pressionada = win.checkKey()
                p_gravar = win.checkMouse()


                if p_gravar and btn_quit.clicked(p_gravar):
                    aviso_gravar.undraw()
                    if win.isOpen():
                        win.close()
                    return

                if tecla_pressionada:  # Sai do loop se carregar em qualquer tecla
                    break

                import time
                time.sleep(0.05)
                win.update()

            aviso_gravar.undraw()
            win.update()

            if tecla_pressionada in ["G", "g"]:
                save_trajectory(win, trajectory_t, trajectory_x, trajectory_y, data_hora_inicio, 400, 400)

    if win.isOpen():
        win.close()


def cen3():
    xscreen_limiter = 350
    yscreen_limiter = 200
    win3 = GraphWin("Basketball Game", 600, 400, autoflush=False)
    win3.setCoords(0, -10, xscreen_limiter, yscreen_limiter)
    # parabola
    parabola_finalx = 140
    parabola(0, win3, xoffset=90, yoffset=10, mirror_dif=-parabola_finalx, scalar=0.02)

    # cria paredes
    parabola_wall = Static(Point(parabola_finalx, 0), "wall", "black", "black", win3, 60)
    back_wall = Static(Point(xscreen_limiter - 10, 0), "wall", "black", "black", win3, yscreen_limiter)

    # cria o stickman
    stickman = StickMan(Point(290, 52), 0, "left", win3)

    # cria o cesto
    basket_left_center = Point(270, 120)
    basket = Static(center=basket_left_center, shape="basket", radius=3, color="slategrey", outline="black",
                    window=win3, offset=40)

    # cria o chão
    floor_line = Static(center=Point(0, 0), shape="line", color="black", outline="black", window=win3, offset=400)

    # cria a bola que rola
    parabola_ball = ShotTracker1(xpoint=10, ypoint=190, xoffset=90, yoffset=16.48, win=win3, color="green",
                                 outline="black", r=6, scalar=1.134 * 0.02)

    quit_button = Button(win3, Point(120, 180), 25, 20, "QUIT")
    quit_button.activate()

    scoreboard = ScoreBoard(Point(80, 185), Point(100, 140), win3)
    # condição que verifica se a bola foi lançada no final da parábola
    ball_is_thrown = False
    # condição para marcar ponto
    scored = False
    # condição que verifica a altura da bola
    is_above = False
    # cria tracker antes do loop para n haver problemas com o scope da variável porque eu não quero torná-la global
    launcher_ball = None
    player_ball = None

    # inicializa a gravação da trajetória
    data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

    while win3.isOpen():
        point = win3.checkMouse()
        if point is not None:
            if quit_button.clicked(point):
                quit_button.deactivate()
                win3.update()
                time.sleep(0.3)

                # apresenta a opção de gravar antes de fechar
                aviso_gravar = Text(Point(175, 180), "Press 'G' to save or any other key to continue")
                aviso_gravar.setTextColor("red")
                aviso_gravar.setStyle("bold")
                aviso_gravar.draw(win3)

                tecla_pressionada = win3.getKey()
                aviso_gravar.undraw()

                if tecla_pressionada in ["G", "g"]:
                    save_trajectory(win3, trajectory_t, trajectory_x, trajectory_y, data_hora_inicio, 600, 400)

                win3.close()
                break

        # ball_is_thrown verifica se a bola já atingiu o final da parábola
        if not ball_is_thrown:
            if parabola_ball.getx() >= parabola_finalx:
                parabola_ball.xpos = parabola_finalx

                parabola_ball.destroy()
                # assume que a velocidade final da bola obtém-se a partir da sua velocidade em x e do seu angulo final
                # evitando erros no cenário em que o cos fosse igual a 0
                try:
                    final_vel = parabola_ball.xvel / cos((-1) * parabola_ball.angle)
                except ZeroDivisionError:
                    final_vel = parabola_ball.xvel

                # cria a ilusão de uma nova bola a ser projetada
                launcher_ball = ShotTracker1(xpoint=parabola_finalx, ypoint=parabola_ball.gety(),
                                             xoffset=90, yoffset=16.48, win=win3, color="green",
                                             outline="black", r=6, scalar=0, vel0=final_vel * 1.67,
                                             angle=degrees(parabola_ball.angle))

                ball_is_thrown = True
            else:
                parabola_ball.update_tracker(0.1)
        #update da posicao
        if ball_is_thrown and launcher_ball is not None:

            # verifica a posicao da bola
            if parabola_finalx <= launcher_ball.getx() and launcher_ball.gety() < 200:
                left_limit = basket_left_center.getX() + basket.radius
                right_limit = basket_left_center.getX() + basket.radius + basket.offset

                if launcher_ball.gety() >= basket_left_center.getY():
                    is_above = True
                    if is_above and not scored and left_limit < launcher_ball.getx() < right_limit and basket_left_center.getY() - 5 < launcher_ball.gety() < basket_left_center.getY() + 5:
                        scored = True
                        scoreboard.update_score()
                launcher_ball.update_tracker(0.1)
                # regista a posição atual da bola lançada
                tempo_atual = record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual, launcher_ball.getx(), launcher_ball.gety())

        time.sleep(0.01)
        win3.update()
        update(60)


# cenário 1
# cen1()
# cenário 2
# cen2()
# cenário 3
#cen3()