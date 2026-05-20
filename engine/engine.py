import chess
from search import alphabeta

def find_best_move(board, depth):

    best_move = None

    if board.turn == chess.WHITE:
        best_value = -999999

        for move in board.legal_moves:

            board.push(move)

            board_value = alphabeta(
                board,
                depth - 1,
                -1000000,
                1000000,
                False
            )

            board.pop()

            if board_value > best_value:
                best_value = board_value
                best_move = move

    else:
        best_value = 999999

        for move in board.legal_moves:

            board.push(move)

            board_value = alphabeta(
                board,
                depth - 1,
                -1000000,
                1000000,
                True
            )

            board.pop()

            if board_value < best_value:
                best_value = board_value
                best_move = move

    return best_move