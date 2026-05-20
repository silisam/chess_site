import chess
from evaluation import evaluate_board


def score_move(board, move):

    score = 0


    if board.is_capture(move):
        score += 1000

        captured_piece = board.piece_at(move.to_square)
        moving_piece = board.piece_at(move.from_square)


        if captured_piece and moving_piece:

            piece_values = {
                chess.PAWN: 100,
                chess.KNIGHT: 300,
                chess.BISHOP: 300,
                chess.ROOK: 500,
                chess.QUEEN: 900,
                chess.KING: 0
            }

            score += (
                piece_values[captured_piece.piece_type]
                - piece_values[moving_piece.piece_type]
            )


    if move.promotion:
        score += 900


    board.push(move)

    if board.is_check():
        score += 500

    board.pop()

    return score


def get_ordered_moves(board):

    moves = list(board.legal_moves)

    moves.sort(
        key=lambda move: score_move(board, move),
        reverse=True
    )

    return moves


def alphabeta(board, depth, alpha, beta, maximizing_player):


    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    ordered_moves = get_ordered_moves(board)


    if maximizing_player:

        max_eval = -999999

        for move in ordered_moves:

            board.push(move)

            evaluation = alphabeta(
                board,
                depth - 1,
                alpha,
                beta,
                False
            )

            board.pop()

            max_eval = max(max_eval, evaluation)

            alpha = max(alpha, evaluation)

  
            if beta <= alpha:
                break

        return max_eval


    else:

        min_eval = 999999

        for move in ordered_moves:

            board.push(move)

            evaluation = alphabeta(
                board,
                depth - 1,
                alpha,
                beta,
                True
            )

            board.pop()

            min_eval = min(min_eval, evaluation)

            beta = min(beta, evaluation)


            if beta <= alpha:
                break

        return min_eval