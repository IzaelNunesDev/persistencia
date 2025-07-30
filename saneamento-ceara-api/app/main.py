from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
from app.database import engine
from app import models
from app.routers import municipios, analises, dashboard

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar tabelas no banco de dados
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso no banco de dados")
except Exception as e:
    logger.error(f"Erro ao criar tabelas: {e}")
    raise

# Criar aplicação FastAPI
app = FastAPI(
    title="API de Análise de Saneamento do Ceará",
    description="API RESTful para análise de dados de saneamento básico no Ceará baseada no SNIS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir routers
app.include_router(municipios.router, prefix="/api/v1")
app.include_router(analises.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/dashboard")

@app.get("/")
async def root():
    """
    Endpoint raiz da API - redireciona para o dashboard
    """
    logger.info("Acesso ao endpoint raiz - redirecionando para dashboard")
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")

@app.get("/health")
async def health_check():
    """
    Endpoint para verificação de saúde da API
    """
    logger.info("Verificação de saúde da API")
    return {"status": "healthy", "message": "API funcionando corretamente"}

@app.get("/api/v1")
async def api_info():
    """
    Informações sobre a API
    """
    logger.info("Acesso às informações da API")
    return {
        "name": "API de Análise de Saneamento do Ceará",
        "version": "1.0.0",
        "description": "API para análise de dados de saneamento básico no Ceará",
        "endpoints": {
            "municipios": "/api/v1/municipios",
            "analises": "/api/v1/analises",
            "dashboard": "/dashboard",
            "docs": "/docs"
        }
    }

@app.on_event("startup")
async def startup_event():
    """
    Evento executado na inicialização da aplicação
    """
    logger.info("Iniciando API de Análise de Saneamento do Ceará")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento executado no encerramento da aplicação
    """
    logger.info("Encerrando API de Análise de Saneamento do Ceará") 