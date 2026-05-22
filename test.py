from graphics import *
from Projectiles import *
from entities import *
import time

win2=GraphWin(title="Title", width=500, height=500, autoflush=False)
win2.setCoords(-15, -5, 15, 20)
parabola(-12, win2)
ball=Moveable(xpoint=-8, ypoint=20)
#se meter y=0 ent ele fica a rolar
tracker=ShotTracker1(xpoint=-8,ypoint=20, win=win2, color="red", outline="black", r=1)

#cria o botão de quit
quit_button = Button(win2, Point(0,18), 3,2, "QUIT!")


 

while win2.isOpen():
    point=win2.checkMouse()
    if quit_button.clicked(point)==True:
        quit_button.activate()
        
        win2.close()

    ball.update(0.05)
    tracker.update_tracker(0.05)
    time.sleep(0.05)


    if win2.checkMouse():
        win2.close()