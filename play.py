#!/usr/bin/env python3
import asyncio
import chess
import chess.engine
import requests
import traceback
from collections import defaultdict

async def play_handler(engine, board):
  try:
    # 100ms max
    result = await asyncio.wait_for(engine.play(board, chess.engine.Limit(time=0.01)), 0.1)
    return result
  except Exception:
    traceback.print_exc()
    return None

# battle two github users
async def battle(user1, user2):
  print("battle %s %s" % (user1, user2))
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
      result = await play_handler(engine1, board)
      if result is None:
        print("%s(white) forfeits" % user1)
        return "0-1"
    else:
      # black
      result = await play_handler(engine2, board)
      if result is None:
        print("%s(black) forfeits" % user2)
        return "1-0"
    board.push(result.move)

  await engine1.quit()
  await engine2.quit()

  print(board)
  return board.result()

async def main():
  forks = ["geohot"]
  r = requests.get("https://api.github.com/repos/geohot/battlechess/forks")
  # filter stupid forks that didn't change anything
  blacklisted_times = ["2019-04-20T00:56:04Z"]
  forks += [arr['full_name'].replace("/battlechess", "") for arr in r.json() if arr['pushed_at'] not in blacklisted_times]
  print("battling", forks)
  score = defaultdict(int)
  # TODO: not n^2 tournament, double elimination?
  for u1 in forks:
    for u2 in forks:
      if u1 != u2:
        result = await battle(u1, u2)
        print("result of %s vs %s is %s" % (u1, u2, result))
        if result == '1-0':
          score[u1] += 2
          score[u2] += 0
        elif result == '0-1':
          score[u1] += 0
          score[u2] += 2
        elif result == '1/2-1/2':
          score[u1] += 1
          score[u2] += 1
  print("final scores:")
  for k,v in sorted(score.items(), key=lambda x: -x[1]):
    print("%30s : %d" % (k,v))

if __name__ == "__main__":
  asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
  loop = asyncio.get_event_loop()
  result = loop.run_until_complete(main())

