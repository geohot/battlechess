#!/usr/bin/env python3
import sys
import time
import random
import chess
from itertools import repeat, starmap
from multiprocessing import Pool


resultToScore = {"0": -1000, "1": 1000, "1/2": 0}


def evaluate(board):
    if board.is_game_over():
        result = list(map(float, board.result().split("-")))
        my_result = result[int(board.turn)]
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


def evaluate_move(fen, move, max_depth):
    move_score = 0
    n_moves = 0

    b_our_move = chess.Board(fen)
    b_our_move.push(move)

    if b_our_move.is_game_over():
        move_score -= evaluate(b_our_move)  # It's now their turn
        return (move, move_score)
    else:
        for their_move in b_our_move.legal_moves:
            n_moves += 1
            b_their_move = b_our_move.copy()
            b_their_move.push(their_move)

            move_score += evaluate(b_their_move)  # It's now our turn
            # if max_depth > 1 and not b_their_move.is_game_over():
            #     move_score += move_optimality(b_their_move, max_depth - 1, False)[2]
            # else:
            #     # negative because it's their board
            #     move_score -= evaluate(b_their_move)

    return (move, move_score / n_moves)


# Returns tuple of (best_move, best_score, average_score) for all moves on board
def move_optimality(board, max_depth, use_multiprocess):
    move_scores = None
    fen = board.fen()
    args = zip(repeat(fen), board.legal_moves, repeat(max_depth))

    # if use_multiprocess:
    #     with Pool(10) as p:  # todo: use number of cpu cores
    #         move_scores = p.starmap(evaluate_move, args)
    # else:
        move_scores = starmap(evaluate_move, args)

    move_scores = [x for x in move_scores]
    random.shuffle(move_scores)  # make things more interesting
    # find move with max score
    (best_move, best_score) = max(move_scores, key=lambda i: i[1])

    return (
        best_move,
        best_score,
        sum(map(lambda i: i[1], move_scores)) / len(move_scores),
    )


def get_move(board, limit=None):
    (best_move, best_score, _) = move_optimality(board, 2, True)
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
