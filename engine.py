#!/usr/bin/env python3
import sys
import time
import random
import chess


def evaluate(board):
    if board.is_game_over():
        result = list(map(float, board.result().split("-")))
        my_result = result[int(board.turn)]
        return (my_result - 0.5) * 2000  # maps set {0, 1/2, 1} to {-1000, 0, 1000}
    else:
        # Simple piece adding
        score = 0

        score += 1 * len(board.pieces(chess.PAWN, board.turn))
        score += 3 * len(board.pieces(chess.KNIGHT, board.turn))
        score += 3 * len(board.pieces(chess.BISHOP, board.turn))
        score += 5 * len(board.pieces(chess.ROOK, board.turn))
        score += 9 * len(board.pieces(chess.QUEEN, board.turn))

        score -= 1 * len(board.pieces(chess.PAWN, not board.turn))
        score -= 3 * len(board.pieces(chess.KNIGHT, not board.turn))
        score -= 3 * len(board.pieces(chess.BISHOP, not board.turn))
        score -= 5 * len(board.pieces(chess.ROOK, not board.turn))
        score -= 9 * len(board.pieces(chess.QUEEN, not board.turn))

        return score


# Returns tuple of (best_move, best_score, average_score) for all moves on board
def move_optimality(board, max_depth):
    best_move = None
    best_score = -9999
    move_scores = []

    for move in board.legal_moves:
        move_score = 0

        b_my_move = board.copy()
        b_my_move.push(move)

        for their_move in b_my_move.legal_moves:
            b_their_move = b_my_move.copy()
            b_their_move.push(their_move)

            if max_depth > 1 and not b_their_move.is_game_over():
                move_score = move_optimality(b_their_move, max_depth - 1)[2]
            else:
                # negative because it's their board
                move_score -= evaluate(b_their_move)

        move_scores.append(move_score)
        if move_score > best_score:
            best_score = move_score
            best_move = move

    return (best_move, best_score, sum(move_scores) / len(move_scores))


def get_move(board, limit=None):
    (best_move, best_score, _) = move_optimality(board, 2)
    # print(best_score)
    return best_move


if __name__ == "__main__":
    while 1:
        cmd = input().split(" ")
        # print(cmd, file=sys.stderr)

        if cmd[0] == "uci":
            print("uciok")
        elif cmd[0] == "ucinewgame":
            pass
        elif cmd[0] == "isready":
            print("readyok")
        elif cmd[0] == "position":
            if cmd[1] == "startpos":
                board = chess.Board()
                if len(cmd) > 2 and cmd[2] == "moves":
                    for m in cmd[3:]:
                        board.push(chess.Move.from_uci(m))
        elif cmd[0] == "go":
            if len(cmd) > 1 and cmd[1] == "movetime":
                move = get_move(board, limit=int(cmd[2]))
            else:
                move = get_move(board)
            print("bestmove %s" % move)
        elif cmd[0] == "quit":
            exit(0)
