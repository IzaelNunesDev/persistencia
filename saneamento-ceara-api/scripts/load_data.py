import pandas as pd
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

# Adicionar o diretório pai ao path para importar módulos da aplicação
sys.path.append(str(Path(__file__).parent.parent))

from app.database import DATABASE_URL
from app.models import Base, Municipio, IndicadoresDesempenhoAnual, PrestadorServico
from app import crud, schemas

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def criar_engine():
    """
    Cria engine de conexão com o banco de dados
    """
    return create_engine(DATABASE_URL)

def criar_tabelas(engine):
    """
    Cria as tabelas no banco de dados
    """
    logger.info("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)

def carregar_municipios_ceara(engine, csv_path: str = None):
    """
    Carrega dados dos municípios do Ceará
    """
    logger.info("Carregando dados dos municípios do Ceará...")
    
    if csv_path and os.path.exists(csv_path):
        # Carregar municípios do CSV
        logger.info(f"Carregando municípios do arquivo: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Extrair municípios únicos do Ceará
        municipios_ceara = {}
        for _, row in df.iterrows():
            if row['sigla_uf'] == 'CE':
                id_municipio = str(row['id_municipio']).zfill(7)
                # Usar nome do município se disponível, senão usar código
                nome = row.get('nome_municipio', f"Município {id_municipio}")
                municipios_ceara[id_municipio] = nome
    else:
        # Dados dos municípios do Ceará (códigos IBGE e nomes) - fallback
        logger.info("Usando dados hardcoded dos municípios")
        municipios_ceara = {
        "2300101": "Abaiara",
        "2300150": "Acarape",
        "2300200": "Acaraú",
        "2300309": "Acopiara",
        "2300408": "Aiuaba",
        "2300507": "Alcântaras",
        "2300606": "Altaneira",
        "2300705": "Alto Santo",
        "2300754": "Amontada",
        "2300804": "Antonina do Norte",
        "2300903": "Apuiarés",
        "2301000": "Aquiraz",
        "2301109": "Aracati",
        "2301208": "Aracoiaba",
        "2301257": "Ararendá",
        "2301307": "Araripe",
        "2301406": "Aratuba",
        "2301505": "Arneiroz",
        "2301604": "Assaré",
        "2301703": "Aurora",
        "2301802": "Baixio",
        "2301851": "Banabuiú",
        "2301901": "Barbalha",
        "2301950": "Barreira",
        "2302008": "Barro",
        "2302057": "Barroquinha",
        "2302107": "Baturité",
        "2302206": "Beberibe",
        "2302305": "Bela Cruz",
        "2302404": "Boa Viagem",
        "2302503": "Brejo Santo",
        "2302602": "Camocim",
        "2302701": "Campos Sales",
        "2302800": "Canindé",
        "2302909": "Capistrano",
        "2303006": "Caridade",
        "2303105": "Cariré",
        "2303204": "Caririaçu",
        "2303303": "Cariús",
        "2303402": "Carnaubal",
        "2303501": "Cascavel",
        "2303600": "Catarina",
        "2303659": "Catunda",
        "2303709": "Caucaia",
        "2303808": "Cedro",
        "2303907": "Chaval",
        "2303931": "Choró",
        "2303956": "Chorozinho",
        "2304004": "Coreaú",
        "2304103": "Crateús",
        "2304202": "Crato",
        "2304236": "Croatá",
        "2304251": "Cruz",
        "2304269": "Deputado Irapuan Pinheiro",
        "2304277": "Ererê",
        "2304285": "Eusébio",
        "2304301": "Farias Brito",
        "2304350": "Forquilha",
        "2304400": "Fortaleza",
        "2304459": "Fortim",
        "2304509": "Frecheirinha",
        "2304608": "General Sampaio",
        "2304657": "Graça",
        "2304707": "Granja",
        "2304806": "Granjeiro",
        "2304905": "Groaíras",
        "2304954": "Guaiúba",
        "2305001": "Guaraciaba do Norte",
        "2305100": "Guaramiranga",
        "2305209": "Hidrolândia",
        "2305233": "Horizonte",
        "2305266": "Ibaretama",
        "2305308": "Ibiapina",
        "2305332": "Ibicuitinga",
        "2305357": "Icapuí",
        "2305407": "Icó",
        "2305506": "Iguatu",
        "2305605": "Independência",
        "2305654": "Ipaporanga",
        "2305704": "Ipaumirim",
        "2305803": "Ipu",
        "2305902": "Ipueiras",
        "2306009": "Iracema",
        "2306108": "Irauçuba",
        "2306207": "Itaiçaba",
        "2306256": "Itaitinga",
        "2306306": "Itapagé",
        "2306405": "Itapipoca",
        "2306504": "Itapiúna",
        "2306553": "Itarema",
        "2306603": "Itatira",
        "2306702": "Jaguaretama",
        "2306801": "Jaguaribara",
        "2306900": "Jaguaribe",
        "2307007": "Jaguaruana",
        "2307106": "Jardim",
        "2307205": "Jati",
        "2307254": "Jijoca de Jericoacoara",
        "2307304": "Juazeiro do Norte",
        "2307403": "Jucás",
        "2307502": "Lavras da Mangabeira",
        "2307601": "Limoeiro do Norte",
        "2307635": "Madalena",
        "2307650": "Maracanaú",
        "2307700": "Maranguape",
        "2307809": "Marco",
        "2307908": "Martinópole",
        "2308005": "Massapê",
        "2308104": "Mauriti",
        "2308203": "Meruoca",
        "2308302": "Milagres",
        "2308351": "Milhã",
        "2308377": "Miraíma",
        "2308401": "Missão Velha",
        "2308500": "Mombaça",
        "2308609": "Monsenhor Tabosa",
        "2308708": "Morada Nova",
        "2308807": "Moraújo",
        "2308906": "Morrinhos",
        "2309003": "Mucambo",
        "2309102": "Mulungu",
        "2309201": "Nova Olinda",
        "2309300": "Nova Russas",
        "2309409": "Novo Oriente",
        "2309458": "Ocara",
        "2309508": "Orós",
        "2309607": "Pacajus",
        "2309706": "Pacatuba",
        "2309805": "Pacoti",
        "2309904": "Pacujá",
        "2310001": "Palhano",
        "2310100": "Palmácia",
        "2310209": "Paracuru",
        "2310258": "Paraipaba",
        "2310308": "Parambu",
        "2310407": "Paramoti",
        "2310506": "Pedra Branca",
        "2310605": "Penaforte",
        "2310704": "Pentecoste",
        "2310803": "Pereiro",
        "2310852": "Pindoretama",
        "2310902": "Piquet Carneiro",
        "2310951": "Pires Ferreira",
        "2311009": "Poranga",
        "2311108": "Porteiras",
        "2311207": "Potengi",
        "2311231": "Potiretama",
        "2311264": "Quiterianópolis",
        "2311306": "Quixadá",
        "2311355": "Quixelô",
        "2311405": "Quixeramobim",
        "2311504": "Quixeré",
        "2311603": "Redenção",
        "2311702": "Reriutaba",
        "2311801": "Russas",
        "2311900": "Saboeiro",
        "2311959": "Salitre",
        "2312007": "Santana do Acaraú",
        "2312106": "Santana do Cariri",
        "2312205": "Santa Quitéria",
        "2312304": "São Benedito",
        "2312403": "São Gonçalo do Amarante",
        "2312502": "São João do Jaguaribe",
        "2312601": "São Luís do Curu",
        "2312700": "Senador Pompeu",
        "2312809": "Senador Sá",
        "2312908": "Sobral",
        "2313005": "Solonópole",
        "2313104": "Tabuleiro do Norte",
        "2313203": "Tamboril",
        "2313252": "Tarrafas",
        "2313302": "Tauá",
        "2313351": "Tejuçuoca",
        "2313401": "Tianguá",
        "2313500": "Trairi",
        "2313559": "Tururu",
        "2313609": "Ubajara",
        "2313708": "Umari",
        "2313757": "Umirim",
        "2313807": "Uruburetama",
        "2313906": "Uruoca",
        "2313955": "Varjota",
        "2314003": "Várzea Alegre",
        "2314102": "Viçosa do Ceará"
    }
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        for id_municipio, nome in municipios_ceara.items():
            # Verificar se o município já existe
            municipio_existente = crud.get_municipio(db, id_municipio)
            if not municipio_existente:
                municipio_data = schemas.MunicipioCreate(
                    id_municipio=id_municipio,
                    nome=nome,
                    microrregiao="",  # Será preenchido posteriormente se necessário
                    mesorregiao="",   # Será preenchido posteriormente se necessário
                    ddd=""            # Será preenchido posteriormente se necessário
                )
                crud.create_municipio(db, municipio_data)
                logger.info(f"Município criado: {nome} ({id_municipio})")
        
        db.commit()
        logger.info("Municípios do Ceará carregados com sucesso!")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao carregar municípios: {e}")
        raise
    finally:
        db.close()

def carregar_dados_snis(engine, csv_path: str):
    """
    Carrega dados do SNIS no banco de dados
    """
    logger.info(f"Carregando dados do SNIS: {csv_path}")
    
    if not os.path.exists(csv_path):
        logger.error(f"Arquivo não encontrado: {csv_path}")
        return
    
    # Ler dados processados
    df = pd.read_csv(csv_path)
    logger.info(f"Total de registros para carregar: {len(df)}")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Criar prestador padrão se não existir
        prestador_padrao = crud.get_prestador_by_sigla(db, "SNIS")
        if not prestador_padrao:
            prestador_data = schemas.PrestadorServicoCreate(
                sigla="SNIS",
                nome="Sistema Nacional de Informações sobre Saneamento",
                natureza_juridica="Público"
            )
            prestador_padrao = crud.create_prestador(db, prestador_data)
            logger.info("Prestador padrão SNIS criado")
        
        # Processar dados em lotes
        batch_size = 1000
        total_processed = 0
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            for _, row in batch.iterrows():
                try:
                    # Criar dados de saneamento
                    dados_saneamento = schemas.IndicadoresDesempenhoCreate(
                        ano=int(row['ano']),
                        municipio_id=str(row['id_municipio']),
                        prestador_id=prestador_padrao.id,
                        populacao_total_atendida_agua=row.get('populacao_atendida_agua'),
                        populacao_total_atendida_esgoto=row.get('populacao_atentida_esgoto'),
                        indice_atendimento_agua=row.get('indice_atendimento_total_agua'),
                        indice_coleta_esgoto=row.get('indice_coleta_esgoto'),
                        indice_tratamento_esgoto=row.get('indice_tratamento_esgoto'),
                        indice_perda_faturamento=row.get('indice_perda_faturamento'),
                        volume_agua_produzido=row.get('volume_agua_produzido'),
                        volume_esgoto_tratado=row.get('volume_esgoto_tratado'),
                        receita_operacional_total=row.get('receita_operacional_total'),
                        despesa_total_servicos=row.get('despesa_total_servico'),
                        investimento_total=row.get('investimento_total_prestador')
                    )
                    
                    crud.create_indicadores(db, dados_saneamento)
                    total_processed += 1
                    
                except Exception as e:
                    logger.warning(f"Erro ao processar linha {i} (municipio_id={row.get('id_municipio')}, ano={row.get('ano')}): {e}")
                    import traceback
                    logger.warning(traceback.format_exc())
                    continue
            
            # Commit a cada lote
            db.commit()
            logger.info(f"Processados {total_processed} registros...")
        
        logger.info(f"Carregamento concluído! Total de registros carregados: {total_processed}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao carregar dados: {e}")
        raise
    finally:
        db.close()

def main():
    """
    Função principal
    """
    logger.info("Iniciando carregamento de dados...")
    
    # Criar engine
    engine = criar_engine()
    
    # Criar tabelas
    criar_tabelas(engine)
    
    # Verificar se existe o CSV principal
    csv_principal = "../../br_mdr_snis_municipio_agua_esgoto.csv"
    csv_limpo = "data/dados_snis_ceara_limpos.csv"
    
    # Carregar municípios do Ceará
    if os.path.exists(csv_principal):
        carregar_municipios_ceara(engine, csv_principal)
    else:
        carregar_municipios_ceara(engine)
    
    # Carregar dados do SNIS limpos
    if os.path.exists(csv_limpo):
        carregar_dados_snis(engine, csv_limpo)
    else:
        logger.warning(f"Arquivo de dados limpos não encontrado: {csv_limpo}")
        logger.info("Execute primeiro o script extract_data.py para processar os dados")
    
    logger.info("Carregamento de dados concluído!")

if __name__ == "__main__":
    main() 