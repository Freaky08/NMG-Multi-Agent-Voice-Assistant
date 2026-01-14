import json
import uuid
from pathlib import Path

BOOKING_PATH = Path(__file__).parent.parent / "data" / "bookings.json"


def booking_agent(state: dict) -> dict:
    """
    Books a test drive ONLY when model, date, and time are present.
 
    """

  
    #Book only when data exists

    if not all([
        state.get("model"),
        state.get("date"),
        state.get("time")
    ]):
        return state

    booking = {
        "booking_id": str(uuid.uuid4()),
        "model": state["model"],
        "date": state["date"],
        "time": state["time"]
    }

    
    # Load existing bookings safely

    bookings = []

    if BOOKING_PATH.exists():
        content = BOOKING_PATH.read_text().strip()
        if content:
            try:
                bookings = json.loads(content)
            except json.JSONDecodeError:
                
                bookings = []

    
    # new booking
    
    bookings.append(booking)

    
    BOOKING_PATH.write_text(
        json.dumps(bookings, indent=2)
    )

    state["booking_details"] = booking
    return state
