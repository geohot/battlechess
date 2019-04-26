#!/usr/bin/env python3
import sys
import time
import random
import chess
from timeit import default_timer as timer

moveCount = 0
baseAlpha = -1000000
baseBeta = 1000000
playingAs = None # chess.WHITE or chess.BLACK

def get_move(board, limit=None):
  # TODO: Fill this in with an actual chess engine

  try: 
    playingAs = board.turn

    before = timer()
    move = minimaxEngine(board, 1)
    after = timer()
    speed = after - before
    print("Time to generate move:", speed, file=sys.stderr )
    print("playing", move, file=sys.stderr)
    return move

  except:
    print("Caught exception, use backup random move", move, file=sys.stderr)

    return random.choice(list(board.legal_moves))

  return move

def minimax(board, depth, maximizer, alpha, beta):
  if depth == 0:
    return boardValue(board)
  
  if maximizer:
    maxMoveBoardValue = baseAlpha
    for move in board.legal_moves:
      board.push(move)
      maxMoveBoardValue = max(maxMoveBoardValue, minimax(board, depth - 1, False, alpha, beta))
      board.pop()
      if beta <= alpha:
        return maxMoveBoardValue
    return maxMoveBoardValue
  else:
    minMoveBoardValue = baseBeta
    for move in board.legal_moves:
      board.push(move)
      minMoveBoardValue = min(minMoveBoardValue, minimax(board, depth - 1, True, alpha, beta))
      board.pop()
      if beta <= alpha:
        return minMoveBoardValue
    return minMoveBoardValue


def minimaxEngine(board, depth):
  print(baseAlpha, file=sys.stderr)

  bestMoveBoardValue = baseAlpha
  bestMove = None
  availableMoves = board.legal_moves

  for move in availableMoves:
    board.push(move)
    moveBoardValue = minimax(board, depth-1, False, baseAlpha, baseBeta)
    board.pop()
    if moveBoardValue >= bestMoveBoardValue:
      bestMoveBoardValue = moveBoardValue
      bestMove = move

  return bestMove


# Chess boards are 8x8, 64 positions
def boardValue(board):
  value = 0
  color = board.turn
  friendly = color == playingAs
  for i in range(64):
    value = value + pieceValue(board.piece_at(i), friendly)
  return value

def pieceValue(piece, friendly):
  if piece == None:
    return 0
  #Types | 1,2,3,4,5,6 | Pawn, Knight, Bishop, Rook, Queen, King
  t = piece.piece_type

  v = 0
  if t == 1:
    v = 100
  elif t == 2:
    v = 300
  elif t == 3:
    v = 325
  elif t == 4:
    v = 600
  elif t == 5:
    v = 1000
  elif t == 6:
    v = 9999
  else:
    v = 0
  if friendly:
    return v
  else:
    return -1 * v
  

if __name__ == "__main__":
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
      
