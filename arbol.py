def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)


def generate_states():
    empty_board = [[" "] * 3 for _ in range(3)]
    states = []

    # Generar todas las combinaciones posibles de movimientos para los primeros dos turnos
    for i in range(3):
        for j in range(3):
            for x in range(3):
                for y in range(3):
                    if i != x or j != y:
                        new_board = [row.copy() for row in empty_board]
                        new_board[i][j] = "X"
                        new_board[x][y] = "O"
                        states.append(new_board)

    return states


def main():
    all_states = generate_states()
    for index, state in enumerate(all_states):
        print(f"Estado {index + 1}:")
        print_board(state)
        print()


if __name__ == "__main__":
    main()
