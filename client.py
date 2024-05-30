import socket
import json
import tkinter as tk
from tkinter import messagebox
import threading

class TicTacToeClient(tk.Tk):
    def __init__(self, player, server_ip, server_port):
        super().__init__()
        self.title("Tic Tac Toe")
        self.player = player
        self.current_turn = 'X'  # O jogo começa com o jogador 'X'
        self.server_ip = server_ip
        self.server_port = server_port
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.connect_to_server()

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self, text='', font='normal 20 bold', width=5, height=2,
                                               command=lambda i=i, j=j: self.make_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)

        self.message_list = tk.Listbox(self, height=5, width=50)
        self.message_list.grid(row=3, column=0, columnspan=3)

        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.grid(row=4, column=0, columnspan=2)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=4, column=2)

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.send((json.dumps({'action': 'join', 'player': self.player}) + "\n").encode('utf-8'))
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to server: {e}")
            self.destroy()

    def make_move(self, i, j):
        if self.board[i][j] == '' and self.player == self.current_turn:
            move = {
                'action': 'move',
                'player': self.player,
                'x': i,
                'y': j
            }
            try:
                self.client_socket.send((json.dumps(move) + "\n").encode('utf-8'))
            except ConnectionAbortedError as e:
                print("Error:", e)
                # Adicione qualquer outra ação necessária para lidar com o erro de conexão

    def receive_messages(self):
        buffer = ""
        while True:
            try:
                buffer += self.client_socket.recv(1024).decode('utf-8')
                while "\n" in buffer:
                    msg, buffer = buffer.split("\n", 1)
                    data = json.loads(msg)
                    if data['action'] == 'message':
                        self.update_messages(data['message'])
                    elif data['action'] == 'update':
                        self.board = data['board']
                        self.update_buttons()
                    elif data['action'] == 'game_over':
                        winner = data['winner']
                        self.show_winner(winner)
                    elif data['action'] == 'reset':
                        self.reset_board()
                    elif data['action'] == 'turn':
                        self.update_turn(data['player'])
            except Exception as e:
                print("Error receiving message:", e)
                break

    def update_messages(self, message):
        self.message_list.insert(tk.END, message)

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])

    def send_message(self):
        message = self.message_entry.get()
        if message:
            msg = {
                'action': 'message',
                'player': self.player,
                'message': message
            }
            try:
                self.client_socket.send((json.dumps(msg) + "\n").encode('utf-8'))
            except ConnectionAbortedError as e:
                print("Error:", e)
                # Adicione qualquer outra ação necessária para lidar com o erro de conexão
            self.message_entry.delete(0, tk.END)

    def show_winner(self, winner):
        if winner == 'Draw':
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
        self.reset_board()

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.update_buttons()

    def update_turn(self, player):
        self.current_turn = player
        self.title(f"Tic Tac Toe - Player {self.player} - {player}'s turn")

if __name__ == "__main__":
    player = input("Choose your player (X or O): ").upper()
    if player not in ['X', 'O']:
        print("Invalid player choice. Please choose X or O.")
    else:
        server_ip = input("Enter server IP: ")
        server_port = int(input("Enter server port: "))
        app = TicTacToeClient(player, server_ip, server_port)
        app.mainloop()
