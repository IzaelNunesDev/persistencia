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
    microrregiao: Optional[str] = Query(None, description="Filtrar por microrregião"),
    db: Session = Depends(get_db)
):
    """
    Lista municípios com paginação e filtros opcionais.
    
    - **skip**: Número de registros para pular (para paginação)
    - **limit**: Número máximo de registros retornados
    - **nome**: Filtrar por nome do município (busca parcial)
    - **microrregiao**: Filtrar por microrregião específica
    """
    municipios = crud.get_municipios(
        db=db, 
        skip=skip, 
        limit=limit, 
        nome=nome, 
        microrregiao=microrregiao
    )
    return municipios

@router.get("/{id_municipio}", response_model=schemas.MunicipioComCapital)
def obter_municipio(
    id_municipio: str,
    db: Session = Depends(get_db)
):
    """
    Obtém dados detalhados de um município específico, incluindo informações da capital se aplicável.
    
    - **id_municipio**: Código IBGE do município
    """
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar dados da capital se existir
    capital = crud.get_capital(db=db, municipio_id=id_municipio)
    
    # Criar resposta com dados do município e capital
    response = schemas.MunicipioComCapital(
        id_municipio=municipio.id_municipio,
        nome=municipio.nome,
        microrregiao=municipio.microrregiao,
        mesorregiao=municipio.mesorregiao,
        ddd=municipio.ddd,
        capital=capital
    )
    
    return response

@router.get("/{id_municipio}/saneamento/historico", response_model=schemas.HistoricoSaneamento)
def obter_historico_saneamento(
    id_municipio: str,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Retorna a série histórica completa de dados de saneamento para um município.
    
    - **id_municipio**: Código IBGE do município
    - **skip**: Número de registros para pular (para paginação)
    - **limit**: Número máximo de registros retornados
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar dados históricos de saneamento
    dados = crud.get_dados_saneamento_municipio(
        db=db, 
        municipio_id=id_municipio,
        skip=skip,
        limit=limit
    )
    
    return schemas.HistoricoSaneamento(
        municipio=municipio,
        dados=dados
    )

@router.post("/", response_model=schemas.Municipio)
def criar_municipio(
    municipio: schemas.MunicipioCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo município.
    
    - **municipio**: Dados do município a ser criado
    """
    # Verificar se o município já existe
    db_municipio = crud.get_municipio(db=db, id_municipio=municipio.id_municipio)
    if db_municipio:
        raise HTTPException(status_code=400, detail="Município já existe")
    
    return crud.create_municipio(db=db, municipio=municipio) 