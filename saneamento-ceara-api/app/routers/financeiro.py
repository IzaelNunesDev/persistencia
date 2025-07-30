from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/financeiro", tags=["financeiro"])

@router.get("/", response_model=List[schemas.FinanceiroList])
def read_financeiro(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    indicador_id: Optional[int] = Query(None, gt=0, description="ID do indicador"),
    receita_min: Optional[float] = Query(None, ge=0, description="Receita mínima"),
    receita_max: Optional[float] = Query(None, ge=0, description="Receita máxima"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("asc", pattern="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros financeiros com filtros opcionais.
    """
    financeiro = crud.get_financeiro_list(
        db,
        skip=skip,
        limit=limit,
        indicador_id=indicador_id,
        receita_min=receita_min,
        receita_max=receita_max,
        order_by=order_by,
        order_direction=order_direction
    )
    return financeiro

@router.get("/{financeiro_id}", response_model=schemas.Financeiro)
def read_financeiro_by_id(financeiro_id: int, db: Session = Depends(get_db)):
    """
    Obtém um registro financeiro específico por ID.
    """
    financeiro = crud.get_financeiro(db, financeiro_id=financeiro_id)
    if financeiro is None:
        raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
    return financeiro

@router.get("/indicador/{indicador_id}", response_model=schemas.Financeiro)
def read_financeiro_by_indicador(indicador_id: int, db: Session = Depends(get_db)):
    """
    Obtém os dados financeiros de um indicador específico.
    """
    financeiro = crud.get_financeiro_by_indicador(db, indicador_id=indicador_id)
    if financeiro is None:
        raise HTTPException(status_code=404, detail="Dados financeiros não encontrados para este indicador")
    return financeiro

@router.post("/", response_model=schemas.Financeiro, status_code=201)
def create_financeiro(financeiro: schemas.FinanceiroCreate, db: Session = Depends(get_db)):
    """
    Cria um novo registro financeiro.
    """
    # Verificar se já existe um registro para este indicador
    existing = crud.get_financeiro_by_indicador(db, indicador_id=financeiro.indicador_id)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Já existe um registro financeiro para este indicador"
        )
    
    # Verificar se o indicador existe
    indicador = crud.get_indicador(db, indicador_id=financeiro.indicador_id)
    if indicador is None:
        raise HTTPException(status_code=404, detail="Indicador não encontrado")
    
    return crud.create_financeiro(db=db, financeiro=financeiro)

@router.put("/{financeiro_id}", response_model=schemas.Financeiro)
def update_financeiro(
    financeiro_id: int,
    financeiro: schemas.FinanceiroUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro financeiro existente.
    """
    db_financeiro = crud.update_financeiro(db=db, financeiro_id=financeiro_id, financeiro=financeiro)
    if db_financeiro is None:
        raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
    return db_financeiro

@router.delete("/{financeiro_id}", status_code=204)
def delete_financeiro(financeiro_id: int, db: Session = Depends(get_db)):
    """
    Remove um registro financeiro.
    """
    success = crud.delete_financeiro(db=db, financeiro_id=financeiro_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")

@router.get("/estatisticas/receitas-despesas", response_model=dict)
def get_estatisticas_receitas_despesas(
    ano: Optional[int] = Query(None, ge=1900, le=2100, description="Ano para filtrar"),
    db: Session = Depends(get_db)
):
    """
    Obtém estatísticas sobre receitas e despesas.
    """
    from sqlalchemy import func
    
    query = db.query(
        func.avg(crud.models.FinanceiroAnual.receita_operacional_total).label("media_receita"),
        func.avg(crud.models.FinanceiroAnual.despesa_exploracao).label("media_despesa_exploracao"),
        func.avg(crud.models.FinanceiroAnual.despesa_pessoal).label("media_despesa_pessoal"),
        func.avg(crud.models.FinanceiroAnual.despesa_energia).label("media_despesa_energia"),
        func.avg(crud.models.FinanceiroAnual.despesa_total_servicos).label("media_despesa_servicos"),
        func.avg(crud.models.FinanceiroAnual.investimento_total_prestador).label("media_investimento"),
        func.sum(crud.models.FinanceiroAnual.receita_operacional_total).label("total_receita"),
        func.sum(crud.models.FinanceiroAnual.despesa_total_servicos).label("total_despesa"),
        func.sum(crud.models.FinanceiroAnual.investimento_total_prestador).label("total_investimento")
    )
    
    if ano:
        query = query.join(crud.models.IndicadoresDesempenhoAnual).filter(
            crud.models.IndicadoresDesempenhoAnual.ano == ano
        )
    
    result = query.first()
    
    return {
        "media_receita": crud._safe_float(result.media_receita),
        "media_despesa_exploracao": crud._safe_float(result.media_despesa_exploracao),
        "media_despesa_pessoal": crud._safe_float(result.media_despesa_pessoal),
        "media_despesa_energia": crud._safe_float(result.media_despesa_energia),
        "media_despesa_servicos": crud._safe_float(result.media_despesa_servicos),
        "media_investimento": crud._safe_float(result.media_investimento),
        "total_receita": crud._safe_float(result.total_receita),
        "total_despesa": crud._safe_float(result.total_despesa),
        "total_investimento": crud._safe_float(result.total_investimento)
    }

@router.get("/sustentabilidade/{ano}", response_model=schemas.SustentabilidadeResponse)
def get_sustentabilidade_financeira(ano: int, db: Session = Depends(get_db)):
    """
    Analisa a sustentabilidade financeira dos municípios em um ano específico.
    """
    from sqlalchemy import func
    
    # Buscar dados financeiros do ano
    query = db.query(
        crud.models.FinanceiroAnual,
        crud.models.IndicadoresDesempenhoAnual,
        crud.models.Municipio
    ).join(
        crud.models.IndicadoresDesempenhoAnual
    ).join(
        crud.models.Municipio
    ).filter(
        crud.models.IndicadoresDesempenhoAnual.ano == ano,
        crud.models.FinanceiroAnual.receita_operacional_total.isnot(None),
        crud.models.FinanceiroAnual.despesa_total_servicos.isnot(None)
    )
    
    resultados = query.all()
    
    sustentaveis = []
    insustentaveis = []
    
    for financeiro, indicador, municipio in resultados:
        receita = financeiro.receita_operacional_total or 0
        despesa = financeiro.despesa_total_servicos or 0
        saldo = receita - despesa
        sustentavel = saldo >= 0
        
        item = schemas.SustentabilidadeFinanceira(
            municipio=municipio,
            receita=receita,
            despesa=despesa,
            saldo=saldo,
            sustentavel=sustentavel
        )
        
        if sustentavel:
            sustentaveis.append(item)
        else:
            insustentaveis.append(item)
    
    return schemas.SustentabilidadeResponse(
        ano=ano,
        sustentaveis=sustentaveis,
        insustentaveis=insustentaveis
    ) 