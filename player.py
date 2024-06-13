import socket
import json
import tkinter as tk
from tkinter import messagebox
import threading

class TicTacToeClient(tk.Tk):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.title("Fitxe-Fatxe")
        self.server_ip = server_ip
        self.server_port = server_port
        self.player = None
        self.current_turn = 'X'
        self.last_winner = 'X'  # Para armazenar o vencedor do último jogo
        self.client_socket = None
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.logged_in = False
        self.create_register_widgets()
        
    def create_login_widgets(self):
            self.clear_widgets()
            self.username_label = tk.Label(self, text="nome:")
            self.username_label.grid(row=0, column=0)
            self.username_entry = tk.Entry(self)
            self.username_entry.grid(row=0, column=1)
            
            self.password_label = tk.Label(self, text="Password:")
            self.password_label.grid(row=1, column=0)
            self.password_entry = tk.Entry(self, show="*")
            self.password_entry.grid(row=1, column=1)
            
            self.login_button = tk.Button(self, text="Login", command=self.login)
            self.login_button.grid(row=2, column=0, columnspan=2)
            
            self.register_link = tk.Label(self, text="Não tem conta? Registre aqui.", fg="blue", cursor="hand2")
            self.register_link.grid(row=3, column=0, columnspan=2)
            self.register_link.bind("<Button-1>", lambda e: self.create_register_widgets())

    def create_register_widgets(self):
        self.clear_widgets()
        self.username_label = tk.Label(self, text="nome de Usuario:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)
        
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)
        
        self.register_button = tk.Button(self, text="Registar", command=self.register)
        self.register_button.grid(row=2, column=0, columnspan=2)
        
        self.login_link = tk.Label(self, text="Já tem conta? Faça Login aqui.", fg="blue", cursor="hand2")
        self.login_link.grid(row=3, column=0, columnspan=2)
        self.login_link.bind("<Button-1>", lambda e: self.create_login_widgets())

   
    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.grid_remove()

    def create_game_widgets(self):
        self.clear_widgets()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self, text='', font='normal 20 bold', width=5, height=2,
                                               command=lambda i=i, j=j: self.make_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)
        
        self.message_list = tk.Listbox(self, height=5, width=50)
        self.message_list.grid(row=3, column=0, columnspan=3)

        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.grid(row=4, column=0, columnspan=2)

        self.send_button = tk.Button(self, text="Enviar", command=self.send_message)
        self.send_button.grid(row=4, column=2)
        self.create_ranking_table()
        
    def create_ranking_table(self):
        self.ranking_frame = tk.Frame(self)
        self.ranking_frame.grid(row=5, column=0, columnspan=3, pady=10)

        tk.Label(self.ranking_frame, text="Ranking", font="bold").grid(row=0, column=0, columnspan=4)

        # Cabeçalho da tabela
        tk.Label(self.ranking_frame, text="Rank", font="bold").grid(row=1, column=0)
        tk.Label(self.ranking_frame, text="Player", font="bold").grid(row=1, column=1)
        tk.Label(self.ranking_frame, text="Wins", font="bold").grid(row=1, column=2)
        tk.Label(self.ranking_frame, text="Draws", font="bold").grid(row=1, column=3)
        tk.Label(self.ranking_frame, text="Points", font="bold").grid(row=1, column=4)

   
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Erro ao registar", "Por faavor insira nome e password! ")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            register_data = {'action': 'register', 'username': username, 'password': password}
            self.client_socket.send((json.dumps(register_data) + "\n").encode('utf-8'))
            
            response = self.client_socket.recv(1024).decode('utf-8').strip()
            response_data = json.loads(response)

            if response_data['status'] == 'success':
                messagebox.showinfo("Registrado com sucesso", "Por favor faça Login!")
                self.create_login_widgets()
            else:
                messagebox.showerror("Erro de registro", response_data['message'])
                self.client_socket.close()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Não foi possivel conectar com o servidor: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Erro de Login","Por faavor insira o nome e a password! ")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            login_data = {'action': 'login', 'username': username, 'password': password}
            self.client_socket.send((json.dumps(login_data) + "\n").encode('utf-8'))
            
            response = self.client_socket.recv(1024).decode('utf-8').strip()
            response_data = json.loads(response)

            if response_data['status'] == 'success':
                self.player = response_data['player']
                self.logged_in = True
                self.create_game_widgets()
                threading.Thread(target=self.receive_messages).start()
            else:
                messagebox.showerror("Login Error", response_data['message'])
                self.client_socket.close()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Não foi possivel conectar com o servidor: {e}")

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
            except Exception as e:
                messagebox.showerror("Connection Error", f"Error: {e}")
    
    def update_ranking_table(self, ranking):
        for widget in self.ranking_frame.winfo_children():
            widget.grid_remove()

        tk.Label(self.ranking_frame, text="Ranking", font="bold").grid(row=0, column=0, columnspan=4)

        # Cabeçalho da tabela
        tk.Label(self.ranking_frame, text="Rank", font="bold").grid(row=1, column=0)
        tk.Label(self.ranking_frame, text="Player", font="bold").grid(row=1, column=1)
        tk.Label(self.ranking_frame, text="Wins", font="bold").grid(row=1, column=2)
        tk.Label(self.ranking_frame, text="Draws", font="bold").grid(row=1, column=3)
        tk.Label(self.ranking_frame, text="Points", font="bold").grid(row=1, column=4)

        for i, user in enumerate(ranking):
            tk.Label(self.ranking_frame, text=user['rank']).grid(row=i+2, column=0)
            tk.Label(self.ranking_frame, text=user['username']).grid(row=i+2, column=1)
            tk.Label(self.ranking_frame, text=user['wins']).grid(row=i+2, column=2)
            tk.Label(self.ranking_frame, text=user['draws']).grid(row=i+2, column=3)
            tk.Label(self.ranking_frame, text=user['points']).grid(row=i+2, column=4)

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
                    elif data['action'] == 'user_info':
                        self.update_user_info(data['user_info'])
                    elif data['action'] == 'ranking':
                        self.update_ranking(data['ranking'])
            except Exception as e:
                messagebox.showerror("Connection Error", f"Error receiving message: {e}")
                break

    def update_ranking(self, ranking):
        # Atualiza a tabela de ranking com base nos dados recebidos
        self.clear_ranking_table()
        for i, user in enumerate(ranking):
            tk.Label(self.ranking_frame, text=user['username']).grid(row=i+2, column=0)
            tk.Label(self.ranking_frame, text=user['wins']).grid(row=i+2, column=1)
            tk.Label(self.ranking_frame, text=user['draws']).grid(row=i+2, column=2)
            tk.Label(self.ranking_frame, text=user['points']).grid(row=i+2, column=3)

    def clear_ranking_table(self):
        for widget in self.ranking_frame.winfo_children():
            widget.destroy()
        tk.Label(self.ranking_frame, text="Ranking", font="bold").grid(row=0, column=0, columnspan=3)
        tk.Label(self.ranking_frame, text="Jogador", font="bold").grid(row=1, column=0)
        tk.Label(self.ranking_frame, text="Vitorias(A)", font="bold").grid(row=1, column=1)
        tk.Label(self.ranking_frame, text="Empates", font="bold").grid(row=1, column=2)
        tk.Label(self.ranking_frame, text="Pts", font="bold").grid(row=1, column=3)


    def update_user_info(self, user_info):
        self.username = user_info['username']
        self.wins = user_info['wins']
        self.points = user_info['points']
        self.draws = user_info['draws']
        self.title(f"Tic Tac Toe - Player {self.username} - Wins: {self.wins}, Points: {self.points}, Draws: {self.draws}")


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
            except Exception as e:
                messagebox.showerror("Connection Error", f"Error: {e}")
            self.message_entry.delete(0, tk.END)

    def show_winner(self, winner):
        if winner == 'Draw':
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.last_winner = winner  # Armazenar o vencedor do jogo
        self.reset_board()

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = self.last_winner if self.last_winner != 'Draw' else 'X'  # Definir o turno inicial com base no vencedor anterior ou 'X' se empate
        self.update_buttons()
        self.title(f"Tic Tac Toe - Player {self.player} - {self.current_turn}'s turn")


    def update_turn(self, player):
        self.current_turn = player
        self.title(f"Tic Tac Toe - Player {self.player} - {player}'s turn")

if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    app = TicTacToeClient(server_ip, server_port)
    app.mainloop()