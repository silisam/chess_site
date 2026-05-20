import chess

from tables import (
    PAWN_TABLE,
    KNIGHT_TABLE,
    BISHOP_TABLE,
    ROOK_TABLE,
    QUEEN_TABLE,
    KING_TABLE
)

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}


def get_piece_position_value(piece, square):

    row = square // 8
    col = square % 8


    if piece.color == chess.BLACK:
        row = 7 - row

    if piece.piece_type == chess.PAWN:
        return PAWN_TABLE[row][col]

    elif piece.piece_type == chess.KNIGHT:
        return KNIGHT_TABLE[row][col]

    elif piece.piece_type == chess.BISHOP:
        return BISHOP_TABLE[row][col]

    elif piece.piece_type == chess.ROOK:
        return ROOK_TABLE[row][col]

    elif piece.piece_type == chess.QUEEN:
        return QUEEN_TABLE[row][col]

    elif piece.piece_type == chess.KING:
        return KING_TABLE[row][col]

    return 0


def evaluate_board(board):

    if board.is_checkmate():

        if board.turn == chess.WHITE:
            return -99999
        else:
            return 99999

    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.is_seventyfive_moves()
        or board.is_fivefold_repetition()
    ):
        return 0

    score = 0

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece is None:
            continue

        material_value = PIECE_VALUES[piece.piece_type]

        positional_value = get_piece_position_value(
            piece,
            square
        )

        total_value = material_value + positional_value

        if piece.color == chess.WHITE:
            score += total_value
        else:
            score -= total_value

    return score