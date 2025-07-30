from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
from app.database import engine
from app import models
from app.routers import municipios, analises, prestadores, indicadores, recursos_hidricos, financeiro
from app.logging_config import setup_logging, get_logger, log_request

# Configurar logging
setup_logging()
logger = get_logger(__name__)

# Criar tabelas no banco de dados (opcional)
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso no banco de dados")
except Exception as e:
    logger.warning(f"Erro ao criar tabelas: {e}")
    logger.info("As tabelas podem ser criadas posteriormente usando Alembic")

# Criar aplicação FastAPI
app = FastAPI(
    title="API de Análise de Saneamento do Ceará",
    description="API RESTful para análise de dados de saneamento básico no Ceará baseada no SNIS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
import os
environment = os.getenv("ENVIRONMENT", "development")

if environment == "production":
    # Em produção, permitir apenas domínios específicos
    allowed_origins = [
        "https://saneamento-ceara-api.onrender.com",
        "https://*.onrender.com"
    ]
else:
    # Em desenvolvimento, permitir todos os domínios
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Log da requisição recebida
    logger.info(f"Request {request_id}: {request.method} {request.url.path} - Started")
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Log da resposta
        log_request(
            request_id=request_id,
            method=request.method,
            url=str(request.url.path),
            status_code=response.status_code,
            duration=duration
        )
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Request {request_id}: {request.method} {request.url.path} - ERROR: {str(e)} ({duration:.3f}s)")
        raise

# Incluir routers
app.include_router(municipios.router, prefix="/api/v1")
app.include_router(analises.router, prefix="/api/v1")
app.include_router(prestadores.router, prefix="/api/v1")
app.include_router(indicadores.router, prefix="/api/v1")
app.include_router(recursos_hidricos.router, prefix="/api/v1")
app.include_router(financeiro.router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Endpoint raiz da API - informações sobre a API
    """
    logger.info("Acesso ao endpoint raiz")
    return {
        "message": "API de Análise de Saneamento do Ceará",
        "version": "1.0.0",
        "description": "API RESTful para análise de dados de saneamento básico no Ceará",
        "documentation": "/docs",
        "endpoints": {
            "municipios": "/api/v1/municipios",
            "prestadores": "/api/v1/prestadores",
            "indicadores": "/api/v1/indicadores",
            "recursos_hidricos": "/api/v1/recursos-hidricos",
            "financeiro": "/api/v1/financeiro",
            "analises": "/api/v1/analises",
            "docs": "/docs"
        }
    }

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
            "prestadores": "/api/v1/prestadores",
            "indicadores": "/api/v1/indicadores",
            "recursos_hidricos": "/api/v1/recursos-hidricos",
            "financeiro": "/api/v1/financeiro",
            "analises": "/api/v1/analises",
            "docs": "/docs"
        }
    }

@app.on_event("startup")
async def startup_event():
    """
    Evento executado na inicialização da aplicação
    """
    logger.info("🚀 Iniciando API de Análise de Saneamento do Ceará")
    logger.info("📊 Endpoints disponíveis:")
    logger.info("   - Municípios: /api/v1/municipios")
    logger.info("   - Prestadores: /api/v1/prestadores")
    logger.info("   - Indicadores: /api/v1/indicadores")
    logger.info("   - Recursos Hídricos: /api/v1/recursos-hidricos")
    logger.info("   - Financeiro: /api/v1/financeiro")
    logger.info("   - Análises: /api/v1/analises")
    logger.info("📚 Documentação: /docs")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento executado no encerramento da aplicação
    """
    logger.info("🛑 Encerrando API de Análise de Saneamento do Ceará") 