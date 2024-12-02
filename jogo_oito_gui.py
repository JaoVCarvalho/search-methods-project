# jogo_oito_gui.py
import tkinter as tk
from tkinter import messagebox
from a_star_search import a_star, generate_puzzle, print_puzzle  # Importando funções do arquivo de busca

# Função para verificar se o tabuleiro é solucionável
def is_solvable(state):
    inversion_count = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] and state[j] and state[i] > state[j]:
                inversion_count += 1
    return inversion_count % 2 == 0

# Gerar um tabuleiro solucionável
def generate_solvable_puzzle():
    while True:
        state = generate_puzzle()
        if is_solvable(state):
            return state

# Classe para a interface gráfica
class PuzzleGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo dos Oito - A* Algorithm")
        self.geometry("400x500")  # Aumentar o tamanho da janela para se ajustar aos elementos
        self.resizable(True, True)  # Permitir redimensionamento
        self.configure(bg="#f0f0f0")  # Cor de fundo da janela

        # Gerar o tabuleiro inicial e o objetivo
        self.initial_state = generate_solvable_puzzle()
        self.goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]  # Novo estado objetivo
        self.solution = []

        self.create_widgets()

    def create_widgets(self):
        # Botão para gerar um novo tabuleiro
        self.generate_button = tk.Button(self, text="Novo Jogo", command=self.generate_new_game,
                                         font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="solid", bd=2,
                                         width=20, height=2)
        self.generate_button.pack(pady=10)

        # Frame para exibir os botões do tabuleiro
        self.puzzle_frame = tk.Frame(self, bg="#f0f0f0")
        self.puzzle_frame.pack(pady=10)

        # Botão para mostrar a solução
        self.solve_button = tk.Button(self, text="Mostrar Solução", command=self.show_solution,
                                      font=("Helvetica", 12), bg="#FF5733", fg="white", relief="solid", bd=2,
                                      width=20, height=2)
        self.solve_button.pack(pady=10)

        # Criar o tabuleiro inicial
        self.create_puzzle(self.initial_state)

    def create_puzzle(self, state):
        # Limpar o tabuleiro anterior
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()

        self.tiles = []
        for i in range(9):
            tile_value = state[i] if state[i] != 0 else ''
            button = tk.Button(self.puzzle_frame, text=str(tile_value), font=("Helvetica", 14), width=6, height=3,
                               bg="#fff", fg="#333", relief="raised", bd=3,
                               activebackground="#4CAF50", activeforeground="white",
                               state=tk.DISABLED)
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.tiles.append(button)

    def generate_new_game(self):
        # Gerar um novo tabuleiro solucionável
        self.initial_state = generate_solvable_puzzle()
        self.create_puzzle(self.initial_state)

    def show_solution(self):
        # Antes de tentar resolver, verificamos se o tabuleiro é solucionável
        if not is_solvable(self.initial_state):
            messagebox.showerror("Erro", "Este tabuleiro não é solucionável.")
            return

        # Resolver o tabuleiro e mostrar a solução
        self.solution = a_star(self.initial_state, self.goal_state)
        if self.solution:
            self.display_solution_step(0)
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar uma solução")

    def display_solution_step(self, step_index):
        if step_index < len(self.solution):
            self.create_puzzle(self.solution[step_index])
            self.after(1000, self.display_solution_step, step_index + 1)

# Iniciar o aplicativo
if __name__ == "__main__":
    app = PuzzleGame()
    app.mainloop()
