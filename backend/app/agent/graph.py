from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.agent.nodes.classify_intent import classify_intent_node
from app.agent.nodes.extract_filters import extract_filters_node
from app.agent.nodes.run_analysis import run_analysis_node
from app.agent.nodes.generate_response import generate_response_node


def route_by_intent(state: AgentState) -> str:
    """Decide o próximo nó baseado no intent classificado."""
    intent = state.get("query_intent", "unknown")
    if intent == "unknown":
        return "generate_response"  # pede clarificação
    return "extract_filters"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Nós
    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("extract_filters", extract_filters_node)
    graph.add_node("run_analysis", run_analysis_node)
    graph.add_node("generate_response", generate_response_node)

    # Fluxo
    graph.set_entry_point("classify_intent")
    graph.add_conditional_edges("classify_intent", route_by_intent)
    graph.add_edge("extract_filters", "run_analysis")
    graph.add_edge("run_analysis", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


# Instância global do agente
agent = build_graph()