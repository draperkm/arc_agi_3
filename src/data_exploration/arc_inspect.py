import arc_agi
from arcengine import GameAction, GameState

arc = arc_agi.Arcade()                         # the client
env = arc.make("ls20", render_mode="terminal") # ls20 is one of the public games

# --- Inspect static info about the environment ---
info = env.info
print(info.game_id, info.title, info.tags)

# --- Inspect what actions are currently legal ---
print([a.name for a in env.action_space])

# --- Reset and inspect the initial frame ---
obs = env.reset()
print("state:", obs.state)                 # e.g. NOT_PLAYED, NOT_FINISHED, WIN, GAME_OVER
print("levels_completed:", obs.levels_completed)

# --- Take a step with a simple action ---
obs = env.step(GameAction.ACTION1)

# --- Take a step with a coordinate action ---
obs = env.step(GameAction.ACTION6, data={"x": 32, "y": 32})

# --- Scorecard aggregates results across environments ---
print(arc.get_scorecard())