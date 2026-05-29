from math import cos, sin, radians, degrees, atan, sqrt, atan2
from graphics import *
import random

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

    elif cenx != None and ceny != None and cenr != None:
        dx = tracker.getx() - cenx
        dy = tracker.gety() - ceny

        norm2 = dx ** 2 + dy ** 2
        min_dist = ball_r + cenr

        if norm2 < min_dist ** 2 and norm2 > 0:

            dist = sqrt(norm2)

            normx = dx / dist
            normy = dy / dist

            tracker.xpos = cenx + normx * (min_dist + 0.1)
            tracker.ypos = ceny + normy * (min_dist + 0.1)

            dotp = tracker.xvel * normx + tracker.yvel * normy
            if dotp < 0:
                tracker.xvel = e * (tracker.xvel - 2 * dotp * normx)
                tracker.yvel = e * (tracker.yvel - 2 * dotp * normy)

            return True
        return False
    else:
        return False


def dynamic_collision_detector(tracker1, tracker2, r1, r2, e=0.85):
    dx = tracker1.getx() - tracker2.getx()
    dy = tracker1.gety() - tracker2.gety()
    norm2 = dx ** 2 + dy ** 2
    minimmum_dist = r1 + r2

    if 0 < norm2 < minimmum_dist ** 2:
        norm = sqrt(norm2)

        # Correct unit normal vector (was dividing by dist_sq before — bug)
        normx = dx / norm
        normy = dy / norm

        # Push balls apart so they no longer overlap
        overlap = (minimmum_dist - norm) / 2
        tracker1.xpos += normx * overlap
        tracker1.ypos += normy * overlap
        tracker2.xpos -= normx * overlap
        tracker2.ypos -= normy * overlap

        # Relative velocity along the normal
        rel_vx = tracker1.xvel - tracker2.xvel
        rel_vy = tracker1.yvel - tracker2.yvel
        norm_vel = rel_vx * normx + rel_vy * normy

        # Only resolve if balls are actually moving toward each other
        if norm_vel < 0:
            # Equal mass + restitution impulse
            impulse = (1 + e) * norm_vel / 2
            tracker1.xvel -= impulse * normx
            tracker1.yvel -= impulse * normy
            tracker2.xvel += impulse * normx
            tracker2.yvel += impulse * normy
            return True
        return False