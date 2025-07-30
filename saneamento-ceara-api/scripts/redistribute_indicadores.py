#!/usr/bin/env python3
"""
Script para redistribuir indicadores para os prestadores corretos
baseado no nome_prestador_predominante dos municípios
"""

import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker
import logging

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine
from app import models, crud, schemas

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mapeamento de nomes de prestadores para IDs
PRESTADOR_MAPPING = {
    "CAGECE": 2,
    "SAAE": 3,
    "CAGEFOR": 4,
    "EMAE": 5,
    "SANEAMENTO": 6,
    "AGUAS": 7,
    "SANEAMENTO_CE": 8
}

def redistribute_indicadores():
    """Redistribui os indicadores para os prestadores corretos"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        logger.info("Iniciando redistribuição dos indicadores...")
        
        # Buscar todos os indicadores que estão associados ao prestador "Não Informado"
        indicadores = db.query(models.IndicadoresDesempenhoAnual).filter(
            models.IndicadoresDesempenhoAnual.prestador_id == 1
        ).all()
        
        logger.info(f"Encontrados {len(indicadores)} indicadores para redistribuir")
        
        updated_count = 0
        
        for indicador in indicadores:
            try:
                # Buscar o município associado
                municipio = db.query(models.Municipio).filter(
                    models.Municipio.id_municipio == indicador.municipio_id
                ).first()
                
                if not municipio:
                    logger.warning(f"Município {indicador.municipio_id} não encontrado")
                    continue
                
                # Verificar o prestador predominante do município
                prestador_nome = municipio.nome_prestador_predominante
                
                if prestador_nome and prestador_nome in PRESTADOR_MAPPING:
                    # Atualizar o prestador_id do indicador
                    novo_prestador_id = PRESTADOR_MAPPING[prestador_nome]
                    indicador.prestador_id = novo_prestador_id
                    updated_count += 1
                    
                    if updated_count % 100 == 0:
                        logger.info(f"Atualizados {updated_count} indicadores...")
                
            except Exception as e:
                logger.error(f"Erro ao processar indicador {indicador.id}: {e}")
                continue
        
        db.commit()
        logger.info(f"Redistribuição concluída! {updated_count} indicadores atualizados")
        
        # Verificar distribuição final
        for prestador_nome, prestador_id in PRESTADOR_MAPPING.items():
            count = db.query(models.IndicadoresDesempenhoAnual).filter(
                models.IndicadoresDesempenhoAnual.prestador_id == prestador_id
            ).count()
            logger.info(f"{prestador_nome}: {count} indicadores")
        
        # Verificar quantos ainda estão com "Não Informado"
        nao_informado_count = db.query(models.IndicadoresDesempenhoAnual).filter(
            models.IndicadoresDesempenhoAnual.prestador_id == 1
        ).count()
        logger.info(f"Ainda com 'Não Informado': {nao_informado_count} indicadores")
        
    except Exception as e:
        logger.error(f"Erro durante a redistribuição: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    redistribute_indicadores() 