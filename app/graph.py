from langgraph.graph import StateGraph
from app.state import AgentState
from app.agents.conversational_agent import conversational_agent
from app.agents.knowledge_agent import knowledge_agent
from app.agents.booking_agent import booking_agent

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("conversation", conversational_agent)
    graph.add_node("knowledge", knowledge_agent)
    graph.add_node("booking", booking_agent)

    graph.set_entry_point("conversation")
    graph.add_edge("conversation", "knowledge")
    graph.add_edge("knowledge", "booking")

    graph.set_finish_point("booking")
    return graph.compile()
