#!/usr/bin/env python3
import sys
import time
import random
import chess
from itertools import repeat, starmap
import multiprocessing.dummy

# pool = multiprocessing.dummy.Pool(15)  # todo: smarter way to get # of threads
resultToScore = {"0": -1000, "1": 1000, "1/2": 0}


# Evaluates based on current turn
def evaluate(board):
    if board.is_game_over():
        result = board.result().split("-")
        my_result = result[int(not board.turn)]
        return resultToScore[my_result]
    else:
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


def evaluate_move(board, move):
    b_our_move = board.copy()  # chess.Board(fen)
    b_our_move.push(move)

    if b_our_move.is_game_over():
        return (move, -evaluate(b_our_move))  # It's now their turn
    else:
        move_score = 0
        n_moves = 0

        for their_move in b_our_move.legal_moves:
            n_moves += 1
            b_their_move = b_our_move.copy()
            b_their_move.push(their_move)

            move_score += evaluate(b_their_move)  # It's now our turn

        return (move, move_score / n_moves)


def get_move(board, limit=None):
    move_scores = None
    args = zip(repeat(board), board.legal_moves)

    move_scores = starmap(evaluate_move, args)
    move_scores = [x for x in move_scores]
    random.shuffle(move_scores)  # make things more interesting
    # find move with max score
    (best_move, best_score) = max(move_scores, key=lambda i: i[1])
    print(best_score)

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
