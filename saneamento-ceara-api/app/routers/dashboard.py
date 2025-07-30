from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from typing import Optional
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Criar router
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """
    Página inicial do dashboard
    """
    logger.info("Acesso à página inicial do dashboard")
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/municipios", response_class=HTMLResponse)
async def dashboard_municipios(request: Request, db: Session = Depends(get_db)):
    """
    Lista de municípios
    """
    logger.info("Acesso à página de municípios")
    
    try:
        # Buscar todos os municípios
        municipios = crud.get_municipios(db, skip=0, limit=100)
        return templates.TemplateResponse("municipios.html", {
            "request": request,
            "municipios": municipios
        })
    except Exception as e:
        logger.error(f"Erro ao carregar municípios: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/municipios/{municipio_id}", response_class=HTMLResponse)
async def dashboard_municipio_detail(request: Request, municipio_id: str, db: Session = Depends(get_db)):
    """
    Detalhes de um município específico
    """
    logger.info(f"Acesso aos detalhes do município {municipio_id}")
    
    try:
        # Buscar dados do município
        municipio = crud.get_municipio(db, municipio_id)
        if not municipio:
            raise HTTPException(status_code=404, detail="Município não encontrado")
        
        # Buscar ano atual (último ano com dados)
        ano_atual = crud.get_ultimo_ano_dados(db)
        
        return templates.TemplateResponse("municipio.html", {
            "request": request,
            "municipio": municipio,
            "ano_atual": ano_atual
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao carregar detalhes do município {municipio_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/analises", response_class=HTMLResponse)
async def dashboard_analises(request: Request):
    """
    Página de análises e rankings
    """
    logger.info("Acesso à página de análises")
    return templates.TemplateResponse("analises.html", {"request": request})

@router.get("/comparativo", response_class=HTMLResponse)
async def dashboard_comparativo(request: Request, ano: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Página de comparação entre municípios
    """
    logger.info("Acesso à página de comparativo")
    
    try:
        # Se não especificado, usar o ano mais recente
        if ano is None:
            ano = crud.get_ultimo_ano_dados(db)
        
        # Buscar dados para comparação
        municipios_comparacao = crud.get_municipios_comparacao(db, ano)
        
        return templates.TemplateResponse("comparativo.html", {
            "request": request,
            "ano": ano,
            "municipios": municipios_comparacao
        })
    except Exception as e:
        logger.error(f"Erro ao carregar dados de comparação: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/sustentabilidade", response_class=HTMLResponse)
async def dashboard_sustentabilidade(request: Request, ano: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Página de análise de sustentabilidade financeira
    """
    logger.info("Acesso à página de sustentabilidade")
    
    try:
        # Se não especificado, usar o ano mais recente
        if ano is None:
            ano = crud.get_ultimo_ano_dados(db)
        
        # Buscar dados de sustentabilidade
        dados_sustentabilidade = crud.get_analise_sustentabilidade_financeira(db, ano)
        
        return templates.TemplateResponse("sustentabilidade.html", {
            "request": request,
            "ano": ano,
            "dados": dados_sustentabilidade
        })
    except Exception as e:
        logger.error(f"Erro ao carregar dados de sustentabilidade: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/recursos-hidricos", response_class=HTMLResponse)
async def dashboard_recursos_hidricos(request: Request, ano: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Página de análise de recursos hídricos
    """
    logger.info("Acesso à página de recursos hídricos")
    
    try:
        # Se não especificado, usar o ano mais recente
        if ano is None:
            ano = crud.get_ultimo_ano_dados(db)
        
        # Buscar dados de recursos hídricos
        dados_hidricos = crud.get_analise_eficiencia_hidrica(db, ano)
        
        return templates.TemplateResponse("recursos_hidricos.html", {
            "request": request,
            "ano": ano,
            "dados": dados_hidricos
        })
    except Exception as e:
        logger.error(f"Erro ao carregar dados de recursos hídricos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/evolucao", response_class=HTMLResponse)
async def dashboard_evolucao(request: Request, municipio_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Página de evolução temporal
    """
    logger.info("Acesso à página de evolução temporal")
    
    try:
        municipio = None
        if municipio_id:
            municipio = crud.get_municipio(db, municipio_id)
            if not municipio:
                raise HTTPException(status_code=404, detail="Município não encontrado")
        
        return templates.TemplateResponse("evolucao.html", {
            "request": request,
            "municipio": municipio
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao carregar página de evolução: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor") 