#!/usr/bin/env python3
"""
Script para melhorar os dados dos municípios com informações mais específicas
baseadas nos dados do SNIS
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import logging

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine
from app import models, crud, schemas

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def enhance_municipios_from_snis():
    """Melhora os dados dos municípios com informações do SNIS"""
    logger.info("Iniciando melhoria dos dados dos municípios...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Ler dados do SNIS
        csv_path = "data/dados_snis_ceara_limpos.csv"
        if not os.path.exists(csv_path):
            logger.error(f"Arquivo de dados não encontrado: {csv_path}")
            return
        
        logger.info(f"Lendo dados de {csv_path}")
        df = pd.read_csv(csv_path, low_memory=False)
        
        # Agrupar dados por município para obter informações consolidadas
        municipios_snis = df.groupby('id_municipio').agg({
            'quantidade_sede_municipal_agua': 'max',
            'quantidade_sede_municipal_esgoto': 'max'
        }).reset_index()
        
        logger.info(f"Processando {len(municipios_snis)} municípios do SNIS")
        
        municipios_atualizados = 0
        
        for _, row in municipios_snis.iterrows():
            municipio_id = str(int(row['id_municipio'])).zfill(7)
            
            # Buscar município no banco
            municipio = crud.get_municipio(db, municipio_id)
            if not municipio:
                logger.warning(f"Município {municipio_id} não encontrado no banco")
                continue
            
            # Atualizar dados com informações do SNIS
            municipio.quantidade_sedes_agua = int(row['quantidade_sede_municipal_agua']) if pd.notna(row['quantidade_sede_municipal_agua']) else 1
            municipio.quantidade_sedes_esgoto = int(row['quantidade_sede_municipal_esgoto']) if pd.notna(row['quantidade_sede_municipal_esgoto']) else 1
            
            # Manter prestador predominante como CAGECE (padrão)
            municipio.nome_prestador_predominante = 'CAGECE'
            
            db.add(municipio)
            municipios_atualizados += 1
            
            if municipios_atualizados % 50 == 0:
                logger.info(f"Processados {municipios_atualizados} municípios")
        
        db.commit()
        logger.info(f"Melhoria concluída! Municípios atualizados: {municipios_atualizados}")
        
    except Exception as e:
        logger.error(f"Erro durante a melhoria: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

def add_population_estimates():
    """Adiciona estimativas de população urbana baseadas na população total"""
    logger.info("Adicionando estimativas de população urbana...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Buscar todos os municípios
        municipios = db.query(models.Municipio).all()
        
        municipios_atualizados = 0
        
        for municipio in municipios:
            if municipio.populacao_total_estimada_2022:
                # Estimativa: 70% da população total é urbana (média do Ceará)
                populacao_urbana = int(municipio.populacao_total_estimada_2022 * 0.7)
                municipio.populacao_urbana_estimada_2022 = populacao_urbana
                
                db.add(municipio)
                municipios_atualizados += 1
        
        db.commit()
        logger.info(f"Estimativas de população urbana adicionadas: {municipios_atualizados} municípios")
        
    except Exception as e:
        logger.error(f"Erro ao adicionar estimativas: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal"""
    logger.info("Script de melhoria de municípios iniciado")
    
    # Melhorar dados com informações do SNIS
    enhance_municipios_from_snis()
    
    # Adicionar estimativas de população urbana
    add_population_estimates()
    
    logger.info("Script concluído")

if __name__ == "__main__":
    main() 