from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, START, END
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import get_distance, send_notification

class State(TypedDict):
    ticket_id: str
    user_id: str
    inputs: dict
    price_attempts: int
    distance: Optional[float]
    base_price: Optional[float]
    urgency_multiplier: Optional[float]
    surcharge: Optional[float]
    location_modifier: Optional[float]
    total_price: Optional[float]
    action_log: List[str]

def user_input_node(state: State) -> State:
    # Already initialized
    state["action_log"].append("User input received")
    return state

def distance_calc_node(state: State) -> State:
    try:
        origin = state["inputs"].get("origin", "New York, NY")
        destination = state["inputs"].get("destination", "Los Angeles, CA")
        distance = get_distance(origin, destination)
        state["distance"] = distance
        state["action_log"].append(f"Distance calculated: {distance} km")
    except Exception as e:
        state["action_log"].append(f"Distance calculation failed: {str(e)}")
        # Trigger escalation
        raise e
    return state

def material_price_node(state: State) -> State:
    material = state["inputs"]["material_type"]
    prices = {"standard": 10, "fragile": 20, "perishable": 15}
    state["base_price"] = prices.get(material, 10)
    state["action_log"].append(f"Material price applied: {state['base_price']}")
    return state

def urgency_node(state: State) -> State:
    urgency = state["inputs"]["urgency"]
    multipliers = {"standard": 1.0, "express": 1.5, "same-day": 2.0}
    # Default to 1.0 if urgency not recognized
    state["urgency_multiplier"] = multipliers.get(urgency, 1.0)
    state["action_log"].append(f"Urgency multiplier applied: {state['urgency_multiplier']}")
    return state

def weight_volume_node(state: State) -> State:
    weight = state["inputs"].get("weight", 0)
    surcharge = 5 if weight > 10 else 0
    state["surcharge"] = surcharge
    state["action_log"].append(f"Weight surcharge applied: {surcharge}")
    return state

def location_node(state: State) -> State:
    location = state["inputs"].get("location_type", "urban")
    modifier = 1.1 if location == "rural" else 1.0
    state["location_modifier"] = modifier
    state["action_log"].append(f"Location modifier applied: {modifier}")
    return state

def final_price_node(state: State) -> State:
    base = state["base_price"]
    urgency = state["urgency_multiplier"]
    surcharge = state["surcharge"]
    location = state["location_modifier"]
    total = (base * urgency + surcharge) * location
    state["total_price"] = total
    state["action_log"].append(f"Total price calculated: {total}")
    return state

def notification_node(state: State) -> State:
    # Assume phone from user, placeholder
    phone = "+1234567890"
    message = f"Your total delivery price is {state['total_price']}"
    send_notification(phone, message)
    state["action_log"].append("Notification sent")
    return state

def escalation_node(state: State) -> State:
    state["action_log"].append("Escalation triggered")
    # Log to DB or something
    return state

graph = StateGraph(State)
graph.add_node("user_input", user_input_node)
graph.add_node("distance_calc", distance_calc_node)
graph.add_node("material_price", material_price_node)
graph.add_node("urgency", urgency_node)
graph.add_node("weight_volume", weight_volume_node)
graph.add_node("location", location_node)
graph.add_node("final_price", final_price_node)
graph.add_node("notification", notification_node)
graph.add_node("escalation", escalation_node)

graph.add_edge(START, "user_input")
graph.add_edge("user_input", "distance_calc")
graph.add_edge("distance_calc", "material_price")
graph.add_edge("material_price", "urgency")
graph.add_edge("urgency", "weight_volume")
graph.add_edge("weight_volume", "location")
graph.add_edge("location", "final_price")
graph.add_edge("final_price", "notification")
graph.add_edge("notification", END)

# For escalation, add conditional
def route_after_distance(state):
    if any("failed" in log for log in state["action_log"]):
        return "escalation"
    return "material_price"

graph.add_conditional_edges("distance_calc", route_after_distance)

compiled_graph = graph.compile()
