import math

SAMPLE_TREE = (
    None, [
        (None, [
            (None, [(3, []), (5, [])]),
            (None, [(2, []), (9, [])])
        ]),
        (None, [
            (None, [(1, []), (7, [])]),
            (None, [(4, []), (6, [])])
        ])
    ]
)


def minimax(node, depth, is_maximizing):

    value, children = node

    if not children or depth == 0:
        return value

    if is_maximizing:

        best = -math.inf

        for child in children:

            score = minimax(child, depth - 1, False)

            best = max(best, score)

        return best

    else:

        best = math.inf

        for child in children:

            score = minimax(child, depth - 1, True)

            best = min(best, score)

        return best


def print_board(board):

    print()

    for i in range(3):

        print(" | ".join(board[i*3 : i*3+3]))

        if i < 2:
            print("---------")

    print()


def check_winner(board):

    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for combo in wins:

        vals = [board[i] for i in combo]

        if vals == ['X','X','X']:
            return 'X'

        if vals == ['O','O','O']:
            return 'O'

    return None


def is_full(board):

    return '.' not in board


def ttt_minimax(board, is_maximizing):

    winner = check_winner(board)

    if winner == 'X':
        return 1

    if winner == 'O':
        return -1

    if is_full(board):
        return 0

    if is_maximizing:

        best = -math.inf

        for i in range(9):

            if board[i] == '.':

                board[i] = 'X'

                score = ttt_minimax(board, False)

                board[i] = '.'

                best = max(best, score)

        return best

    else:

        best = math.inf

        for i in range(9):

            if board[i] == '.':

                board[i] = 'O'

                score = ttt_minimax(board, True)

                board[i] = '.'

                best = min(best, score)

        return best


def best_move(board):

    best_val = -math.inf

    move = -1

    for i in range(9):

        if board[i] == '.':

            board[i] = 'X'

            val = ttt_minimax(board, False)

            board[i] = '.'

            if val > best_val:

                best_val = val

                move = i

    return move


def test_minimax():

    print("=" * 40)
    print("TEST 1 – Generic game tree")
    print("=" * 40)

    result = minimax(
        SAMPLE_TREE,
        depth=3,
        is_maximizing=True
    )

    print(f"Minimax value of root: {result}")

    assert result == 6

    print("PASS\n")

    print("=" * 40)
    print("TEST 2 – Tic-Tac-Toe block move")
    print("=" * 40)

    board = list("XXO" "OO." "X..")

    print("Board before X moves:")

    print_board(board)

    move = best_move(board)

    board[move] = 'X'

    print(f"X chose position {move}")

    print_board(board)

    assert move == 5

    print("PASS\n")

    print("=" * 40)
    print("TEST 3 – Winning move")
    print("=" * 40)

    board = list("XX." "OO." "...")

    print("Board before X moves:")

    print_board(board)

    move = best_move(board)

    board[move] = 'X'

    print(f"X chose position {move}")

    print_board(board)

    assert check_winner(board) == 'X'

    print("PASS\n")


if __name__ == "__main__":

    test_minimax()

    print("All Minimax tests passed!")