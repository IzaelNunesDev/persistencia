from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/analises", tags=["analises"])

@router.get("/ranking", response_model=schemas.RankingResponse)
def obter_ranking(
    indicador: str = Query(..., description="Indicador para ranking (ex: indice_atendimento_agua)"),
    ano: Optional[int] = Query(None, description="Ano de referência (padrão: mais recente)"),
    ordem: str = Query("desc", description="Ordem do ranking (asc/desc)"),
    limit: int = Query(10, ge=1, le=100, description="Número de posições no ranking"),
    municipio_id: Optional[str] = Query(None, description="ID do município para buscar posição específica"),
    db: Session = Depends(get_db)
):
    """
    Retorna um ranking dos municípios para um indicador específico.
    
    Indicadores disponíveis:
    - indice_atendimento_agua: Índice de atendimento de água (%)
    - indice_coleta_esgoto: Índice de coleta de esgoto (%)
    - indice_tratamento_esgoto: Índice de tratamento de esgoto (%)
    - indice_perda_faturamento: Índice de perda de faturamento (%)
    """
    try:
        if ano is None:
            ano = crud.get_ultimo_ano_dados(db)
        
        ranking_data = crud.get_ranking_indicador(
            db=db,
            ano=ano,
            indicador=indicador,
            ordem=ordem,
            limit=limit,
            municipio_id=municipio_id
        )
        
        return ranking_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/evolucao", response_model=schemas.EvolucaoResponse)
def obter_evolucao_indicadores(
    municipio_id: str = Query(..., description="Código IBGE do município"),
    indicadores: Optional[str] = Query(None, description="Lista de indicadores separados por vírgula"),
    db: Session = Depends(get_db)
):
    """
    Retorna a evolução de múltiplos indicadores para um município.
    
    Indicadores disponíveis:
    - indice_atendimento_agua: Índice de atendimento de água (%)
    - indice_coleta_esgoto: Índice de coleta de esgoto (%)
    - indice_tratamento_esgoto: Índice de tratamento de esgoto (%)
    - indice_perda_faturamento: Índice de perda de faturamento (%)
    """
    # Verificar se o município existe
    municipio = crud.get_municipio(db=db, id_municipio=municipio_id)
    if not municipio:
        raise HTTPException(status_code=404, detail="Município não encontrado")
    
    # Converter string de indicadores em lista
    indicadores_list = None
    if indicadores:
        indicadores_list = [ind.strip() for ind in indicadores.split(",")]
    
    try:
        evolucao_data = crud.get_evolucao_indicadores(
            db=db,
            municipio_id=municipio_id,
            indicadores=indicadores_list
        )
        
        return schemas.EvolucaoResponse(
            municipio=municipio,
            indicadores=evolucao_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/indicadores-principais")
def obter_indicadores_principais(
    ano: Optional[int] = Query(None, description="Ano de referência (padrão: mais recente)"),
    db: Session = Depends(get_db)
):
    """
    Retorna as médias dos indicadores principais para um ano específico.
    """
    try:
        return crud.get_indicadores_principais(db=db, ano=ano)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/evolucao-temporal")
def obter_evolucao_temporal(db: Session = Depends(get_db)):
    """
    Retorna a evolução temporal dos indicadores médios ao longo dos anos.
    """
    try:
        return crud.get_evolucao_temporal(db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/comparativo", response_model=schemas.ComparativoResponse)
def obter_comparativo_municipios(
    ano: Optional[int] = Query(None, description="Ano de referência (padrão: mais recente)"),
    ids_municipios: Optional[str] = Query(None, description="Lista de códigos IBGE dos municípios separados por vírgula"),
    db: Session = Depends(get_db)
):
    """
    Compara os dados de múltiplos municípios em um ano específico.
    """
    try:
        if ano is None:
            ano = crud.get_ultimo_ano_dados(db)
        
        if ids_municipios:
            ids_list = [id.strip() for id in ids_municipios.split(",")]
            # Implementar filtro por municípios específicos se necessário
            pass
        
        municipios_data = crud.get_municipios_comparacao(db=db, ano=ano)
        
        return schemas.ComparativoResponse(
            ano=ano,
            municipios=municipios_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/sustentabilidade-financeira", response_model=schemas.SustentabilidadeResponse)
def obter_sustentabilidade_financeira(
    ano: Optional[int] = Query(None, description="Ano de referência (padrão: mais recente)"),
    db: Session = Depends(get_db)
):
    """
    Retorna análise de sustentabilidade financeira dos municípios.
    """
    try:
        if ano is None:
            ano = crud.get_ultimo_ano_dados(db)
        
        dados = crud.get_analise_sustentabilidade_financeira(db=db, ano=ano)
        
        return schemas.SustentabilidadeResponse(
            ano=ano,
            sustentaveis=dados["sustentaveis"],
            insustentaveis=dados["insustentaveis"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/eficiencia-hidrica", response_model=schemas.EficienciaHidricaResponse)
def obter_eficiencia_hidrica(
    ano: Optional[int] = Query(None, description="Ano de referência (padrão: mais recente)"),
    db: Session = Depends(get_db)
):
    """
    Retorna análise de eficiência hídrica dos municípios.
    """
    try:
        if ano is None:
            ano = crud.get_ultimo_ano_dados(db)
        
        dados = crud.get_analise_eficiencia_hidrica(db=db, ano=ano)
        
        return schemas.EficienciaHidricaResponse(
            ano=ano,
            mais_eficientes=dados["mais_eficientes"],
            menos_eficientes=dados["menos_eficientes"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}") 