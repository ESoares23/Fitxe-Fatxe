import socket
import threading
import json
import redis
import time

# Configuração do Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class TicTacToeServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        print("Server started, waiting for players...")
        self.clients = []
        self.game_id = "tictactoe_game"
        self.lock = threading.Lock()
        self.expiration_time = 60  # Expirar dados em 60 segundos
        self.current_player = 'X'  # Jogador que começa o jogo

        # Thread para expirar dados periodicamente
        threading.Thread(target=self.expire_cache_periodically, daemon=True).start()

    def expire_cache_periodically(self):
        while True:
            time.sleep(self.expiration_time)
            with self.lock:
                redis_client.expire(self.game_id, self.expiration_time)
                print("Cache invalidated.")

    def handle_client(self, client_socket, player):
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                data = json.loads(msg)
                if data['action'] == 'move':
                    self.handle_move(data, player)
                elif data['action'] == 'message':
                    self.handle_message(data)
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def handle_move(self, data, player):
        with self.lock:
            if player != self.current_player:
                # Não é a vez deste jogador
                return

            board = json.loads(redis_client.get(self.game_id) or json.dumps([['', '', ''], ['', '', ''], ['', '', '']]))
            x, y = data['x'], data['y']
            if board[x][y] == '':
                board[x][y] = player
                redis_client.set(self.game_id, json.dumps(board))
                self.broadcast({'action': 'update', 'board': board})
                winner = self.check_winner(board)
                if winner:
                    self.broadcast({'action': 'game_over', 'winner': winner})
                    self.reset_board()
                else:
                    # Alterna para o próximo jogador
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                    self.broadcast({'action': 'turn', 'player': self.current_player})

    def handle_message(self, data):
        self.broadcast({'action': 'message', 'player': data['player'], 'message': data['message']})

    def broadcast(self, msg):
        message = json.dumps(msg) + "\n"
        for client in self.clients:
            client.send(message.encode('utf-8'))

    def check_winner(self, board):
        # Verificar linhas
        for row in board:
            if row[0] == row[1] == row[2] != '':
                return row[0]

        # Verificar colunas
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != '':
                return board[0][col]

        # Verificar diagonais
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]

        # Verificar empate
        if all(cell != '' for row in board for cell in row):
            return 'Draw'

        return None

    def reset_board(self):
        # Reiniciar o tabuleiro
        redis_client.set(self.game_id, json.dumps([['', '', ''], ['', '', ''], ['', '', '']]))
        self.current_player = 'X'  # Reiniciar o jogador inicial
        self.broadcast({'action': 'reset'})

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Player connected from {addr}")
            self.clients.append(client_socket)
            player = 'X' if len(self.clients) == 1 else 'O'
            threading.Thread(target=self.handle_client, args=(client_socket, player)).start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
