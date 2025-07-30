from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date

# Schemas para Municípios
class MunicipioBase(BaseModel):
    id_municipio: str = Field(..., min_length=7, max_length=7, description="Código IBGE do município")
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do município")
    sigla_uf: str = Field(..., min_length=2, max_length=2, description="Sigla do estado")
    populacao_urbana_estimada_2022: Optional[int] = Field(None, ge=0, description="População urbana estimada em 2022")
    populacao_total_estimada_2022: Optional[int] = Field(None, ge=0, description="População total estimada em 2022")
    quantidade_sedes_agua: Optional[int] = Field(None, ge=0, description="Quantidade de sedes de água")
    quantidade_sedes_esgoto: Optional[int] = Field(None, ge=0, description="Quantidade de sedes de esgoto")
    nome_prestador_predominante: Optional[str] = Field(None, max_length=255, description="Nome do prestador predominante")

    @validator('sigla_uf')
    def validate_sigla_uf(cls, v):
        if v.upper() != 'CE':
            raise ValueError('Apenas municípios do Ceará são suportados')
        return v.upper()

class MunicipioCreate(MunicipioBase):
    pass

class MunicipioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    populacao_urbana_estimada_2022: Optional[int] = Field(None, ge=0)
    populacao_total_estimada_2022: Optional[int] = Field(None, ge=0)
    quantidade_sedes_agua: Optional[int] = Field(None, ge=0)
    quantidade_sedes_esgoto: Optional[int] = Field(None, ge=0)
    nome_prestador_predominante: Optional[str] = Field(None, max_length=255)

class Municipio(MunicipioBase):
    class Config:
        from_attributes = True

class MunicipioList(BaseModel):
    id_municipio: str
    nome: str
    sigla_uf: str
    populacao_total_estimada_2022: Optional[int]
    quantidade_sedes_agua: Optional[int]
    quantidade_sedes_esgoto: Optional[int]
    nome_prestador_predominante: Optional[str]

    class Config:
        from_attributes = True

# Schemas para Prestadores de Serviço
class PrestadorServicoBase(BaseModel):
    sigla: str = Field(..., min_length=1, max_length=20, description="Sigla do prestador")
    nome: str = Field(..., min_length=1, max_length=255, description="Nome completo do prestador")
    natureza_juridica: Optional[str] = Field(None, max_length=100, description="Natureza jurídica")
    total_investido_historico: Optional[float] = Field(None, ge=0, description="Total investido historicamente")
    media_arrecadacao_anual: Optional[float] = Field(None, ge=0, description="Média de arrecadação anual")
    quantidade_municipios_atendidos: Optional[int] = Field(None, ge=0, description="Quantidade de municípios atendidos")
    ano_primeiro_registro: Optional[int] = Field(None, ge=1900, le=2100, description="Ano do primeiro registro")

class PrestadorServicoCreate(PrestadorServicoBase):
    pass

class PrestadorServicoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    natureza_juridica: Optional[str] = Field(None, max_length=100)
    total_investido_historico: Optional[float] = Field(None, ge=0)
    media_arrecadacao_anual: Optional[float] = Field(None, ge=0)
    quantidade_municipios_atendidos: Optional[int] = Field(None, ge=0)
    ano_primeiro_registro: Optional[int] = Field(None, ge=1900, le=2100)

class PrestadorServico(PrestadorServicoBase):
    id: int
    
    class Config:
        from_attributes = True

class PrestadorServicoList(BaseModel):
    id: int
    sigla: str
    nome: str
    natureza_juridica: Optional[str]
    quantidade_municipios_atendidos: Optional[int]
    ano_primeiro_registro: Optional[int]

    class Config:
        from_attributes = True

# Schemas para Indicadores de Desempenho Anual
class IndicadoresDesempenhoBase(BaseModel):
    ano: int = Field(..., ge=1900, le=2100, description="Ano de referência")
    municipio_id: str = Field(..., min_length=7, max_length=7, description="Código IBGE do município")
    prestador_id: int = Field(..., gt=0, description="ID do prestador de serviço")
    
    # Dados populacionais
    populacao_atendida_agua: Optional[int] = Field(None, ge=0, description="População atendida com água")
    populacao_atendida_esgoto: Optional[int] = Field(None, ge=0, description="População atendida com esgoto")
    
    # Índices de desempenho
    indice_atendimento_agua: Optional[float] = Field(None, ge=0, le=100, description="Índice de atendimento de água (%)")
    indice_coleta_esgoto: Optional[float] = Field(None, ge=0, le=100, description="Índice de coleta de esgoto (%)")
    indice_tratamento_esgoto: Optional[float] = Field(None, ge=0, le=100, description="Índice de tratamento de esgoto (%)")
    indice_perda_faturamento: Optional[float] = Field(None, ge=0, le=100, description="Índice de perda de faturamento (%)")

class IndicadoresDesempenhoCreate(IndicadoresDesempenhoBase):
    pass

class IndicadoresDesempenhoUpdate(BaseModel):
    populacao_atendida_agua: Optional[int] = Field(None, ge=0)
    populacao_atendida_esgoto: Optional[int] = Field(None, ge=0)
    indice_atendimento_agua: Optional[float] = Field(None, ge=0, le=100)
    indice_coleta_esgoto: Optional[float] = Field(None, ge=0, le=100)
    indice_tratamento_esgoto: Optional[float] = Field(None, ge=0, le=100)
    indice_perda_faturamento: Optional[float] = Field(None, ge=0, le=100)

class IndicadoresDesempenho(IndicadoresDesempenhoBase):
    id: int
    municipio: Municipio
    prestador: PrestadorServico
    
    class Config:
        from_attributes = True

class IndicadoresDesempenhoList(BaseModel):
    id: int
    ano: int
    municipio_id: str
    prestador_id: int
    populacao_atendida_agua: Optional[int]
    populacao_atendida_esgoto: Optional[int]
    indice_atendimento_agua: Optional[float]
    indice_coleta_esgoto: Optional[float]
    indice_tratamento_esgoto: Optional[float]
    indice_perda_faturamento: Optional[float]
    municipio: MunicipioList
    prestador: PrestadorServicoList

    class Config:
        from_attributes = True

# Schemas para Recursos Hídricos Anual
class RecursosHidricosBase(BaseModel):
    indicador_id: int = Field(..., gt=0, description="ID do indicador de desempenho")
    
    # Volumes de água
    volume_agua_produzido: Optional[float] = Field(None, ge=0, description="Volume de água produzido (m³)")
    volume_agua_consumido: Optional[float] = Field(None, ge=0, description="Volume de água consumido (m³)")
    volume_agua_faturado: Optional[float] = Field(None, ge=0, description="Volume de água faturado (m³)")
    
    # Volumes de esgoto
    volume_esgoto_coletado: Optional[float] = Field(None, ge=0, description="Volume de esgoto coletado (m³)")
    volume_esgoto_tratado: Optional[float] = Field(None, ge=0, description="Volume de esgoto tratado (m³)")
    
    # Consumo energético
    consumo_eletrico_sistemas_agua: Optional[float] = Field(None, ge=0, description="Consumo elétrico dos sistemas de água (kWh)")

class RecursosHidricosCreate(RecursosHidricosBase):
    pass

class RecursosHidricosUpdate(BaseModel):
    volume_agua_produzido: Optional[float] = Field(None, ge=0)
    volume_agua_consumido: Optional[float] = Field(None, ge=0)
    volume_agua_faturado: Optional[float] = Field(None, ge=0)
    volume_esgoto_coletado: Optional[float] = Field(None, ge=0)
    volume_esgoto_tratado: Optional[float] = Field(None, ge=0)
    consumo_eletrico_sistemas_agua: Optional[float] = Field(None, ge=0)

class RecursosHidricos(RecursosHidricosBase):
    id: int
    
    class Config:
        from_attributes = True

class RecursosHidricosList(BaseModel):
    id: int
    indicador_id: int
    volume_agua_produzido: Optional[float]
    volume_agua_consumido: Optional[float]
    volume_agua_faturado: Optional[float]
    volume_esgoto_coletado: Optional[float]
    volume_esgoto_tratado: Optional[float]
    consumo_eletrico_sistemas_agua: Optional[float]

    class Config:
        from_attributes = True

# Schemas para Financeiro Anual
class FinanceiroBase(BaseModel):
    indicador_id: int = Field(..., gt=0, description="ID do indicador de desempenho")
    
    # Receitas
    receita_operacional_total: Optional[float] = Field(None, ge=0, description="Receita operacional total (R$)")
    
    # Despesas
    despesa_exploracao: Optional[float] = Field(None, ge=0, description="Despesa de exploração (R$)")
    despesa_pessoal: Optional[float] = Field(None, ge=0, description="Despesa com pessoal (R$)")
    despesa_energia: Optional[float] = Field(None, ge=0, description="Despesa com energia (R$)")
    despesa_total_servicos: Optional[float] = Field(None, ge=0, description="Despesa total com serviços (R$)")
    
    # Investimentos
    investimento_total_prestador: Optional[float] = Field(None, ge=0, description="Investimento total do prestador (R$)")
    
    # Contas a receber
    credito_a_receber: Optional[float] = Field(None, ge=0, description="Crédito a receber (R$)")

class FinanceiroCreate(FinanceiroBase):
    pass

class FinanceiroUpdate(BaseModel):
    receita_operacional_total: Optional[float] = Field(None, ge=0)
    despesa_exploracao: Optional[float] = Field(None, ge=0)
    despesa_pessoal: Optional[float] = Field(None, ge=0)
    despesa_energia: Optional[float] = Field(None, ge=0)
    despesa_total_servicos: Optional[float] = Field(None, ge=0)
    investimento_total_prestador: Optional[float] = Field(None, ge=0)
    credito_a_receber: Optional[float] = Field(None, ge=0)

class Financeiro(FinanceiroBase):
    id: int
    
    class Config:
        from_attributes = True

class FinanceiroList(BaseModel):
    id: int
    indicador_id: int
    receita_operacional_total: Optional[float]
    despesa_exploracao: Optional[float]
    despesa_pessoal: Optional[float]
    despesa_energia: Optional[float]
    despesa_total_servicos: Optional[float]
    investimento_total_prestador: Optional[float]
    credito_a_receber: Optional[float]

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

# Schemas para filtros e paginação
class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros a retornar")

class MunicipioFilters(BaseModel):
    nome: Optional[str] = Field(None, description="Filtrar por nome do município")
    populacao_min: Optional[int] = Field(None, ge=0, description="População mínima")
    populacao_max: Optional[int] = Field(None, ge=0, description="População máxima")
    order_by: Optional[str] = Field(None, description="Campo para ordenação")
    order_direction: str = Field("asc", pattern="^(asc|desc)$", description="Direção da ordenação")

class IndicadoresFilters(BaseModel):
    ano_inicio: Optional[int] = Field(None, ge=1900, le=2100, description="Ano inicial")
    ano_fim: Optional[int] = Field(None, ge=1900, le=2100, description="Ano final")
    prestador_id: Optional[int] = Field(None, gt=0, description="ID do prestador")
    order_by: Optional[str] = Field(None, description="Campo para ordenação")
    order_direction: str = Field("asc", pattern="^(asc|desc)$", description="Direção da ordenação")

class PrestadorFilters(BaseModel):
    nome: Optional[str] = Field(None, description="Filtrar por nome do prestador")
    sigla: Optional[str] = Field(None, description="Filtrar por sigla")
    natureza_juridica: Optional[str] = Field(None, description="Filtrar por natureza jurídica")
    order_by: Optional[str] = Field(None, description="Campo para ordenação")
    order_direction: str = Field("asc", pattern="^(asc|desc)$", description="Direção da ordenação") 