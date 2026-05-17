from graphics import*
#cia a linha com medições de distância
def create_line(window):
    big_line=Line(Point(-10, 0), Point(210, 0))
    big_line.draw(window)
    for val in range(0, 210, 50):
        line = Line(Point(val, 0), Point(val, 4))
        line.draw(window)
        mark = Text(Point(val, -5), f"{val}")
        mark.draw(window)
#Cria um cesto
def create_basket(win):
    left_side=Circle(Point(160, 100), 3)
    left_side.draw(win)
    right_side=Circle(Point(200, 100), 3)
    right_side.draw(win)
    line=Line(Point(160, 103), Point(200, 103))
    line.draw(win)

class ScoreBoard:
    def __init__(self, win):
        self.message = Text(Point(100, 100), "BOA!")
        self.score_number=0
        self.scoreboard=Text(Point(15, 150), f"Score: {self.score_number}")
        self.scoreboard.draw(win)
    def update_score(self):
        self.score_number+=2
        self.scoreboard.setText(f"Score: {self.score_number}")
    def flash(self, win):
        self.message.setSize(20)
        self.message.draw(win)
        self.message.undraw()
#cria a classe botão
class Button:
    def __init__(self, window, center, width, height, label):
        self.active=True

        w,h = width/2.0, height/2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(window)
        self.label = Text(center, label)
        self.label.draw(window)
        self.deactivate()

        #ativa o botão
    def activate(self):

        self.label.setFill("black")
        self.rect.setWidth(2)
        self.active = True
#impossibilita o uso do botão
    def deactivate(self):

        self.label.setFill("darkgrey")
        self.rect.setWidth(1)
        self.active = 0
#verifica se o botão foi pressionado
    def clicked(self, p):

        return self.active and \
            self.xmin <= p.getX() <= self.xmax and \
            self.ymin <= p.getY() <= self.ymax

#cria a janela que aceita os valores escolhidos pelo utilizador
class InputDialog:
    #inicializa uma nova janela onde vão ser colocados os valores
    def __init__(self, angle, vel0):
        self.win=window=GraphWin("Valores Iniciais", 200, 300, autoflush=False)
        self.win.setCoords(0, 5, 4, 0.5)
        self.win.setBackground("grey")

        Text(Point(1,2), "Angulo").draw(window)
        self.angle = Entry(Point(3,2), 5)
        self.angle.draw(window)
        self.angle.setText(str(angle))

        Text(Point(1,3.5 ), "Velocidade").draw(window)
        self.vel=Entry(Point(3,3.5), 5)
        self.vel.draw(window)
        self.vel.setText(str(vel0))

        # Text(Point(1, 3), "Altura").draw(window)
        # self.height = Entry(Point(3, 3), 5)
        # self.height.draw(window)
        # self.height.setText(str(height))


        self.shoot = Button(window, Point(1, 4.5), 1.25, .5, "Disparar!")
        self.shoot.activate()
        self.quit = Button(window, Point(3, 4.5), 1.25, .5, "Sair")
        self.quit.activate()

#cria um utcome para cada botão possivelmente pressionado
    def interaction(self):
        while True:
            pt=self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            elif self.shoot.clicked(pt):
                return "Fire!"
#Guarda os valores do utilizador
    def collect_values(self):
        angle=float(self.angle.getText())
        vel0=float(self.vel.getText())
        # height=float(self.height.getText())
        return angle,vel0

    def close(self):
        self.win.close()

def parabola(left_side_xcord, win):
    while left_side_xcord < 10:
        point=Point(left_side_xcord, left_side_xcord**2)
        nextx_coord=left_side_xcord+0.2
        next_point=Point(nextx_coord, nextx_coord**2)
        line=Line(point, next_point)
        line.draw(win)
        left_side_xcord+=0.2


class StickMan:
    def __init__(self, win):

        #Bola
        self.ball = Circle(Point(23, 48), 6)
        self.ball.draw(win)
        self.ball.setFill("orange")
        self.ball.setOutline("black")

        #Cabeça e tronco
        self.head=Circle(Point(5, 60), 8)
        self.head.setWidth(2)
        self.head.draw(win)
        self.torso=Line(Point(5,52), Point(5,30))
        self.torso.setWidth(2)
        self.torso.draw(win)
        #Pernas
        self.rleg=Line(Point(5, 30),Point(14, 0))
        self.rleg.setWidth(2)
        self.rleg.draw(win)
        self.lleg=Line(Point(5, 30), Point(-5, 0))
        self.lleg.setWidth(2)
        self.lleg.draw(win)
        #primeiro braço(trás, esqeurda)
        self.larm1=Line(Point(5, 50), Point(15, 40))
        self.larm1.setWidth(2)
        self.larm1.draw(win)
        self.larm2=Line(Point(15, 40), Point(18, 50))
        self.larm2.setWidth(2)
        self.larm2.draw(win)

        #segundo braço(frente, direita)
        self.rarm1 = Line(Point(5, 50), Point(10, 35))
        self.rarm1.setWidth(2)
        self.rarm1.draw(win)
        self.rarm2 = Line(Point(10, 35), Point(25, 45))
        self.rarm2.setWidth(2)
        self.rarm2.draw(win)

    def clear_arms(self):
        self.ball.undraw()
        self.rarm1.undraw()
        self.rarm2.undraw()
        self.larm1.undraw()
        self.larm2.undraw()
    def shoot(self, win):
        self.clear_arms()

        self.larm1 = Line(Point(5, 50), Point(20, 55))
        self.larm1.setWidth(2)
        self.larm1.draw(win)
        self.larm2 = Line(Point(20, 55), Point(24, 64))
        self.larm2.setWidth(2)
        self.larm2.draw(win)

        # segundo braço(frente, direita)
        self.rarm1 = Line(Point(5, 50), Point(25, 58))
        self.rarm1.setWidth(2)
        self.rarm1.draw(win)
        self.rarm2 = Line(Point(25, 58), Point(40, 68 ))
        self.rarm2.setWidth(2)
        self.rarm2.draw(win)








