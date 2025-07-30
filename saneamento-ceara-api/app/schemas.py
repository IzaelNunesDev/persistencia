from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Schemas para Municípios
class MunicipioBase(BaseModel):
    id_municipio: str = Field(..., description="Código IBGE do município")
    nome: str = Field(..., description="Nome do município")
    microrregiao: Optional[str] = Field(None, description="Microrregião")
    mesorregiao: Optional[str] = Field(None, description="Mesorregião")
    ddd: Optional[str] = Field(None, description="DDD do município")

class MunicipioCreate(MunicipioBase):
    pass

class Municipio(MunicipioBase):
    class Config:
        from_attributes = True

# Schemas para Capitais
class CapitalBase(BaseModel):
    municipio_id: str = Field(..., description="Código IBGE do município")
    data_fundacao: Optional[date] = Field(None, description="Data de fundação")
    prefeito_atual: Optional[str] = Field(None, description="Nome do prefeito atual")

class CapitalCreate(CapitalBase):
    pass

class Capital(CapitalBase):
    id: int
    municipio: Municipio
    
    class Config:
        from_attributes = True

# Schemas para Prestadores de Serviço
class PrestadorServicoBase(BaseModel):
    sigla: str = Field(..., description="Sigla do prestador")
    nome: str = Field(..., description="Nome completo do prestador")
    natureza_juridica: Optional[str] = Field(None, description="Natureza jurídica")

class PrestadorServicoCreate(PrestadorServicoBase):
    pass

class PrestadorServico(PrestadorServicoBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Dados de Saneamento
class DadosSaneamentoBase(BaseModel):
    ano: int = Field(..., description="Ano de referência")
    municipio_id: str = Field(..., description="Código IBGE do município")
    prestador_id: int = Field(..., description="ID do prestador de serviço")
    
    # Dados populacionais
    populacao_total_atendida_agua: Optional[int] = Field(None, description="População total atendida com água")
    populacao_total_atendida_esgoto: Optional[int] = Field(None, description="População total atendida com esgoto")
    
    # Índices de atendimento
    indice_atendimento_agua: Optional[float] = Field(None, description="Índice de atendimento de água (%)")
    indice_coleta_esgoto: Optional[float] = Field(None, description="Índice de coleta de esgoto (%)")
    indice_tratamento_esgoto: Optional[float] = Field(None, description="Índice de tratamento de esgoto (%)")
    indice_perda_faturamento: Optional[float] = Field(None, description="Índice de perda de faturamento (%)")
    
    # Volumes
    volume_agua_produzido: Optional[float] = Field(None, description="Volume de água produzido (m³)")
    volume_esgoto_tratado: Optional[float] = Field(None, description="Volume de esgoto tratado (m³)")
    
    # Dados financeiros
    receita_operacional_total: Optional[float] = Field(None, description="Receita operacional total (R$)")
    despesa_total_servicos: Optional[float] = Field(None, description="Despesa total com serviços (R$)")
    investimento_total: Optional[float] = Field(None, description="Investimento total (R$)")

class DadosSaneamentoCreate(DadosSaneamentoBase):
    pass

class DadosSaneamento(DadosSaneamentoBase):
    id: int
    municipio: Municipio
    prestador: PrestadorServico
    
    class Config:
        from_attributes = True

# Schemas para respostas da API
class MunicipioComCapital(Municipio):
    capital: Optional[Capital] = None

class HistoricoSaneamento(BaseModel):
    municipio: Municipio
    dados: List[DadosSaneamento]

class RankingItem(BaseModel):
    posicao: int
    municipio: Municipio
    valor: float
    indicador: str

class RankingResponse(BaseModel):
    ano: int
    indicador: str
    ranking: List[RankingItem]

class EvolucaoIndicador(BaseModel):
    ano: int
    valor: float

class EvolucaoResponse(BaseModel):
    municipio: Municipio
    indicadores: dict[str, List[EvolucaoIndicador]]

class ComparativoItem(BaseModel):
    municipio: Municipio
    dados: DadosSaneamento

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