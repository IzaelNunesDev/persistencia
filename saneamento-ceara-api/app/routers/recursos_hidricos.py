from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/recursos-hidricos", tags=["recursos-hidricos"])

@router.get("/", response_model=List[schemas.RecursosHidricosList])
def read_recursos_hidricos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    indicador_id: Optional[int] = Query(None, gt=0, description="ID do indicador"),
    volume_min: Optional[float] = Query(None, ge=0, description="Volume mínimo de água produzida"),
    volume_max: Optional[float] = Query(None, ge=0, description="Volume máximo de água produzida"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("asc", pattern="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de recursos hídricos com filtros opcionais.
    """
    recursos_hidricos = crud.get_recursos_hidricos_list(
        db,
        skip=skip,
        limit=limit,
        indicador_id=indicador_id,
        volume_min=volume_min,
        volume_max=volume_max,
        order_by=order_by,
        order_direction=order_direction
    )
    return recursos_hidricos

@router.get("/{recursos_id}", response_model=schemas.RecursosHidricos)
def read_recursos_hidricos_by_id(recursos_id: int, db: Session = Depends(get_db)):
    """
    Obtém um registro específico de recursos hídricos por ID.
    """
    recursos_hidricos = crud.get_recursos_hidricos(db, recursos_id=recursos_id)
    if recursos_hidricos is None:
        raise HTTPException(status_code=404, detail="Recursos hídricos não encontrados")
    return recursos_hidricos

@router.get("/indicador/{indicador_id}", response_model=schemas.RecursosHidricos)
def read_recursos_hidricos_by_indicador(indicador_id: int, db: Session = Depends(get_db)):
    """
    Obtém os recursos hídricos de um indicador específico.
    """
    recursos_hidricos = crud.get_recursos_hidricos_by_indicador(db, indicador_id=indicador_id)
    if recursos_hidricos is None:
        raise HTTPException(status_code=404, detail="Recursos hídricos não encontrados para este indicador")
    return recursos_hidricos

@router.post("/", response_model=schemas.RecursosHidricos, status_code=201)
def create_recursos_hidricos(recursos: schemas.RecursosHidricosCreate, db: Session = Depends(get_db)):
    """
    Cria um novo registro de recursos hídricos.
    """
    # Verificar se já existe um registro para este indicador
    existing = crud.get_recursos_hidricos_by_indicador(db, indicador_id=recursos.indicador_id)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Já existe um registro de recursos hídricos para este indicador"
        )
    
    # Verificar se o indicador existe
    indicador = crud.get_indicador(db, indicador_id=recursos.indicador_id)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador não encontrado")
    
    return crud.create_recursos_hidricos(db=db, recursos=recursos)

@router.put("/{recursos_id}", response_model=schemas.RecursosHidricos)
def update_recursos_hidricos(
    recursos_id: int,
    recursos: schemas.RecursosHidricosUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro de recursos hídricos existente.
    """
    db_recursos = crud.update_recursos_hidricos(db=db, recursos_id=recursos_id, recursos=recursos)
    if db_recursos is None:
        raise HTTPException(status_code=404, detail="Recursos hídricos não encontrados")
    return db_recursos

@router.delete("/{recursos_id}", status_code=204)
def delete_recursos_hidricos(recursos_id: int, db: Session = Depends(get_db)):
    """
    Remove um registro de recursos hídricos.
    """
    success = crud.delete_recursos_hidricos(db=db, recursos_id=recursos_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recursos hídricos não encontrados")

@router.get("/estatisticas/volume-agua", response_model=dict)
def get_estatisticas_volume_agua(
    ano: Optional[int] = Query(None, ge=1900, le=2100, description="Ano para filtrar"),
    db: Session = Depends(get_db)
):
    """
    Obtém estatísticas sobre volumes de água.
    """
    from sqlalchemy import func
    
    query = db.query(
        func.avg(crud.models.RecursosHidricosAnual.volume_agua_produzido).label("media_produzido"),
        func.avg(crud.models.RecursosHidricosAnual.volume_agua_consumido).label("media_consumido"),
        func.avg(crud.models.RecursosHidricosAnual.volume_agua_faturado).label("media_faturado"),
        func.sum(crud.models.RecursosHidricosAnual.volume_agua_produzido).label("total_produzido"),
        func.sum(crud.models.RecursosHidricosAnual.volume_agua_consumido).label("total_consumido"),
        func.sum(crud.models.RecursosHidricosAnual.volume_agua_faturado).label("total_faturado")
    )
    
    if ano:
        query = query.join(crud.models.IndicadoresDesempenhoAnual).filter(
            crud.models.IndicadoresDesempenhoAnual.ano == ano
        )
    
    result = query.first()
    
    return {
        "media_produzido": crud._safe_float(result.media_produzido),
        "media_consumido": crud._safe_float(result.media_consumido),
        "media_faturado": crud._safe_float(result.media_faturado),
        "total_produzido": crud._safe_float(result.total_produzido),
        "total_consumido": crud._safe_float(result.total_consumido),
        "total_faturado": crud._safe_float(result.total_faturado)
    } 