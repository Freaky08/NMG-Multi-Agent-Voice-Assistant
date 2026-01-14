import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "cars.json"

def knowledge_agent(state):
    # user already selected a model
    if state.get("model"):
        return state

    # list models 
    if not state.get("car_type"):
        return state

    with open(DATA_PATH) as f:
        cars = json.load(f)

    state["available_models"] = [
        c["model"] for c in cars.get(state["car_type"], [])
    ]

    return state
