def print_pretty_table(board, paths):
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = [' '] + [i for i in range(board.shape[1])]
    for row in range(board.shape[0]):
        x.add_row([row] + [board[row, i] if board[row, i] != 0 else ' ' for i in range(board.shape[1])])
    print(x)