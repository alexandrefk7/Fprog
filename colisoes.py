from math import sqrt

COEF = 0.85  # velocidade de saída

def colisao_chao(tracker, ball_r, floor_y=0):
    """Colisão com o chão: reflexão vertical com 85% da velocidade."""
    if tracker.gety() <= floor_y + ball_r:
        tracker.ypos = floor_y + ball_r     # corrige posição para não penetrar
        if tracker.yvel < 0:
            tracker.yvel = -tracker.yvel * COEF
            tracker.xvel *= COEF
        return True
    return False

def colisao_parede(tracker, ball_r, wall_x):
    """Colisão com parede vertical: reflexão horizontal com 85% da velocidade."""
    if tracker.getx() >= wall_x - ball_r:
        tracker.xpos = wall_x - ball_r     # corrige posição para não penetrar
        if tracker.xvel > 0:
            tracker.xvel = -tracker.xvel * COEF
            tracker.yvel *= COEF
        return True
    return False

def colisao_circulo(tracker, ball_r, cx, cy, cr):
    """Colisão elástica com objeto circular."""
    dx = tracker.getx() - cx
    dy = tracker.gety() - cy
    dist = sqrt(dx**2 + dy**2)
    min_dist = ball_r + cr
    if dist < min_dist and dist > 0:
        # Vetor normal: do centro do objeto para o centro da bola
        nx = dx / dist
        ny = dy / dist
        # Corrige posição: empurra a bola para fora da sobreposição
        tracker.xpos = cx + nx * (min_dist + 0.1)
        tracker.ypos = cy + ny * (min_dist + 0.1)
        # Reflexão: v_out = v_in - 2*(v_in · n)*n, escalada por 0.85
        dot = tracker.xvel * nx + tracker.yvel * ny
        if dot < 0:  # bola a mover-se em direção ao objeto
            tracker.xvel = COEF * (tracker.xvel - 2 * dot * nx)
            tracker.yvel = COEF * (tracker.yvel - 2 * dot * ny)
        return True
    return False
