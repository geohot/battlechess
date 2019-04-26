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


def check_pawn_needs_to_be_kicked(board, move):
    # sorry python-chess for messing with you
    if chess.Piece.symbol(board.piece_at(move.from_square)) == 'p':
        print("found a pawn", move, file=sys.stderr)
        if board.turn == chess.WHITE:
            print("white pawn at", move.uci()[1])
            if move.uci()[1] == '2':
                print("white pawn needs to be kicked", move, file=sys.stderr)
                return True
        else:
            print("black pawn at", move.uci()[1])
            if move.uci()[1] == '7':
                print("black pawn needs to be kicked", move, file=sys.stderr)
                return True

    return False


def get_move(board, limit=None):
    start = timer()
    best_move = None
    best_board_value = -sys.maxsize
    for move in board.legal_moves:
        if check_pawn_needs_to_be_kicked(board, move):
            return move
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
