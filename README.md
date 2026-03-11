# 🍔 Feedback Agent

Agente conversacional com IA para análise de feedbacks de redes de food service.

> Projeto desenvolvido em modo **Build in Public** — cada fase documentada e publicada no LinkedIn.

---

## 🎯 O que é

Gestores de redes de restaurantes recebem centenas de avaliações por mês no Google, iFood e Rappi — tudo disperso, manual e reativo.

O **Feedback Agent** resolve isso: você pergunta em português, ele responde com dados reais dos seus clientes.

```
"Qual loja teve mais reclamação sobre tempo de entrega essa semana?"
"O atendimento melhorou em relação ao mês passado?"
"Qual categoria de problema é mais recorrente na unidade do centro?"
```

---

## 🏗️ Arquitetura

```
React + Vite (Frontend)
      ↓
FastAPI (Backend REST)
      ↓
LangGraph (Agente IA)
      ↓
OpenAI API (GPT-4o / gpt-4o-mini)
      ↓
SQLite + ChromaDB (Dados)
```

---

## 🗂️ Estrutura do Projeto

```
feedback-agent/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/         # Endpoints FastAPI
│   │   │       ├── health.py
│   │   │       ├── ingest.py   # Upload de CSV
│   │   │       ├── chat.py     # Chat com o agente
│   │   │       └── dashboard.py # Métricas e gráficos
│   │   ├── agent/
│   │   │   ├── graph.py        # Grafo LangGraph
│   │   │   ├── state.py        # Estado do agente
│   │   │   └── nodes/          # Nós do agente
│   │   │       ├── classify_intent.py
│   │   │       ├── extract_filters.py
│   │   │       ├── run_analysis.py
│   │   │       └── generate_response.py
│   │   ├── core/
│   │   │   ├── config.py       # Configurações e variáveis de ambiente
│   │   │   └── store.py        # Store em memória para os dados carregados
│   │   └── main.py             # Entry point FastAPI
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx   # Métricas e gráficos reais
│   │   │   ├── UploadCSV.tsx   # Upload conectado na API
│   │   │   └── Chat.tsx        # Chat conectado no agente
│   │   └── components/
│   ├── package.json
│   └── Dockerfile
├── data/                       # Dados locais (não versionados)
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Stack Técnica

| Camada          | Tecnologia                     |
| --------------- | ------------------------------ |
| Frontend        | React + Vite + Tailwind CSS    |
| Backend         | FastAPI + Python 3.11+         |
| Agente IA       | LangGraph                      |
| LLM             | OpenAI GPT-4o / gpt-4o-mini    |
| Busca semântica | ChromaDB                       |
| Banco de dados  | SQLite                         |
| Deploy          | Docker Compose (VPS Hostinger) |

---

## 🚀 Como rodar localmente

### Backend

```bash
# 1. Clone o repositório
git clone https://github.com/VanthuirMaia/feedback-agent.git
cd feedback-agent/backend

# 2. Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com sua OPENAI_API_KEY

# 5. Rode o servidor
python -m uvicorn app.main:app --reload
```

Acesse a documentação: `http://localhost:8000/docs`

### Frontend

```bash
cd feedback-agent/frontend

# 1. Instale as dependências
npm install

# 2. Rode o servidor de desenvolvimento
npm run dev
```

Acesse: `http://localhost:8080`

---

## 📋 Fases do Projeto

- [x] Fase 1 — Visão Estratégica
- [x] Fase 2 — Insights do Mercado
- [x] Fase 3 — Arquitetura Técnica
- [x] Fase 4 — Criação Interativa ← _em andamento_
- [ ] Fase 5 — Lançamento e PDCA

---

## 👨‍💻 Autor

**Vanthuir Maia** — Dev com perfil Tech Lead / IA Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin)](https://linkedin.com/in/vanthuirmaia)
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/VanthuirMaia)
