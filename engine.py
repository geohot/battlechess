#!/usr/bin/env python3
import sys
import time
from random import choice
import chess


def evaluate(board):
    if board.is_game_over():
        result = list(map(float, board.result.split("-")))
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


def move_optimality(board, max_depth):
    best_move = None
    best_score = 0
    move_scores = []

    for move in board.legal_moves:
        move_score = None

        test_board = board.copy()
        test_board.push(move)

        for other_player_move in board.legal_moves:
            test_board_2 = test_board.copy()
            test_board_2.push(other_player_move)

            if max_depth > 0:
                move_score = move_optimality(test_board_2, max_depth - 1)[2]
            else:
                move_score = evaluate(test_board)
            if move_score > best_score:
                best_score = move_score
                best_move = move
            move_scores.append(move_score)

        return (best_move, best_score, sum(move_scores) / len(move_scores))


def get_move(board, limit=None):
    return move_optimality(board, 1)[0]


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
