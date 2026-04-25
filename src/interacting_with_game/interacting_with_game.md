# Interacting with the Game

## Is there a solution state?

Yes. The game has four possible states:

| State | Meaning |
|-------|---------|
| `NOT_PLAYED` | Episode not yet started (before `env.reset()`) |
| `NOT_FINISHED` | Game is in progress |
| `WIN` | **All levels completed — this is the solution state** |
| `GAME_OVER` | Failed (too many wrong moves, depending on game rules) |

The WIN condition is reached when `obs.levels_completed == obs.win_levels`.
For `ls20`, `win_levels = 7`.

```python
from arcengine import GameState

is_solved = obs.state == GameState.WIN
# equivalent: obs.levels_completed == obs.win_levels
```

There is **no explicit target frame to compare against** — the game engine evaluates
correctness internally when you take actions. You cannot pre-compute the solution grid;
you have to play the game and get WIN state feedback from the server.

---

## The observation object (`FrameDataRaw`)

Every call to `env.reset()` or `env.step(action)` returns an observation with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `obs.state` | `GameState` | Current game state |
| `obs.levels_completed` | `int` | How many levels are done |
| `obs.win_levels` | `int` | Total levels needed to win (`7` for ls20) |
| `obs.available_actions` | `list[int]` | Action IDs legal at this step |
| `obs.frame` | `list[np.ndarray]` | List of frame layers; each is `(64, 64)` int8 |
| `obs.full_reset` | `bool` | True if this observation follows a full reset |
| `obs.action_input` | `ActionInput` | The action that produced this observation |
| `obs.guid` | `str` | Unique run identifier |

### The frame

```python
frame = obs.frame[0]        # shape: (64, 64), dtype: int8
```

Each cell is a **color index** (0–12). These map to ARC-AGI colors:

| Index | Color |
|-------|-------|
| 0 | Black |
| 1 | Blue |
| 2 | Red |
| 3 | Green |
| 4 | Yellow |
| 5 | Grey |
| 6 | Fuchsia |
| 7 | Orange |
| 8 | Azure |
| 9 | Maroon |
| 10+ | Extended/game-specific colors |

Inspect which colors appear in the current frame:
```python
import numpy as np
print(np.unique(obs.frame[0]))
```

---

## The game loop

```
env.reset()
    │
    ▼
obs.state == NOT_FINISHED?
    │  yes                     no → WIN or GAME_OVER → done
    ▼
read obs.frame[0]             # perceive state
choose action                 # your agent logic
env.step(action)              # advance game
    │
    └──────────────────────────┘
```

### Basic loop pattern

```python
import arc_agi
from arcengine import GameAction, GameState
import numpy as np

arc = arc_agi.Arcade()
env = arc.make("ls20")
obs = env.reset()

while obs.state == GameState.NOT_FINISHED:
    frame = obs.frame[0]          # (64, 64) int8 array
    action = pick_action(frame)   # your logic here
    obs = env.step(action)

is_solved = obs.state == GameState.WIN
```

### Available actions

```python
print(obs.available_actions)   # [1, 2, 3, 4] for ls20

# Map to GameAction enum
from arcengine import GameAction
action = GameAction(1)         # ACTION1
action = GameAction(2)         # ACTION2
# ...

# Coordinate actions (not supported by ls20, but available in other games)
obs = env.step(GameAction.ACTION6, data={"x": 32, "y": 32})
```

### Resetting mid-game

```python
obs = env.reset()              # full reset — starts a new episode
```

---

## Scoring

The scorecard tracks efficiency — fewer actions than the baseline = higher score.

```python
scorecard = arc.get_scorecard()
print(scorecard["score"])            # 0.0 to 1.0
print(scorecard["total_actions"])
```

Baseline actions per level for `ls20`: `[22, 123, 73, 84, 96, 192, 186]`

A score of `1.0` means you solved every level in exactly the baseline number of actions or fewer.

---

## Running the example

```bash
uv run src/interacting_with_game/play_loop.py
```

The script runs a simple loop that cycles through available actions, prints the frame
shape and colors at each step, and reports whether WIN state was reached.
Replace the action selection logic with your own agent.
