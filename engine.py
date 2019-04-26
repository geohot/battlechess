#!/usr/bin/env python3
import sys
import time
import random
import chess
import chess.uci
import chess.pgn
import operator
from timeit import default_timer as timer

piece_strength = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900,
}


def evaluate(board):
    score = 0
    color = board.turn
    op = operator.add
    if color != chess.WHITE:
        op = operator.sub
    for piece in piece_strength.keys():
        score = op(score, piece_strength[piece]
                   * len(board.pieces(piece, color)))
    return score


def get_move(board, limit=None):
    start = timer()
    best_move = None
    best_board_value = -sys.maxsize
    for move in board.legal_moves:
        board.push(move)
        board_value = evaluate(board)
        board.pop()
        if board_value > best_board_value:
            best_board_value = board_value
            best_move = move
    print("playing", best_move, file=sys.stderr)
    end = timer()
    print("took", end - start, "seconds", file=sys.stderr)
    return best_move


if __name__ == "__main__":
    print("welcome to the greatest chess engine", file=sys.stderr)
    while 1:
        cmd = input().split(" ")
        #print(cmd, file=sys.stderr)

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
