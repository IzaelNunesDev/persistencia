#!/usr/bin/env python3
"""
Script para extrair e processar dados do SNIS para o Ceará
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Adicionar o diretório pai ao path para importar módulos da aplicação
sys.path.append(str(Path(__file__).parent.parent))

# Mapeamento de colunas do CSV para o modelo
COLUMN_MAPPING = {
    'populacao_atentida_esgoto': 'populacao_total_atendida_esgoto',
    'indice_atendimento_total_agua': 'indice_atendimento_agua',
    'receita_operacional_direta': 'receita_operacional_total',
    'despesa_total_servico': 'despesa_total_servicos',
    'investimento_total_prestador': 'investimento_total'
}

def processar_csv_snis(csv_path: str, output_dir: str = "../data"):
    """
    Processa o CSV do SNIS e extrai dados do Ceará
    """
    print(f"Processando arquivo: {csv_path}")
    
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Ler o CSV em chunks para economizar memória
    chunk_size = 10000
    chunks = []
    
    print("Lendo arquivo CSV...")
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
        # Filtrar apenas dados do Ceará
        chunk_ceara = chunk[chunk['sigla_uf'] == 'CE'].copy()
        if not chunk_ceara.empty:
            chunks.append(chunk_ceara)
    
    if not chunks:
        print("Nenhum dado do Ceará encontrado no arquivo!")
        return None
    
    # Concatenar todos os chunks
    df_ceara = pd.concat(chunks, ignore_index=True)
    print(f"Total de registros do Ceará encontrados: {len(df_ceara)}")
    
    # Limpar e processar dados
    df_ceara = limpar_dados(df_ceara)
    
    # Salvar dados processados
    output_file = os.path.join(output_dir, "dados_snis_ceara_limpos.csv")
    df_ceara.to_csv(output_file, index=False)
    print(f"Dados salvos em: {output_file}")
    
    # Gerar estatísticas
    gerar_estatisticas(df_ceara, output_dir)
    
    return df_ceara

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e processa os dados do DataFrame
    """
    print("Limpando dados...")
    
    # Remover linhas com dados completamente nulos
    df = df.dropna(how='all')
    
    # Renomear colunas conforme mapeamento
    df = df.rename(columns=COLUMN_MAPPING)
    
    # Converter tipos de dados
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df['id_municipio'] = df['id_municipio'].astype(str).str.zfill(7)
    
    # Converter colunas numéricas
    colunas_numericas = [
        'populacao_atendida_agua', 'populacao_total_atendida_esgoto',
        'indice_atendimento_agua', 'indice_coleta_esgoto', 'indice_tratamento_esgoto',
        'indice_perda_faturamento', 'volume_agua_produzido', 'volume_esgoto_tratado',
        'receita_operacional_total', 'despesa_total_servicos', 'investimento_total'
    ]
    
    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
    
    # Remover registros com ano inválido
    df = df[df['ano'].notna() & (df['ano'] >= 2010) & (df['ano'] <= 2023)]
    
    # Remover registros sem município
    df = df[df['id_municipio'].notna()]
    
    print(f"Dados limpos: {len(df)} registros")
    return df

def gerar_estatisticas(df: pd.DataFrame, output_dir: str):
    """
    Gera estatísticas dos dados processados
    """
    print("Gerando estatísticas...")
    
    stats = {
        "total_registros": len(df),
        "periodo_anos": f"{df['ano'].min()} - {df['ano'].max()}",
        "total_municipios": df['id_municipio'].nunique(),
        "anos_disponiveis": sorted(df['ano'].unique().tolist()),
        "municipios_com_dados": df['id_municipio'].unique().tolist()
    }
    
    # Estatísticas por ano
    stats_por_ano = df.groupby('ano').agg({
        'id_municipio': 'count',
        'populacao_atendida_agua': ['mean', 'sum'],
        'indice_atendimento_total_agua': 'mean',
        'indice_coleta_esgoto': 'mean',
        'indice_tratamento_esgoto': 'mean'
    }).round(2)
    
    # Salvar estatísticas
    stats_file = os.path.join(output_dir, "estatisticas.txt")
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("ESTATÍSTICAS DOS DADOS DO SNIS - CEARÁ\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Total de registros: {stats['total_registros']}\n")
        f.write(f"Período: {stats['periodo_anos']}\n")
        f.write(f"Total de municípios: {stats['total_municipios']}\n")
        f.write(f"Anos disponíveis: {stats['anos_disponiveis']}\n\n")
        
        f.write("ESTATÍSTICAS POR ANO:\n")
        f.write("-" * 30 + "\n")
        f.write(stats_por_ano.to_string())
    
    print(f"Estatísticas salvas em: {stats_file}")
    
    return stats

def main():
    """
    Função principal
    """
    # Caminho para o CSV do SNIS
    csv_path = "../../br_mdr_snis_municipio_agua_esgoto.csv"
    
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        print("Certifique-se de que o arquivo CSV do SNIS está no diretório pai")
        return
    
    # Processar dados
    df_ceara = processar_csv_snis(csv_path)
    
    if df_ceara is not None:
        print("\nProcessamento concluído com sucesso!")
        print(f"Total de registros processados: {len(df_ceara)}")
    else:
        print("Erro no processamento dos dados!")

if __name__ == "__main__":
    main() 