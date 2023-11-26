import tkinter as tk
from tkinter import messagebox

class Peca:
    def __init__(self, cor, rei=False):
        self.cor = cor
        self.rei = rei

class TabuleiroDamas:
    def __init__(self, root, tamanho_tabuleiro=8):
        self.root = root
        self.tamanho_tabuleiro = tamanho_tabuleiro
        self.largura_casa = 50
        self.altura_casa = 50
        self.tabuleiro = [[None for _ in range(tamanho_tabuleiro)] for _ in range(tamanho_tabuleiro)]
        self.peca_selecionada = None

        self.criar_tabuleiro()
        self.adicionar_pecas_iniciais()

    def criar_tabuleiro(self):
        self.canvas = tk.Canvas(self.root, width=self.largura_casa * self.tamanho_tabuleiro,
                                height=self.altura_casa * self.tamanho_tabuleiro)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clique)

    def adicionar_pecas_iniciais(self):
        # Adicione peças às casas escuras iniciais
        for linha in range(3):
            for coluna in range(self.tamanho_tabuleiro):
                if (linha + coluna) % 2 != 0:
                    self.tabuleiro[linha][coluna] = Peca("branca")

        for linha in range(self.tamanho_tabuleiro - 3, self.tamanho_tabuleiro):
            for coluna in range(self.tamanho_tabuleiro):
                if (linha + coluna) % 2 != 0:
                    self.tabuleiro[linha][coluna] = Peca("preta")

        self.atualizar_tabuleiro()

    def clique(self, event):
        coluna = event.x // self.largura_casa
        linha = event.y // self.altura_casa

        if self.peca_selecionada is None:
            self.selecionar_peca(linha, coluna)
        else:
            destino = (linha, coluna)
            if self.movimento_valido(self.peca_selecionada, destino):
                self.mover_peca(self.peca_selecionada, destino)
                if self.verificar_vencedor():
                    return  # Evitar que a função continue após o fim do jogo
            self.peca_selecionada = None

        self.atualizar_tabuleiro()

    def selecionar_peca(self, linha, coluna):
        if self.tabuleiro[linha][coluna] is not None:
            self.peca_selecionada = (linha, coluna)

    def mover_peca(self, origem, destino):
        linha_origem, coluna_origem = origem
        linha_destino, coluna_destino = destino
        self.tabuleiro[linha_destino][coluna_destino] = self.tabuleiro[linha_origem][coluna_origem]
        self.tabuleiro[linha_origem][coluna_origem] = None

    def movimento_valido(self, origem, destino):
        linha_origem, coluna_origem = origem
        linha_destino, coluna_destino = destino

        peca = self.tabuleiro[linha_origem][coluna_origem]

        if peca is not None:
            # Permitir movimento para qualquer direção, mas apenas uma casa por vez
            if abs(linha_destino - linha_origem) == 1 and abs(coluna_destino - coluna_origem) == 1:
                return True

        return False

    def verificar_vencedor(self):
        if not self.ha_movimentos_possiveis("preta"):
            messagebox.showinfo("Fim de Jogo", "As peças brancas venceram!")
            self.root.quit()
            return True
        elif not self.ha_movimentos_possiveis("branca"):
            messagebox.showinfo("Fim de Jogo", "As peças pretas venceram!")
            self.root.quit()
            return True
        else:
            return False  # Não há vencedor ainda

    def ha_movimentos_possiveis(self, cor):
        for linha in range(self.tamanho_tabuleiro):
            for coluna in range(self.tamanho_tabuleiro):
                if self.tabuleiro[linha][coluna] is not None and self.tabuleiro[linha][coluna].cor == cor:
                    if self.possui_movimentos_validos((linha, coluna)):
                        return True
        return False

    def possui_movimentos_validos(self, origem):
        linha_origem, coluna_origem = origem
        peca = self.tabuleiro[linha_origem][coluna_origem]

        for linha_destino in range(self.tamanho_tabuleiro):
            for coluna_destino in range(self.tamanho_tabuleiro):
                destino = (linha_destino, coluna_destino)
                if self.movimento_valido(origem, destino):
                    return True

        return False

    def atualizar_tabuleiro(self):
        self.canvas.delete("all")
        for linha in range(self.tamanho_tabuleiro):
            for coluna in range(self.tamanho_tabuleiro):
                x0 = coluna * self.largura_casa
                y0 = linha * self.altura_casa
                x1 = x0 + self.largura_casa
                y1 = y0 + self.altura_casa
                cor = "black" if (linha + coluna) % 2 == 0 else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor)

                peca = self.tabuleiro[linha][coluna]
                if peca:
                    cor_peca = "black" if peca.cor == "preta" else "white"
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=cor_peca)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jogo de Damas")
    tabuleiro = TabuleiroDamas(root)
    root.mainloop()
