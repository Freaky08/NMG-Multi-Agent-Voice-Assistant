from typing import TypedDict, Optional, List, Dict

class AgentState(TypedDict):
    user_input: Optional[str]

    intent: Optional[str]
    car_type: Optional[str]
    model: Optional[str]
    date: Optional[str]
    time: Optional[str]

    available_models: Optional[List[str]]
    booking_details: Optional[Dict]

    response: Optional[str]
