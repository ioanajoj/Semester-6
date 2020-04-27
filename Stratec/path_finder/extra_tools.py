def distance(v1, v2):
    import numpy as np
    return np.sqrt(np.sum((v1 - v2) ** 2))


def print_pretty_table(board):
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = [' '] + [str(i) for i in range(board.shape[1])]
    for row in range(board.shape[0]):
        x.add_row([row] + [board[row, i] if board[row, i] != 0 else ' ' for i in range(board.shape[1])])
    print(x)
