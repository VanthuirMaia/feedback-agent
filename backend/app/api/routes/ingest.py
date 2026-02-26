from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import pandas as pd
import io

router = APIRouter()

REQUIRED_COLUMNS = {"texto_avaliacao", "nota", "data", "loja_id"}

class IngestResponse(BaseModel):
    success: bool
    total: int
    lojas: list[str]
    periodo: dict
    message: str

@router.post("/csv", response_model=IngestResponse)
async def ingest_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser um CSV.")

    content = await file.read()
    try:
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao ler o CSV.")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Colunas obrigatórias ausentes: {', '.join(missing)}"
        )

    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["texto_avaliacao", "nota", "data", "loja_id"])
    df = df.drop_duplicates()

    lojas = sorted(df["loja_id"].unique().tolist())
    periodo = {
        "inicio": str(df["data"].min().date()),
        "fim": str(df["data"].max().date()),
    }

    return IngestResponse(
        success=True,
        total=len(df),
        lojas=lojas,
        periodo=periodo,
        message=f"{len(df)} avaliações carregadas. Lojas: {', '.join(lojas)}."
    )