import json
from datetime import date
from openai import OpenAI
from app.core.config import settings
from app.agent.state import AgentState

client = OpenAI(api_key=settings.openai_api_key)

PROMPT = """
Extraia os filtros da pergunta abaixo para consulta em banco de dados de feedbacks de restaurantes.

Retorne APENAS um JSON válido com os campos:
{{
  "loja_id": "nome da loja ou null se não mencionado",
  "periodo_inicio": "YYYY-MM-DD ou null",
  "periodo_fim": "YYYY-MM-DD ou null",
  "categoria": "atendimento | tempo_de_espera | qualidade_produto | entrega | limpeza | preco_valor | pedido_incorreto | app_sistema | null"
}}

Hoje é {today}. Interprete expressões como "essa semana", "mês passado", "ontem" corretamente.

Pergunta: {message}
"""


def extract_filters_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]["content"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": PROMPT.format(
                message=last_message,
                today=date.today().isoformat()
            )}
        ],
        temperature=0,
        max_tokens=200,
    )

    try:
        filters = json.loads(response.choices[0].message.content.strip())
    except json.JSONDecodeError:
        filters = {"loja_id": None, "periodo_inicio": None, "periodo_fim": None, "categoria": None}

    return {**state, "filters": filters}