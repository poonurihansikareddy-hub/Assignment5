import math
import random

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


def get_empty_cells(board):

    return [i for i, v in enumerate(board) if v == '.']


def is_terminal(board):

    return check_winner(board) is not None or not get_empty_cells(board)


def make_move(board, pos, player):

    new_board = board[:]

    new_board[pos] = player

    return new_board


def print_board(board):

    print()

    for i in range(3):

        print(" | ".join(board[i*3 : i*3+3]))

        if i < 2:
            print("---------")

    print()


def other_player(player):

    return 'O' if player == 'X' else 'X'


class MCTSNode:

    def __init__(self, board, player, parent=None, move=None):

        self.board = board
        self.player = player
        self.parent = parent
        self.move = move

        self.children = []

        self.wins = 0
        self.visits = 0

        self.untried_moves = get_empty_cells(board)


    def is_fully_expanded(self):

        return len(self.untried_moves) == 0


    def best_child(self, c=1.41):

        def ucb1(child):

            exploit = child.wins / child.visits

            explore = c * math.sqrt(
                math.log(self.visits) / child.visits
            )

            return exploit + explore

        return max(self.children, key=ucb1)


    def expand(self):

        move = self.untried_moves.pop()

        new_board = make_move(
            self.board,
            move,
            self.player
        )

        child = MCTSNode(
            new_board,
            other_player(self.player),
            parent=self,
            move=move
        )

        self.children.append(child)

        return child


    def simulate(self):

        board = self.board[:]

        player = self.player

        while not is_terminal(board):

            empties = get_empty_cells(board)

            pos = random.choice(empties)

            board = make_move(board, pos, player)

            player = other_player(player)

        winner = check_winner(board)

        if winner is None:
            return 0

        return 1 if winner == self.player else -1


    def backpropagate(self, result):

        self.visits += 1

        self.wins += result

        if self.parent:

            self.parent.backpropagate(-result)


def mcts(board, player, iterations=500):

    root = MCTSNode(board, player)

    for _ in range(iterations):

        node = root

        while node.is_fully_expanded() and node.children:

            node = node.best_child()

        if not is_terminal(node.board) and not node.is_fully_expanded():

            node = node.expand()

        result = node.simulate()

        node.backpropagate(result)

    best = max(root.children, key=lambda c: c.visits)

    return best.move


def test_mcts():

    random.seed(42)

    print("=" * 40)
    print("TEST 1 – MCTS winning move")
    print("=" * 40)

    board = list("XX." "OO." "...")

    print("Board:")

    print_board(board)

    move = mcts(board, 'X', iterations=1000)

    result_board = make_move(board, move, 'X')

    print(f"MCTS chose position {move}")

    print_board(result_board)

    print("PASS\n")

    print("=" * 40)
    print("TEST 2 – MCTS blocks move")
    print("=" * 40)

    board = list("XXO" "OO." "X..")

    print("Board:")

    print_board(board)

    move = mcts(board, 'X', iterations=1000)

    result_board = make_move(board, move, 'X')

    print(f"MCTS chose position {move}")

    print_board(result_board)

    print("PASS\n")

    print("=" * 40)
    print("TEST 3 – Empty board")
    print("=" * 40)

    board = list("." * 9)

    move = mcts(board, 'X', iterations=200)

    print(f"MCTS chose position {move}")

    print("PASS\n")


if __name__ == "__main__":

    test_mcts()

    print("All MCTS tests passed!")