import pandas as pd
from app.agent.state import AgentState


def run_analysis_node(state: AgentState) -> AgentState:
    df = state.get("feedbacks_df")
    filters = state.get("filters", {})
    intent = state.get("query_intent", "unknown")

    if df is None or (hasattr(df, 'empty') and df.empty):
        return {**state, "result": {"error": "Nenhum dado carregado. Faça upload de um CSV primeiro."}}

    filtered = df.copy()

    if filters.get("loja_id"):
        filtered = filtered[filtered["loja_id"].str.lower() == filters["loja_id"].lower()]

    if filters.get("periodo_inicio"):
        filtered = filtered[filtered["data"] >= pd.to_datetime(filters["periodo_inicio"])]

    if filters.get("periodo_fim"):
        filtered = filtered[filtered["data"] <= pd.to_datetime(filters["periodo_fim"])]

    if filters.get("categoria") and "categoria" in filtered.columns:
        filtered = filtered[filtered["categoria"] == filters["categoria"]]

    if filtered.empty:
        return {**state, "result": {"error": "Nenhum feedback encontrado com os filtros aplicados."}}

    result = {}

    if intent == "ranking":
        ranking = (
            filtered.groupby("loja_id")
            .agg(total=("nota", "count"), media=("nota", "mean"))
            .sort_values("total", ascending=False)
            .reset_index()
            .to_dict(orient="records")
        )
        result = {"type": "ranking", "data": ranking, "total": len(filtered)}

    elif intent == "comparison":
        by_loja = (
            filtered.groupby("loja_id")
            .agg(total=("nota", "count"), media=("nota", "mean"))
            .reset_index()
            .to_dict(orient="records")
        )
        result = {"type": "comparison", "data": by_loja, "total": len(filtered)}

    elif intent == "trend":
        filtered["mes"] = filtered["data"].dt.to_period("M").astype(str)
        trend = (
            filtered.groupby("mes")
            .agg(total=("nota", "count"), media=("nota", "mean"))
            .reset_index()
            .to_dict(orient="records")
        )
        result = {"type": "trend", "data": trend, "total": len(filtered)}

    elif intent == "detail":
        samples = filtered.nsmallest(5, "nota")[["loja_id", "data", "nota", "texto_avaliacao"]].to_dict(orient="records")
        result = {"type": "detail", "data": samples, "total": len(filtered)}

    else:
        result = {"type": "summary", "total": len(filtered), "media_geral": round(filtered["nota"].mean(), 2)}

    return {**state, "result": result}