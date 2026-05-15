from Projectiles import Projectile
from graphics import *

class ShotTracker(Projectile):
    def __init__(self, angle, vel0, h0, win):
        super().__init__(angle, vel0, h0)
        self.marker=Circle(Point(self.getx(), self.gety()), 6)
        self.marker.setFill("red")
        self.marker.setOutline("red")
        self.marker.draw(win)

    def update_tracker(self, interval):
        self.update(interval)

        center = self.marker.getCenter()
        dx = self.getx() - center.getX()
        dy = self.gety() - center.getY()
        self.marker.move(dx, dy)

    def destroy(self):
        self.marker.undraw()



