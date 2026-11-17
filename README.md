# makefun-tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/silver-byte/makefun-tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/silver-byte/makefun-tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in under 4 KB of Python: negamax alpha-beta search on a fixed node budget, with quiescence, a transposition table, MVV-LVA / killer / history move ordering and piece-square-table evaluation — built to outscore the sunfish 4 KB baseline on the tiny-chess-01 gauntlet.

## Run it

```sh
node cli/makefun.mjs grade-local --kit . --bot <this repository> --driver docker
```

Run from inside the unpacked tiny-chess-01 dev kit: it plays a practice trial against the house engines, replays it, and prints the Elo the scorer gives it.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
