from fastapi import APIRouter, HTTPException
from app.core.store import store

router = APIRouter()

@router.get("/summary")
async def dashboard_summary():
    df = store.get()

    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="Nenhum dado carregado.")

    # métricas gerais
    media_geral = round(df["nota"].mean(), 2)
    total = len(df)

    # média por loja
    por_loja = (
        df.groupby("loja_id")
        .agg(total=("nota", "count"), media=("nota", "mean"))
        .reset_index()
        .sort_values("media", ascending=False)
    )
    por_loja["media"] = por_loja["media"].round(2)

    melhor = por_loja.iloc[0]
    pior = por_loja.iloc[-1]

    # evolução mensal
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    evolucao = (
        df.groupby("mes")
        .agg(total=("nota", "count"), media=("nota", "mean"))
        .reset_index()
        .sort_values("mes")
    )
    evolucao["media"] = evolucao["media"].round(2)

    return {
        "total": total,
        "media_geral": media_geral,
        "melhor_loja": {"nome": melhor["loja_id"], "media": melhor["media"]},
        "pior_loja": {"nome": pior["loja_id"], "media": pior["media"]},
        "por_loja": por_loja.to_dict(orient="records"),
        "evolucao": evolucao.to_dict(orient="records"),
    }