from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/indicadores", tags=["indicadores"])

@router.get("/", response_model=List[schemas.IndicadoresDesempenhoList])
def read_indicadores(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    ano_inicio: Optional[int] = Query(None, ge=1900, le=2100, description="Ano inicial"),
    ano_fim: Optional[int] = Query(None, ge=1900, le=2100, description="Ano final"),
    municipio_id: Optional[str] = Query(None, description="ID do município"),
    prestador_id: Optional[int] = Query(None, gt=0, description="ID do prestador"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("desc", pattern="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os indicadores de desempenho com filtros opcionais.
    """
    indicadores = crud.get_indicadores(
        db,
        skip=skip,
        limit=limit,
        ano_inicio=ano_inicio,
        ano_fim=ano_fim,
        municipio_id=municipio_id,
        prestador_id=prestador_id,
        order_by=order_by,
        order_direction=order_direction
    )
    return indicadores

@router.get("/{indicador_id}", response_model=schemas.IndicadoresCompleto)
def read_indicador(indicador_id: int, db: Session = Depends(get_db)):
    """
    Obtém um indicador de desempenho específico por ID, incluindo dados de recursos hídricos e financeiro.
    """
    indicador = crud.get_indicador(db, indicador_id=indicador_id)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador de desempenho não encontrado")
    
    # Buscar dados relacionados
    recursos_hidricos = crud.get_recursos_hidricos_by_indicador(db, indicador_id)
    financeiro = crud.get_financeiro_by_indicador(db, indicador_id)
    
    # Criar resposta completa
    indicador_completo = schemas.IndicadoresCompleto(
        **indicador.__dict__,
        recursos_hidricos=recursos_hidricos,
        financeiro=financeiro
    )
    
    return indicador_completo

@router.post("/", response_model=schemas.IndicadoresDesempenho, status_code=201)
def create_indicador(indicador: schemas.IndicadoresDesempenhoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo indicador de desempenho.
    """
    # Verificar se já existe um indicador para o mesmo ano, município e prestador
    existing = db.query(crud.models.IndicadoresDesempenhoAnual).filter(
        crud.models.IndicadoresDesempenhoAnual.ano == indicador.ano,
        crud.models.IndicadoresDesempenhoAnual.municipio_id == indicador.municipio_id,
        crud.models.IndicadoresDesempenhoAnual.prestador_id == indicador.prestador_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Já existe um indicador para este ano, município e prestador"
        )
    
    return crud.create_indicadores(db=db, indicadores=indicador)

@router.put("/{indicador_id}", response_model=schemas.IndicadoresDesempenho)
def update_indicador(
    indicador_id: int,
    indicador: schemas.IndicadoresDesempenhoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um indicador de desempenho existente.
    """
    db_indicador = crud.update_indicadores(db=db, indicador_id=indicador_id, indicadores=indicador)
    if db_indicador is None:
        raise HTTPException(status_code=404, detail="Indicador de desempenho não encontrado")
    return db_indicador

@router.delete("/{indicador_id}", status_code=204)
def delete_indicador(indicador_id: int, db: Session = Depends(get_db)):
    """
    Remove um indicador de desempenho.
    """
    success = crud.delete_indicadores(db=db, indicador_id=indicador_id)
    if not success:
        raise HTTPException(status_code=404, detail="Indicador de desempenho não encontrado")

@router.get("/{indicador_id}/recursos-hidricos", response_model=schemas.RecursosHidricos)
def read_recursos_hidricos_indicador(indicador_id: int, db: Session = Depends(get_db)):
    """
    Obtém os dados de recursos hídricos de um indicador específico.
    """
    # Verificar se o indicador existe
    indicador = crud.get_indicador(db, indicador_id=indicador_id)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador de desempenho não encontrado")
    
    recursos_hidricos = crud.get_recursos_hidricos_by_indicador(db, indicador_id)
    if recursos_hidricos is None:
        raise HTTPException(status_code=404, detail="Dados de recursos hídricos não encontrados")
    
    return recursos_hidricos

@router.get("/{indicador_id}/financeiro", response_model=schemas.Financeiro)
def read_financeiro_indicador(indicador_id: int, db: Session = Depends(get_db)):
    """
    Obtém os dados financeiros de um indicador específico.
    """
    # Verificar se o indicador existe
    indicador = crud.get_indicador(db, indicador_id=indicador_id)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador de desempenho não encontrado")
    
    financeiro = crud.get_financeiro_by_indicador(db, indicador_id)
    if financeiro is None:
        raise HTTPException(status_code=404, detail="Dados financeiros não encontrados")
    
    return financeiro 