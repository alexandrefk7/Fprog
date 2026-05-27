from graphics import *
from entities import Menu
from cenario1e3 import cen1, cen3
from cen2 import cen2
from cen4 import cenario4


def main():
    while True:
        # menu
        win_menu = GraphWin("Menu Principal - Simulador", 500, 600, autoflush=False)
        win_menu.setCoords(0, 0, 6, 8.5)
        win_menu.setBackground("white")

        
        menu_importado = Menu(win_menu)

        cenario_escolhido = [None]

        def abrir_cenario_real(num):
            cenario_escolhido[0] = num
            win_menu.close()
        menu_importado._abre_cenario = abrir_cenario_real

        menu_importado.run()

        if cenario_escolhido[0] is None:
            break

        # modulos
        escolha = cenario_escolhido[0]
        if escolha == 1:
            cen1()
        elif escolha == 2:
            cen2()
        elif escolha == 3:
            cen3()
        elif escolha == 4:
            cenario4()

    print("Simulador encerrado com sucesso.")


if __name__ == "__main__":
    main()