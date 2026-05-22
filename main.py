from Projectiles import *
from entities import *

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

    v_window=InputDialog(angle, vel0)
    option=v_window.interaction()
    v_window.close()
    if option=="Quit":
        break
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