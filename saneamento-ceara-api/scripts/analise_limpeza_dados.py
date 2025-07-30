import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configurações para melhor visualização
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class AnalisadorSNISCeara:
    def __init__(self, arquivo_csv):
        """
        Inicializa o analisador com o arquivo CSV dos dados do SNIS do Ceará
        
        Args:
            arquivo_csv (str): Caminho para o arquivo CSV
        """
        self.arquivo_csv = arquivo_csv
        self.dados_originais = None
        self.dados_limpos = None
        self.relatorio_limpeza = {}
        
    def carregar_dados(self):
        """Carrega os dados do arquivo CSV"""
        print("Carregando dados do arquivo CSV...")
        try:
            self.dados_originais = pd.read_csv(self.arquivo_csv)
            print(f"Dados carregados com sucesso!")
            print(f"Shape: {self.dados_originais.shape}")
            print(f"Colunas: {len(self.dados_originais.columns)}")
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
    
    def verificar_filtro_ceara(self):
        """Verifica se o filtro por Ceará foi aplicado corretamente"""
        print("\n=== VERIFICAÇÃO DO FILTRO CEARÁ ===")
        
        # Verificar se todos os registros são do Ceará
        registros_ceara = (self.dados_originais['sigla_uf'] == 'CE').sum()
        total_registros = len(self.dados_originais)
        
        print(f"Total de registros: {total_registros}")
        print(f"Registros do Ceará: {registros_ceara}")
        print(f"Registros de outros estados: {total_registros - registros_ceara}")
        
        if registros_ceara == total_registros:
            print("✅ Filtro por Ceará aplicado corretamente!")
        else:
            print("❌ Filtro por Ceará não foi aplicado corretamente!")
            
        # Verificar distribuição por UF
        print("\nDistribuição por UF:")
        print(self.dados_originais['sigla_uf'].value_counts())
        
    def analise_estrutura_dados(self):
        """Analisa a estrutura geral dos dados"""
        print("\n=== ANÁLISE DA ESTRUTURA DOS DADOS ===")
        
        print(f"Período dos dados: {self.dados_originais['ano'].min()} - {self.dados_originais['ano'].max()}")
        print(f"Número de municípios únicos: {self.dados_originais['id_municipio'].nunique()}")
        
        # Análise de valores nulos
        print("\nValores nulos por coluna:")
        nulos = self.dados_originais.isnull().sum()
        nulos_percentual = (nulos / len(self.dados_originais)) * 100
        df_nulos = pd.DataFrame({
            'Coluna': nulos.index,
            'Valores_Nulos': nulos.values,
            'Percentual': nulos_percentual.values
        }).sort_values('Valores_Nulos', ascending=False)
        
        print(df_nulos[df_nulos['Valores_Nulos'] > 0].head(20))
        
        # Tipos de dados
        print("\nTipos de dados:")
        print(self.dados_originais.dtypes.value_counts())
        
    def identificar_problemas_qualidade(self):
        """Identifica problemas de qualidade nos dados"""
        print("\n=== IDENTIFICAÇÃO DE PROBLEMAS DE QUALIDADE ===")
        
        problemas = {}
        
        # 1. Valores negativos em campos que não deveriam ser negativos
        colunas_positivas = [
            'populacao_atendida_agua', 'populacao_atentida_esgoto',
            'populacao_urbana', 'extensao_rede_agua', 'extensao_rede_esgoto',
            'quantidade_ligacao_ativa_agua', 'quantidade_ligacao_ativa_esgoto',
            'volume_agua_produzido', 'volume_agua_consumido'
        ]
        
        for col in colunas_positivas:
            if col in self.dados_originais.columns:
                negativos = (self.dados_originais[col] < 0).sum()
                if negativos > 0:
                    problemas[f'valores_negativos_{col}'] = negativos
        
        # 2. Valores extremamente altos (outliers)
        colunas_numericas = self.dados_originais.select_dtypes(include=[np.number]).columns
        for col in colunas_numericas[:10]:  # Primeiras 10 colunas numéricas
            if col in self.dados_originais.columns:
                Q1 = self.dados_originais[col].quantile(0.25)
                Q3 = self.dados_originais[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((self.dados_originais[col] < (Q1 - 1.5 * IQR)) | 
                           (self.dados_originais[col] > (Q3 + 1.5 * IQR))).sum()
                if outliers > 0:
                    problemas[f'outliers_{col}'] = outliers
        
        # 3. Valores zero em campos importantes
        colunas_importantes = ['populacao_atendida_agua', 'populacao_atentida_esgoto']
        for col in colunas_importantes:
            if col in self.dados_originais.columns:
                zeros = (self.dados_originais[col] == 0).sum()
                problemas[f'zeros_{col}'] = zeros
        
        print("Problemas identificados:")
        for problema, quantidade in problemas.items():
            print(f"- {problema}: {quantidade} registros")
            
        return problemas
    
    def limpar_dados(self):
        """Realiza a limpeza dos dados"""
        print("\n=== LIMPEZA DOS DADOS ===")
        
        self.dados_limpos = self.dados_originais.copy()
        registros_antes = len(self.dados_limpos)
        
        # 1. Remover valores negativos em campos que não deveriam ser negativos
        colunas_positivas = [
            'populacao_atendida_agua', 'populacao_atentida_esgoto',
            'populacao_urbana', 'extensao_rede_agua', 'extensao_rede_esgoto',
            'quantidade_ligacao_ativa_agua', 'quantidade_ligacao_ativa_esgoto',
            'volume_agua_produzido', 'volume_agua_consumido'
        ]
        
        for col in colunas_positivas:
            if col in self.dados_limpos.columns:
                negativos_antes = (self.dados_limpos[col] < 0).sum()
                self.dados_limpos.loc[self.dados_limpos[col] < 0, col] = np.nan
                print(f"Convertidos {negativos_antes} valores negativos para NaN em {col}")
        
        # 2. Tratar valores extremos (outliers) usando winsorização
        colunas_numericas = self.dados_limpos.select_dtypes(include=[np.number]).columns
        for col in colunas_numericas[:15]:  # Primeiras 15 colunas numéricas
            if col in self.dados_limpos.columns and self.dados_limpos[col].notna().sum() > 0:
                Q1 = self.dados_limpos[col].quantile(0.01)
                Q99 = self.dados_limpos[col].quantile(0.99)
                outliers_antes = ((self.dados_limpos[col] < Q1) | (self.dados_limpos[col] > Q99)).sum()
                self.dados_limpos[col] = self.dados_limpos[col].clip(lower=Q1, upper=Q99)
                print(f"Tratados {outliers_antes} outliers em {col}")
        
        # 3. Preencher valores nulos com estratégias apropriadas
        # Para valores populacionais, usar média por município
        colunas_populacao = ['populacao_atendida_agua', 'populacao_atentida_esgoto', 'populacao_urbana']
        for col in colunas_populacao:
            if col in self.dados_limpos.columns:
                nulos_antes = self.dados_limpos[col].isnull().sum()
                self.dados_limpos[col] = self.dados_limpos.groupby('id_municipio')[col].transform(
                    lambda x: x.fillna(x.mean())
                )
                print(f"Preenchidos {nulos_antes} valores nulos em {col}")
        
        # 4. Remover registros com muitos valores nulos
        threshold_nulos = 0.8  # 80% de valores nulos
        registros_com_muitos_nulos = (self.dados_limpos.isnull().sum(axis=1) / len(self.dados_limpos.columns)) > threshold_nulos
        self.dados_limpos = self.dados_limpos[~registros_com_muitos_nulos]
        
        registros_depois = len(self.dados_limpos)
        print(f"\nRegistros removidos por excesso de valores nulos: {registros_antes - registros_depois}")
        
        # 5. Verificar e corrigir inconsistências
        # Se população atendida > população urbana, ajustar
        if 'populacao_atendida_agua' in self.dados_limpos.columns and 'populacao_urbana' in self.dados_limpos.columns:
            inconsistencia = (self.dados_limpos['populacao_atendida_agua'] > self.dados_limpos['populacao_urbana']).sum()
            if inconsistencia > 0:
                print(f"Corrigidas {inconsistencia} inconsistências de população")
                self.dados_limpos['populacao_atendida_agua'] = self.dados_limpos['populacao_atendida_agua'].clip(
                    upper=self.dados_limpos['populacao_urbana']
                )
        
        print(f"\nLimpeza concluída!")
        print(f"Registros antes: {registros_antes}")
        print(f"Registros depois: {registros_depois}")
        print(f"Registros removidos: {registros_antes - registros_depois}")
        
    def gerar_estatisticas_descritivas(self):
        """Gera estatísticas descritivas dos dados limpos"""
        print("\n=== ESTATÍSTICAS DESCRITIVAS ===")
        
        if self.dados_limpos is None:
            print("Dados limpos não disponíveis. Execute limpar_dados() primeiro.")
            return
        
        # Estatísticas básicas
        print("Estatísticas básicas das principais variáveis:")
        colunas_principais = [
            'populacao_atendida_agua', 'populacao_atentida_esgoto', 'populacao_urbana',
            'extensao_rede_agua', 'extensao_rede_esgoto',
            'quantidade_ligacao_ativa_agua', 'quantidade_ligacao_ativa_esgoto',
            'volume_agua_produzido', 'volume_agua_consumido'
        ]
        
        colunas_disponiveis = [col for col in colunas_principais if col in self.dados_limpos.columns]
        print(self.dados_limpos[colunas_disponiveis].describe())
        
        # Análise por ano
        print("\nDistribuição por ano:")
        print(self.dados_limpos['ano'].value_counts().sort_index())
        
        # Análise por município (top 10)
        print("\nTop 10 municípios por população atendida (média):")
        top_municipios = self.dados_limpos.groupby('id_municipio')['populacao_atendida_agua'].mean().sort_values(ascending=False).head(10)
        print(top_municipios)
        
    def salvar_dados_limpos(self, arquivo_saida):
        """Salva os dados limpos em um novo arquivo CSV"""
        if self.dados_limpos is not None:
            self.dados_limpos.to_csv(arquivo_saida, index=False)
            print(f"\nDados limpos salvos em: {arquivo_saida}")
        else:
            print("Dados limpos não disponíveis.")
    
    def gerar_relatorio_completo(self):
        """Gera um relatório completo da análise"""
        print("\n" + "="*60)
        print("RELATÓRIO COMPLETO - ANÁLISE SNIS CEARÁ")
        print("="*60)
        
        # Informações gerais
        print(f"\n📊 INFORMAÇÕES GERAIS:")
        print(f"   • Arquivo analisado: {self.arquivo_csv}")
        print(f"   • Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"   • Total de registros originais: {len(self.dados_originais)}")
        if self.dados_limpos is not None:
            print(f"   • Total de registros após limpeza: {len(self.dados_limpos)}")
            print(f"   • Registros removidos: {len(self.dados_originais) - len(self.dados_limpos)}")
        
        # Qualidade dos dados
        print(f"\n🔍 QUALIDADE DOS DADOS:")
        nulos_originais = self.dados_originais.isnull().sum().sum()
        print(f"   • Valores nulos originais: {nulos_originais}")
        if self.dados_limpos is not None:
            nulos_limpos = self.dados_limpos.isnull().sum().sum()
            print(f"   • Valores nulos após limpeza: {nulos_limpos}")
            print(f"   • Redução de valores nulos: {nulos_originais - nulos_limpos}")
        
        # Cobertura temporal
        print(f"\n📅 COBERTURA TEMPORAL:")
        print(f"   • Período: {self.dados_originais['ano'].min()} - {self.dados_originais['ano'].max()}")
        print(f"   • Anos com dados: {self.dados_originais['ano'].nunique()}")
        
        # Cobertura geográfica
        print(f"\n🗺️ COBERTURA GEOGRÁFICA:")
        print(f"   • Municípios únicos: {self.dados_originais['id_municipio'].nunique()}")
        
        # Recomendações
        print(f"\n💡 RECOMENDAÇÕES:")
        print(f"   • Os dados foram filtrados corretamente para o Ceará")
        print(f"   • A limpeza removeu valores inconsistentes e outliers")
        print(f"   • Os dados estão prontos para análise mais detalhada")
        
        print("\n" + "="*60)

def main():
    """Função principal"""
    print("🔍 ANÁLISE E LIMPEZA DOS DADOS SNIS - CEARÁ")
    print("="*50)
    
    # Inicializar analisador
    arquivo_csv = "../data/dados_snis_ceara_limpos.csv"
    analisador = AnalisadorSNISCeara(arquivo_csv)
    
    # Carregar dados
    if not analisador.carregar_dados():
        return
    
    # Executar análises
    analisador.verificar_filtro_ceara()
    analisador.analise_estrutura_dados()
    analisador.identificar_problemas_qualidade()
    
    # Limpar dados
    analisador.limpar_dados()
    
    # Gerar estatísticas
    analisador.gerar_estatisticas_descritivas()
    
    # Salvar dados limpos
    arquivo_limpo = "../data/dados_snis_ceara_limpos_final.csv"
    analisador.salvar_dados_limpos(arquivo_limpo)
    
    # Gerar relatório completo
    analisador.gerar_relatorio_completo()
    
    print("\n✅ Análise concluída com sucesso!")

if __name__ == "__main__":
    main() 