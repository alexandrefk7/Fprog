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
        #alterar o ângulo em amt graus 

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
        self.scalar=0.1134
        self.route=self.scalar*xpoint**2 + 1.05
        self.ypos=self.route
        self.tan_vel=0
        self.xvel=0
        self.yvel=0
    
    def update(self, interval):
        #derivada da posição 
        d1=2*self.scalar*self.xpos
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
        self.ypos = self.scalar * (self.xpos**2)+1.05

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

#classe que junta tudo meu deus       
placeholder=0
class Moveable:
    def __init__(self, xpoint, ypoint=placeholder, angle=placeholder, vel0=placeholder):
        #escalar que altera a dilatação da parábola invisível
        self.scalar=0.1134

        #avalaia se tem valores inputados do angle e vel0, se tiver então age como o projetil do basquete
        if angle!=placeholder and vel0!=placeholder:
            self.on_route=False 
            self.angle = radians(angle)
            self.vel = vel0
            self.xvel = self.vel * cos(self.angle)
            self.yvel = self.vel * sin(self.angle)
            self.xpos=xpoint
            self.ypos=ypoint
            self.tan_vel=0
        #age coo um roller, podendo surgir na linha (if,) ou no ar (else)
        else:
            self.xpos=xpoint
            self.tan_vel=0
            self.xvel=0
            self.yvel=0
            self.velovidade_final_queda=0
            if ypoint==placeholder:
                self.ypos=self.scalar*xpoint**2 + 1.05
                self.on_route=True
            else:
                self.ypos=ypoint
                self.on_route=False
    def update(self, interval):
        if self.on_route==False:
            self.xpos = self.xpos + interval * self.xvel
            yvel1 = self.yvel - 9.8 * interval
            self.ypos = self.ypos + interval* (self.yvel + yvel1) / 2.0
            self.yvel = yvel1
            coordenada_y__contacto=self.scalar*self.xpos**2 + 1.05

            if self.ypos<coordenada_y__contacto:
                self.ypos=coordenada_y__contacto
                #self.velovidade_final_queda=-self.yvel
                self.on_route=True
            
        else:
            #self.tan_vel=self.velovidade_final_queda
            #derivada da posição 
            d1=2*self.scalar*self.xpos
            #valor do angulo tangente obtido através do declive da derivada (2x)
            angle=atan(d1)
            #acelaração tangencial (projeta-se a a.g na trajetória usando o ângulo de inclinação)
            tan_accer=-9.8*sin(angle)
            #calcula a variação da velocidade tangencial
            self.tan_vel= self.tan_vel + tan_accer*interval
            #projeta a velocidade tangencial no eixo dos xx
            self.xvel= self.tan_vel*cos(angle)
            #soma a velocidade á posição do x
            self.xpos= self.xpos+ interval*self.xvel
            #y fica depende de x porque fica sempre forçado a seguir a restrição y=x*2
            self.ypos = self.scalar * (self.xpos**2)+1.05
           
    def getx(self):
        return self.xpos
    def gety(self):
        return self.ypos
    # def energy_fleeting(self):
    #     if 

class ShotTracker1(Moveable):
    def __init__(self, xpoint, win, color, outline, r,   ypoint=placeholder, angle=placeholder, vel0=placeholder):
        super().__init__(xpoint, ypoint, angle, vel0)
        self.marker=Circle(Point(self.getx(), self.gety()), r)
        self.marker.setFill(color)
        self.marker.setOutline(outline)
        self.marker.draw(win)

    def update_tracker(self, interval):
        self.update(interval)
        center = self.marker.getCenter()
        dx = self.getx() - center.getX()
        dy = self.gety() - center.getY()
        self.marker.move(dx, dy)

    def destroy(self):
        self.marker.undraw()

         