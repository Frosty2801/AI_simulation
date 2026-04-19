# PetCare Medellín - AI Automation System

Sistema de automatización con IA para la clínica veterinaria PetCare Medellín. Maneja consultas de múltiples canales (Telegram, email, formularios web) usando clasificación de mensajes y RAG (Retrieval-Augmented Generation).

## Características

- **Recepción multi-canal**: Telegram, Email, Webhooks
- **Clasificación automática**: 5 categorías (URGENCIA, AGENDAMIENTO, CONSULTA, SEGUIMIENTO, ADMINISTRATIVA)
- **RAG**: Retrieval-Augmented Generation con ChromaDB
- **Soporte Ollama**: Embeddings y LLM locales
- **Tests**: Suite completa de tests unitarios

## Requisitos

- Python 3.10+
- Docker (para n8n + ngrok)
- Ollama (opcional, para embeddings/LLM locales)

## Instalación

### 1. Clonar y configurar entorno

```bash
# Clonar repositorio
git clone https://github.com/Frosty2801/AI_simulation.git
cd AI_simulation

# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y configurar:

```bash
# Embeddings provider: openai | ollama
EMBEDDING_PROVIDER=ollama

# OpenAI (si usa openai)
OPENAI_API_KEY=sk-...
OPENAI_EMBED_MODEL=text-embedding-3-small

# Ollama (si usa ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_MODEL=llama3.2

# Document Indexing
DOCS_DIR=docs
CHROMA_DB_DIR=./chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 3. Indexar documentos

```bash
python src/index_documents.py --test
```

Esto cargará los 4 documentos del negocio y creará el vector store en ChromaDB.

## Estructura del Proyecto

```
AI_simulation/
├── docs/                      # Documentos del negocio
│   ├── petcare_faq.md
│   ├── petcare_policies.md
│   ├── petcare_protocols.md
│   └── petcare_services_pricing.md
├── src/
│   ├── core/
│   │   ├── embeddings.py      # Embeddings (OpenAI/Ollama)
│   │   ├── llm.py             # LLM Client + Clasificación
│   │   └── retriever.py       # ChromaDB RAG
│   ├── data/
│   │   ├── loader.py          # Carga de documentos
│   │   └── chunkers.py        # Text chunking
│   └── index_documents.py     # Script de indexación
├── tests/                     # Suite de tests
├── workflows/                 # Workflows n8n
├── docker-compose.yml         # n8n + ngrok
├── requirements.txt           # Dependencias Python
└── pytest.ini                 # Configuración de tests
```

## Uso

### Indexar documentos

```bash
python src/index_documents.py --reset --test
```

### Ejecutar tests

```bash
# Todos los tests
python -m pytest tests/ -v

# Tests específicos
python -m pytest tests/test_loader.py -v

# Solo unit tests (sin integration)
python -m pytest tests/ -v -m "not integration"
```

### Usar el clasificador

```python
from src.core.llm import LLMClient

client = LLMClient(provider="ollama")
result = client.classify_message("Mi perro no puede respirar")
print(result.categoria)  # URGENCIA
print(result.prioridad)  # ALTA
```

### Retrieval RAG

```python
from src.core.retriever import VectorStoreManager

manager = VectorStoreManager(
    persist_directory="./chroma_db",
    embedding_provider="ollama"
)

results = manager.similarity_search("vacunas para perros", k=4)
for doc in results:
    print(doc.page_content)
```

## n8n + Telegram

Para exponer n8n a internet (necesario para Telegram webhooks):

```bash
# Configurar ngrok en .env
NGROK_AUTHTOKEN=tu_token

# Iniciar stack
docker compose up -d

# Obtener URL de ngrok
# http://localhost:4040
```

## Tecnologías

| Componente | Tecnología |
|------------|------------|
| Orquestación | n8n |
| Exposición | ngrok |
| RAG | LangChain + ChromaDB |
| Embeddings | OpenAI / Ollama |
| LLM | OpenAI / Ollama |
| Testing | pytest |

## Licencia

MIT
