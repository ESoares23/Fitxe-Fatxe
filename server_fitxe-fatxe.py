import socket
import threading
import json
import redis
import time
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Configuração do Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Configuração do MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['tictactoe_db']
users_collection = db['users']
users_collection.update_many({}, {'$set': {'draws': 0}})
users_collection.update_many({}, {'$set': {'points': 0}})
games_collection = db['games']

class TicTacToeServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        print("Server started, waiting for players...")
        self.clients = []
        self.connected_users = {}  # Dicionário para rastrear usuários conectados
        self.game_id = "tictactoe_game"
        self.lock = threading.Lock()
        self.expiration_time = 120  
        self.current_player = 'X'
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
                if data['action'] == 'register':
                    self.handle_register(data, client_socket)
                elif data['action'] == 'login':
                    self.handle_login(data, client_socket)
                elif data['action'] == 'move':
                    self.handle_move(data, player)
                elif data['action'] == 'message':
                    self.handle_message(data)
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def handle_login(self, data, client_socket):
        username = data['username']
        password = data['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            player = 'X' if len(self.clients) == 0 else 'O'
            response = {'status': 'success', 'player': player}
            self.clients.append(client_socket)
            self.connected_users[username] = client_socket  # Adiciona o usuário à lista de conectados
            users_collection.update_one({'username': username}, {'$set': {'socket': client_socket.getpeername()}})
            client_socket.send((json.dumps(response) + "\n").encode('utf-8'))
            self.send_user_info(client_socket)
            self.send_ranking()  # Envia o ranking atualizado
        else:
            response = {'status': 'error', 'message': 'Invalid username or password.'}
            client_socket.send((json.dumps(response) + "\n").encode('utf-8'))

    def handle_register(self, data, client_socket):
        username = data['username']
        password = data['password']
        if users_collection.find_one({'username': username}):
            response = {'status': 'error', 'message': 'Username already exists.'}
        else:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({'username': username, 'password': hashed_password, 'wins': 0, 'points': 0, 'draws': 0})
            response = {'status': 'success', 'message': 'Registration successful.'}
        client_socket.send((json.dumps(response) + "\n").encode('utf-8'))

   
    def send_user_info(self, client_socket):
        try:
            client_info = client_socket.getpeername()
            username = users_collection.find_one({'socket': client_info})['username']
            user_info = users_collection.find_one({'username': username}, {'_id': 0, 'username': 1, 'wins': 1, 'points': 1, 'draws': 1})
            client_socket.send((json.dumps({'action': 'user_info', 'user_info': user_info}) + "\n").encode('utf-8'))
        except Exception as e:  
            print(f"Error sending user info: {e}")
            
    def send_ranking(self):
        try:
            connected_usernames = list(self.connected_users.keys())
            users = list(users_collection.find({'username': {'$in': connected_usernames}}, {'_id': 0, 'username': 1, 'wins': 1, 'points': 1, 'draws': 1}).sort([('points', -1), ('wins', -1)]))
            ranking = [{'rank': i + 1, 'username': user['username'], 'wins': user['wins'], 'points': user['points'], 'draws': user['draws']} for i, user in enumerate(users)]
            self.broadcast({'action': 'ranking', 'ranking': ranking})
        except Exception as e:
            print(f"Error sending ranking: {e}")

    def handle_move(self, data, player):
        with self.lock:
            if player != self.current_player:
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
                    self.update_winner(winner)
                    self.reset_board()  # Remover o argumento aqui
                else:
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

    def update_winner(self, winner):
        try:
            if winner in ['X', 'O']:
                player_index = 0 if winner == 'X' else 1
                client_socket = self.clients[player_index]
                client_info = client_socket.getpeername()
                username = users_collection.find_one({'socket': client_info})['username']
                users_collection.update_one({'username': username}, {'$inc': {'wins': 1, 'points': 3}})
                print(f"Updated {username}'s points and wins for winning.")
            elif winner == 'Draw':
                for client_socket in self.clients:
                    client_info = client_socket.getpeername()
                    username = users_collection.find_one({'socket': client_info})['username']
                    users_collection.update_one({'username': username}, {'$inc': {'points': 1, 'draws': 1}})
                    print(f"Updated {username}'s points and draws for draw.")
            self.send_ranking()  # Enviar ranking após atualização dos pontos
        except Exception as e:
            print(f"Error updating winner in database: {e}")

    def reset_board(self):
        redis_client.set(self.game_id, json.dumps([['', '', ''], ['', '', ''], ['', '', '']]))
        self.broadcast({'action': 'reset'})

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} has been established.")
            player = 'X' if len(self.clients) == 0 else 'O'
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, player))
            client_thread.start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
