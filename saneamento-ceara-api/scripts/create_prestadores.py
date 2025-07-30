#!/usr/bin/env python3
"""
Script para criar prestadores de serviço reais do Ceará
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

# Dados dos principais prestadores do Ceará
PRESTADORES_CEARA = [
    {
        "sigla": "CAGECE",
        "nome": "Companhia de Água e Esgoto do Ceará",
        "natureza_juridica": "Empresa Pública",
        "quantidade_municipios_atendidos": 150,
        "ano_primeiro_registro": 1970,
        "total_investido_historico": 5000000000.0,
        "media_arrecadacao_anual": 800000000.0
    },
    {
        "sigla": "SAAE",
        "nome": "Serviço Autônomo de Água e Esgoto",
        "natureza_juridica": "Autarquia Municipal",
        "quantidade_municipios_atendidos": 20,
        "ano_primeiro_registro": 1980,
        "total_investido_historico": 200000000.0,
        "media_arrecadacao_anual": 15000000.0
    },
    {
        "sigla": "CAGEFOR",
        "nome": "Companhia de Água e Esgoto de Fortaleza",
        "natureza_juridica": "Empresa Pública Municipal",
        "quantidade_municipios_atendidos": 1,
        "ano_primeiro_registro": 1960,
        "total_investido_historico": 3000000000.0,
        "media_arrecadacao_anual": 400000000.0
    },
    {
        "sigla": "EMAE",
        "nome": "Empresa Municipal de Água e Esgoto",
        "natureza_juridica": "Empresa Pública Municipal",
        "quantidade_municipios_atendidos": 5,
        "ano_primeiro_registro": 1990,
        "total_investido_historico": 100000000.0,
        "media_arrecadacao_anual": 8000000.0
    },
    {
        "sigla": "SANEAMENTO",
        "nome": "Empresa de Saneamento Municipal",
        "natureza_juridica": "Empresa Pública Municipal",
        "quantidade_municipios_atendidos": 3,
        "ano_primeiro_registro": 1995,
        "total_investido_historico": 50000000.0,
        "media_arrecadacao_anual": 5000000.0
    },
    {
        "sigla": "AGUAS",
        "nome": "Companhia de Águas Municipais",
        "natureza_juridica": "Empresa Pública Municipal",
        "quantidade_municipios_atendidos": 2,
        "ano_primeiro_registro": 2000,
        "total_investido_historico": 30000000.0,
        "media_arrecadacao_anual": 3000000.0
    },
    {
        "sigla": "SANEAMENTO_CE",
        "nome": "Saneamento do Ceará",
        "natureza_juridica": "Empresa Pública Estadual",
        "quantidade_municipios_atendidos": 8,
        "ano_primeiro_registro": 1985,
        "total_investido_historico": 150000000.0,
        "media_arrecadacao_anual": 12000000.0
    }
]

def create_prestadores():
    """Cria os prestadores de serviço reais do Ceará"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        logger.info("Iniciando criação dos prestadores de serviço...")
        
        # Verificar se já existem prestadores além do "Não Informado"
        existing_prestadores = db.query(models.PrestadorServico).filter(
            models.PrestadorServico.sigla != "NAO_INFORMADO"
        ).all()
        
        if existing_prestadores:
            logger.info(f"Já existem {len(existing_prestadores)} prestadores cadastrados")
            return
        
        # Criar prestadores
        for prestador_data in PRESTADORES_CEARA:
            try:
                # Verificar se já existe
                existing = db.query(models.PrestadorServico).filter(
                    models.PrestadorServico.sigla == prestador_data["sigla"]
                ).first()
                
                if existing:
                    logger.info(f"Prestador {prestador_data['sigla']} já existe")
                    continue
                
                # Criar novo prestador
                prestador = models.PrestadorServico(**prestador_data)
                db.add(prestador)
                logger.info(f"Criado prestador: {prestador_data['sigla']} - {prestador_data['nome']}")
                
            except Exception as e:
                logger.error(f"Erro ao criar prestador {prestador_data['sigla']}: {e}")
                continue
        
        db.commit()
        logger.info("Prestadores criados com sucesso!")
        
        # Listar prestadores criados
        prestadores = db.query(models.PrestadorServico).all()
        logger.info(f"Total de prestadores no sistema: {len(prestadores)}")
        
        for prestador in prestadores:
            logger.info(f"- {prestador.sigla}: {prestador.nome}")
        
    except Exception as e:
        logger.error(f"Erro durante a criação dos prestadores: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_prestadores() 