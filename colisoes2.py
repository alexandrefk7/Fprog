from math import sqrt

COEF = 0.85  # velocidade de saída


def line_collision(tracker, ball_r, px, py, nx, ny):

    #vetor do ponto da linha para o centro da bola
    dx = tracker.getx() - px
    dy = tracker.gety() - py

    #distância perpendicular da bola à linha
    dist = dx * nx + dy * ny

    if dist < ball_r:
        #corrige a posição para não penetrar
        penetracao = ball_r - dist
        tracker.xpos += nx * penetracao
        tracker.ypos += ny * penetracao

        #reflexão elástica da velocidade
        dot = tracker.xvel * nx + tracker.yvel * ny
        if dot < 0:
            tracker.xvel = COEF * (tracker.xvel - 2 * dot * nx)
            tracker.yvel = COEF * (tracker.yvel - 2 * dot * ny)

        return True
    return False


def circle_collision(tracker, ball_r, cx, cy, cr):
    dx = tracker.getx() - cx
    dy = tracker.gety() - cy

    #colides
    dist_sq = dx ** 2 + dy ** 2
    min_dist = ball_r + cr

    if dist_sq < min_dist ** 2 and dist_sq > 0:

        #calcula a raiz quadrada se a colisão acontecer
        dist = sqrt(dist_sq)

        #vetor normal: do centro do objeto para o centro da bola
        nx = dx / dist
        ny = dy / dist

        #empurra a bola para fora da sobreposição
        tracker.xpos = cx + nx * (min_dist + 0.1)
        tracker.ypos = cy + ny * (min_dist + 0.1)

        # reflexão
        dot = tracker.xvel * nx + tracker.yvel * ny
        if dot < 0:  # bola a mover-se em direção ao objeto
            tracker.xvel = COEF * (tracker.xvel - 2 * dot * nx)
            tracker.yvel = COEF * (tracker.yvel - 2 * dot * ny)

        return True
    return False