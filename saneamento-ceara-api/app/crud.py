from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException
from app import models, schemas
import math

# Funções para Municípios
def get_municipio(db: Session, id_municipio: str) -> Optional[models.Municipio]:
    return db.query(models.Municipio).filter(models.Municipio.id_municipio == id_municipio).first()

def get_municipios(db: Session, skip: int = 0, limit: int = 200, nome: Optional[str] = None) -> List[models.Municipio]:
    query = db.query(models.Municipio).order_by(models.Municipio.nome)
    if nome:
        query = query.filter(models.Municipio.nome.ilike(f"%{nome}%"))
    return query.offset(skip).limit(limit).all()

def create_municipio(db: Session, municipio: schemas.MunicipioCreate) -> models.Municipio:
    db_municipio = models.Municipio(**municipio.dict())
    db.add(db_municipio)
    db.commit()
    db.refresh(db_municipio)
    return db_municipio

# Funções para Prestadores de Serviço
def get_prestador_by_sigla(db: Session, sigla: str) -> Optional[models.PrestadorServico]:
    return db.query(models.PrestadorServico).filter(models.PrestadorServico.sigla == sigla).first()

def create_prestador(db: Session, prestador: schemas.PrestadorServicoCreate) -> models.PrestadorServico:
    db_prestador = models.PrestadorServico(**prestador.dict())
    db.add(db_prestador)
    db.commit()
    db.refresh(db_prestador)
    return db_prestador

# Funções para Indicadores e dados relacionados
def get_indicadores_municipio(db: Session, municipio_id: str) -> List[models.IndicadoresDesempenhoAnual]:
    return db.query(models.IndicadoresDesempenhoAnual)\
        .filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)\
        .order_by(models.IndicadoresDesempenhoAnual.ano.desc()).all()

def create_indicadores(db: Session, indicadores: schemas.IndicadoresDesempenhoCreate) -> models.IndicadoresDesempenhoAnual:
    db_indicadores = models.IndicadoresDesempenhoAnual(**indicadores.dict())
    db.add(db_indicadores)
    db.commit()
    db.refresh(db_indicadores)
    return db_indicadores

def create_recursos_hidricos(db: Session, recursos: schemas.RecursosHidricosCreate) -> models.RecursosHidricosAnual:
    db_recursos = models.RecursosHidricosAnual(**recursos.dict())
    db.add(db_recursos)
    db.commit()
    db.refresh(db_recursos)
    return db_recursos

def create_financeiro(db: Session, financeiro: schemas.FinanceiroCreate) -> models.FinanceiroAnual:
    db_financeiro = models.FinanceiroAnual(**financeiro.dict())
    db.add(db_financeiro)
    db.commit()
    db.refresh(db_financeiro)
    return db_financeiro

# Funções de Análise
def get_ultimo_ano_dados(db: Session) -> int:
    return db.query(func.max(models.IndicadoresDesempenhoAnual.ano)).scalar() or 2022

def _safe_float(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return float(value)

def get_ranking_indicador(db: Session, ano: int, indicador: str, ordem: str, limit: int, municipio_id: Optional[str]) -> dict:
    indicador_map = {
        "indice_atendimento_agua": models.IndicadoresDesempenhoAnual.indice_atendimento_agua,
        "indice_coleta_esgoto": models.IndicadoresDesempenhoAnual.indice_coleta_esgoto,
        "indice_tratamento_esgoto": models.IndicadoresDesempenhoAnual.indice_tratamento_esgoto,
        "indice_perda_faturamento": models.IndicadoresDesempenhoAnual.indice_perda_faturamento
    }
    if indicador not in indicador_map:
        raise HTTPException(status_code=400, detail="Indicador inválido")

    coluna = indicador_map[indicador]
    order_func = desc if ordem == "desc" else asc
    
    query = db.query(
        models.IndicadoresDesempenhoAnual, models.Municipio
    ).join(models.Municipio).filter(
        models.IndicadoresDesempenhoAnual.ano == ano,
        coluna.isnot(None)
    ).order_by(order_func(coluna))

    all_results = query.all()
    
    ranking = []
    for i, (indicador_obj, municipio_obj) in enumerate(all_results, 1):
        if i <= limit:
            ranking.append({
                "posicao": i,
                "municipio": {
                    "id_municipio": municipio_obj.id_municipio,
                    "nome": municipio_obj.nome,
                    "sigla_uf": municipio_obj.sigla_uf
                },
                "valor": _safe_float(getattr(indicador_obj, indicador))
            })

    posicao_especifica = None
    if municipio_id:
        for i, (indicador_obj, municipio_obj) in enumerate(all_results, 1):
            if municipio_obj.id_municipio == municipio_id:
                posicao_especifica = {
                    "municipio_id": municipio_id,
                    "posicao": i,
                    "total": len(all_results),
                    "valor": _safe_float(getattr(indicador_obj, indicador))
                }
                break

    return {
        "ano": ano,
        "indicador": indicador,
        "ranking": ranking,
        "posicao_especifica": posicao_especifica
    }

def get_evolucao_indicadores(db: Session, municipio_id: str) -> dict:
    municipio = get_municipio(db, municipio_id)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")

    query = db.query(models.IndicadoresDesempenhoAnual)\
        .filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)\
        .order_by(models.IndicadoresDesempenhoAnual.ano.asc()).all()
    
    evolucao = []
    for dado in query:
        evolucao.append({
            "ano": dado.ano,
            "indice_atendimento_agua": _safe_float(dado.indice_atendimento_agua),
            "indice_coleta_esgoto": _safe_float(dado.indice_coleta_esgoto),
            "indice_tratamento_esgoto": _safe_float(dado.indice_tratamento_esgoto)
        })
    
    return {"municipio": municipio, "indicadores": {"evolucao": evolucao}}


def get_indicadores_principais(db: Session, ano: Optional[int] = None) -> dict:
    if ano is None:
        ano = get_ultimo_ano_dados(db)
    
    if not ano:
        return {}

    medias = db.query(
        func.avg(models.IndicadoresDesempenhoAnual.indice_atendimento_agua).label("media_agua"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_coleta_esgoto).label("media_coleta"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_tratamento_esgoto).label("media_tratamento"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_perda_faturamento).label("media_perda")
    ).filter(models.IndicadoresDesempenhoAnual.ano == ano).first()
    
    return {
        "media_atendimento_agua": _safe_float(medias.media_agua),
        "media_coleta_esgoto": _safe_float(medias.media_coleta),
        "media_tratamento_esgoto": _safe_float(medias.media_tratamento),
        "media_perda_faturamento": _safe_float(medias.media_perda)
    }

def get_evolucao_temporal(db: Session) -> dict:
    dados = db.query(
        models.IndicadoresDesempenhoAnual.ano,
        func.avg(models.IndicadoresDesempenhoAnual.indice_atendimento_agua).label("agua"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_coleta_esgoto).label("coleta"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_tratamento_esgoto).label("tratamento")
    ).group_by(models.IndicadoresDesempenhoAnual.ano)\
     .order_by(models.IndicadoresDesempenhoAnual.ano.asc()).all()

    return {
        "anos": [d.ano for d in dados],
        "atendimento_agua": [_safe_float(d.agua) for d in dados],
        "coleta_esgoto": [_safe_float(d.coleta) for d in dados],
        "tratamento_esgoto": [_safe_float(d.tratamento) for d in dados]
    } 