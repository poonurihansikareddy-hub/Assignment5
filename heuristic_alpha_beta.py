import math

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


def print_board(board):

    print()

    for i in range(3):

        print(" | ".join(board[i*3 : i*3+3]))

        if i < 2:
            print("---------")

    print()


def heuristic(board):

    lines = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    score = 0

    for line in lines:

        vals = [board[i] for i in line]

        x_count = vals.count('X')
        o_count = vals.count('O')

        if o_count == 0:
            score += x_count * 10

        if x_count == 0:
            score -= o_count * 10

    return score


def heuristic_alpha_beta(board, depth, alpha, beta, is_maximizing):

    winner = check_winner(board)

    if winner == 'X':
        return 1000

    if winner == 'O':
        return -1000

    if is_full(board):
        return 0

    if depth == 0:
        return heuristic(board)

    if is_maximizing:

        best = -math.inf

        for i in range(9):

            if board[i] == '.':

                board[i] = 'X'

                score = heuristic_alpha_beta(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )

                board[i] = '.'

                best = max(best, score)

                alpha = max(alpha, best)

                if beta <= alpha:
                    break

        return best

    else:

        best = math.inf

        for i in range(9):

            if board[i] == '.':

                board[i] = 'O'

                score = heuristic_alpha_beta(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )

                board[i] = '.'

                best = min(best, score)

                beta = min(beta, best)

                if beta <= alpha:
                    break

        return best


def best_move_heuristic(board, depth=4):

    best_val = -math.inf
    move = -1

    for i in range(9):

        if board[i] == '.':

            board[i] = 'X'

            val = heuristic_alpha_beta(
                board,
                depth,
                -math.inf,
                math.inf,
                False
            )

            board[i] = '.'

            if val > best_val:
                best_val = val
                move = i

    return move


def test_heuristic():

    print("=" * 40)
    print("TEST 1 – Heuristic on empty board")
    print("=" * 40)

    board = list("." * 9)

    score = heuristic(board)

    print(f"Empty board heuristic score: {score}")

    print("PASS\n")

    print("=" * 40)
    print("TEST 2 – X should take winning move")
    print("=" * 40)

    board = list("XX." "OO." "...")

    print("Board:")

    print_board(board)

    move = best_move_heuristic(board, depth=2)

    board[move] = 'X'

    print(f"X chose position {move}")

    print_board(board)

    assert check_winner(board) == 'X'

    print("PASS\n")

    print("=" * 40)
    print("TEST 3 – X blocks O winning move")
    print("=" * 40)

    board = list("XXO" "OO." "X..")

    print("Board:")

    print_board(board)

    move = best_move_heuristic(board, depth=3)

    board[move] = 'X'

    print(f"X chose position {move}")

    print_board(board)

    assert move == 5

    print("PASS\n")


if __name__ == "__main__":

    test_heuristic()

    print("All Heuristic Alpha-Beta tests passed!")