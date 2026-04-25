import arc_agi
from arcengine import GameAction, GameState
import numpy as np

arc = arc_agi.Arcade()
env = arc.make("ls20")

# --- Reset: returns the initial observation ---
obs = env.reset()

print(f"Target: complete {obs.win_levels} levels to reach WIN state")
print(f"Available actions: {obs.available_actions}\n")

MAX_STEPS = 50
step = 0

while obs.state == GameState.NOT_FINISHED and step < MAX_STEPS:
    step += 1

    # Inspect the current frame (64x64 grid of color indices 0-12)
    frame = obs.frame[0]                          # numpy array, shape (64, 64), dtype int8
    unique_colors = np.unique(frame)

    print(f"--- Step {step} ---")
    print(f"  state            : {obs.state.value}")
    print(f"  levels_completed : {obs.levels_completed} / {obs.win_levels}")
    print(f"  frame shape      : {frame.shape}")
    print(f"  colors present   : {unique_colors.tolist()}")

    # Check if this observation matches the WIN condition
    # WIN state: obs.state == GameState.WIN  (i.e. levels_completed == win_levels)
    if obs.state == GameState.WIN:
        print("\nSolved! WIN state reached.")
        break

    # ------------------------------------------------------------------
    # Replace this with your agent logic.
    # Here we simply cycle through available actions.
    action_id = obs.available_actions[(step - 1) % len(obs.available_actions)]
    action = GameAction(action_id)
    # ------------------------------------------------------------------

    obs = env.step(action)

# --- Final state ---
print(f"\nFinal state : {obs.state.value}")
print(f"Levels done : {obs.levels_completed} / {obs.win_levels}")
is_solved = obs.state == GameState.WIN
print(f"Solved      : {is_solved}")

scorecard = arc.get_scorecard()
print(f"\nScorecard score : {scorecard['score']}")
