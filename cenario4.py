from graphics import *
from entities import *
from Projectiles import *
from entities import PortalPair
import time


def cenario4():
    # constantes da janela (base: cenário 1)
    xright_screen_limiter = 300
    ceiling = 180

    # constantes do cenário 4
    BALL_R      = 6
    ARO_R       = 3
    PAREDE_X    = 100
    ESPESSURA   = 8
    PORTAL_LARG = 20
    PASSO       = 5
    meia        = PORTAL_LARG / 2
    WALL_X      = xright_screen_limiter - 20  # alinhado com right_wall

    # posições iniciais dos portais
    p1_cy      = 50
    p2_cx, p2_cy = 200, 85

    dt = 0.1  # passo de tempo da simulação

    # janela
    win = GraphWin("Basketball Game - Portais", 400, 400, autoflush=False)
    win.setCoords(-10, -10, xright_screen_limiter, ceiling)

    # elementos estáticos base (cenário 1)
    basket_left_center    = Point(200, 100)
    marked_distance_line  = Static(center=Point(0, 0), shape="metric", color="black", outline="black",
                                   window=win, offset=xright_screen_limiter)
    basket     = Static(center=basket_left_center, shape="basket", radius=ARO_R, color="slategrey",
                        outline="black", window=win, offset=40)
    right_wall = Static(Point(xright_screen_limiter - 20, 0), "wall", "black", "black", win, ceiling + 20)
    static_list = [basket, marked_distance_line, right_wall]

    # muro central (cenário 4)
    muro = Rectangle(Point(PAREDE_X, -10), Point(PAREDE_X + ESPESSURA, ceiling))
    muro.setFill("darkgray")
    muro.setOutline("black")
    muro.setWidth(1)
    muro.draw(win)

    # botões de controlo dos portais, disparo e saída
    btn_p1_up   = Button(win, Point(30,  158), 55, 8,  "Azul Cima")
    btn_p1_dn   = Button(win, Point(30,  148), 55, 8,  "Azul Baixo")
    btn_p2_esq  = Button(win, Point(260, 158), 55, 8,  "Lar Esq")
    btn_p2_dir  = Button(win, Point(260, 148), 55, 8,  "Lar Dir")
    btn_fire    = Button(win, Point(150,  -2), 40, 8,  "ATIRAR")
    quit_button = Button(win, Point(xright_screen_limiter - 60, 170), 40, 15, "QUIT")

    # ativa todos os botões de controlo
    for b in [btn_p1_up, btn_p1_dn, btn_p2_esq, btn_p2_dir, btn_fire, quit_button]:
        b.activate()

    # portais
    portais = PortalPair(
        win,
        Point(PAREDE_X - 1, p1_cy), (1, 0),
        Point(p2_cx, p2_cy), (0.5, 1),
        portal_width=PORTAL_LARG
    )

    # placar e jogador (cenário 1)
    scoreboard = ScoreBoard(Point(25, ceiling - 10), Point(80, 140), win, subject="Score")
    player     = StickMan(Point(5, 52), 0, "right", win)

    stickman_hand_height  = 48
    stickman_right_disloc = 23

    # flags de estado
    has_fired = False
    scored    = False
    tracker   = None
    angle     = None
    vel0      = None

    # inicializa trajetória antes do loop principal
    data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

    while win.isOpen():

        # --- fase 1: ajuste dos portais ---
        msg = Text(Point(150, 10), "Ajuste os portais e clique ATIRAR")
        msg.setFill("blue")
        msg.draw(win)
        win.update()

        while win.isOpen():
            p = win.getMouse()

            if btn_p1_up.clicked(p) and p1_cy + PASSO <= ceiling - 37:
                portais.move_p1(0, PASSO);  p1_cy += PASSO
            elif btn_p1_dn.clicked(p) and p1_cy - PASSO >= 12:
                portais.move_p1(0, -PASSO); p1_cy -= PASSO
            elif btn_p2_esq.clicked(p) and p2_cx - PASSO >= PAREDE_X + 20 + ESPESSURA:
                portais.move_p2(-PASSO, 0); p2_cx -= PASSO
            elif btn_p2_dir.clicked(p) and p2_cx + PASSO <= WALL_X - 15:
                portais.move_p2(PASSO, 0);  p2_cx += PASSO
            elif btn_fire.clicked(p):
                break
            elif quit_button.clicked(p):
                msg.undraw()
                aviso_gravar = Text(Point(150, ceiling - 10), "Press 'G' to save or any other key to continue")
                aviso_gravar.setTextColor("red")
                aviso_gravar.setStyle("bold")
                aviso_gravar.draw(win)
                win.update()
                tecla = win.getKey()
                aviso_gravar.undraw()
                if tecla in ["G", "g"]:
                    save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio)
                win.close()
                return

            win.update()
            update(25)

        msg.undraw()

        # --- fase 2: input de ângulo e velocidade (cenário 1) ---
        value_window = InputDialog()
        angle, vel0 = value_window.collect_val()
        value_window.destroy()
        if angle is None:
            win.close()
            return
        has_fired = False
        scored    = False
        # redireciona o foco para a janela de jogo após fechar o InputDialog
        win.bind_all("<Key>", win._onKey)
        win.master.lift()
        win.master.focus_force()
        win.update()

        # --- fase 3: voo com space para disparar (cenário 1) ---
        while win.isOpen():
            key   = win.checkKey()
            point = win.checkMouse()

            if point is not None:
                if quit_button.clicked(point):
                    quit_button.deactivate()
                    win.update()
                    time.sleep(0.3)
                    if tracker:  # destrói a bola se ainda estiver em voo
                        tracker.destroy()
                    aviso_gravar = Text(Point(150, ceiling - 10), "Press 'G' to save or any other key to continue")
                    aviso_gravar.setTextColor("red")
                    aviso_gravar.setStyle("bold")
                    aviso_gravar.draw(win)
                    win.update()
                    tecla = win.getKey()
                    aviso_gravar.undraw()
                    if tecla in ["G", "g"]:
                        save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio)
                    win.close()
                    return

                # mover portais durante o voo
                if btn_p1_up.clicked(point) and p1_cy + PASSO <= ceiling - 37:
                    portais.move_p1(0, PASSO);  p1_cy += PASSO
                elif btn_p1_dn.clicked(point) and p1_cy - PASSO >= 12:
                    portais.move_p1(0, -PASSO); p1_cy -= PASSO
                elif btn_p2_esq.clicked(point) and p2_cx - PASSO >= PAREDE_X + 20 + ESPESSURA:
                    portais.move_p2(-PASSO, 0); p2_cx -= PASSO
                elif btn_p2_dir.clicked(point) and p2_cx + PASSO <= WALL_X - 15:
                    portais.move_p2(PASSO, 0);  p2_cx += PASSO

            if key == "space" and not has_fired:
                has_fired = True
                data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()
                tracker = ShotTracker1(
                    xpoint=stickman_right_disloc, win=win, color="orange", outline="black", r=BALL_R,
                    ypoint=stickman_hand_height, angle=angle, vel0=vel0 * 1.12, scalar=0)
                player.shoot(win)

            if has_fired and tracker is not None:
                tracker.update_tracker(dt)
                tempo_atual = record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual,
                                           tracker.getx(), tracker.gety())

                # colisão com portais e muro central (cenário 4)
                if not portais.apply(tracker, BALL_R):
                    # só colide com o muro se a bola não estiver na abertura do portal
                    na_zona_portal = (p1_cy - meia <= tracker.gety() <= p1_cy + meia)
                    if not na_zona_portal:
                        # ponto médio do muro para determinar o lado da colisão
                        meio_muro = PAREDE_X + ESPESSURA / 2
                        if tracker.getx() < meio_muro:
                            static_colision_detector(tracker, BALL_R, px=PAREDE_X,             py=0, normx=-1, normy=0)
                        else:
                            static_colision_detector(tracker, BALL_R, px=PAREDE_X + ESPESSURA, py=0, normx=1,  normy=0)

                # colisões via static_list: chão, parede direita e aros (cenário 1)
                for obj in static_list:
                    if obj.shape == "wall":
                        nx = 1 if tracker.getx() > obj.center.getX() else -1
                        if tracker.gety() < obj.offset:
                            static_colision_detector(tracker, BALL_R, px=obj.center.getX(), py=obj.center.getY(),
                                                     normx=nx, normy=0)
                    elif obj.shape == "metric":
                        static_colision_detector(tracker, BALL_R, px=obj.center.getX(), py=obj.center.getY(),
                                                 normx=0, normy=1)
                    elif obj.shape == "basket":
                        left_cx  = obj.center.getX()
                        right_cx = obj.center.getX() + obj.offset
                        ball_cy  = obj.center.getY() + obj.radius
                        static_colision_detector(tracker, BALL_R, cenx=left_cx,  ceny=ball_cy, cenr=obj.radius)
                        static_colision_detector(tracker, BALL_R, cenx=right_cx, ceny=ball_cy, cenr=obj.radius)

                # pontuação dinâmica (cenário 1)
                left_limit  = basket_left_center.getX() + basket.radius
                right_limit = basket_left_center.getX() + basket.radius + basket.offset
                if not scored and left_limit < tracker.getx() < right_limit \
                        and basket_left_center.getY() - 5 < tracker.gety() < basket_left_center.getY() + 5:
                    scoreboard.update_score()
                    scored = True
                    scoreboard.message.undraw()
                    scoreboard.unecessary_cheers(win)

                # condição de paragem (cenário 1)
                if (abs(tracker.xvel) < 10 and abs(tracker.yvel) < 10) or tracker.xpos < -10:
                    tracker.destroy()
                    tracker    = None
                    has_fired  = False
                    scored     = False
                    player.clear_arms()
                    player.create_arms(win)

                    # opção de gravar
                    aviso_gravar = Text(Point(150, ceiling - 10), "Press 'G' to save or any other key to continue")
                    aviso_gravar.setTextColor("red")
                    aviso_gravar.setStyle("bold")
                    aviso_gravar.draw(win)
                    win.update()
                    tecla = win.getKey()
                    aviso_gravar.undraw()
                    win.update()
                    if tecla in ["G", "g"]:
                        save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio)

                    break  # volta à fase 1 (ajuste de portais)

            win.update()
            update(20)

    if win.isOpen():
        win.close()
