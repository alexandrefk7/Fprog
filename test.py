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
quit_button = Button(win2, Point(0,18), 3,2, "QUIT")
quit_button.activate()

 

while win2.isOpen():
    point=win2.checkMouse()
    if point is not None:
        if quit_button.clicked(point):
            quit_button.deactivate()
            win2.update()      
            time.sleep(0.3)         
            win2.close()
            break

    ball.update(0.05)
    tracker.update_tracker(0.05)
    time.sleep(0.05)

