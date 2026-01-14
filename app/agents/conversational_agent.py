
import json
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

PROMPT_DIR = Path(__file__).parent.parent / "prompts"

llm = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.3)

def load_prompt(name):
    return (PROMPT_DIR / name).read_text()

def conversational_agent(state):
    if state.get("user_input") is None:
        # Greeting only
        prompt = ChatPromptTemplate.from_messages([
            ("system", load_prompt("greeting_prompt.txt")),
            ("human", "Greet the customer")
        ])
        state["response"] = llm.invoke(prompt.format_messages()).content
        return state

    # Extract intent 
    prompt = ChatPromptTemplate.from_messages([
        ("system", load_prompt("intent_extraction_prompt.txt")),
        ("human", state["user_input"])
    ])

    extracted = json.loads(llm.invoke(prompt.format_messages()).content)

    # Update 
    for key, value in extracted.items():
        if value:
            state[key] = value
    if state.get("model"):
        state["available_models"] = None

    return state



def generate_speech(state):
   

    prompt = ChatPromptTemplate.from_messages([
        ("system", load_prompt("nlg_prompt.txt")),
        ("human", "{context}")
    ])

    # Case 1: Models need to be listed
    if (
    state.get("available_models")
    and not state.get("model")
    and not state.get("booking_details")
):
        context = {
        "available_models": state["available_models"]
    }

    # Case 2: Booking completed
    elif state.get("booking_details"):
        context = state["booking_details"]

    else:
        return state

    state["response"] = llm.invoke(
        prompt.format_messages(context=str(context))
    ).content

    return state

