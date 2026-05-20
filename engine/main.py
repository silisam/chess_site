import sys
import chess

from engine import find_best_move

fen = sys.argv[1]

board = chess.Board(fen)

best_move = find_best_move(board, depth=4)

print(best_move)