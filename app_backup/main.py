import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from.database import engine, Base
from.routers import b2g, wearables
# from.routers import family, auth  <-- Comentei isto para já para não dar erro de falta de ficheiros

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar as tabelas na DB automaticamente (para dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=os.getenv("API_TITLE", "Guardi.IA Platform API"),
    description=os.getenv("API_DESCRIPTION", "API para gestão logística de cuidados familiares e comunitários."),
    version=os.getenv("API_VERSION", "1.0.0")
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Registar os módulos (Rotas)
routers = [
    # ("auth", auth.router),
    # ("family", family.router),
    ("b2g", b2g.router),
    ("wearables", wearables.router)
]
for name, router in routers:
    app.include_router(router)

@app.get("/")
def health_check():
    active_modules = [name for name, _ in routers]
    logger.info(f"Health check called. Active modules: {active_modules}")
    return {
        "system": os.getenv("SYSTEM_NAME", "Guardi.IA"),
        "status": "operational",
        "modules_active": active_modules
    }