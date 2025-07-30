from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/municipios", tags=["municipios"])

@router.get("/", response_model=List[schemas.MunicipioList])
def read_municipios(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    nome: Optional[str] = Query(None, description="Filtrar por nome do município"),
    populacao_min: Optional[int] = Query(None, ge=0, description="População mínima"),
    populacao_max: Optional[int] = Query(None, ge=0, description="População máxima"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("asc", pattern="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os municípios com filtros opcionais.
    """
    municipios = crud.get_municipios(
        db, 
        skip=skip, 
        limit=limit, 
        nome=nome,
        populacao_min=populacao_min,
        populacao_max=populacao_max,
        order_by=order_by,
        order_direction=order_direction
    )
    return municipios

@router.get("/{id_municipio}", response_model=schemas.Municipio)
def read_municipio(id_municipio: str, db: Session = Depends(get_db)):
    """
    Obtém um município específico por ID.
    """
    municipio = crud.get_municipio(db, id_municipio=id_municipio)
    if municipio is None:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    return municipio

@router.post("/", response_model=schemas.Municipio, status_code=201)
def create_municipio(municipio: schemas.MunicipioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo município.
    """
    db_municipio = crud.get_municipio(db, id_municipio=municipio.id_municipio)
    if db_municipio:
        raise HTTPException(status_code=400, detail="Município já existe")
    return crud.create_municipio(db=db, municipio=municipio)

@router.put("/{id_municipio}", response_model=schemas.Municipio)
def update_municipio(
    id_municipio: str, 
    municipio: schemas.MunicipioUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza um município existente.
    """
    db_municipio = crud.update_municipio(db=db, id_municipio=id_municipio, municipio=municipio)
    if db_municipio is None:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    return db_municipio

@router.delete("/{id_municipio}", status_code=204)
def delete_municipio(id_municipio: str, db: Session = Depends(get_db)):
    """
    Remove um município.
    """
    success = crud.delete_municipio(db=db, id_municipio=id_municipio)
    if not success:
        raise HTTPException(status_code=404, detail="Município não encontrado")

@router.get("/{id_municipio}/indicadores", response_model=List[schemas.IndicadoresCompleto])
def read_indicadores_municipio(
    id_municipio: str,
    ano_inicio: Optional[int] = Query(None, ge=1900, le=2100, description="Ano inicial"),
    ano_fim: Optional[int] = Query(None, ge=1900, le=2100, description="Ano final"),
    prestador_id: Optional[int] = Query(None, gt=0, description="ID do prestador"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("desc", pattern="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_db)
):
    """
    Obtém os indicadores de desempenho de um município específico.
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db, id_municipio=id_municipio)
    if municipio is None:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Buscar indicadores com filtros
    indicadores = crud.get_indicadores(
        db,
        municipio_id=id_municipio,
        ano_inicio=ano_inicio,
        ano_fim=ano_fim,
        prestador_id=prestador_id,
        order_by=order_by,
        order_direction=order_direction
    )
    
    # Converter para IndicadoresCompleto
    indicadores_completos = []
    for indicador in indicadores:
        recursos_hidricos = crud.get_recursos_hidricos_by_indicador(db, indicador.id)
        financeiro = crud.get_financeiro_by_indicador(db, indicador.id)
        
        indicador_completo = schemas.IndicadoresCompleto(
            **indicador.__dict__,
            recursos_hidricos=recursos_hidricos,
            financeiro=financeiro
        )
        indicadores_completos.append(indicador_completo)
    
    return indicadores_completos 