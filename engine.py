from math import cos, sin, radians, degrees, atan, sqrt, atan2
from graphics import *
import random


# classe de projetil abandonda (apagar)
class Projectile:
    def __init__(self, angle, vel0, h0):
        random_factor = random.randint(1, 10) * 0.35
        theta = radians(angle + random_factor)
        self.xvel = (vel0 + random_factor) * cos(theta)
        self.yvel = (vel0 + random_factor) * sin(theta)
        self.ypos = h0
        self.xpos = 23

    def update(self, interval):
        self.xpos = self.xpos + interval * self.xvel
        yvel1 = self.yvel - 9.8 * interval
        self.ypos = self.ypos + interval * (self.yvel + yvel1) / 2.0
        self.yvel = yvel1

    def getx(self):
        return self.xpos

    def gety(self):
        return self.ypos


# classe rejeitada do Shotracker
class ShotTracker(Projectile):
    def __init__(self, angle, vel0, h0, win):
        super().__init__(angle, vel0, h0)
        self.marker = Circle(Point(self.getx(), self.gety()), 6)
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


# classe que permite usar as teclas para alterar a trajetória e o ângulo
class Launcher:
    def __init__(self, angle, vel0, h0, win):
        super().__init__(angle, vel0, h0)
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
        # desenha um novo ponteiro com a nova coordenada
        self.arrow.undraw()

        pt1 = Point(self.xvel, self.yvel)
        self.arrow = Line(Point(0, 0), pt1)
        self.arrow.setArrow("last")
        self.arrow.draw(win)

    def increase_angle(self, amount, win):
        # alterar o ângulo em amt graus

        self.angle = self.angle + radians(amount)
        self.redraw(win)

    def increase_vel(self, amount, win):
        self.vel = self.vel + amount
        self.redraw(win)

    def Shoot(self, win):
        return ShotTracker(win, degrees(self.angle), self.vel, 48)


# classe rejeitada para o rolador
class Roller:
    def __init__(self, xpoint, scalar=0.1134):
        self.xpos = xpoint
        self.scalar = scalar
        self.route = self.scalar * xpoint ** 2 + 1.05
        self.ypos = self.route
        self.tan_vel = 0
        self.xvel = 0
        self.yvel = 0

    def update(self, interval):
        # derivada da posição
        d1 = 2 * self.scalar * self.xpos
        # valor do angulo tangente obtido através do declive da derivada (2x)
        angle = atan(d1)
        # acelaração tangencial (projeta-se a a.g na trajetória usando o ângulo de inclinação)
        tan_accer = -9.8 * sin(angle)
        # calcula a variação da velocidade tangencial
        self.tan_vel = self.tan_vel + tan_accer * interval
        # projeta a velocidade tangencial no eixo dos xx
        self.xvel = self.tan_vel * cos(angle)
        # soma a velocidade á posição do x
        self.xpos = self.xpos + interval * self.xvel
        # y fica depende de x porque fica sempre forçado a seguir a restrição y=x*2
        self.ypos = self.scalar * (self.xpos ** 2) + 1.05

    def getx(self):
        return self.xpos

    def gety(self):
        return self.ypos


# classe rejitada do tracker
class Tracker(Roller):
    def __init__(self, xpoint, win):
        super().__init__(xpoint)
        self.marker = Circle(Point(self.getx(), self.gety()), 1)
        self.marker.setFill("red")
        self.marker.setOutline("black")
        self.marker.draw(win)

    def update_tracker(self, interval):
        self.update(interval)
        center = self.marker.getCenter()
        dx = self.getx() - center.getX()
        dy = self.gety() - center.getY()
        self.marker.move(dx, dy)


# classe que junta tudo meu deus
placeholder = 0


class Moveable:
    def __init__(self, xpoint, xoffset, yoffset, ypoint=placeholder, angle=placeholder, vel0=placeholder,
                 scalar=0.1134):
        # escalar que altera a dilatação da parábola invisível
        self.scalar = scalar
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.i = 0

        # avalaia se tem valores inputados do angle e vel0, se tiver então age como o projetil do basquete
        if angle != placeholder and vel0 != placeholder:
            self.angle = radians(angle)
            self.vel = vel0
            self.xvel = self.vel * cos(self.angle)
            self.yvel = self.vel * sin(self.angle)
            self.xpos = xpoint
            self.ypos = ypoint
            self.tan_vel = 0
            self.in_air = True
            self.on_route = False
            # age coo um roller, podendo surgir na linha (if) ou no ar (else)
        else:
            self.xpos = xpoint
            self.tan_vel = 0
            self.xvel = 0
            self.yvel = 0
            self.velovidade_final_queda = 0
            self.in_air = False
            if ypoint == placeholder:
                self.ypos = self.scalar * ((xpoint - self.xoffset) ** 2) + (self.yoffset)
                self.on_route = True
            else:
                self.ypos = ypoint
                self.on_route = False

    def update(self, interval, hand=None):

        self.i += 0.05
        if self.on_route == False:
            self.xpos = self.xpos + interval * self.xvel
            yvel1 = self.yvel - 9.8 * interval
            self.ypos = self.ypos + interval * (self.yvel + yvel1) / 2.0
            self.yvel = yvel1

            if self.in_air:
                if self.ypos < 0:
                    self.xvel, self.yvel = 0, 0

            else:
                coordenada_y__contacto = self.scalar * (self.xpos - self.xoffset) ** 2 + (self.yoffset)
                if self.ypos < coordenada_y__contacto:
                    self.ypos = coordenada_y__contacto
                    d1 = 2 * self.scalar * (self.xpos - self.xoffset)
                    self.angle = atan(d1)
                    self.xvel = self.yvel * sin(self.angle) * cos(self.angle)
                    self.on_route = True

        else:
            # self.tan_vel=self.velovidade_final_queda
            # derivada da posição
            d1 = 2 * self.scalar * (self.xpos - self.xoffset)
            # valor do angulo tangente obtido através do declive da derivada (2x)
            self.angle = atan(d1)
            # acelaração tangencial (projeta-se a a.g na trajetória usando o ângulo de inclinação)
            tan_accer = -9.8 * sin(self.angle)

            # projeta a velocidade tangencial no eixo dos xx, depois de calcular a variação da velocidade tangencial
            self.xvel = self.xvel + (-9.8 * sin(self.angle) * interval) * cos(self.angle)

            # valor da dissipação de energia por intervalo
            self.xvel *= 0.998

            # soma a velocidade á posição do x
            self.xpos = self.xpos + interval * self.xvel

            # y fica dependente x porque fica sempre forçado a seguir a restrição y=x*2
            self.ypos = self.scalar * ((self.xpos - self.xoffset) ** 2) + (self.yoffset)

            # if hand is not None:
            # hand.write(f"{self.i}, {self.xpos}, {self.xvel}\n")

    def collision_with_static(self, particle, surface):
        self.center = particle.getCenter()
        self.radius = particle.getRadius()
        self.surface = surface
        dx = self.center.getX() - self.surface.getCenter().getX()
        dy = self.center.getY() - self.surface.getCenter().getY()
        distance_between_bodies = sqrt(dx ** 2 + dy ** 2)
        if distance_between_bodies <= self.radius:
            print("yepi")

    def getx(self):
        return self.xpos

    def gety(self):
        return self.ypos


# Classe geral que desenha tudo
class ShotTracker1(Moveable):
    def __init__(self, xpoint, scalar, win, color, outline, r, xoffset=placeholder, yoffset=placeholder,
                 ypoint=placeholder, angle=placeholder, vel0=placeholder):
        super().__init__(xpoint, xoffset, yoffset, ypoint, angle, vel0, scalar=scalar)
        self.marker = Circle(Point(self.getx(), self.gety()), r)
        self.marker.setFill(color)
        self.marker.setOutline(outline)
        self.marker.draw(win)

    def update_tracker(self, interval, hand=None):
        self.update(interval, hand)
        center = self.marker.getCenter()
        dx = self.getx() - center.getX()
        dy = self.gety() - center.getY()
        self.marker.move(dx, dy)

    def destroy(self):
        self.marker.undraw()

    # def colides_with_static(self):


# P-vetor da parede ao centro da bola, N-normal à superficie C-bola que toca na outra
def static_colision_detector(tracker, ball_r, px=None, py=None, normx=None, normy=None, cenx=None, ceny=None,
                             cenr=None):
    e = 0.85
    # faz a colisão com paredes e chão
    if px != None and py != None and normx != None and normy != None:

        dx = tracker.getx() - px
        dy = tracker.gety() - py

        dist = dx * normx + dy * normy

        if dist < ball_r:
            entered_inside = ball_r - dist
            tracker.xpos += normx * entered_inside
            tracker.ypos += normy * entered_inside

            dot = tracker.xvel * normx + tracker.yvel * normy
            if dot < 0:
                tracker.xvel = e * (tracker.xvel - 2 * dot * normx)
                tracker.yvel = e * (tracker.yvel - 2 * dot * normy)

            return True
        return False


    #
    elif cenx != None and ceny != None and cenr != None:
        dx = tracker.getx() - cenx
        dy = tracker.gety() - ceny

        dist_sq = dx ** 2 + dy ** 2
        min_dist = ball_r + cenr

        if dist_sq < min_dist ** 2 and dist_sq > 0:

            dist = sqrt(dist_sq)

            normx = dx / dist
            normy = dy / dist

            tracker.xpos = cenx + normx * (min_dist + 0.1)
            tracker.ypos = ceny + normy * (min_dist + 0.1)

            # reflexão
            dot = tracker.xvel * normx + tracker.yvel * normy
            if dot < 0:
                tracker.xvel = e * (tracker.xvel - 2 * dot * normx)
                tracker.yvel = e * (tracker.yvel - 2 * dot * normy)

            return True
        return False


    else:
        return False