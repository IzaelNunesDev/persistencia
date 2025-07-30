from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/analises", tags=["analises"])

@router.get("/rankings/{ano}", response_model=schemas.RankingResponse)
def obter_ranking(
    ano: int,
    indicador: str = Query(..., description="Indicador para ranking (ex: indice_atendimento_agua)"),
    ordem: str = Query("desc", description="Ordem do ranking (asc/desc)"),
    limit: int = Query(10, ge=1, le=100, description="Número de posições no ranking"),
    db: Session = Depends(get_db)
):
    """
    Retorna um ranking dos municípios para um indicador específico.
    
    Indicadores disponíveis:
    - indice_atendimento_agua: Índice de atendimento de água (%)
    - indice_coleta_esgoto: Índice de coleta de esgoto (%)
    - indice_tratamento_esgoto: Índice de tratamento de esgoto (%)
    - indice_perda_faturamento: Índice de perda de faturamento (%)
    - volume_agua_produzido: Volume de água produzido (m³)
    - volume_esgoto_tratado: Volume de esgoto tratado (m³)
    - receita_operacional_total: Receita operacional total (R$)
    - investimento_total: Investimento total (R$)
    
    - **ano**: Ano de referência para o ranking
    - **indicador**: Indicador específico para ordenação
    - **ordem**: Ordem do ranking (asc para crescente, desc para decrescente)
    - **limit**: Número de posições no ranking
    """
    try:
        ranking_data = crud.get_ranking_indicador(
            db=db,
            ano=ano,
            indicador=indicador,
            ordem=ordem,
            limit=limit
        )
        
        return schemas.RankingResponse(
            ano=ano,
            indicador=indicador,
            ranking=ranking_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/evolucao", response_model=schemas.EvolucaoResponse)
def obter_evolucao_indicadores(
    id_municipio: str = Query(..., description="Código IBGE do município"),
    indicadores: str = Query(..., description="Lista de indicadores separados por vírgula"),
    db: Session = Depends(get_db)
):
    """
    Retorna a evolução de múltiplos indicadores para um município.
    
    Indicadores disponíveis:
    - indice_atendimento_agua: Índice de atendimento de água (%)
    - indice_coleta_esgoto: Índice de coleta de esgoto (%)
    - indice_tratamento_esgoto: Índice de tratamento de esgoto (%)
    - indice_perda_faturamento: Índice de perda de faturamento (%)
    - volume_agua_produzido: Volume de água produzido (m³)
    - volume_esgoto_tratado: Volume de esgoto tratado (m³)
    - receita_operacional_total: Receita operacional total (R$)
    - investimento_total: Investimento total (R$)
    
    - **id_municipio**: Código IBGE do município
    - **indicadores**: Lista de indicadores separados por vírgula
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=id_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Converter string de indicadores em lista
    indicadores_list = [ind.strip() for ind in indicadores.split(",")]
    
    try:
        evolucao_data = crud.get_evolucao_indicadores(
            db=db,
            municipio_id=id_municipio,
            indicadores=indicadores_list
        )
        
        return schemas.EvolucaoResponse(
            municipio=municipio,
            indicadores=evolucao_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comparativo", response_model=schemas.ComparativoResponse)
def obter_comparativo_municipios(
    ano: int = Query(..., description="Ano de referência"),
    ids_municipios: str = Query(..., description="Lista de códigos IBGE dos municípios separados por vírgula"),
    db: Session = Depends(get_db)
):
    """
    Compara os dados de dois ou mais municípios em um ano específico.
    
    - **ano**: Ano de referência para comparação
    - **ids_municipios**: Lista de códigos IBGE dos municípios separados por vírgula
    """
    # Converter string de IDs em lista
    ids_list = [id_municipio.strip() for id_municipio in ids_municipios.split(",")]
    
    if len(ids_list) < 2:
        raise HTTPException(status_code=400, detail="É necessário pelo menos 2 municípios para comparação")
    
    comparativo_data = crud.get_comparativo_municipios(
        db=db,
        ano=ano,
        ids_municipios=ids_list
    )
    
    return schemas.ComparativoResponse(
        ano=ano,
        municipios=comparativo_data
    )

@router.get("/sustentabilidade-financeira/{ano}", response_model=schemas.SustentabilidadeResponse)
def obter_sustentabilidade_financeira(
    ano: int,
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de municípios com receita > despesa (sustentáveis) e os que têm despesa > receita (insustentáveis).
    
    - **ano**: Ano de referência para análise
    """
    sustentabilidade_data = crud.get_sustentabilidade_financeira(
        db=db,
        ano=ano
    )
    
    return schemas.SustentabilidadeResponse(
        ano=ano,
        sustentaveis=sustentabilidade_data["sustentaveis"],
        insustentaveis=sustentabilidade_data["insustentaveis"]
    ) 