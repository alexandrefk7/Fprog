from graphics import *
from Projectiles import *
from entities import *


import time
from math import pi, cos
from gravar_trajetoria import *


def cen1():
    xright_screen_limiter = 300
    ceiling = 180
    win1 = GraphWin("Basketball Game", 400, 400, autoflush=False)
    win1.setCoords(-10, -10, xright_screen_limiter, ceiling)

    basket_left_center = Point(200, 100)
    # Objetos estáticos
    marked_distance_line = Static(center=Point(0, 0), shape="metric", color="black", outline="black", window=win1,
                                  offset=xright_screen_limiter)
    basket = Static(center=basket_left_center, shape="basket", radius=3, color="slategrey", outline="black",
                    window=win1, offset=40)
    right_wall = Static(Point(xright_screen_limiter - 20, 0), "wall", "black", "black", win1, ceiling + 20)
    static_list = [basket, marked_distance_line, right_wall]

    stickman_hand_height = 48
    stickman_right_disloc = 23
    dt = 0.1

    # UI elements
    scoreboard = ScoreBoard(Point(25, ceiling - 10), Point(80, 140), win1, subject="Score")
    player = StickMan(Point(5, 52), 0, "right", win1)
    quit_button = Button(win1, Point(xright_screen_limiter - 60, 160), 40, 15, "QUIT")
    quit_button.activate()

    asks_for_inputs = True
    has_fired = False
    scored = False
    tracker = None
    angle = None
    vel0 = None

    data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()

    while win1.isOpen():

        # --- Input phase ---
        while asks_for_inputs:
            value_window = InputDialog()
            angle, vel0 = value_window.collect_val()
            value_window.destroy()
            if angle is None:
                win1.close()
                return
            asks_for_inputs = False
            has_fired = False
            win1.bind_all("<Key>", win1._onKey)

        key = win1.checkKey()
        point = win1.checkMouse()

        if point is not None:
            if quit_button.clicked(point):
                quit_button.deactivate()
                win1.update()
                time.sleep(0.3)
                aviso_gravar = Text(Point(150, ceiling - 10), "Press 'G' to save or any other key to continue")
                aviso_gravar.setTextColor("red")
                aviso_gravar.setStyle("bold")
                aviso_gravar.draw(win1)
                win1.update()
                tecla = win1.getKey()
                aviso_gravar.undraw()
                if tecla in ["G", "g"]:
                    save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio)
                win1.close()
                return

        if key == "space" and not has_fired:
            has_fired = True
            scored = False
            data_hora_inicio, tempo_atual, trajectory_t, trajectory_x, trajectory_y = start_trajectory()
            tracker = ShotTracker1(
                xpoint=stickman_right_disloc, win=win1, color="orange", outline="black", r=6,
                ypoint=stickman_hand_height, angle=angle, vel0=vel0 * 1.12, scalar=0)
            player.shoot(win1)

        if has_fired and tracker is not None:
            tracker.update_tracker(dt)
            tempo_atual = record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual, tracker.getx(), tracker.gety())

            # detetor de colisões
            for obj in static_list:
                if obj.shape == "wall":
                    nx = 1 if tracker.getx() > obj.center.getX() else -1
                    if tracker.gety() < obj.offset:
                        static_colision_detector(tracker, ball_r=6, px=obj.center.getX(), py=obj.center.getY(),
                                                 normx=nx, normy=0)

                elif obj.shape == "metric":
                    static_colision_detector(tracker, ball_r=6, px=obj.center.getX(), py=obj.center.getY(), normx=0,
                                             normy=1)

                elif obj.shape == "basket":
                    left_cx = obj.center.getX()
                    right_cx = obj.center.getX() + obj.offset
                    ball_cy = obj.center.getY() + obj.radius
                    static_colision_detector(tracker, ball_r=6, cenx=left_cx, ceny=ball_cy, cenr=obj.radius)
                    static_colision_detector(tracker, ball_r=6, cenx=right_cx, ceny=ball_cy, cenr=obj.radius)

            left_limit = basket_left_center.getX() + basket.radius
            right_limit = basket_left_center.getX() + basket.radius + basket.offset
            # detetor de pontuação
            if not scored and left_limit < tracker.getx() < right_limit and basket_left_center.getY() - 5 < tracker.gety() < basket_left_center.getY() + 5:
                scoreboard.update_score()
                scored = True
                scoreboard.message.undraw()
                scoreboard.unecessary_cheers(win1)

            if (abs(tracker.xvel) < 10 and abs(tracker.yvel) < 10) or tracker.xpos < -10:
                tracker.destroy()
                tracker = None
                player.clear_arms()
                player.create_arms(win1)
                has_fired = False
                scored = False
                aviso_gravar = Text(Point(150, ceiling - 10), "Press 'G' to save or any other key to continue")
                aviso_gravar.setTextColor("red")
                aviso_gravar.setStyle("bold")
                aviso_gravar.draw(win1)
                win1.update()
                tecla = win1.getKey()
                aviso_gravar.undraw()
                win1.update()
                if tecla in ["G", "g"]:
                    save_trajectory(trajectory_t, trajectory_x, trajectory_y, data_hora_inicio)
                asks_for_inputs = True

        win1.update()
        update(20)