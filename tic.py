def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    # Verificar linhas
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Verificar colunas
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Verificar diagonais
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        row = int(input(f"Jogador {current_player}, escolha a linha (0, 1, 2): "))
        col = int(input(f"Jogador {current_player}, escolha a coluna (0, 1, 2): "))

        if board[row][col] != " ":
            print("Essa posição já está ocupada. Escolha outra.")
            continue

        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Parabéns! Jogador {current_player} venceu!")
            break

        if all(all(cell != " " for cell in row) for row in board):
            print_board(board)
            print("Empate!")
            break

        current_player = "O" if current_player == "X" else "X"

tic_tac_toe()
