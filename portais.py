from math import sqrt
from graphics import *


class PortalPair:

    def __init__(self, win, centro1, normal1, centro2, normal2, largura,
                 cor1="blue", cor2="orange"):

        self.win     = win
        self.largura = largura
        self.cor1    = cor1
        self.cor2    = cor2
        self.p1, self.linha1 = self._create(win, centro1, normal1, largura, cor1)
        self.p2, self.linha2 = self._create(win, centro2, normal2, largura, cor2)

    def _create(self, win, centro, normal, largura, cor):
        """Creates a portal: normalises the vector, computes the tangent and draws the line."""
        cx, cy = centro.getX(), centro.getY()
        m = sqrt(normal[0]**2 + normal[1]**2)
        nx, ny = normal[0] / m, normal[1] / m
        tx, ty = -ny, nx          # tangent perpendicular to normal
        meia = largura / 2
        linha = Line(Point(cx - tx*meia, cy - ty*meia),
                     Point(cx + tx*meia, cy + ty*meia))
        linha.setFill(cor)
        linha.setWidth(4)
        linha.draw(win)
        return (cx, cy, nx, ny, tx, ty), linha

    def move_p1(self, dx, dy):
        """Moves the entry portal (p1) by (dx, dy) and redraws it."""
        cx, cy, nx, ny, tx, ty = self.p1
        cx += dx
        cy += dy
        self.linha1.undraw()
        meia = self.largura / 2
        self.linha1 = Line(Point(cx - tx*meia, cy - ty*meia),
                           Point(cx + tx*meia, cy + ty*meia))
        self.linha1.setFill(self.cor1)
        self.linha1.setWidth(4)
        self.linha1.draw(self.win)
        self.p1 = (cx, cy, nx, ny, tx, ty)

    def move_p2(self, dx, dy):
        """Moves the exit portal (p2) by (dx, dy) and redraws it."""
        cx, cy, nx, ny, tx, ty = self.p2
        cx += dx
        cy += dy
        self.linha2.undraw()
        meia = self.largura / 2
        self.linha2 = Line(Point(cx - tx*meia, cy - ty*meia),
                           Point(cx + tx*meia, cy + ty*meia))
        self.linha2.setFill(self.cor2)
        self.linha2.setWidth(4)
        self.linha2.draw(self.win)
        self.p2 = (cx, cy, nx, ny, tx, ty)

    def _in_zone(self, tracker, ball_r, portal):
        """Checks whether the ball is inside the detection zone of the portal."""
        cx, cy, nx, ny, tx, ty = portal
        dx = tracker.getx() - cx
        dy = tracker.gety() - cy
        dist_n = abs(dx*nx + dy*ny)    # perpendicular distance to portal
        dist_t = abs(dx*tx + dy*ty)    # distance along portal
        return dist_n <= ball_r and dist_t <= self.largura / 2

    def _teleport(self, tracker, ball_r, p_entrada, p_saida):
        """Applies the velocity and position transform between the two portals.

        The velocity is decomposed in the entry portal frame (normal component vn
        and tangential component vt) and recomposed in the exit portal frame,
        preserving the magnitude.
        """
        _, _, nx_e, ny_e, tx_e, ty_e = p_entrada
        cx_s, cy_s, nx_s, ny_s, tx_s, ty_s = p_saida

        # Decompose in entry portal frame
        vn = tracker.xvel * nx_e + tracker.yvel * ny_e   # normal component
        vt = tracker.xvel * tx_e + tracker.yvel * ty_e   # tangential component

        # Recompose in exit portal frame (|v| preserved)
        tracker.xvel = vn * nx_s + vt * tx_s
        tracker.yvel = vn * ny_s + vt * ty_s

        # Place ball just outside exit portal (prevents re-detection)
        tracker.xpos = cx_s + nx_s * (ball_r + 0.5)
        tracker.ypos = cy_s + ny_s * (ball_r + 0.5)

    def apply(self, tracker, ball_r):
        """Checks whether the ball enters one of the portals and applies teleportation.

        Returns True if teleportation occurred, False otherwise.
        Must be called every animation loop step.
        """
        _, _, nx1, ny1, _, _ = self.p1
        if self._in_zone(tracker, ball_r, self.p1):
            if tracker.xvel * nx1 + tracker.yvel * ny1 > 0:  # ball entering p1
                self._teleport(tracker, ball_r, self.p1, self.p2)
                return True

        _, _, nx2, ny2, _, _ = self.p2
        if self._in_zone(tracker, ball_r, self.p2):
            if tracker.xvel * nx2 + tracker.yvel * ny2 > 0:  # ball entering p2
                self._teleport(tracker, ball_r, self.p2, self.p1)
                return True

        return False
