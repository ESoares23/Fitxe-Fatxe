import tkinter as tk
from tkinter import messagebox

# Definições do jogo
BOARD_SIZE = 3

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Fitxe-Fatxe")
        self.create_board_buttons()
        self.restart_game()
        
    def create_board_buttons(self):
        self.buttons = []
        for i in range(BOARD_SIZE):
            row_buttons = []
            for j in range(BOARD_SIZE):
                button = tk.Button(self.master, text="", width=5, height=2,
                                   font=("Helvetica", 24), command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
    
    def on_button_click(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.show_winner_message(self.current_player)
                self.restart_game()
            elif all(all(cell != " " for cell in row) for row in self.board):
                self.show_winner_message("Tie")
                self.restart_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
    
    def check_winner(self, player):
        # Verifica linhas e colunas
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == player for j in range(BOARD_SIZE)) or all(self.board[j][i] == player for j in range(BOARD_SIZE)):
                return True
        # Verifica diagonais
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)) or all(self.board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
            return True
        return False
    
    def show_winner_message(self, winner):
        if winner == "Tie":
            message = "Empate"
        else:
            message = f"O jogador {winner} venceu, parabens!"
        messagebox.showinfo("Game Over", message)
    
    def restart_game(self):
        self.board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = "X"
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(text="")

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
