from graphics import *
from entities import Menu
from cenario3 import cen3
from cen2 import cen2
from cenario4 import cenario4
from cenario1 import cen1

"""
main — ponto de entrada do simulador; gere o menu principal e abre os cenários.
cria a janela de menu a cada iteração e aguarda a escolha do utilizador.
quando o utilizador sai do menu sem escolher, o ciclo termina e o programa encerra.
"""
def main():
    while True:
        # menu
        win_menu = GraphWin("Menu Principal - Simulador", 500, 600, autoflush=False)
        win_menu.setCoords(0, 0, 6, 8.5)
        win_menu.setBackground("white")

        
        # instancia o menu e desenha os elementos gráficos
        menu_importado = Menu(win_menu)

        # lista usada como contentor mutável para capturar a escolha dentro da função interna
        cenario_escolhido = [None]

        # substitui o placeholder do menu pelo comportamento real de abertura
        def abrir_cenario_real(num):
            cenario_escolhido[0] = num
            win_menu.close()
        # injeta a função real no objeto menu
        menu_importado._abre_cenario = abrir_cenario_real

        # corre o loop do menu até o utilizador sair ou escolher um cenário
        menu_importado.run()

        # se saiu sem escolher cenário, termina o simulador
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