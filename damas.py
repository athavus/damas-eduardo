import tkinter as tk

# Função para criar o tabuleiro de damas
def criar_tabuleiro():
    tabuleiro = tk.Tk()
    tabuleiro.title("Tabuleiro de Damas")

    # Defina o tamanho do tabuleiro
    largura_casa = 50
    altura_casa = 50
    tamanho_tabuleiro = 8 # Tabuleiro 8x8

    # Crie um canvas para desenhar o tabuleiro
    canvas = tk.Canvas(tabuleiro, width=largura_casa * tamanho_tabuleiro, height=altura_casa * tamanho_tabuleiro)
    canvas.pack()

    # Desenhe as casas escuras e claras e adicione peças nas casas escuras
    for linha in range(tamanho_tabuleiro):
        for coluna in range(tamanho_tabuleiro):
            x0 = coluna * largura_casa
            y0 = linha * altura_casa
            x1 = x0 + largura_casa
            y1 = y0 + altura_casa
            cor = "black" if (linha + coluna) % 2 == 0 else "white"
            canvas.create_rectangle(x0, y0, x1, y1, fill=cor)

            # Adicione peças nas casas escuras (exemplo: círculos)
            if cor == "black":
                canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="blue")

    tabuleiro.mainloop()


def iniciar_jogo():
  criar_tabuleiro()
  

def sair_do_jogo():
  menu.destroy()


#criando menu
menu = tk.Tk()
menu.title("menu inicial")

#criando rotulos
titulo_label = tk.Label(menu, text="bem vindo ao jogo de damas")
titulo_label.pack(pady=20)

novo_jogo_button = tk.Button(menu, text="Novo Jogo", command=iniciar_jogo)
novo_jogo_button.pack(pady=10)

sair_button = tk.Button(menu, text="Sair", command=sair_do_jogo)
sair_button.pack(pady=10)

menu.mainloop()
  
# Chame a função para criar o tabuleiro com peças
iniciar_jogo()
criar_tabuleiro()
