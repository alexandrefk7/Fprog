from graphics import *
from Projectiles import *
from entities import *
import time

win2=GraphWin(title="Title", width=500, height=500, autoflush=False)
win2.setCoords(-15, -5, 15, 20)
parabola(-12, win2)

ball=Roller(-10)
tracker=Tracker(-10, win2)
 



while win2.isOpen():
    ball.update(0.05)
    tracker.update_tracker(0.05)
    time.sleep(0.05)


    if win2.checkMouse():
        win2.close()