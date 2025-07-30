# Em scripts/load_data.py

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

from app.database import engine, Base
from app import models, crud, schemas

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Funções auxiliares para tratar dados
def safe_float(value):
    if value is None or np.isnan(value):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_int(value):
    if value is None or np.isnan(value):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def main():
    logger.info("Iniciando o script de carregamento de dados...")
    
    # Criar sessão com o banco de dados
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Caminho para o arquivo CSV limpo
    csv_path = "data/dados_snis_ceara_limpos.csv"
    if not os.path.exists(csv_path):
        logger.error(f"Arquivo de dados não encontrado em: {csv_path}")
        logger.error("Execute o script 'scripts/extract_data.py' primeiro.")
        return

    # Ler o CSV
    logger.info(f"Lendo dados de {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Renomear colunas para consistência
    df.rename(columns={'populacao_atentida_esgoto': 'populacao_atendida_esgoto'}, inplace=True)
    
    logger.info(f"Total de {len(df)} registros a serem processados.")

    try:
        # 1. Garantir que todos os municípios existam
        municipios_df = df[['id_municipio', 'sigla_uf', 'populacao_urbana']].drop_duplicates(subset=['id_municipio'])
        for _, row in municipios_df.iterrows():
            municipio_id = str(row['id_municipio']).zfill(7)
            if not crud.get_municipio(db, municipio_id):
                municipio_schema = schemas.MunicipioCreate(
                    id_municipio=municipio_id,
                    nome=f"Município {municipio_id}", # Nome genérico, pode ser melhorado
                    sigla_uf=row['sigla_uf'],
                    populacao_total_estimada_2022=safe_int(row['populacao_urbana']) # Usando pop urbana como base
                )
                crud.create_municipio(db, municipio_schema)
        db.commit()
        logger.info("Verificação de municípios concluída.")

        # 2. Garantir que o prestador padrão exista
        prestador_sigla = "CAGECE" # Exemplo, você pode extrair do CSV se houver
        prestador = crud.get_prestador_by_sigla(db, prestador_sigla)
        if not prestador:
            prestador_schema = schemas.PrestadorServicoCreate(
                sigla=prestador_sigla,
                nome="Companhia de Água e Esgoto do Ceará",
                natureza_juridica="Economia Mista"
            )
            prestador = crud.create_prestador(db, prestador_schema)
        db.commit()
        logger.info(f"Prestador '{prestador_sigla}' garantido no banco.")
        
        # 3. Iterar e carregar os dados
        registros_criados = 0
        registros_ignorados = 0
        for index, row in df.iterrows():
            municipio_id = str(row['id_municipio']).zfill(7)
            ano = int(row['ano'])

            # Evitar duplicatas
            existing_indicador = db.query(models.IndicadoresDesempenhoAnual).filter_by(
                ano=ano, municipio_id=municipio_id, prestador_id=prestador.id
            ).first()
            
            if existing_indicador:
                registros_ignorados += 1
                continue
            
            # Criar Tabela Fato: IndicadoresDesempenhoAnual
            indicador_schema = schemas.IndicadoresDesempenhoCreate(
                ano=ano,
                municipio_id=municipio_id,
                prestador_id=prestador.id,
                populacao_atendida_agua=safe_int(row.get('populacao_atendida_agua')),
                populacao_atendida_esgoto=safe_int(row.get('populacao_atendida_esgoto')),
                indice_atendimento_agua=safe_float(row.get('indice_atendimento_total_agua')),
                indice_coleta_esgoto=safe_float(row.get('indice_coleta_esgoto')),
                indice_tratamento_esgoto=safe_float(row.get('indice_tratamento_esgoto')),
                indice_perda_faturamento=safe_float(row.get('indice_perda_faturamento'))
            )
            indicador_db = crud.create_indicadores(db, indicador_schema)

            # Criar Tabela de Detalhes: RecursosHidricosAnual
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

            # Criar Tabela de Detalhes: FinanceiroAnual
            financeiro_schema = schemas.FinanceiroCreate(
                indicador_id=indicador_db.id,
                receita_operacional_total=safe_float(row.get('receita_operacional_direta')),
                despesa_exploracao=safe_float(row.get('despesa_exploracao')),
                despesa_pessoal=safe_float(row.get('despesa_pessoal')),
                despesa_energia=safe_float(row.get('despesa_energia')),
                despesa_total_servicos=safe_float(row.get('despesa_total_servico')),
                investimento_total_prestador=safe_float(row.get('investimento_total_prestador')),
                credito_a_receber=safe_float(row.get('credito_areceber'))
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
        logger.error(f"Ocorreu um erro durante o carregamento: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 