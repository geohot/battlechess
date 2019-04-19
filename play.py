#!/usr/bin/env python3
import asyncio
import chess
import chess.engine

async def main():
  engine1_path = "stockfish"
  engine2_path = "./engine.py"

  transport, engine1 = await chess.engine.popen_uci(engine1_path)
  transport, engine2 = await chess.engine.popen_uci(engine2_path)

  board = chess.Board()
  while not board.is_game_over():
    print("***** move %d turn %d *****" % (board.fullmove_number, board.turn))
    print(board)
    if board.turn:
      # white
      result = await engine1.play(board, chess.engine.Limit(time=0.01))
    else:
      # black
      result = await engine2.play(board, chess.engine.Limit(time=0.01))
    board.push(result.move)

  print("after %d moves, result is %s" % (board.fullmove_number, board.result()))
  print(board)
  await engine1.quit()
  await engine2.quit()

if __name__ == "__main__":
  asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
  loop = asyncio.get_event_loop()
  result = loop.run_until_complete(main())

