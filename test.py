from graphics import *
from Projectiles import *

win2=GraphWin(title="Title", width=800, height=600, autoflush=False)
win2.setCoords(-50, -50, 50, 2000)
for x in range(-40, 40):
    point=Point(x, x**2)
    next_point=Point(x+1, (x+1)**2)
    line=Line(point, next_point)
    line.draw(win2)

ball=Roller(-38)
tracker=Tracker(-38, win2)



while win2.isOpen():

    ball.update(0.1)
    

    if win2.checkMouse():
        win2.close()