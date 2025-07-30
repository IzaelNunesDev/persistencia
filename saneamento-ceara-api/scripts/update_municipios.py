#!/usr/bin/env python3
"""
Script para atualizar os dados dos municípios do Ceará com informações reais
"""

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

# Dados dos municípios do Ceará (IBGE 2022)
MUNICIPIOS_CEARA = {
    "2300101": {"nome": "Abaiara", "populacao": 11115},
    "2300150": {"nome": "Acarape", "populacao": 15353},
    "2300200": {"nome": "Acaraú", "populacao": 62680},
    "2300309": {"nome": "Acopiara", "populacao": 53207},
    "2300408": {"nome": "Aiuaba", "populacao": 16247},
    "2300507": {"nome": "Alcântaras", "populacao": 11362},
    "2300606": {"nome": "Altaneira", "populacao": 7486},
    "2300705": {"nome": "Alto Santo", "populacao": 16389},
    "2300754": {"nome": "Amontada", "populacao": 42444},
    "2300804": {"nome": "Antonina do Norte", "populacao": 6984},
    "2300903": {"nome": "Apuiarés", "populacao": 14554},
    "2301000": {"nome": "Aquiraz", "populacao": 81415},
    "2301109": {"nome": "Aracati", "populacao": 75105},
    "2301208": {"nome": "Aracoiaba", "populacao": 25515},
    "2301257": {"nome": "Ararendá", "populacao": 10491},
    "2301307": {"nome": "Araripe", "populacao": 20685},
    "2301406": {"nome": "Aratuba", "populacao": 11529},
    "2301505": {"nome": "Arneiroz", "populacao": 7650},
    "2301604": {"nome": "Assaré", "populacao": 22446},
    "2301703": {"nome": "Aurora", "populacao": 24566},
    "2301802": {"nome": "Baixio", "populacao": 6026},
    "2301851": {"nome": "Banabuiú", "populacao": 17315},
    "2301901": {"nome": "Barbalha", "populacao": 57328},
    "2301950": {"nome": "Barreira", "populacao": 19573},
    "2302008": {"nome": "Barro", "populacao": 21514},
    "2302057": {"nome": "Barroquinha", "populacao": 14476},
    "2302107": {"nome": "Baturité", "populacao": 35957},
    "2302206": {"nome": "Beberibe", "populacao": 49371},
    "2302305": {"nome": "Bela Cruz", "populacao": 30834},
    "2302404": {"nome": "Boa Viagem", "populacao": 52458},
    "2302503": {"nome": "Brejo Santo", "populacao": 45193},
    "2302602": {"nome": "Camocim", "populacao": 62052},
    "2302701": {"nome": "Campos Sales", "populacao": 26506},
    "2302800": {"nome": "Canindé", "populacao": 74473},
    "2302909": {"nome": "Capistrano", "populacao": 17062},
    "2303006": {"nome": "Caridade", "populacao": 20020},
    "2303105": {"nome": "Cariré", "populacao": 18347},
    "2303204": {"nome": "Caririaçu", "populacao": 26393},
    "2303303": {"nome": "Cariús", "populacao": 18567},
    "2303402": {"nome": "Carnaubal", "populacao": 16746},
    "2303501": {"nome": "Cascavel", "populacao": 66142},
    "2303600": {"nome": "Catarina", "populacao": 18745},
    "2303659": {"nome": "Catunda", "populacao": 9952},
    "2303709": {"nome": "Caucaia", "populacao": 360396},
    "2303808": {"nome": "Cedro", "populacao": 24527},
    "2303907": {"nome": "Chaval", "populacao": 12615},
    "2303931": {"nome": "Choró", "populacao": 12853},
    "2303956": {"nome": "Chorozinho", "populacao": 18915},
    "2304004": {"nome": "Coreaú", "populacao": 21956},
    "2304103": {"nome": "Crateús", "populacao": 72802},
    "2304202": {"nome": "Crato", "populacao": 133031},
    "2304236": {"nome": "Croatá", "populacao": 17007},
    "2304251": {"nome": "Cruz", "populacao": 22479},
    "2304269": {"nome": "Deputado Irapuan Pinheiro", "populacao": 9095},
    "2304277": {"nome": "Ererê", "populacao": 6840},
    "2304285": {"nome": "Eusébio", "populacao": 46033},
    "2304301": {"nome": "Farias Brito", "populacao": 19007},
    "2304350": {"nome": "Forquilha", "populacao": 21786},
    "2304400": {"nome": "Fortaleza", "populacao": 2669342},
    "2304459": {"nome": "Fortim", "populacao": 14817},
    "2304509": {"nome": "Frecheirinha", "populacao": 12913},
    "2304608": {"nome": "General Sampaio", "populacao": 6218},
    "2304657": {"nome": "Graça", "populacao": 15049},
    "2304707": {"nome": "Granja", "populacao": 52645},
    "2304806": {"nome": "Granjeiro", "populacao": 4625},
    "2304905": {"nome": "Groaíras", "populacao": 10228},
    "2304954": {"nome": "Guaiúba", "populacao": 24091},
    "2305001": {"nome": "Guaraciaba do Norte", "populacao": 37775},
    "2305100": {"nome": "Guaramiranga", "populacao": 4164},
    "2305209": {"nome": "Hidrolândia", "populacao": 19325},
    "2305233": {"nome": "Horizonte", "populacao": 63817},
    "2305266": {"nome": "Ibaretama", "populacao": 12922},
    "2305308": {"nome": "Ibiapina", "populacao": 23808},
    "2305332": {"nome": "Ibicuitinga", "populacao": 11335},
    "2305357": {"nome": "Icapuí", "populacao": 18392},
    "2305407": {"nome": "Icó", "populacao": 65456},
    "2305506": {"nome": "Iguatu", "populacao": 98445},
    "2305605": {"nome": "Independência", "populacao": 25572},
    "2305654": {"nome": "Ipaporanga", "populacao": 11347},
    "2305704": {"nome": "Ipaumirim", "populacao": 12097},
    "2305803": {"nome": "Ipu", "populacao": 40296},
    "2305902": {"nome": "Ipueiras", "populacao": 37862},
    "2306009": {"nome": "Iracema", "populacao": 13722},
    "2306108": {"nome": "Irauçuba", "populacao": 22336},
    "2306207": {"nome": "Itaiçaba", "populacao": 7316},
    "2306256": {"nome": "Itaitinga", "populacao": 35817},
    "2306306": {"nome": "Itapagé", "populacao": 48350},
    "2306405": {"nome": "Itapipoca", "populacao": 130539},
    "2306504": {"nome": "Itapiúna", "populacao": 18626},
    "2306553": {"nome": "Itarema", "populacao": 37471},
    "2306603": {"nome": "Itatira", "populacao": 18894},
    "2306702": {"nome": "Jaguaretama", "populacao": 17863},
    "2306801": {"nome": "Jaguaribara", "populacao": 10399},
    "2306900": {"nome": "Jaguaribe", "populacao": 34422},
    "2307007": {"nome": "Jaguaruana", "populacao": 32236},
    "2307106": {"nome": "Jardim", "populacao": 26688},
    "2307205": {"nome": "Jati", "populacao": 7660},
    "2307254": {"nome": "Jijoca de Jericoacoara", "populacao": 17002},
    "2307304": {"nome": "Juazeiro do Norte", "populacao": 270383},
    "2307403": {"nome": "Jucás", "populacao": 23807},
    "2307502": {"nome": "Lavras da Mangabeira", "populacao": 31090},
    "2307601": {"nome": "Limoeiro do Norte", "populacao": 56264},
    "2307635": {"nome": "Madalena", "populacao": 18088},
    "2307650": {"nome": "Maracanaú", "populacao": 229458},
    "2307700": {"nome": "Maranguape", "populacao": 122210},
    "2307809": {"nome": "Marco", "populacao": 24703},
    "2307908": {"nome": "Martinópole", "populacao": 10214},
    "2308005": {"nome": "Massapê", "populacao": 35191},
    "2308104": {"nome": "Mauriti", "populacao": 44240},
    "2308203": {"nome": "Meruoca", "populacao": 13693},
    "2308302": {"nome": "Milagres", "populacao": 28316},
    "2308351": {"nome": "Milhã", "populacao": 13086},
    "2308377": {"nome": "Miraíma", "populacao": 12800},
    "2308401": {"nome": "Missão Velha", "populacao": 34274},
    "2308500": {"nome": "Mombaça", "populacao": 42690},
    "2308609": {"nome": "Monsenhor Tabosa", "populacao": 16705},
    "2308708": {"nome": "Morada Nova", "populacao": 62065},
    "2308807": {"nome": "Moraújo", "populacao": 8070},
    "2308906": {"nome": "Morrinhos", "populacao": 20700},
    "2309003": {"nome": "Mucambo", "populacao": 14102},
    "2309102": {"nome": "Mulungu", "populacao": 11485},
    "2309201": {"nome": "Nova Olinda", "populacao": 14256},
    "2309300": {"nome": "Nova Russas", "populacao": 30965},
    "2309409": {"nome": "Novo Oriente", "populacao": 27453},
    "2309458": {"nome": "Ocara", "populacao": 24007},
    "2309508": {"nome": "Orós", "populacao": 21389},
    "2309607": {"nome": "Pacajus", "populacao": 61838},
    "2309706": {"nome": "Pacatuba", "populacao": 72299},
    "2309805": {"nome": "Pacoti", "populacao": 11607},
    "2309904": {"nome": "Pacujá", "populacao": 5986},
    "2310001": {"nome": "Palhano", "populacao": 8866},
    "2310100": {"nome": "Palmácia", "populacao": 12005},
    "2310209": {"nome": "Paracuru", "populacao": 31636},
    "2310258": {"nome": "Paraipaba", "populacao": 30041},
    "2310308": {"nome": "Parambu", "populacao": 31309},
    "2310407": {"nome": "Paramoti", "populacao": 11308},
    "2310506": {"nome": "Pedra Branca", "populacao": 41890},
    "2310605": {"nome": "Penaforte", "populacao": 8226},
    "2310704": {"nome": "Pentecoste", "populacao": 35400},
    "2310803": {"nome": "Pereiro", "populacao": 15757},
    "2310852": {"nome": "Pindoretama", "populacao": 18683},
    "2310902": {"nome": "Piquet Carneiro", "populacao": 15467},
    "2310951": {"nome": "Pires Ferreira", "populacao": 10216},
    "2311009": {"nome": "Poranga", "populacao": 12201},
    "2311108": {"nome": "Porteiras", "populacao": 15061},
    "2311207": {"nome": "Potengi", "populacao": 10276},
    "2311231": {"nome": "Potiretama", "populacao": 6126},
    "2311264": {"nome": "Quiterianópolis", "populacao": 19912},
    "2311306": {"nome": "Quixadá", "populacao": 87354},
    "2311355": {"nome": "Quixelô", "populacao": 15000},
    "2311405": {"nome": "Quixeramobim", "populacao": 81275},
    "2311504": {"nome": "Quixeré", "populacao": 19412},
    "2311603": {"nome": "Redenção", "populacao": 26415},
    "2311702": {"nome": "Reriutaba", "populacao": 19455},
    "2311801": {"nome": "Russas", "populacao": 69433},
    "2311900": {"nome": "Saboeiro", "populacao": 15752},
    "2311959": {"nome": "Salitre", "populacao": 15453},
    "2312007": {"nome": "Santana do Acaraú", "populacao": 29946},
    "2312106": {"nome": "Santana do Cariri", "populacao": 17170},
    "2312205": {"nome": "Santa Quitéria", "populacao": 42763},
    "2312304": {"nome": "São Benedito", "populacao": 44178},
    "2312403": {"nome": "São Gonçalo do Amarante", "populacao": 43890},
    "2312502": {"nome": "São João do Jaguaribe", "populacao": 7900},
    "2312601": {"nome": "São Luís do Curu", "populacao": 12332},
    "2312700": {"nome": "Senador Pompeu", "populacao": 26469},
    "2312809": {"nome": "Senador Sá", "populacao": 6852},
    "2312908": {"nome": "Sobral", "populacao": 203023},
    "2313005": {"nome": "Solonópole", "populacao": 17665},
    "2313104": {"nome": "Tabuleiro do Norte", "populacao": 29204},
    "2313203": {"nome": "Tamboril", "populacao": 25451},
    "2313252": {"nome": "Tarrafas", "populacao": 8910},
    "2313302": {"nome": "Tauá", "populacao": 55716},
    "2313351": {"nome": "Tejuçuoca", "populacao": 16827},
    "2313401": {"nome": "Tianguá", "populacao": 73219},
    "2313500": {"nome": "Trairi", "populacao": 51422},
    "2313559": {"nome": "Tururu", "populacao": 14408},
    "2313609": {"nome": "Ubajara", "populacao": 31787},
    "2313708": {"nome": "Umari", "populacao": 7545},
    "2313757": {"nome": "Umirim", "populacao": 18802},
    "2313807": {"nome": "Uruburetama", "populacao": 19765},
    "2313906": {"nome": "Uruoca", "populacao": 12883},
    "2313955": {"nome": "Varjota", "populacao": 17593},
    "2314003": {"nome": "Várzea Alegre", "populacao": 38434},
    "2314102": {"nome": "Viçosa do Ceará", "populacao": 55156}
}

def update_municipios():
    """Atualiza os dados dos municípios com informações reais"""
    logger.info("Iniciando atualização dos dados dos municípios...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        municipios_atualizados = 0
        municipios_criados = 0
        
        for codigo_ibge, dados in MUNICIPIOS_CEARA.items():
            # Verificar se o município já existe
            municipio = crud.get_municipio(db, codigo_ibge)
            
            if municipio:
                # Atualizar município existente
                municipio.nome = dados["nome"]
                municipio.populacao_total_estimada_2022 = dados["populacao"]
                municipio.quantidade_sedes_agua = 1  # Valor padrão
                municipio.quantidade_sedes_esgoto = 1  # Valor padrão
                municipio.nome_prestador_predominante = "CAGECE"  # Valor padrão
                
                db.add(municipio)
                municipios_atualizados += 1
                logger.info(f"Atualizado: {dados['nome']} ({codigo_ibge})")
            else:
                # Criar novo município
                municipio_schema = schemas.MunicipioCreate(
                    id_municipio=codigo_ibge,
                    nome=dados["nome"],
                    sigla_uf="CE",
                    populacao_total_estimada_2022=dados["populacao"],
                    quantidade_sedes_agua=1,
                    quantidade_sedes_esgoto=1,
                    nome_prestador_predominante="CAGECE"
                )
                crud.create_municipio(db, municipio_schema)
                municipios_criados += 1
                logger.info(f"Criado: {dados['nome']} ({codigo_ibge})")
        
        db.commit()
        logger.info(f"Atualização concluída! Municípios atualizados: {municipios_atualizados}, criados: {municipios_criados}")
        
    except Exception as e:
        logger.error(f"Erro durante a atualização: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal"""
    logger.info("Script de atualização de municípios iniciado")
    update_municipios()
    logger.info("Script concluído")

if __name__ == "__main__":
    main() 