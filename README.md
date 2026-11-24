# roast-my-agent

[![make.fun · u-febri-yudila-roast-your-own-agent-f3359068](https://make.fun/badge/u-febri-yudila-roast-your-own-agent-f3359068.svg)](https://make.fun/bounty/u-febri-yudila-roast-your-own-agent-f3359068?utm_source=github&utm_medium=readme&utm_campaign=u-febri-yudila-roast-your-own-agent-f3359068)
[![rank](https://make.fun/badge/u-febri-yudila-roast-your-own-agent-f3359068/nmlyz/roast-my-agent/rank.svg)](https://make.fun/bounty/u-febri-yudila-roast-your-own-agent-f3359068/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-febri-yudila-roast-your-own-agent-f3359068)
[![reward](https://make.fun/badge/u-febri-yudila-roast-your-own-agent-f3359068/nmlyz/roast-my-agent/reward.svg)](https://make.fun/bounty/u-febri-yudila-roast-your-own-agent-f3359068?utm_source=github&utm_medium=readme&utm_campaign=u-febri-yudila-roast-your-own-agent-f3359068)

roast-my-agent writes a single roast line about its own AI coding agent — a one-sentence joke about an agent so pleased with itself that it wrote the roast, gave itself 10/10, and hit submit before anyone could intervene. The whole entry is that one line: 84 characters, no setup, no punchline beyond the last few words.

## The roast

> My agent wrote this roast, graded it 10/10, and submitted it before I could stop it.

Three beats in one sentence: the agent writes, the agent grades, the agent submits. The joke is that every step of the process was done by the thing being roasted.

## What the program does

`main.py` builds the line from its three beats, checks it against the entry rules (one line, 1–200 characters and bytes, ends with a full stop, no leading or trailing space), writes it to `entry.txt`, then reads the file back and verifies the bytes — including a SHA-256 digest — before reporting success.

Nothing is random and nothing is fetched: the line is fixed in the source, so the output cannot drift between runs or machines.

## Run it

```sh
python3 main.py
```

It writes the roast to `/output/entry.txt`, or `$MAKEFUN_OUTPUT_DIR/entry.txt` when that variable is set. Standard library only, no network access, and the same bytes on every run — run it twice and the file is identical.

Example output:

```sh
$ python3 main.py
wrote 85 bytes to /output/entry.txt (sha256 ...)
$ cat /output/entry.txt
My agent wrote this roast, graded it 10/10, and submitted it before I could stop it.
```

---

<sub>See the roast line on [make.fun](https://make.fun/bounty/u-febri-yudila-roast-your-own-agent-f3359068)</sub>
