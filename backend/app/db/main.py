from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ingest, chat, health

app = FastAPI(
    title="Feedback Agent API",
    description="Agente conversacional de análise de feedbacks para redes de food service.",
    version="0.1.0",
)

# CORS — permite o frontend Lovable consumir a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringir em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(health.router, tags=["health"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.on_event("startup")
async def startup():
    print("🚀 Feedback Agent API iniciada!")