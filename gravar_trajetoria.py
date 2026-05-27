from graphics import *
from datetime import datetime
import numpy as np
import tkinter as tk
from tkinter import filedialog

# inicializa a data/hora de início e as listas de pontos da trajetória
def start_trajectory():
    return datetime.now(), 0.0, [], [], []

# acrescenta um novo ponto (t, x, y) às listas e avança o contador de tempo
def record_point(trajectory_t, trajectory_x, trajectory_y, tempo_atual, bola_x, bola_y):
    trajectory_t.append(round(tempo_atual, 4))
    trajectory_x.append(round(bola_x, 4))
    trajectory_y.append(round(bola_y, 4))
    tempo_atual = round(tempo_atual + 0.002, 4)
    return tempo_atual

# guarda a trajetória num ficheiro de texto escolhido pelo utilizador
def save_trajectory(win, trajectory_t, trajectory_x, trajectory_y, data_hora_inicio, largura, altura):
    # abre a janela de diálogo para selecionar o destino do ficheiro
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    nome_ficheiro = filedialog.asksaveasfilename(
         defaultextension=".txt",
         filetypes=[("Ficheiros de Texto", "*.txt"), ("Todos os Ficheiros", "*.*")],
         title="Guardar Trajetória",
         parent=root
    )

    if not nome_ficheiro:
        return

    # converte as listas em arrays numpy
    arr_t = np.array(trajectory_t)
    arr_x = np.array(trajectory_x)
    arr_y = np.array(trajectory_y)

    # formata cada conjunto de valores como uma string separada por espaços
    data_hora_str = data_hora_inicio.strftime("%c")
    tempos_str    = " ".join(str(t) for t in arr_t)
    xs_str        = " ".join(str(x) for x in arr_x)
    ys_str        = " ".join(str(y) for y in arr_y)

    # escreve data/hora, tempos e coordenadas x e y em linhas separadas
    with open(nome_ficheiro, "w") as f:
        f.write(data_hora_str + "\n")
        f.write(tempos_str    + "\n")
        f.write(xs_str        + "\n")
        f.write(ys_str        + "\n")
