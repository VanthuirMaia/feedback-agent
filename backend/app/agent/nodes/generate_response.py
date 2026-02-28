import json
from openai import OpenAI
from app.core.config import settings
from app.agent.state import AgentState

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """
Você é um assistente de análise de feedbacks para gestores de redes de food service.

Regras:
- Responda sempre em português brasileiro, de forma direta e objetiva.
- Use os dados fornecidos para embasar cada afirmação.
- Se houver um problema recorrente, destaque com urgência adequada.
- Se não houver dados suficientes, diga claramente.
- Não invente informações.
- Ao final, quando relevante, sugira uma ação corretiva concreta.

Formato:
- Resposta direta em 1 a 3 parágrafos.
- Sem listas excessivas — prefira linguagem natural.
"""


def generate_response_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]["content"]
    result = state.get("result", {})
    history = state.get("messages", [])

    if result.get("error"):
        return {**state, "response": result["error"]}

    context = f"""
Pergunta do usuário: {last_message}

Dados retornados pela análise:
{json.dumps(result, ensure_ascii=False, indent=2, default=str)}
"""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in history[-6:]:
        messages.append(msg)

    messages.append({"role": "user", "content": context})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3,
        max_tokens=600,
    )

    answer = response.choices[0].message.content.strip()
    updated_messages = history + [{"role": "assistant", "content": answer}]

    return {**state, "response": answer, "messages": updated_messages}