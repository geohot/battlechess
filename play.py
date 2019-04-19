#!/usr/bin/env python3
import asyncio
import chess
import chess.engine

# battle two github users
async def battle(user1, user2):
  engine1_path = ["./launch.sh", user1]
  engine2_path = ["./launch.sh", user2]

  transport, engine1 = await chess.engine.popen_uci(engine1_path)
  transport, engine2 = await chess.engine.popen_uci(engine2_path)

  board = chess.Board()
  while not board.is_game_over():
    #print("***** move %d turn %d *****" % (board.fullmove_number, board.turn))
    #print(board)
    if board.turn:
      # white
      result = await engine1.play(board, chess.engine.Limit(time=0.01))
    else:
      # black
      result = await engine2.play(board, chess.engine.Limit(time=0.01))
    board.push(result.move)

  await engine1.quit()
  await engine2.quit()

  print("after %d moves, result of %s vs %s is %s" % (board.fullmove_number, user1, user2, board.result()))
  print(board)

async def main():
  # TODO: Fetch forks of battlechess from github API
  await battle("geohot", "geohot")

if __name__ == "__main__":
  asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
  loop = asyncio.get_event_loop()
  result = loop.run_until_complete(main())

