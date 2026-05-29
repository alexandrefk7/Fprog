from Projectiles import *
from entities import *
from cen2 import cen2
import time


"""
cen3 — cenário de basquetebol com parábola: a bola verde rola pela rampa e é lançada como projétil.
o jogador também lança a sua bola laranja podendo intercetá-la ou tentar fazer o cesto diretamente.
tem sistema de vidas e pontuação, e termina quando as vidas se esgotam.
"""
def cen3():
    asks_for_inputs = True

    # flags de estado do jogo
    ball_is_thrown = False
    scored = False
    launcher_ball = None
    player_ball = None
    lives = 3
    has_started = False
    player_ball_launch = False
    dt = 1 / 16
    xscreen_limiter = 350
    yscreen_limiter = 200
    win3 = GraphWin("Basketball Game", 600, 400, autoflush=False)
    win3.setCoords(0, -10, xscreen_limiter, yscreen_limiter)

    parabola_finalx = 140
    parabola(0, win3, xoffset=90, yoffset=10, mirror_dif=-parabola_finalx, scalar=0.02)

    stickman = StickMan(Point(290, 52), 0, "left", win3)

    back_wall = Static(Point(xscreen_limiter - 20, 0), "wall", "black", "black", win3, yscreen_limiter)
    basket_left_center = Point(270, 120)
    basket = Static(center=basket_left_center, shape="basket", radius=3, color="slategrey", outline="black",
                    window=win3, offset=40)
    floor_line = Static(center=Point(0, 0), shape="line", color="black", outline="black", window=win3, offset=400)
    parabola_wall = Static(Point(parabola_finalx + 10, 0), "wall", "black", "black", win3, 60)
    parabola_line = Static(center=Point(parabola_finalx, 60), shape="line", color="black", outline="black", window=win3,
                           offset=10)
    static_list = [basket, floor_line, back_wall, parabola_wall]

    parabola_ball = ShotTracker1(xpoint=10, ypoint=190, xoffset=90, yoffset=16.48, win=win3, color="green",
                                 outline="black", r=6, scalar=1.134 * 0.02)

    quit_button = Button(win3, Point(120, 180), 25, 20, "QUIT")
    quit_button.activate()

    lifeboard = ScoreBoard(Point(80, 185), Point(100, 140), win3, lives, subject="Lives")
    scoreboard = ScoreBoard(Point(80, 170), Point(100, 140), win3, 0)

    data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

    while win3.isOpen():

        while asks_for_inputs:
            value_window = InputDialog()
            angle, vel0 = value_window.collect_val()
            value_window.destroy()
            asks_for_inputs = False
            player_ball_launch = False
            win3.bind_all("<Key>", win3._onKey)
            win3.master.lift()
            win3.master.focus_force()
            win3.update()

        # loop de jogo ativo após receber os parâmetros de lançamento
        while asks_for_inputs == False:
            point = win3.checkMouse()
            key = win3.checkKey()
            if point is not None:
                if quit_button.clicked(point):
                    quit_button.deactivate()
                    win3.update()
                    time.sleep(0.1)
                    aviso_gravar = Text(Point(175, 185), "Press 'G' to save or any other key to continue")
                    aviso_gravar.setTextColor("red")
                    aviso_gravar.setStyle("bold")
                    aviso_gravar.draw(win3)
                    win3.update()
                    tecla = win3.getKey()
                    aviso_gravar.undraw()
                    if tecla in ["G", "g"]:
                        save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio)
                    win3.close()
                    break

            # espera pela tecla 's' para iniciar o movimento da bola verde
            if key == "s" and not has_started:
                has_started = True

            # lança a bola do jogador com barra de espaço
            if has_started and key == "space" and not player_ball_launch and player_ball is None:
                hand_placement = stickman.ball.getCenter()
                stickman.shoot(win3)
                player_ball = ShotTracker1(xpoint=hand_placement.getX(), ypoint=hand_placement.getY(),
                                           win=win3, color="orange", outline="black",
                                           r=6, scalar=0, vel0=vel0, angle=180 - angle)
                player_ball_launch = True

            # condição que, ao verificar que a bola já foi deix<da cair, realiza a verificação da posição x
            # da bola na parábola, de fomr a a perceber quando o trajeto acaba, alterando o tipo de movimento (rolador=>projétil)

            # atualiza as bolas e verifica colisões enquanto o jogo está ativo
            if has_started:
                if not ball_is_thrown:
                    parabola_ball.update_tracker(dt)
                    # se a bola está na posição x final da parábola, etnão troca de movimento. Caso contrário, esta apenas atualiza a sua posição
                    if parabola_ball.getx() >= parabola_finalx:
                        parabola_ball.xpos = parabola_finalx
                        parabola_ball.destroy()
                        try:
                            final_vel = parabola_ball.xvel / cos((-1) * parabola_ball.angle)
                        except ZeroDivisionError:
                            final_vel = parabola_ball.xvel
                        launcher_ball = ShotTracker1(xpoint=parabola_finalx, ypoint=parabola_ball.gety(),
                                                     xoffset=90, yoffset=16.48, win=win3, color="green",
                                                     outline="black", r=6, scalar=0, vel0=final_vel * 2.2,
                                                     angle=degrees(parabola_ball.angle))
                        data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()
                        ball_is_thrown = True

                # condição que verifica se a bola já alterou o seu movimento, caso este onde  haverá um loop pela lista de objetos, realizando a verificação de colisões

                if launcher_ball is not None and ball_is_thrown:
                    launcher_ball.update_tracker(dt)
                    tempo_atual = record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual, launcher_ball.getx(), launcher_ball.gety())
                    for obj in static_list:
                        if obj.shape == "wall":
                            if launcher_ball.getx() > obj.center.getX():
                                nx = 1
                            else:
                                nx = -1
                            if launcher_ball.gety() < obj.offset:
                                static_colision_detector(launcher_ball, ball_r=6, px=obj.center.getX(),
                                                         py=obj.center.getY(), normx=nx, normy=0)
                        elif obj.shape == "line":
                            static_colision_detector(launcher_ball, ball_r=6, px=obj.center.getX(),
                                                     py=obj.center.getY(), normx=0, normy=1)

                        elif obj.shape == "basket":
                            left_cx = obj.center.getX()
                            right_cx = obj.center.getX() + obj.offset
                            ball_cy = obj.center.getY() + obj.radius

                            static_colision_detector(launcher_ball, ball_r=6, cenx=left_cx, ceny=ball_cy,
                                                     cenr=obj.radius)
                            static_colision_detector(launcher_ball, ball_r=6, cenx=right_cx, ceny=ball_cy,
                                                     cenr=obj.radius)

                    if player_ball is not None:
                        hit = dynamic_collision_detector(launcher_ball, player_ball, 6, 6)
                        if hit and not scored:
                            scored = True
                            scoreboard.update_score()
                    left_limit = basket_left_center.getX() + basket.radius
                    right_limit = basket_left_center.getX() + basket.radius + basket.offset

                    if not scored and left_limit < launcher_ball.getx() < right_limit and basket_left_center.getY() - 5 < launcher_ball.gety() < basket_left_center.getY() + 5:
                        scored = True
                        lives -= 1
                        lifeboard.update_lives()
                    if abs(launcher_ball.xvel) < 15 and (
                    launcher_ball.yvel) < 15 and launcher_ball.ypos < 40 or launcher_ball.xpos < 0:
                        launcher_ball.destroy()
                        launcher_ball = None
                        ball_is_thrown = False
                        scored = False
                        aviso_gravar = Text(Point(175, 185), "Press 'G' to save or any other key to continue")
                        aviso_gravar.setTextColor("red")
                        aviso_gravar.setStyle("bold")
                        aviso_gravar.draw(win3)
                        win3.update()
                        tecla = win3.getKey()
                        aviso_gravar.undraw()
                        win3.update()
                        if tecla in ["G", "g"]:
                            save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio)
                        asks_for_inputs = True

                        if player_ball is not None:
                            player_ball.destroy()
                            player_ball = None
                            stickman.clear_arms()
                            stickman.create_arms(win3)

                        parabola_ball = ShotTracker1(xpoint=10, ypoint=190, xoffset=90, yoffset=16.48,
                                                     win=win3, color="green", outline="black", r=6,
                                                     scalar=1.134 * 0.02)

                if player_ball is not None:
                    player_ball.update_tracker(dt)

                    for obj in static_list:
                        if obj.shape == "wall":
                            if player_ball.getx() > obj.center.getX():
                                nx = 1
                            else:
                                nx = -1
                            if player_ball.gety() <= obj.offset:
                                static_colision_detector(player_ball, ball_r=6, px=obj.center.getX(),
                                                         py=obj.center.getY(), normx=nx, normy=0)

                        elif obj.shape == "line":
                            static_colision_detector(player_ball, ball_r=6, px=0, py=obj.center.getY(), normx=0,
                                                     normy=1)
                        elif obj.shape == "basket":
                            left_cx = obj.center.getX()
                            right_cx = obj.center.getX() + obj.offset
                            ball_cy = obj.center.getY() + obj.radius

                            static_colision_detector(player_ball, ball_r=6, cenx=left_cx, ceny=ball_cy, cenr=obj.radius)
                            static_colision_detector(player_ball, ball_r=6, cenx=right_cx, ceny=ball_cy,
                                                     cenr=obj.radius)

                    if player_ball.getx() < -10 or player_ball.getx() > xscreen_limiter:
                        player_ball.destroy()
                        player_ball = None
                        stickman.clear_arms()
                        stickman.create_arms(win3)

            # verifica o fim de jogo após cada frame
            if lives == 0:
                lifeboard.game_over(win3)
                win3.update()
                time.sleep(3)
                win3.close()
                break

            update(40)