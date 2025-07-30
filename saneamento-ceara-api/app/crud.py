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
    nome: Optional[str] = None
) -> List[models.Municipio]:
    query = db.query(models.Municipio)
    
    if nome:
        query = query.filter(models.Municipio.nome.ilike(f"%{nome}%"))
    
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

# Funções para Prestadores de Serviço
def get_prestador(db: Session, prestador_id: int) -> Optional[models.PrestadorServico]:
    return db.query(models.PrestadorServico).filter(models.PrestadorServico.id == prestador_id).first()

def get_prestador_by_sigla(db: Session, sigla: str) -> Optional[models.PrestadorServico]:
    return db.query(models.PrestadorServico).filter(models.PrestadorServico.sigla == sigla).first()

def get_prestadores(db: Session, skip: int = 0, limit: int = 100) -> List[models.PrestadorServico]:
    return db.query(models.PrestadorServico).offset(skip).limit(limit).all()

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

# Funções para Indicadores de Desempenho Anual
def get_indicadores_municipio(
    db: Session, 
    municipio_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[models.IndicadoresDesempenhoAnual]:
    return db.query(models.IndicadoresDesempenhoAnual)\
        .filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)\
        .order_by(models.IndicadoresDesempenhoAnual.ano.desc())\
        .offset(skip).limit(limit).all()

def get_indicadores_ano(
    db: Session,
    ano: int,
    municipio_id: Optional[str] = None
) -> List[models.IndicadoresDesempenhoAnual]:
    query = db.query(models.IndicadoresDesempenhoAnual).filter(models.IndicadoresDesempenhoAnual.ano == ano)
    
    if municipio_id:
        query = query.filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)
    
    return query.all()

def get_indicador_atual_municipio(db: Session, municipio_id: str) -> Optional[models.IndicadoresDesempenhoAnual]:
    return db.query(models.IndicadoresDesempenhoAnual)\
        .filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)\
        .order_by(models.IndicadoresDesempenhoAnual.ano.desc())\
        .first()

def create_indicadores(db: Session, indicadores: schemas.IndicadoresDesempenhoCreate) -> models.IndicadoresDesempenhoAnual:
    try:
        db_indicadores = models.IndicadoresDesempenhoAnual(**indicadores.dict())
        db.add(db_indicadores)
        db.commit()
        db.refresh(db_indicadores)
        return db_indicadores
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Indicadores já existem para este município/ano/prestador")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar indicadores: {str(e)}")

# Funções para Recursos Hídricos Anual
def get_recursos_hidricos(db: Session, indicador_id: int) -> Optional[models.RecursosHidricosAnual]:
    return db.query(models.RecursosHidricosAnual)\
        .filter(models.RecursosHidricosAnual.indicador_id == indicador_id).first()

def create_recursos_hidricos(db: Session, recursos: schemas.RecursosHidricosCreate) -> models.RecursosHidricosAnual:
    try:
        db_recursos = models.RecursosHidricosAnual(**recursos.dict())
        db.add(db_recursos)
        db.commit()
        db.refresh(db_recursos)
        return db_recursos
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Recursos hídricos já existem para este indicador")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar recursos hídricos: {str(e)}")

# Funções para Financeiro Anual
def get_financeiro(db: Session, indicador_id: int) -> Optional[models.FinanceiroAnual]:
    return db.query(models.FinanceiroAnual)\
        .filter(models.FinanceiroAnual.indicador_id == indicador_id).first()

def create_financeiro(db: Session, financeiro: schemas.FinanceiroCreate) -> models.FinanceiroAnual:
    try:
        db_financeiro = models.FinanceiroAnual(**financeiro.dict())
        db.add(db_financeiro)
        db.commit()
        db.refresh(db_financeiro)
        return db_financeiro
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Dados financeiros já existem para este indicador")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar dados financeiros: {str(e)}")

# Funções de análise e relatórios
def get_ranking_indicador(
    db: Session,
    ano: int,
    indicador: str,
    ordem: str = "desc",
    limit: int = 10,
    municipio_id: Optional[str] = None
) -> dict:
    """
    Retorna ranking de municípios por indicador específico
    """
    import math  # Importar math para verificar NaN
    
    # Mapear nome do indicador para coluna
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
        models.IndicadoresDesempenhoAnual,
        models.Municipio
    ).join(models.Municipio).filter(
        models.IndicadoresDesempenhoAnual.ano == ano,
        coluna.isnot(None)
    ).order_by(order_func(coluna))
    
    if municipio_id:
        # CORREÇÃO: Em vez de retornar um formato diferente,
        # vamos encontrar a posição e ainda retornar o ranking completo.
        # Isso é mais útil para o frontend de qualquer maneira.

        # Primeiro, pegamos o ranking completo sem limite
        todos_os_resultados = query.all()
        
        posicao_municipio = None
        valor_municipio = None
        
        # Montar ranking e encontrar o município alvo
        ranking = []
        for i, (indicador_obj, municipio_obj) in enumerate(todos_os_resultados, 1):
            valor = indicador_obj.__getattribute__(indicador)
            valor_limpo = None if valor is None or math.isnan(valor) else float(valor)
            
            # Adicionar ao ranking geral (os 10 primeiros)
            if i <= limit:
                ranking.append({
                    "posicao": i,
                    "municipio": {
                        "id_municipio": municipio_obj.id_municipio,
                        "nome": municipio_obj.nome,
                        "sigla_uf": municipio_obj.sigla_uf
                    },
                    "valor": valor_limpo
                })

            # Verificar se é o município que estamos procurando
            if municipio_obj.id_municipio == municipio_id:
                posicao_municipio = i
                valor_municipio = valor_limpo
        
        # Retornar o ranking e a posição do município específico
        return {
            "ano": ano,
            "indicador": indicador,
            "ranking": ranking,  # Retorna o Top 10
            "posicao_especifica": {  # Adiciona uma chave extra com a info
                "municipio_id": municipio_id,
                "posicao": posicao_municipio,
                "total": len(todos_os_resultados),
                "valor": valor_municipio
            }
        }
    
    # Retornar ranking completo
    resultados = query.limit(limit).all()
    
    ranking = []
    for i, (indicador_obj, municipio) in enumerate(resultados, 1):
        valor = indicador_obj.__getattribute__(indicador)
        
        # CORREÇÃO: Tratar NaN e None antes de adicionar
        if valor is None or math.isnan(valor):
            valor_limpo = None  # JSON suporta 'null'
        else:
            valor_limpo = float(valor)
        
        ranking.append({
            "posicao": i,
            "municipio": {
                "id_municipio": municipio.id_municipio,
                "nome": municipio.nome,
                "sigla_uf": municipio.sigla_uf
            },
            "valor": valor_limpo  # Usar o valor limpo
        })
    
    return {
        "ano": ano,
        "indicador": indicador,
        "ranking": ranking
    }

def get_evolucao_indicadores(
    db: Session,
    municipio_id: str,
    indicadores: List[str] = None
) -> dict:
    """
    Retorna evolução temporal dos indicadores de um município
    """
    import math
    
    if indicadores is None:
        indicadores = ["indice_atendimento_agua", "indice_coleta_esgoto", "indice_tratamento_esgoto"]
    
    query = db.query(models.IndicadoresDesempenhoAnual)\
        .filter(models.IndicadoresDesempenhoAnual.municipio_id == municipio_id)\
        .order_by(models.IndicadoresDesempenhoAnual.ano.asc())
    
    dados = query.all()
    
    evolucao = []
    for dado in dados:
        item = {"ano": dado.ano}
        for indicador in indicadores:
            valor = getattr(dado, indicador)
            # CORREÇÃO: Tratar valores None e NaN
            if valor is None or math.isnan(valor):
                item[indicador] = None
            else:
                item[indicador] = float(valor)
        evolucao.append(item)
    
    return {
        "municipio_id": municipio_id,
        "evolucao": evolucao
    }

def get_indicadores_principais(db: Session, ano: int = None) -> dict:
    """
    Retorna médias dos indicadores principais
    """
    import math
    
    if ano is None:
        # Usar ano mais recente
        ano = db.query(func.max(models.IndicadoresDesempenhoAnual.ano)).scalar()
    
    if not ano:
        return {
            "media_atendimento_agua": 0,
            "media_coleta_esgoto": 0,
            "media_tratamento_esgoto": 0,
            "media_perda_faturamento": 0
        }
    
    medias = db.query(
        func.avg(models.IndicadoresDesempenhoAnual.indice_atendimento_agua).label("media_agua"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_coleta_esgoto).label("media_coleta"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_tratamento_esgoto).label("media_tratamento"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_perda_faturamento).label("media_perda")
    ).filter(models.IndicadoresDesempenhoAnual.ano == ano).first()
    
    # Tratar valores None e NaN
    def safe_float(value):
        if value is None or math.isnan(value):
            return None
        return float(value)
    
    return {
        "media_atendimento_agua": safe_float(medias.media_agua),
        "media_coleta_esgoto": safe_float(medias.media_coleta),
        "media_tratamento_esgoto": safe_float(medias.media_tratamento),
        "media_perda_faturamento": safe_float(medias.media_perda)
    }

def get_evolucao_temporal(db: Session) -> dict:
    """
    Retorna evolução temporal dos indicadores médios
    """
    import math
    
    dados = db.query(
        models.IndicadoresDesempenhoAnual.ano,
        func.avg(models.IndicadoresDesempenhoAnual.indice_atendimento_agua).label("agua"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_coleta_esgoto).label("coleta"),
        func.avg(models.IndicadoresDesempenhoAnual.indice_tratamento_esgoto).label("tratamento")
    ).group_by(models.IndicadoresDesempenhoAnual.ano)\
     .order_by(models.IndicadoresDesempenhoAnual.ano.asc()).all()
    
    anos = []
    agua = []
    coleta = []
    tratamento = []
    
    for dado in dados:
        anos.append(dado.ano)
        
        # CORREÇÃO: Tratar valores None e NaN de forma mais robusta
        agua_val = dado.agua
        if agua_val is None or math.isnan(agua_val):
            agua.append(None)
        else:
            agua.append(float(agua_val))
        
        coleta_val = dado.coleta
        if coleta_val is None or math.isnan(coleta_val):
            coleta.append(None)
        else:
            coleta.append(float(coleta_val))
        
        tratamento_val = dado.tratamento
        if tratamento_val is None or math.isnan(tratamento_val):
            tratamento.append(None)
        else:
            tratamento.append(float(tratamento_val))
    
    return {
        "anos": anos,
        "atendimento_agua": agua,
        "coleta_esgoto": coleta,
        "tratamento_esgoto": tratamento
    }

def get_ultimo_ano_dados(db: Session) -> int:
    """
    Retorna o ano mais recente com dados
    """
    return db.query(func.max(models.IndicadoresDesempenhoAnual.ano)).scalar() or 2022

def get_municipios_comparacao(db: Session, ano: int) -> List[dict]:
    """
    Retorna dados para comparação entre municípios
    """
    dados = db.query(
        models.IndicadoresDesempenhoAnual,
        models.Municipio
    ).join(models.Municipio)\
     .filter(models.IndicadoresDesempenhoAnual.ano == ano)\
     .all()
    
    return [
        {
            "municipio": municipio,
            "indicadores": indicadores
        }
        for indicadores, municipio in dados
    ]

def get_analise_sustentabilidade_financeira(db: Session, ano: int) -> dict:
    """
    Retorna análise de sustentabilidade financeira
    """
    import math
    
    dados = db.query(
        models.IndicadoresDesempenhoAnual,
        models.Municipio,
        models.FinanceiroAnual
    ).join(models.Municipio)\
     .outerjoin(models.FinanceiroAnual)\
     .filter(models.IndicadoresDesempenhoAnual.ano == ano)\
     .all()
    
    sustentaveis = []
    insustentaveis = []
    
    for indicadores, municipio, financeiro in dados:
        if financeiro:
            # CORREÇÃO: Tratar valores None e NaN
            receita = financeiro.receita_operacional_total
            if receita is None or math.isnan(receita):
                receita = 0
            else:
                receita = float(receita)
            
            despesa = financeiro.despesa_total_servicos
            if despesa is None or math.isnan(despesa):
                despesa = 0
            else:
                despesa = float(despesa)
            
            saldo = receita - despesa
            sustentavel = saldo > 0
            
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
        "ano": ano,
        "sustentaveis": sustentaveis,
        "insustentaveis": insustentaveis
    }

def get_analise_eficiencia_hidrica(db: Session, ano: int) -> dict:
    """
    Retorna análise de eficiência hídrica
    """
    import math
    
    dados = db.query(
        models.IndicadoresDesempenhoAnual,
        models.Municipio,
        models.RecursosHidricosAnual
    ).join(models.Municipio)\
     .outerjoin(models.RecursosHidricosAnual)\
     .filter(models.IndicadoresDesempenhoAnual.ano == ano)\
     .all()
    
    eficiencias = []
    
    for indicadores, municipio, recursos in dados:
        if recursos and recursos.volume_agua_produzido:
            # CORREÇÃO: Tratar valores None e NaN
            indice_perda = indicadores.indice_perda_faturamento
            if indice_perda is None or math.isnan(indice_perda):
                indice_perda = 0
            else:
                indice_perda = float(indice_perda)
            
            volume_produzido = recursos.volume_agua_produzido
            if volume_produzido is None or math.isnan(volume_produzido):
                continue  # Pular se não há volume produzido
            
            volume_faturado = recursos.volume_agua_faturado
            if volume_faturado is None or math.isnan(volume_faturado):
                volume_faturado = 0
            else:
                volume_faturado = float(volume_faturado)
            
            eficiencia = ((volume_faturado / volume_produzido) * 100) if volume_produzido > 0 else 0
            
            eficiencias.append({
                "municipio": municipio,
                "indice_perda": indice_perda,
                "volume_produzido": float(volume_produzido),
                "volume_faturado": volume_faturado,
                "eficiencia": eficiencia
            })
    
    # Ordenar por eficiência
    eficiencias.sort(key=lambda x: x["eficiencia"], reverse=True)
    
    return {
        "ano": ano,
        "mais_eficientes": eficiencias[:10],
        "menos_eficientes": eficiencias[-10:] if len(eficiencias) > 10 else []
    } 