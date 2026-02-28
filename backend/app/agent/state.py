from typing import TypedDict, Any


class AgentState(TypedDict):
    """Estado compartilhado entre todos os nós do grafo LangGraph."""

    # Conversa
    messages: list[dict]
    session_id: str

    # Dados carregados
    feedbacks_df: Any

    # Análise
    query_intent: str
    filters: dict
    sql_query: str

    # Resultado
    result: dict
    response: str