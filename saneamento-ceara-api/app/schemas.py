from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Schemas para Municípios
class MunicipioBase(BaseModel):
    id_municipio: str = Field(..., description="Código IBGE do município")
    nome: str = Field(..., description="Nome do município")
    sigla_uf: str = Field(..., description="Sigla do estado")
    populacao_urbana_estimada_2022: Optional[int] = Field(None, description="População urbana estimada em 2022")
    populacao_total_estimada_2022: Optional[int] = Field(None, description="População total estimada em 2022")
    quantidade_sedes_agua: Optional[int] = Field(None, description="Quantidade de sedes de água")
    quantidade_sedes_esgoto: Optional[int] = Field(None, description="Quantidade de sedes de esgoto")
    nome_prestador_predominante: Optional[str] = Field(None, description="Nome do prestador predominante")

class MunicipioCreate(MunicipioBase):
    pass

class Municipio(MunicipioBase):
    class Config:
        from_attributes = True

# Schemas para Prestadores de Serviço
class PrestadorServicoBase(BaseModel):
    sigla: str = Field(..., description="Sigla do prestador")
    nome: str = Field(..., description="Nome completo do prestador")
    natureza_juridica: Optional[str] = Field(None, description="Natureza jurídica")
    total_investido_historico: Optional[float] = Field(None, description="Total investido historicamente")
    media_arrecadacao_anual: Optional[float] = Field(None, description="Média de arrecadação anual")
    quantidade_municipios_atendidos: Optional[int] = Field(None, description="Quantidade de municípios atendidos")
    ano_primeiro_registro: Optional[int] = Field(None, description="Ano do primeiro registro")

class PrestadorServicoCreate(PrestadorServicoBase):
    pass

class PrestadorServico(PrestadorServicoBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Indicadores de Desempenho Anual
class IndicadoresDesempenhoBase(BaseModel):
    ano: int = Field(..., description="Ano de referência")
    municipio_id: str = Field(..., description="Código IBGE do município")
    prestador_id: int = Field(..., description="ID do prestador de serviço")
    
    # Dados populacionais
    populacao_atendida_agua: Optional[int] = Field(None, description="População atendida com água")
    populacao_atendida_esgoto: Optional[int] = Field(None, description="População atendida com esgoto")
    
    # Índices de desempenho
    indice_atendimento_agua: Optional[float] = Field(None, description="Índice de atendimento de água (%)")
    indice_coleta_esgoto: Optional[float] = Field(None, description="Índice de coleta de esgoto (%)")
    indice_tratamento_esgoto: Optional[float] = Field(None, description="Índice de tratamento de esgoto (%)")
    indice_perda_faturamento: Optional[float] = Field(None, description="Índice de perda de faturamento (%)")

class IndicadoresDesempenhoCreate(IndicadoresDesempenhoBase):
    pass

class IndicadoresDesempenho(IndicadoresDesempenhoBase):
    id: int
    municipio: Municipio
    prestador: PrestadorServico
    
    class Config:
        from_attributes = True

# Schemas para Recursos Hídricos Anual
class RecursosHidricosBase(BaseModel):
    indicador_id: int = Field(..., description="ID do indicador de desempenho")
    
    # Volumes de água
    volume_agua_produzido: Optional[float] = Field(None, description="Volume de água produzido (m³)")
    volume_agua_consumido: Optional[float] = Field(None, description="Volume de água consumido (m³)")
    volume_agua_faturado: Optional[float] = Field(None, description="Volume de água faturado (m³)")
    
    # Volumes de esgoto
    volume_esgoto_coletado: Optional[float] = Field(None, description="Volume de esgoto coletado (m³)")
    volume_esgoto_tratado: Optional[float] = Field(None, description="Volume de esgoto tratado (m³)")
    
    # Consumo energético
    consumo_eletrico_sistemas_agua: Optional[float] = Field(None, description="Consumo elétrico dos sistemas de água (kWh)")

class RecursosHidricosCreate(RecursosHidricosBase):
    pass

class RecursosHidricos(RecursosHidricosBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Financeiro Anual
class FinanceiroBase(BaseModel):
    indicador_id: int = Field(..., description="ID do indicador de desempenho")
    
    # Receitas
    receita_operacional_total: Optional[float] = Field(None, description="Receita operacional total (R$)")
    
    # Despesas
    despesa_exploracao: Optional[float] = Field(None, description="Despesa de exploração (R$)")
    despesa_pessoal: Optional[float] = Field(None, description="Despesa com pessoal (R$)")
    despesa_energia: Optional[float] = Field(None, description="Despesa com energia (R$)")
    despesa_total_servicos: Optional[float] = Field(None, description="Despesa total com serviços (R$)")
    
    # Investimentos
    investimento_total_prestador: Optional[float] = Field(None, description="Investimento total do prestador (R$)")
    
    # Contas a receber
    credito_a_receber: Optional[float] = Field(None, description="Crédito a receber (R$)")

class FinanceiroCreate(FinanceiroBase):
    pass

class Financeiro(FinanceiroBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para respostas da API
class IndicadoresCompleto(IndicadoresDesempenho):
    recursos_hidricos: Optional[RecursosHidricos] = None
    financeiro: Optional[Financeiro] = None

class HistoricoSaneamento(BaseModel):
    municipio: Municipio
    indicadores: List[IndicadoresCompleto]

class PosicaoEspecifica(BaseModel):
    municipio_id: str
    posicao: Optional[int] = None
    total: int
    valor: Optional[float] = None

class RankingItem(BaseModel):
    posicao: int
    municipio: dict
    valor: Optional[float] = None

class RankingResponse(BaseModel):
    ano: int
    indicador: str
    ranking: List[RankingItem]
    posicao_especifica: Optional[PosicaoEspecifica] = None  # Adicionar campo opcional

class EvolucaoIndicador(BaseModel):
    ano: int
    valor: float

class EvolucaoResponse(BaseModel):
    municipio: Municipio
    indicadores: dict[str, List[EvolucaoIndicador]]

class ComparativoItem(BaseModel):
    municipio: Municipio
    indicadores: IndicadoresCompleto

class ComparativoResponse(BaseModel):
    ano: int
    municipios: List[ComparativoItem]

class SustentabilidadeFinanceira(BaseModel):
    municipio: Municipio
    receita: float
    despesa: float
    saldo: float
    sustentavel: bool

class SustentabilidadeResponse(BaseModel):
    ano: int
    sustentaveis: List[SustentabilidadeFinanceira]
    insustentaveis: List[SustentabilidadeFinanceira]

# Schemas para análise de recursos hídricos
class EficienciaHidrica(BaseModel):
    municipio: Municipio
    indice_perda: float
    volume_produzido: float
    volume_faturado: float
    eficiencia: float

class EficienciaHidricaResponse(BaseModel):
    ano: int
    mais_eficientes: List[EficienciaHidrica]
    menos_eficientes: List[EficienciaHidrica] 