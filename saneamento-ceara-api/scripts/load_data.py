import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import logging

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine
from app import models, crud, schemas

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Funções auxiliares para tratar dados
def safe_float(value):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_int(value):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    try:
        return int(value)
    except (ValueError, TypeError, OverflowError): # Lida com números muito grandes
        return None

def get_or_create_prestador(db: sessionmaker, sigla: str, nome: str) -> models.PrestadorServico:
    prestador = crud.get_prestador_by_sigla(db, sigla)
    if not prestador:
        logger.info(f"Criando novo prestador: {sigla}")
        prestador_schema = schemas.PrestadorServicoCreate(sigla=sigla, nome=nome)
        prestador = crud.create_prestador(db, prestador_schema)
    return prestador

def get_or_create_municipio(db: sessionmaker, row: pd.Series) -> models.Municipio:
    municipio_id = str(row.get('id_municipio')).zfill(7)
    municipio = crud.get_municipio(db, municipio_id)
    if not municipio:
        logger.info(f"Criando novo município: {municipio_id}")
        municipio_schema = schemas.MunicipioCreate(
            id_municipio=municipio_id,
            nome=row.get('nome_municipio', f"Município {municipio_id}"), # Usa nome real se existir
            sigla_uf=row.get('sigla_uf', 'CE'),
            populacao_total_estimada_2022=safe_int(row.get('populacao_total_estimada_2022'))
        )
        municipio = crud.create_municipio(db, municipio_schema)
    return municipio

def main():
    logger.info("Iniciando o script de carregamento de dados...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    csv_path = "data/dados_snis_ceara_limpos.csv"
    if not os.path.exists(csv_path):
        logger.error(f"Arquivo de dados não encontrado: {csv_path}. Execute 'scripts/extract_data.py' primeiro.")
        return

    logger.info(f"Lendo dados de {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)
    
    logger.info(f"Total de {len(df)} registros a serem processados.")

    try:
        # Garantir que um prestador padrão exista para casos sem sigla
        prestador_padrao = get_or_create_prestador(db, "NAO_INFORMADO", "Não Informado")

        registros_criados = 0
        registros_ignorados = 0
        
        for index, row in df.iterrows():
            municipio = get_or_create_municipio(db, row)
            prestador_sigla = row.get('sigla_prestador', 'NAO_INFORMADO').strip()
            prestador_nome = row.get('nome_prestador', 'Não Informado').strip()
            prestador = get_or_create_prestador(db, prestador_sigla, prestador_nome)

            ano = int(row['ano'])

            # Evitar duplicatas (ano, municipio, prestador)
            if db.query(models.IndicadoresDesempenhoAnual).filter_by(
                ano=ano, municipio_id=municipio.id_municipio, prestador_id=prestador.id
            ).first():
                registros_ignorados += 1
                continue
            
            # 1. Indicadores de Desempenho
            indicador_schema = schemas.IndicadoresDesempenhoCreate(
                ano=ano,
                municipio_id=municipio.id_municipio,
                prestador_id=prestador.id,
                populacao_atendida_agua=safe_int(row.get('populacao_atendida_agua')),
                populacao_atendida_esgoto=safe_int(row.get('populacao_atentida_esgoto')), # Note o typo do CSV
                indice_atendimento_agua=safe_float(row.get('indice_atendimento_total_agua')),
                indice_coleta_esgoto=safe_float(row.get('indice_coleta_esgoto')),
                indice_tratamento_esgoto=safe_float(row.get('indice_tratamento_esgoto')),
                indice_perda_faturamento=safe_float(row.get('indice_perda_faturamento'))
            )
            indicador_db = crud.create_indicadores(db, indicador_schema)

            # 2. Recursos Hídricos
            recursos_schema = schemas.RecursosHidricosCreate(
                indicador_id=indicador_db.id,
                volume_agua_produzido=safe_float(row.get('volume_agua_produzido')),
                volume_agua_consumido=safe_float(row.get('volume_agua_consumido')),
                volume_agua_faturado=safe_float(row.get('volume_agua_faturado')),
                volume_esgoto_coletado=safe_float(row.get('volume_esgoto_coletado')),
                volume_esgoto_tratado=safe_float(row.get('volume_esgoto_tratado')),
                consumo_eletrico_sistemas_agua=safe_float(row.get('consumo_eletrico_sistemas_agua'))
            )
            crud.create_recursos_hidricos(db, recursos_schema)

            # 3. Financeiro
            financeiro_schema = schemas.FinanceiroCreate(
                indicador_id=indicador_db.id,
                receita_operacional_total=safe_float(row.get('receita_operacional_direta')),
                despesa_exploracao=safe_float(row.get('despesa_exploracao')),
                despesa_pessoal=safe_float(row.get('despesa_pessoal')),
                despesa_energia=safe_float(row.get('despesa_energia')),
                despesa_total_servicos=safe_float(row.get('despesa_total_servico')),
                investimento_total_prestador=safe_float(row.get('investimento_total_prestador')),
                credito_a_receber=safe_float(row.get('credito_areceber')) # Note o typo
            )
            crud.create_financeiro(db, financeiro_schema)
            
            registros_criados += 1
            if (index + 1) % 100 == 0:
                logger.info(f"Processado {index + 1}/{len(df)} registros. Criados: {registros_criados}, Ignorados: {registros_ignorados}")
        
        db.commit()
        logger.info("Carregamento de dados concluído com sucesso!")
        logger.info(f"Total de registros criados: {registros_criados}")
        logger.info(f"Total de registros ignorados (duplicados): {registros_ignorados}")

    except Exception as e:
        logger.error(f"Ocorreu um erro durante o carregamento: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 