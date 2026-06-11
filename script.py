from pathlib import Path

folders = [
    "app",
    "app/api",
    "app/graph",
    "app/graph/nodes",
    "app/graph/routers",
    "app/services",
    "app/models",
    "app/config",
    "app/utils",
    "data",
    "data/raw",
    "data/processed",
    "eval",
    "docs",
    "scripts",
]

files = [
    "app/__init__.py",

    "app/main.py",

    "app/api/__init__.py",
    "app/api/routes.py",

    "app/graph/__init__.py",
    "app/graph/state.py",
    "app/graph/workflow.py",

    "app/graph/nodes/__init__.py",
    "app/graph/nodes/retrieve.py",
    "app/graph/nodes/relevance_check.py",
    "app/graph/nodes/generate_answer.py",
    "app/graph/nodes/no_answer.py",

    "app/graph/routers/__init__.py",
    "app/graph/routers/relevance_router.py",

    "app/services/__init__.py",
    "app/services/pinecone_service.py",
    "app/services/embedding_service.py",
    "app/services/llm_service.py",
    "app/services/chunking_service.py",

    "app/models/__init__.py",
    "app/models/request_models.py",
    "app/models/response_models.py",

    "app/config/__init__.py",
    "app/config/settings.py",

    "app/utils/__init__.py",
    "app/utils/logger.py",

    "scripts/ingest.py",

    "eval/test_cases.json",

    "docs/langgraph.md",

    ".env.example",
    "requirements.txt",
    "README.md",
]
    
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file in files:
    Path(file).touch(exist_ok=True)

print("Project structure created successfully!")