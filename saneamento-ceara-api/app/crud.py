from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException
from app import models, schemas

# Funções para Municípios
def get_municipio(db: Session, id_municipio: str) -> Optional[models.Municipio]:
    return db.query(models.Municipio).filter(models.Municipio.id_municipio == id_municipio).first()

def get_municipios(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    nome: Optional[str] = None,
    microrregiao: Optional[str] = None
) -> List[models.Municipio]:
    query = db.query(models.Municipio)
    
    if nome:
        query = query.filter(models.Municipio.nome.ilike(f"%{nome}%"))
    if microrregiao:
        query = query.filter(models.Municipio.microrregiao == microrregiao)
    
    return query.offset(skip).limit(limit).all()

def create_municipio(db: Session, municipio: schemas.MunicipioCreate) -> models.Municipio:
    try:
        db_municipio = models.Municipio(**municipio.dict())
        db.add(db_municipio)
        db.commit()
        db.refresh(db_municipio)
        return db_municipio
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Município já existe")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar município: {str(e)}")

# Funções para Capitais
def get_capital(db: Session, municipio_id: str) -> Optional[models.Capital]:
    return db.query(models.Capital).filter(models.Capital.municipio_id == municipio_id).first()

def create_capital(db: Session, capital: schemas.CapitalCreate) -> models.Capital:
    try:
        db_capital = models.Capital(**capital.dict())
        db.add(db_capital)
        db.commit()
        db.refresh(db_capital)
        return db_capital
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Capital já existe para este município")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar capital: {str(e)}")

# Funções para Prestadores de Serviço
def get_prestador(db: Session, prestador_id: int) -> Optional[models.PrestadorServico]:
    return db.query(models.PrestadorServico).filter(models.PrestadorServico.id == prestador_id).first()

def get_prestador_by_sigla(db: Session, sigla: str) -> Optional[models.PrestadorServico]:
    return db.query(models.PrestadorServico).filter(models.PrestadorServico.sigla == sigla).first()

def create_prestador(db: Session, prestador: schemas.PrestadorServicoCreate) -> models.PrestadorServico:
    try:
        db_prestador = models.PrestadorServico(**prestador.dict())
        db.add(db_prestador)
        db.commit()
        db.refresh(db_prestador)
        return db_prestador
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Prestador de serviço já existe")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar prestador: {str(e)}")

# Funções para Dados de Saneamento
def get_dados_saneamento_municipio(
    db: Session, 
    municipio_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[models.DadosSaneamentoAnual]:
    return db.query(models.DadosSaneamentoAnual)\
        .filter(models.DadosSaneamentoAnual.municipio_id == municipio_id)\
        .order_by(models.DadosSaneamentoAnual.ano.desc())\
        .offset(skip).limit(limit).all()

def get_dados_saneamento_ano(
    db: Session,
    ano: int,
    municipio_id: Optional[str] = None
) -> List[models.DadosSaneamentoAnual]:
    query = db.query(models.DadosSaneamentoAnual).filter(models.DadosSaneamentoAnual.ano == ano)
    
    if municipio_id:
        query = query.filter(models.DadosSaneamentoAnual.municipio_id == municipio_id)
    
    return query.all()

def create_dados_saneamento(
    db: Session, 
    dados: schemas.DadosSaneamentoCreate
) -> models.DadosSaneamentoAnual:
    try:
        db_dados = models.DadosSaneamentoAnual(**dados.dict())
        db.add(db_dados)
        db.commit()
        db.refresh(db_dados)
        return db_dados
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Dados de saneamento já existem para este ano/município/prestador")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar dados de saneamento: {str(e)}")

# Funções para Rankings
def get_ranking_indicador(
    db: Session,
    ano: int,
    indicador: str,
    ordem: str = "desc",
    limit: int = 10
) -> List[dict]:
    """
    Retorna ranking dos municípios para um indicador específico
    """
    # Mapeamento de indicadores para colunas
    indicadores_map = {
        "indice_atendimento_agua": models.DadosSaneamentoAnual.indice_atendimento_agua,
        "indice_coleta_esgoto": models.DadosSaneamentoAnual.indice_coleta_esgoto,
        "indice_tratamento_esgoto": models.DadosSaneamentoAnual.indice_tratamento_esgoto,
        "indice_perda_faturamento": models.DadosSaneamentoAnual.indice_perda_faturamento,
        "volume_agua_produzido": models.DadosSaneamentoAnual.volume_agua_produzido,
        "volume_esgoto_tratado": models.DadosSaneamentoAnual.volume_esgoto_tratado,
        "receita_operacional_total": models.DadosSaneamentoAnual.receita_operacional_total,
        "investimento_total": models.DadosSaneamentoAnual.investimento_total
    }
    
    if indicador not in indicadores_map:
        raise ValueError(f"Indicador '{indicador}' não suportado")
    
    coluna = indicadores_map[indicador]
    order_func = desc if ordem.lower() == "desc" else asc
    
    query = db.query(
        models.Municipio,
        coluna.label('valor')
    ).join(
        models.DadosSaneamentoAnual,
        models.Municipio.id_municipio == models.DadosSaneamentoAnual.municipio_id
    ).filter(
        models.DadosSaneamentoAnual.ano == ano,
        coluna.isnot(None)
    ).order_by(
        order_func(coluna)
    ).limit(limit)
    
    results = query.all()
    
    ranking = []
    for i, (municipio, valor) in enumerate(results, 1):
        ranking.append({
            "posicao": i,
            "municipio": municipio,
            "valor": valor,
            "indicador": indicador
        })
    
    return ranking

# Funções para Evolução de Indicadores
def get_evolucao_indicadores(
    db: Session,
    municipio_id: str,
    indicadores: List[str]
) -> dict:
    """
    Retorna a evolução de múltiplos indicadores para um município
    """
    indicadores_map = {
        "indice_atendimento_agua": models.DadosSaneamentoAnual.indice_atendimento_agua,
        "indice_coleta_esgoto": models.DadosSaneamentoAnual.indice_coleta_esgoto,
        "indice_tratamento_esgoto": models.DadosSaneamentoAnual.indice_tratamento_esgoto,
        "indice_perda_faturamento": models.DadosSaneamentoAnual.indice_perda_faturamento,
        "volume_agua_produzido": models.DadosSaneamentoAnual.volume_agua_produzido,
        "volume_esgoto_tratado": models.DadosSaneamentoAnual.volume_esgoto_tratado,
        "receita_operacional_total": models.DadosSaneamentoAnual.receita_operacional_total,
        "investimento_total": models.DadosSaneamentoAnual.investimento_total
    }
    
    # Validar indicadores
    for indicador in indicadores:
        if indicador not in indicadores_map:
            raise ValueError(f"Indicador '{indicador}' não suportado")
    
    # Buscar dados do município
    dados = db.query(models.DadosSaneamentoAnual)\
        .filter(models.DadosSaneamentoAnual.municipio_id == municipio_id)\
        .order_by(models.DadosSaneamentoAnual.ano.asc())\
        .all()
    
    evolucao = {}
    for indicador in indicadores:
        evolucao[indicador] = []
        for dado in dados:
            valor = getattr(dado, indicador)
            if valor is not None:
                evolucao[indicador].append({
                    "ano": dado.ano,
                    "valor": valor
                })
    
    return evolucao

# Funções para Comparativo
def get_comparativo_municipios(
    db: Session,
    ano: int,
    ids_municipios: List[str]
) -> List[dict]:
    """
    Compara os dados de múltiplos municípios em um ano específico
    """
    dados = db.query(models.DadosSaneamentoAnual)\
        .join(models.Municipio)\
        .filter(
            models.DadosSaneamentoAnual.ano == ano,
            models.DadosSaneamentoAnual.municipio_id.in_(ids_municipios)
        ).all()
    
    comparativo = []
    for dado in dados:
        comparativo.append({
            "municipio": dado.municipio,
            "dados": dado
        })
    
    return comparativo

# Funções para Sustentabilidade Financeira
def get_sustentabilidade_financeira(
    db: Session,
    ano: int
) -> dict:
    """
    Retorna municípios com receita > despesa e os que têm despesa > receita
    """
    dados = db.query(
        models.Municipio,
        models.DadosSaneamentoAnual.receita_operacional_total,
        models.DadosSaneamentoAnual.despesa_total_servicos
    ).join(
        models.DadosSaneamentoAnual,
        models.Municipio.id_municipio == models.DadosSaneamentoAnual.municipio_id
    ).filter(
        models.DadosSaneamentoAnual.ano == ano,
        models.DadosSaneamentoAnual.receita_operacional_total.isnot(None),
        models.DadosSaneamentoAnual.despesa_total_servicos.isnot(None)
    ).all()
    
    sustentaveis = []
    insustentaveis = []
    
    for municipio, receita, despesa in dados:
        saldo = receita - despesa
        sustentavel = receita > despesa
        
        item = {
            "municipio": municipio,
            "receita": receita,
            "despesa": despesa,
            "saldo": saldo,
            "sustentavel": sustentavel
        }
        
        if sustentavel:
            sustentaveis.append(item)
        else:
            insustentaveis.append(item)
    
    return {
        "sustentaveis": sustentaveis,
        "insustentaveis": insustentaveis
    } 