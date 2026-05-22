from graphics import *
from button import Button

def abre_cenario(num):
    w = GraphWin("Cenario {}".format(num), 600, 450)
    w.setBackground("lightblue")
    try:
        w.getMouse()
        w.close()
    except GraphicsError:
        pass

win = GraphWin("Simulacao de Fisica", 300, 400)
win.setCoords(0, 0, 6, 8)
win.setBackground("slategray")

grid = Rectangle(Point(0.5, 2.5), Point(5.5, 7.5))
grid.setFill("white")
grid.draw(win)
Line(Point(0.5, 5.0), Point(5.5, 5.0)).draw(win)
Line(Point(3.0, 2.5), Point(3.0, 7.5)).draw(win)

nums = []
for i, (x, y) in enumerate([(1.75, 6.25), (4.25, 6.25), (1.75, 3.75), (4.25, 3.75)]):
    t = Text(Point(x, y), str(i + 1))
    t.setSize(18)
    t.setStyle("bold")
    t.draw(win)
    nums.append(t)

start = Circle(Point(3.0, 5.0), 0.9)
start.setFill("red3")
start.setOutline("darkred")
start.setWidth(3)
start.draw(win)
txt = Text(Point(3.0, 5.0), "START")
txt.setFill("white")
txt.setStyle("bold")
txt.setSize(13)
txt.draw(win)

btn = Button(win, Point(3.0, 1.25), 4.0, 0.8, "QUIT")
btn.activate()

sel = None
while True:
    try:
        p = win.getMouse()
    except GraphicsError:
        break
    x, y = p.getX(), p.getY()
    if (x - 3.0)**2 + (y - 5.0)**2 <= 0.81:
        if sel is not None:
            abre_cenario(sel)
    elif btn.clicked(p):
        win.close()
        break
    elif 0.5 <= x <= 5.5 and 2.5 <= y <= 7.5:
        if x <= 3.0 and y >= 5.0: num = 1
        elif x >= 3.0 and y >= 5.0: num = 2
        elif x <= 3.0: num = 3
        else: num = 4
        for t in nums:
            t.setFill("black")
            t.setSize(18)
        nums[num - 1].setFill("red")
        nums[num - 1].setSize(28)
        sel = num
