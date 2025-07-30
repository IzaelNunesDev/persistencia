from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/prestadores", tags=["prestadores"])

@router.get("/", response_model=List[schemas.PrestadorServicoList])
def read_prestadores(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    nome: Optional[str] = Query(None, description="Filtrar por nome do prestador"),
    sigla: Optional[str] = Query(None, description="Filtrar por sigla"),
    natureza_juridica: Optional[str] = Query(None, description="Filtrar por natureza jurídica"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("asc", pattern="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os prestadores de serviço com filtros opcionais.
    """
    prestadores = crud.get_prestadores(
        db,
        skip=skip,
        limit=limit,
        nome=nome,
        sigla=sigla,
        natureza_juridica=natureza_juridica,
        order_by=order_by,
        order_direction=order_direction
    )
    return prestadores

@router.get("/{prestador_id}", response_model=schemas.PrestadorServico)
def read_prestador(prestador_id: int, db: Session = Depends(get_db)):
    """
    Obtém um prestador de serviço específico por ID.
    """
    prestador = crud.get_prestador(db, prestador_id=prestador_id)
    if prestador is None:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return prestador

@router.get("/sigla/{sigla}", response_model=schemas.PrestadorServico)
def read_prestador_by_sigla(sigla: str, db: Session = Depends(get_db)):
    """
    Obtém um prestador de serviço por sigla.
    """
    prestador = crud.get_prestador_by_sigla(db, sigla=sigla)
    if prestador is None:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return prestador

@router.post("/", response_model=schemas.PrestadorServico, status_code=201)
def create_prestador(prestador: schemas.PrestadorServicoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo prestador de serviço.
    """
    # Verificar se já existe um prestador com a mesma sigla
    db_prestador = crud.get_prestador_by_sigla(db, sigla=prestador.sigla)
    if db_prestador:
        raise HTTPException(status_code=400, detail="Já existe um prestador com esta sigla")
    return crud.create_prestador(db=db, prestador=prestador)

@router.put("/{prestador_id}", response_model=schemas.PrestadorServico)
def update_prestador(
    prestador_id: int,
    prestador: schemas.PrestadorServicoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um prestador de serviço existente.
    """
    db_prestador = crud.update_prestador(db=db, prestador_id=prestador_id, prestador=prestador)
    if db_prestador is None:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return db_prestador

@router.delete("/{prestador_id}", status_code=204)
def delete_prestador(prestador_id: int, db: Session = Depends(get_db)):
    """
    Remove um prestador de serviço.
    """
    success = crud.delete_prestador(db=db, prestador_id=prestador_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")

@router.get("/{prestador_id}/indicadores", response_model=List[schemas.IndicadoresDesempenhoList])
def read_indicadores_prestador(
    prestador_id: int,
    ano_inicio: Optional[int] = Query(None, ge=1900, le=2100, description="Ano inicial"),
    ano_fim: Optional[int] = Query(None, ge=1900, le=2100, description="Ano final"),
    municipio_id: Optional[str] = Query(None, description="ID do município"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("desc", pattern="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_db)
):
    """
    Obtém os indicadores de desempenho de um prestador específico.
    """
    # Verificar se o prestador existe
    prestador = crud.get_prestador(db, prestador_id=prestador_id)
    if prestador is None:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    
    # Buscar indicadores com filtros
    indicadores = crud.get_indicadores(
        db,
        prestador_id=prestador_id,
        ano_inicio=ano_inicio,
        ano_fim=ano_fim,
        municipio_id=municipio_id,
        order_by=order_by,
        order_direction=order_direction
    )
    
    return indicadores 