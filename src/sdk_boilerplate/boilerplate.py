import random
import arc_agi
from arcengine import GameState

arc = arc_agi.Arcade()
env = arc.make("ls20")   # no render_mode -> fast

obs = env.reset()
for step in range(500):
    action = random.choice(env.action_space)
    data = {}
    if action.is_complex():                       # ACTION6
        data = {"x": random.randint(0, 63),
                "y": random.randint(0, 63)}
    obs = env.step(action, data=data)

    if obs.state == GameState.WIN:
        print(f"won at step {step}"); break
    if obs.state == GameState.GAME_OVER:
        env.reset()
        

print(arc.get_scorecard())