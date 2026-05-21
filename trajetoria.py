from tkinter import filedialog
from graphics import *
from button import Button

def gravar(data_inicio, tempos, xs, ys):
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Ficheiro de texto", "*.txt")],
        title="Guardar trajetoria"
    )
    if path == "":
        return
    f = open(path, "w")
    f.write(data_inicio + "\n")
    f.write(" ".join([str(t) for t in tempos]) + "\n")
    f.write(" ".join([str(x) for x in xs]) + "\n")
    f.write(" ".join([str(y) for y in ys]) + "\n")
    f.close()

def janela_gravar(data_inicio, tempos, xs, ys):
    win = GraphWin("Gravar trajetoria", 260, 90)
    win.master.geometry("+50+50")
    win.setCoords(0, 0, 5, 2)
    win.setBackground("lightgrey")
    Text(Point(2.5, 1.5), "Deseja guardar a trajetoria?").draw(win)
    btn_sim = Button(win, Point(1.3, 0.7), 2.2, 0.7, "Gravar")
    btn_sim.activate()
    btn_nao = Button(win, Point(3.7, 0.7), 2.2, 0.7, "Continuar")
    btn_nao.activate()
    while True:
        try:
            p = win.getMouse()
        except GraphicsError:
            return
        if btn_sim.clicked(p):
            win.close()
            gravar(data_inicio, tempos, xs, ys)
            return
        if btn_nao.clicked(p):
            win.close()
            return
