from math import cos, sin, radians, degrees, atan
from graphics import *
import random
class Projectile:
    def __init__(self,angle, vel0, h0):
        random_factor=random.randint(1,10)*0.35
        theta = radians(angle+random_factor)
        self.xvel = (vel0+random_factor) * cos(theta)
        self.yvel = (vel0+random_factor) * sin(theta)
        self.ypos = h0
        self.xpos = 23

    def update(self, interval ):
        self.xpos = self.xpos + interval * self.xvel
        yvel1 = self.yvel - 9.8 * interval
        self.ypos = self.ypos + interval* (self.yvel + yvel1) / 2.0
        self.yvel = yvel1

    def getx(self):
        return self.xpos

    def gety(self):
        return self.ypos




class ShotTracker(Projectile):
    def __init__(self, angle, vel0, h0, win):
        super().__init__(angle, vel0, h0)
        self.marker=Circle(Point(self.getx(), self.gety()), 6)
        self.marker.setFill("orange")
        self.marker.setOutline("black")
        self.marker.draw(win)

    def update_tracker(self, interval):
        self.update(interval)

        center = self.marker.getCenter()
        dx = self.getx() - center.getX()
        dy = self.gety() - center.getY()
        self.marker.move(dx, dy)

    def destroy(self):
        self.marker.undraw()

class Launcher:
    def __init__(self, angle,vel0, h0, win):
        super().__init__(angle,vel0,h0)
        # random_factor=random.randint(1,10)*0.35
        ball = Circle(Point(5, 48), 3)
        ball.setOutline("black")
        ball.setFill("orange")
        ball.draw(win)

        self.angle = radians(angle)
        self.vel = vel0
        self.xvel = self.vel * cos(self.angle)
        self.yvel = self.vel * sin(self.angle)
        self.arrow = Line(Point(0, 0), Point(0, 0)).draw(win)
        self.arrow.setWidth(3)
        self.redraw(win)




    def redraw(self, win):
        #desenha um novo ponteiro com a nova coordenada
        self.arrow.undraw()

        pt1 = Point(self.xvel, self.yvel)
        self.arrow = Line(Point(0, 0), pt1)
        self.arrow.setArrow("last")
        self.arrow.draw(win)



    def increase_angle(self, amount,win):
        """ alterar o ângulo em amt graus """

        self.angle = self.angle + radians(amount)
        self.redraw(win)

    def increase_vel(self, amount, win):

        self.vel = self.vel + amount
        self.redraw(win)
    def Shoot(self, win):
        return ShotTracker(win,degrees(self.angle), self.vel, 48)



class Roller:
    def __init__(self, xpoint):
        self.xpos=xpoint
        self.ypos=self.xpos**2
        self.tan_vel=0
        self.xvel=0
        self.yvel=0
    
    def update(self, interval):
        #derivada da posição 
        d1=2*self.xpos
        #valor do angulo tangente obtido através do declive da derivada (2x)
        angle=atan(d1)
        #acelaração tangencial (projeta-se a a.g na trajetória usando o ângulo de inclinação)
        tan_accer=-9.8*sin(angle)
        #calcula a variação da velocidade tangencial
        self.tan_vel=self.tan_vel+tan_accer*interval
        #projeta a velocidade tangencial no eixo dos xx
        self.xvel=self.tan_vel*cos(angle)
        #soma a velocidade á posição do x
        self.xpos=self.xpos+interval*self.xvel
        #y fica depende de x porque fica sempre forçado a seguir a restrição y=x*2
        self.ypos=self.xpos**2

    def getx(self):
        return self.xpos
    def gety(self):
        return self.ypos

class Tracker(Roller):
    def __init__(self,xpoint, win):
        super().__init__(xpoint)
        self.marker=Circle(Point(self.getx(), self.gety()), 1)
        self.marker.setFill("red")
        self.marker.setOutline("black")
        self.marker.draw(win)



    def update_tracker(self, interval):
        self.update(interval)
        center = self.marker.getCenter()
        dx = self.getx() - center.getX()
        dy = self.gety() - center.getY()
        self.marker.move(dx, dy)
        
