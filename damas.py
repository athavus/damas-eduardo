import tkinter as tk
from tkinter import messagebox

class TelaBoasVindas:
    def __init__(self, root):
        self.root = root
        self.root.title("Bem-vindo ao Jogo de Damas")

        self.rotulo_boas_vindas = tk.Label(root, text="Bem-vindo ao Jogo de Damas", font=("Helvetica", 16))
        self.rotulo_boas_vindas.pack(pady=20)

        self.botao_jogar = tk.Button(root, text="Jogar", command=self.iniciar_jogo)
        self.botao_jogar.pack(pady=10)

    def iniciar_jogo(self):
        self.root.destroy()  # Fechar a tela de boas-vindas
        root_jogo = tk.Tk()
        root_jogo.title("Jogo de Damas")
        tabuleiro = TabuleiroDamas(root_jogo)
        root_jogo.mainloop()

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
        self.jogador_atual = "branca"  # Começa com as peças brancas

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
                if not self.captura_continua(destino):
                    if self.verificar_vencedor():
                        return  # Evitar que a função continue após o fim do jogo
                    self.passar_vez()
                self.peca_selecionada = None

        self.atualizar_tabuleiro()

    def captura_continua(self, destino):
        linha_destino, coluna_destino = destino

        for delta_linha in [-2, 2]:
            for delta_coluna in [-2, 2]:
                linha_captura = linha_destino + delta_linha // 2
                coluna_captura = coluna_destino + delta_coluna // 2
                if 0 <= linha_captura < self.tamanho_tabuleiro and 0 <= coluna_captura < self.tamanho_tabuleiro:
                    peca_capturada = self.tabuleiro[linha_captura][coluna_captura]
                    if peca_capturada is not None and peca_capturada.cor != self.jogador_atual:
                        if self.tabuleiro[linha_destino][coluna_destino] is None:
                            return True
        return False

    def selecionar_peca(self, linha, coluna):
        peca = self.tabuleiro[linha][coluna]
        if peca is not None and peca.cor == self.jogador_atual:
            self.peca_selecionada = (linha, coluna)

    def mover_peca(self, origem, destino):
        linha_origem, coluna_origem = origem
        linha_destino, coluna_destino = destino

        # Realizar a captura (remover a peça capturada)
        if abs(linha_destino - linha_origem) == 2 and abs(coluna_destino - coluna_origem) == 2:
            linha_captura = (linha_destino + linha_origem) // 2
            coluna_captura = (coluna_destino + coluna_origem) // 2
            self.tabuleiro[linha_captura][coluna_captura] = None

        # Mover a peça para o destino
        self.tabuleiro[linha_destino][coluna_destino] = self.tabuleiro[linha_origem][coluna_origem]
        self.tabuleiro[linha_origem][coluna_origem] = None

    def movimento_valido(self, origem, destino):
        linha_origem, coluna_origem = origem
        linha_destino, coluna_destino = destino

        peca = self.tabuleiro[linha_origem][coluna_origem]

        # Verificar se a casa de destino está vazia
        if self.tabuleiro[linha_destino][coluna_destino] is not None:
            return False

        # Permitir movimento para qualquer direção, mas apenas uma casa por vez
        if abs(linha_destino - linha_origem) == 1 and abs(coluna_destino - coluna_origem) == 1:
            return True

        # Verificar captura (movimento diagonal pulando uma peça)
        if abs(linha_destino - linha_origem) == 2 and abs(coluna_destino - coluna_origem) == 2:
            linha_captura = (linha_destino + linha_origem) // 2
            coluna_captura = (coluna_destino + coluna_origem) // 2

            peca_capturada = self.tabuleiro[linha_captura][coluna_captura]
            if peca_capturada is not None and peca_capturada.cor != self.jogador_atual:
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

    def passar_vez(self):
        self.jogador_atual = "branca" if self.jogador_atual == "preta" else "preta"

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
    root_boas_vindas = tk.Tk()
    tela_boas_vindas = TelaBoasVindas(root_boas_vindas)
    root_boas_vindas.mainloop()