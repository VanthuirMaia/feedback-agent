from openai import OpenAI
from app.core.config import settings
from app.agent.state import AgentState

client = OpenAI(api_key=settings.openai_api_key)

PROMPT = """
Você é um classificador de intenção para um sistema de análise de feedbacks de restaurantes.

Classifique a pergunta do usuário em uma das categorias abaixo:
- ranking: quer saber qual loja/categoria está melhor ou pior
- comparison: quer comparar dois períodos, lojas ou categorias
- trend: quer saber a evolução ao longo do tempo
- detail: quer ver exemplos ou detalhes específicos de feedbacks
- unknown: não foi possível identificar a intenção

Retorne APENAS a categoria, sem texto adicional.

Pergunta: {message}
"""


def classify_intent_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]["content"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": PROMPT.format(message=last_message)}
        ],
        temperature=0,
        max_tokens=20,
    )

    intent = response.choices[0].message.content.strip().lower()
    valid_intents = {"ranking", "comparison", "trend", "detail", "unknown"}
    if intent not in valid_intents:
        intent = "unknown"

    return {**state, "query_intent": intent}