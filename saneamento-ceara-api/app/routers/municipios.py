from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/municipios", tags=["municipios"])

@router.get("/", response_model=List[schemas.Municipio])
def listar_municipios(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    nome: Optional[str] = Query(None, description="Filtrar por nome do município"),
    db: Session = Depends(get_db)
):
    """
    Lista municípios com paginação e filtros opcionais.
    
    - **skip**: Número de registros para pular (para paginação)
    - **limit**: Número máximo de registros retornados
    - **nome**: Filtrar por nome do município (busca parcial)
    """
    municipios = crud.get_municipios(
        db=db, 
        skip=skip, 
        limit=limit, 
        nome=nome
    )
    return municipios

@router.get("/search")
def buscar_municipios(
    q: str = Query(..., description="Termo de busca"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados"),
    db: Session = Depends(get_db)
):
    """
    Busca municípios por nome (busca parcial).
    
    - **q**: Termo de busca
    - **limit**: Número máximo de resultados
    """
    municipios = crud.get_municipios(
        db=db,
        skip=0,
        limit=limit,
        nome=q
    )
    return municipios

@router.get("/{id_municipio}", response_model=schemas.Municipio)
def obter_municipio(
    id_municipio: str,
    db: Session = Depends(get_db)
):
    """
    Obtém dados detalhados de um município específico.
    
    - **id_municipio**: Código IBGE do município
    """
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    return municipio

@router.get("/{id_municipio}/indicadores", response_model=List[schemas.IndicadoresDesempenho])
def obter_indicadores_municipio(
    id_municipio: str,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Retorna a série histórica completa de indicadores de desempenho para um município.
    
    - **id_municipio**: Código IBGE do município
    - **skip**: Número de registros para pular (para paginação)
    - **limit**: Número máximo de registros retornados
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar dados históricos de indicadores
    indicadores = crud.get_indicadores_municipio(
        db=db, 
        municipio_id=id_municipio,
        skip=skip,
        limit=limit
    )
    
    return indicadores

@router.get("/{id_municipio}/indicadores-atuais")
def obter_indicadores_atuais_municipio(
    id_municipio: str,
    db: Session = Depends(get_db)
):
    """
    Retorna os indicadores mais recentes de um município.
    
    - **id_municipio**: Código IBGE do município
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar indicadores atuais
    indicadores = crud.get_indicador_atual_municipio(
        db=db, 
        municipio_id=id_municipio
    )
    
    if not indicadores:
        raise HTTPException(status_code=404, detail="Nenhum indicador encontrado para este município")
    
    return indicadores

@router.get("/{id_municipio}/evolucao")
def obter_evolucao_municipio(
    id_municipio: str,
    db: Session = Depends(get_db)
):
    """
    Retorna a evolução temporal dos indicadores de um município.
    
    - **id_municipio**: Código IBGE do município
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar evolução
    evolucao = crud.get_evolucao_indicadores(
        db=db, 
        municipio_id=id_municipio
    )
    
    return evolucao

@router.get("/{id_municipio}/recursos-hidricos")
def obter_recursos_hidricos_municipio(
    id_municipio: str,
    db: Session = Depends(get_db)
):
    """
    Retorna os dados de recursos hídricos mais recentes de um município.
    
    - **id_municipio**: Código IBGE do município
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar indicadores atuais
    indicadores = crud.get_indicador_atual_municipio(
        db=db, 
        municipio_id=id_municipio
    )
    
    if not indicadores:
        raise HTTPException(status_code=404, detail="Nenhum indicador encontrado para este município")
    
    # Buscar recursos hídricos
    recursos = crud.get_recursos_hidricos(
        db=db, 
        indicador_id=indicadores.id
    )
    
    if not recursos:
        raise HTTPException(status_code=404, detail="Nenhum dado de recursos hídricos encontrado")
    
    return recursos

@router.get("/{id_municipio}/indicadores-financeiros")
def obter_indicadores_financeiros_municipio(
    id_municipio: str,
    db: Session = Depends(get_db)
):
    """
    Retorna os dados financeiros mais recentes de um município.
    
    - **id_municipio**: Código IBGE do município
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar indicadores atuais
    indicadores = crud.get_indicador_atual_municipio(
        db=db, 
        municipio_id=id_municipio
    )
    
    if not indicadores:
        raise HTTPException(status_code=404, detail="Nenhum indicador encontrado para este município")
    
    # Buscar dados financeiros
    financeiro = crud.get_financeiro(
        db=db, 
        indicador_id=indicadores.id
    )
    
    if not financeiro:
        raise HTTPException(status_code=404, detail="Nenhum dado financeiro encontrado")
    
    return financeiro

@router.post("/", response_model=schemas.Municipio)
def criar_municipio(
    municipio: schemas.MunicipioCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo município.
    
    - **municipio**: Dados do município a ser criado
    """
    return crud.create_municipio(db=db, municipio=municipio) 