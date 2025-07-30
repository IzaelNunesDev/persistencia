from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, asc
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException
from app import models, schemas
from app.logging_config import get_logger, log_database_operation
import math
import time

logger = get_logger(__name__)

def _log_db_operation(operation: str, table: str, start_time: float, success: bool = True, error: str = None):
    """Helper para log de operações de banco de dados"""
    duration = time.time() - start_time
    log_database_operation(operation, table, duration, success)
    if error:
        logger.error(f"DB {operation} on {table} failed: {error}")

# Funções para Municípios
def get_municipio(db: Session, id_municipio: str) -> Optional[models.Municipio]:
    start_time = time.time()
    try:
        result = db.query(models.Municipio).filter(models.Municipio.id_municipio == id_municipio).first()
        _log_db_operation("SELECT", "municipios", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "municipios", start_time, success=False, error=str(e))
        raise

def get_municipios(
    db: Session, 
    skip: int = 0, 
    limit: int = 200, 
    nome: Optional[str] = None,
    populacao_min: Optional[int] = None,
    populacao_max: Optional[int] = None,
    order_by: Optional[str] = None,
    order_direction: str = "asc"
) -> List[models.Municipio]:
    start_time = time.time()
    try:
        query = db.query(models.Municipio)
        
        if nome:
            query = query.filter(models.Municipio.nome.ilike(f"%{nome}%"))
        if populacao_min is not None:
            query = query.filter(models.Municipio.populacao_total_estimada_2022 >= populacao_min)
        if populacao_max is not None:
            query = query.filter(models.Municipio.populacao_total_estimada_2022 <= populacao_max)

        # Ordenação
        if order_by:
            if hasattr(models.Municipio, order_by):
                if order_direction == "desc":
                    query = query.order_by(desc(getattr(models.Municipio, order_by)))
                else:
                    query = query.order_by(asc(getattr(models.Municipio, order_by)))
            else:
                # Ordenação padrão se o campo não existir
                query = query.order_by(models.Municipio.nome)
        else:
            query = query.order_by(models.Municipio.nome)

        result = query.offset(skip).limit(limit).all()
        _log_db_operation("SELECT", "municipios", start_time, success=True)
        logger.info(f"Retrieved {len(result)} municipalities (skip={skip}, limit={limit})")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "municipios", start_time, success=False, error=str(e))
        raise

def create_municipio(db: Session, municipio: schemas.MunicipioCreate) -> models.Municipio:
    start_time = time.time()
    try:
        db_municipio = models.Municipio(**municipio.dict())
        db.add(db_municipio)
        db.commit()
        db.refresh(db_municipio)
        _log_db_operation("INSERT", "municipios", start_time, success=True)
        logger.info(f"Created municipality: {db_municipio.nome} ({db_municipio.id_municipio})")
        return db_municipio
    except Exception as e:
        db.rollback()
        _log_db_operation("INSERT", "municipios", start_time, success=False, error=str(e))
        raise

def update_municipio(db: Session, id_municipio: str, municipio: schemas.MunicipioUpdate) -> Optional[models.Municipio]:
    start_time = time.time()
    try:
        db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == id_municipio).first()
        if db_municipio:
            update_data = municipio.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_municipio, field, value)
            db.add(db_municipio)
            db.commit()
            db.refresh(db_municipio)
            _log_db_operation("UPDATE", "municipios", start_time, success=True)
            logger.info(f"Updated municipality: {db_municipio.nome} ({id_municipio})")
        return db_municipio
    except Exception as e:
        db.rollback()
        _log_db_operation("UPDATE", "municipios", start_time, success=False, error=str(e))
        raise

def delete_municipio(db: Session, id_municipio: str) -> bool:
    start_time = time.time()
    try:
        db_municipio = db.query(models.Municipio).filter(models.Municipio.id_municipio == id_municipio).first()
        if db_municipio:
            db.delete(db_municipio)
            db.commit()
            _log_db_operation("DELETE", "municipios", start_time, success=True)
            logger.info(f"Deleted municipality: {db_municipio.nome} ({id_municipio})")
            return True
        return False
    except Exception as e:
        db.rollback()
        _log_db_operation("DELETE", "municipios", start_time, success=False, error=str(e))
        raise

# Funções para Prestadores de Serviço
def get_prestador(db: Session, prestador_id: int) -> Optional[models.PrestadorServico]:
    start_time = time.time()
    try:
        result = db.query(models.PrestadorServico).filter(models.PrestadorServico.id == prestador_id).first()
        _log_db_operation("SELECT", "prestadores_servico", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "prestadores_servico", start_time, success=False, error=str(e))
        raise

def get_prestador_by_sigla(db: Session, sigla: str) -> Optional[models.PrestadorServico]:
    start_time = time.time()
    try:
        result = db.query(models.PrestadorServico).filter(models.PrestadorServico.sigla == sigla).first()
        _log_db_operation("SELECT", "prestadores_servico", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "prestadores_servico", start_time, success=False, error=str(e))
        raise

def get_prestadores(
    db: Session, 
    skip: int = 0, 
    limit: int = 200,
    nome: Optional[str] = None,
    sigla: Optional[str] = None,
    natureza_juridica: Optional[str] = None,
    order_by: Optional[str] = None,
    order_direction: str = "asc"
) -> List[models.PrestadorServico]:
    start_time = time.time()
    try:
        query = db.query(models.PrestadorServico)
        
        if nome:
            query = query.filter(models.PrestadorServico.nome.ilike(f"%{nome}%"))
        if sigla:
            query = query.filter(models.PrestadorServico.sigla.ilike(f"%{sigla}%"))
        if natureza_juridica:
            query = query.filter(models.PrestadorServico.natureza_juridica.ilike(f"%{natureza_juridica}%"))

        # Ordenação
        if order_by:
            if hasattr(models.PrestadorServico, order_by):
                if order_direction == "desc":
                    query = query.order_by(desc(getattr(models.PrestadorServico, order_by)))
                else:
                    query = query.order_by(asc(getattr(models.PrestadorServico, order_by)))
            else:
                query = query.order_by(models.PrestadorServico.nome)
        else:
            query = query.order_by(models.PrestadorServico.nome)

        result = query.offset(skip).limit(limit).all()
        _log_db_operation("SELECT", "prestadores_servico", start_time, success=True)
        logger.info(f"Retrieved {len(result)} service providers (skip={skip}, limit={limit})")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "prestadores_servico", start_time, success=False, error=str(e))
        raise

def create_prestador(db: Session, prestador: schemas.PrestadorServicoCreate) -> models.PrestadorServico:
    start_time = time.time()
    try:
        db_prestador = models.PrestadorServico(**prestador.dict())
        db.add(db_prestador)
        db.commit()
        db.refresh(db_prestador)
        _log_db_operation("INSERT", "prestadores_servico", start_time, success=True)
        logger.info(f"Created service provider: {db_prestador.nome} ({db_prestador.sigla})")
        return db_prestador
    except Exception as e:
        db.rollback()
        _log_db_operation("INSERT", "prestadores_servico", start_time, success=False, error=str(e))
        raise

def update_prestador(db: Session, prestador_id: int, prestador: schemas.PrestadorServicoUpdate) -> Optional[models.PrestadorServico]:
    start_time = time.time()
    try:
        db_prestador = db.query(models.PrestadorServico).filter(models.PrestadorServico.id == prestador_id).first()
        if db_prestador:
            update_data = prestador.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_prestador, field, value)
            db.add(db_prestador)
            db.commit()
            db.refresh(db_prestador)
            _log_db_operation("UPDATE", "prestadores_servico", start_time, success=True)
            logger.info(f"Updated service provider: {db_prestador.nome} (ID: {prestador_id})")
        return db_prestador
    except Exception as e:
        db.rollback()
        _log_db_operation("UPDATE", "prestadores_servico", start_time, success=False, error=str(e))
        raise

def delete_prestador(db: Session, prestador_id: int) -> bool:
    start_time = time.time()
    try:
        db_prestador = db.query(models.PrestadorServico).filter(models.PrestadorServico.id == prestador_id).first()
        if db_prestador:
            db.delete(db_prestador)
            db.commit()
            _log_db_operation("DELETE", "prestadores_servico", start_time, success=True)
            logger.info(f"Deleted service provider: {db_prestador.nome} (ID: {prestador_id})")
            return True
        return False
    except Exception as e:
        db.rollback()
        _log_db_operation("DELETE", "prestadores_servico", start_time, success=False, error=str(e))
        raise

# Funções para Indicadores de Desempenho
def get_indicador(db: Session, indicador_id: int) -> Optional[models.IndicadoresDesempenhoAnual]:
    start_time = time.time()
    try:
        result = db.query(models.IndicadoresDesempenhoAnual)\
            .options(
                joinedload(models.IndicadoresDesempenhoAnual.municipio),
                joinedload(models.IndicadoresDesempenhoAnual.prestador),
                joinedload(models.IndicadoresDesempenhoAnual.recursos_hidricos),
                joinedload(models.IndicadoresDesempenhoAnual.financeiro)
            )\
            .filter(models.IndicadoresDesempenhoAnual.id == indicador_id).first()
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def get_indicadores(
    db: Session,
    skip: int = 0,
    limit: int = 200,
    ano_inicio: Optional[int] = None,
    ano_fim: Optional[int] = None,
    municipio_id: Optional[str] = None,
    prestador_id: Optional[int] = None,
    order_by: Optional[str] = None,
    order_direction: str = "asc"
) -> List[models.IndicadoresDesempenhoAnual]:
    start_time = time.time()
    try:
        query = db.query(models.IndicadoresDesempenhoAnual)\
            .options(
                joinedload(models.IndicadoresDesempenhoAnual.municipio),
                joinedload(models.IndicadoresDesempenhoAnual.prestador)
            )
        
        if ano_inicio is not None:
            query = query.filter(models.IndicadoresDesempenhoAnual.ano >= ano_inicio)
        if ano_fim is not None:
            query = query.filter(models.IndicadoresDesempenhoAnual.ano <= ano_fim)
        if municipio_id:
            query = query.filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)
        if prestador_id:
            query = query.filter(models.IndicadoresDesempenhoAnual.prestador_id == prestador_id)

        # Ordenação
        if order_by:
            if hasattr(models.IndicadoresDesempenhoAnual, order_by):
                if order_direction == "desc":
                    query = query.order_by(desc(getattr(models.IndicadoresDesempenhoAnual, order_by)))
                else:
                    query = query.order_by(asc(getattr(models.IndicadoresDesempenhoAnual, order_by)))
            else:
                query = query.order_by(models.IndicadoresDesempenhoAnual.ano.desc())
        else:
            query = query.order_by(models.IndicadoresDesempenhoAnual.ano.desc())

        result = query.offset(skip).limit(limit).all()
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        logger.info(f"Retrieved {len(result)} performance indicators (skip={skip}, limit={limit})")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def get_indicadores_municipio(db: Session, municipio_id: str) -> List[models.IndicadoresDesempenhoAnual]:
    """
    Busca indicadores anuais de um município, fazendo o carregamento
    ansioso (eager loading) das tabelas relacionadas para otimização.
    """
    start_time = time.time()
    try:
        result = db.query(models.IndicadoresDesempenhoAnual)\
            .options(
                joinedload(models.IndicadoresDesempenhoAnual.recursos_hidricos),
                joinedload(models.IndicadoresDesempenhoAnual.financeiro)
            )\
            .filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)\
            .order_by(models.IndicadoresDesempenhoAnual.ano.desc()).all()
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        logger.info(f"Retrieved {len(result)} indicators for municipality {municipio_id}")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def create_indicadores(db: Session, indicadores: schemas.IndicadoresDesempenhoCreate) -> models.IndicadoresDesempenhoAnual:
    start_time = time.time()
    try:
        db_indicadores = models.IndicadoresDesempenhoAnual(**indicadores.dict())
        db.add(db_indicadores)
        db.commit()
        db.refresh(db_indicadores)
        _log_db_operation("INSERT", "indicadores_desempenho_anuais", start_time, success=True)
        logger.info(f"Created performance indicator: ID {db_indicadores.id} for municipality {db_indicadores.municipio_id}")
        return db_indicadores
    except Exception as e:
        db.rollback()
        _log_db_operation("INSERT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def update_indicadores(db: Session, indicador_id: int, indicadores: schemas.IndicadoresDesempenhoUpdate) -> Optional[models.IndicadoresDesempenhoAnual]:
    start_time = time.time()
    try:
        db_indicadores = db.query(models.IndicadoresDesempenhoAnual).filter(models.IndicadoresDesempenhoAnual.id == indicador_id).first()
        if db_indicadores:
            update_data = indicadores.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_indicadores, field, value)
            db.add(db_indicadores)
            db.commit()
            db.refresh(db_indicadores)
            _log_db_operation("UPDATE", "indicadores_desempenho_anuais", start_time, success=True)
            logger.info(f"Updated performance indicator: ID {indicador_id}")
        return db_indicadores
    except Exception as e:
        db.rollback()
        _log_db_operation("UPDATE", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def delete_indicadores(db: Session, indicador_id: int) -> bool:
    start_time = time.time()
    try:
        db_indicadores = db.query(models.IndicadoresDesempenhoAnual).filter(models.IndicadoresDesempenhoAnual.id == indicador_id).first()
        if db_indicadores:
            db.delete(db_indicadores)
            db.commit()
            _log_db_operation("DELETE", "indicadores_desempenho_anuais", start_time, success=True)
            logger.info(f"Deleted performance indicator: ID {indicador_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        _log_db_operation("DELETE", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

# Funções para Recursos Hídricos
def get_recursos_hidricos(db: Session, recursos_id: int) -> Optional[models.RecursosHidricosAnual]:
    start_time = time.time()
    try:
        result = db.query(models.RecursosHidricosAnual).filter(models.RecursosHidricosAnual.id == recursos_id).first()
        _log_db_operation("SELECT", "recursos_hidricos_anuais", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "recursos_hidricos_anuais", start_time, success=False, error=str(e))
        raise

def get_recursos_hidricos_by_indicador(db: Session, indicador_id: int) -> Optional[models.RecursosHidricosAnual]:
    start_time = time.time()
    try:
        result = db.query(models.RecursosHidricosAnual).filter(models.RecursosHidricosAnual.indicador_id == indicador_id).first()
        _log_db_operation("SELECT", "recursos_hidricos_anuais", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "recursos_hidricos_anuais", start_time, success=False, error=str(e))
        raise

def get_recursos_hidricos_list(
    db: Session,
    skip: int = 0,
    limit: int = 200,
    indicador_id: Optional[int] = None,
    volume_min: Optional[float] = None,
    volume_max: Optional[float] = None,
    order_by: Optional[str] = None,
    order_direction: str = "asc"
) -> List[models.RecursosHidricosAnual]:
    start_time = time.time()
    try:
        query = db.query(models.RecursosHidricosAnual)
        
        if indicador_id:
            query = query.filter(models.RecursosHidricosAnual.indicador_id == indicador_id)
        if volume_min is not None:
            query = query.filter(models.RecursosHidricosAnual.volume_agua_produzido >= volume_min)
        if volume_max is not None:
            query = query.filter(models.RecursosHidricosAnual.volume_agua_produzido <= volume_max)

        # Ordenação
        if order_by:
            if hasattr(models.RecursosHidricosAnual, order_by):
                if order_direction == "desc":
                    query = query.order_by(desc(getattr(models.RecursosHidricosAnual, order_by)))
                else:
                    query = query.order_by(asc(getattr(models.RecursosHidricosAnual, order_by)))
            else:
                query = query.order_by(models.RecursosHidricosAnual.id)
        else:
            query = query.order_by(models.RecursosHidricosAnual.id)

        result = query.offset(skip).limit(limit).all()
        _log_db_operation("SELECT", "recursos_hidricos_anuais", start_time, success=True)
        logger.info(f"Retrieved {len(result)} water resources records (skip={skip}, limit={limit})")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "recursos_hidricos_anuais", start_time, success=False, error=str(e))
        raise

def create_recursos_hidricos(db: Session, recursos: schemas.RecursosHidricosCreate) -> models.RecursosHidricosAnual:
    start_time = time.time()
    try:
        db_recursos = models.RecursosHidricosAnual(**recursos.dict())
        db.add(db_recursos)
        db.commit()
        db.refresh(db_recursos)
        _log_db_operation("INSERT", "recursos_hidricos_anuais", start_time, success=True)
        logger.info(f"Created water resources record: ID {db_recursos.id} for indicator {db_recursos.indicador_id}")
        return db_recursos
    except Exception as e:
        db.rollback()
        _log_db_operation("INSERT", "recursos_hidricos_anuais", start_time, success=False, error=str(e))
        raise

def update_recursos_hidricos(db: Session, recursos_id: int, recursos: schemas.RecursosHidricosUpdate) -> Optional[models.RecursosHidricosAnual]:
    start_time = time.time()
    try:
        db_recursos = db.query(models.RecursosHidricosAnual).filter(models.RecursosHidricosAnual.id == recursos_id).first()
        if db_recursos:
            update_data = recursos.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_recursos, field, value)
            db.add(db_recursos)
            db.commit()
            db.refresh(db_recursos)
            _log_db_operation("UPDATE", "recursos_hidricos_anuais", start_time, success=True)
            logger.info(f"Updated water resources record: ID {recursos_id}")
        return db_recursos
    except Exception as e:
        db.rollback()
        _log_db_operation("UPDATE", "recursos_hidricos_anuais", start_time, success=False, error=str(e))
        raise

def delete_recursos_hidricos(db: Session, recursos_id: int) -> bool:
    start_time = time.time()
    try:
        db_recursos = db.query(models.RecursosHidricosAnual).filter(models.RecursosHidricosAnual.id == recursos_id).first()
        if db_recursos:
            db.delete(db_recursos)
            db.commit()
            _log_db_operation("DELETE", "recursos_hidricos_anuais", start_time, success=True)
            logger.info(f"Deleted water resources record: ID {recursos_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        _log_db_operation("DELETE", "recursos_hidricos_anuais", start_time, success=False, error=str(e))
        raise

# Funções para Financeiro
def get_financeiro(db: Session, financeiro_id: int) -> Optional[models.FinanceiroAnual]:
    start_time = time.time()
    try:
        result = db.query(models.FinanceiroAnual).filter(models.FinanceiroAnual.id == financeiro_id).first()
        _log_db_operation("SELECT", "financeiro_anuais", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "financeiro_anuais", start_time, success=False, error=str(e))
        raise

def get_financeiro_by_indicador(db: Session, indicador_id: int) -> Optional[models.FinanceiroAnual]:
    start_time = time.time()
    try:
        result = db.query(models.FinanceiroAnual).filter(models.FinanceiroAnual.indicador_id == indicador_id).first()
        _log_db_operation("SELECT", "financeiro_anuais", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "financeiro_anuais", start_time, success=False, error=str(e))
        raise

def get_financeiro_list(
    db: Session,
    skip: int = 0,
    limit: int = 200,
    indicador_id: Optional[int] = None,
    receita_min: Optional[float] = None,
    receita_max: Optional[float] = None,
    order_by: Optional[str] = None,
    order_direction: str = "asc"
) -> List[models.FinanceiroAnual]:
    start_time = time.time()
    try:
        query = db.query(models.FinanceiroAnual)
        
        if indicador_id:
            query = query.filter(models.FinanceiroAnual.indicador_id == indicador_id)
        if receita_min is not None:
            query = query.filter(models.FinanceiroAnual.receita_operacional_total >= receita_min)
        if receita_max is not None:
            query = query.filter(models.FinanceiroAnual.receita_operacional_total <= receita_max)

        # Ordenação
        if order_by:
            if hasattr(models.FinanceiroAnual, order_by):
                if order_direction == "desc":
                    query = query.order_by(desc(getattr(models.FinanceiroAnual, order_by)))
                else:
                    query = query.order_by(asc(getattr(models.FinanceiroAnual, order_by)))
            else:
                query = query.order_by(models.FinanceiroAnual.id)
        else:
            query = query.order_by(models.FinanceiroAnual.id)

        result = query.offset(skip).limit(limit).all()
        _log_db_operation("SELECT", "financeiro_anuais", start_time, success=True)
        logger.info(f"Retrieved {len(result)} financial records (skip={skip}, limit={limit})")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "financeiro_anuais", start_time, success=False, error=str(e))
        raise

def create_financeiro(db: Session, financeiro: schemas.FinanceiroCreate) -> models.FinanceiroAnual:
    start_time = time.time()
    try:
        db_financeiro = models.FinanceiroAnual(**financeiro.dict())
        db.add(db_financeiro)
        db.commit()
        db.refresh(db_financeiro)
        _log_db_operation("INSERT", "financeiro_anuais", start_time, success=True)
        logger.info(f"Created financial record: ID {db_financeiro.id} for indicator {db_financeiro.indicador_id}")
        return db_financeiro
    except Exception as e:
        db.rollback()
        _log_db_operation("INSERT", "financeiro_anuais", start_time, success=False, error=str(e))
        raise

def update_financeiro(db: Session, financeiro_id: int, financeiro: schemas.FinanceiroUpdate) -> Optional[models.FinanceiroAnual]:
    start_time = time.time()
    try:
        db_financeiro = db.query(models.FinanceiroAnual).filter(models.FinanceiroAnual.id == financeiro_id).first()
        if db_financeiro:
            update_data = financeiro.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_financeiro, field, value)
            db.add(db_financeiro)
            db.commit()
            db.refresh(db_financeiro)
            _log_db_operation("UPDATE", "financeiro_anuais", start_time, success=True)
            logger.info(f"Updated financial record: ID {financeiro_id}")
        return db_financeiro
    except Exception as e:
        db.rollback()
        _log_db_operation("UPDATE", "financeiro_anuais", start_time, success=False, error=str(e))
        raise

def delete_financeiro(db: Session, financeiro_id: int) -> bool:
    start_time = time.time()
    try:
        db_financeiro = db.query(models.FinanceiroAnual).filter(models.FinanceiroAnual.id == financeiro_id).first()
        if db_financeiro:
            db.delete(db_financeiro)
            db.commit()
            _log_db_operation("DELETE", "financeiro_anuais", start_time, success=True)
            logger.info(f"Deleted financial record: ID {financeiro_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        _log_db_operation("DELETE", "financeiro_anuais", start_time, success=False, error=str(e))
        raise

# Funções de Análise (mantidas do código original)
def get_ultimo_ano_dados(db: Session) -> int:
    start_time = time.time()
    try:
        result = db.query(func.max(models.IndicadoresDesempenhoAnual.ano)).scalar() or 2022
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        return result
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def _safe_float(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return float(value)

def get_ranking_indicador(db: Session, ano: int, indicador: str, ordem: str, limit: int, municipio_id: Optional[str]) -> dict:
    start_time = time.time()
    try:
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

        result = {
            "ano": ano,
            "indicador": indicador,
            "ranking": ranking,
            "posicao_especifica": posicao_especifica
        }
        
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        logger.info(f"Generated ranking for {indicador} in {ano}: {len(ranking)} municipalities")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def get_evolucao_indicadores(db: Session, municipio_id: str, indicadores: Optional[List[str]] = None) -> dict:
    start_time = time.time()
    try:
        municipio = get_municipio(db, municipio_id)
        if not municipio:
            raise HTTPException(status_code=404, detail="Município não encontrado")

        query = db.query(models.IndicadoresDesempenhoAnual)\
            .filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)\
            .order_by(models.IndicadoresDesempenhoAnual.ano.asc()).all()
        
        # Definir indicadores padrão se não especificados
        if indicadores is None:
            indicadores = ["indice_atendimento_agua", "indice_coleta_esgoto", "indice_tratamento_esgoto", "indice_perda_faturamento"]
        
        # Criar estrutura de dados para cada indicador
        evolucao_por_indicador = {}
        for indicador in indicadores:
            evolucao_por_indicador[indicador] = []
        
        # Processar dados
        for dado in query:
            for indicador in indicadores:
                if hasattr(dado, indicador):
                    valor = _safe_float(getattr(dado, indicador))
                    evolucao_por_indicador[indicador].append({
                        "ano": dado.ano,
                        "valor": valor
                    })
        
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        logger.info(f"Generated evolution data for municipality {municipio_id}: {len(query)} years, {len(indicadores)} indicators")
        return evolucao_por_indicador
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def get_indicadores_principais(db: Session, ano: Optional[int] = None) -> dict:
    start_time = time.time()
    try:
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
        
        result = {
            "media_atendimento_agua": _safe_float(medias.media_agua),
            "media_coleta_esgoto": _safe_float(medias.media_coleta),
            "media_tratamento_esgoto": _safe_float(medias.media_tratamento),
            "media_perda_faturamento": _safe_float(medias.media_perda)
        }
        
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        logger.info(f"Calculated main indicators for year {ano}")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise

def get_evolucao_temporal(db: Session) -> dict:
    start_time = time.time()
    try:
        dados = db.query(
            models.IndicadoresDesempenhoAnual.ano,
            func.avg(models.IndicadoresDesempenhoAnual.indice_atendimento_agua).label("agua"),
            func.avg(models.IndicadoresDesempenhoAnual.indice_coleta_esgoto).label("coleta"),
            func.avg(models.IndicadoresDesempenhoAnual.indice_tratamento_esgoto).label("tratamento")
        ).group_by(models.IndicadoresDesempenhoAnual.ano)\
         .order_by(models.IndicadoresDesempenhoAnual.ano.asc()).all()

        result = {
            "anos": [d.ano for d in dados],
            "atendimento_agua": [_safe_float(d.agua) for d in dados],
            "coleta_esgoto": [_safe_float(d.coleta) for d in dados],
            "tratamento_esgoto": [_safe_float(d.tratamento) for d in dados]
        }
        
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=True)
        logger.info(f"Generated temporal evolution data: {len(dados)} years")
        return result
    except Exception as e:
        _log_db_operation("SELECT", "indicadores_desempenho_anuais", start_time, success=False, error=str(e))
        raise 