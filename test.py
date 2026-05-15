from graphics import *
win=GraphWin("Test", 400, 400)
angle_entry=Entry(Point(100, 100),30 )
angle_entry.draw(win)
print(angle_entry.getText())

win.mainloop()