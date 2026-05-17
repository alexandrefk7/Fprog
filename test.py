from graphics import *
from Projectiles import *
from entities import *

win2=GraphWin(title="Title", width=800, height=600, autoflush=False)
win2.setCoords(-30, -20, 30, 500)
parabola(-20, win2)

ball=Roller(-38)
tracker=Tracker(-38, win2)



while win2.isOpen():
    ball.update(0.1)
    tracker.update_tracker(0.1)
    

    if win2.checkMouse():
        win2.close()