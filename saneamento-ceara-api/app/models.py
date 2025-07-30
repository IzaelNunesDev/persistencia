from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class Municipio(Base):
    __tablename__ = "municipios"
    
    id_municipio = Column(String(7), primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    sigla_uf = Column(String(2), nullable=False, default="CE")
    populacao_urbana_estimada_2022 = Column(Integer)
    populacao_total_estimada_2022 = Column(Integer)
    quantidade_sedes_agua = Column(Integer)
    quantidade_sedes_esgoto = Column(Integer)
    nome_prestador_predominante = Column(String(255))
    
    # Relacionamentos
    indicadores = relationship("IndicadoresDesempenhoAnual", back_populates="municipio")

class PrestadorServico(Base):
    __tablename__ = "prestadores_servico"
    
    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(20), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    natureza_juridica = Column(String(100))
    total_investido_historico = Column(Float)
    media_arrecadacao_anual = Column(Float)
    quantidade_municipios_atendidos = Column(Integer)
    ano_primeiro_registro = Column(Integer)
    
    # Relacionamentos
    indicadores = relationship("IndicadoresDesempenhoAnual", back_populates="prestador")

class IndicadoresDesempenhoAnual(Base):
    __tablename__ = "indicadores_desempenho_anuais"
    
    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False)
    municipio_id = Column(String(7), ForeignKey("municipios.id_municipio"), nullable=False)
    prestador_id = Column(Integer, ForeignKey("prestadores_servico.id"), nullable=False)
    
    # Dados populacionais
    populacao_atendida_agua = Column(Integer)
    populacao_atendida_esgoto = Column(Integer)
    
    # Índices de desempenho
    indice_atendimento_agua = Column(Float)
    indice_coleta_esgoto = Column(Float)
    indice_tratamento_esgoto = Column(Float)
    indice_perda_faturamento = Column(Float)
    
    # Relacionamentos
    municipio = relationship("Municipio", back_populates="indicadores")
    prestador = relationship("PrestadorServico", back_populates="indicadores")
    recursos_hidricos = relationship("RecursosHidricosAnual", back_populates="indicador", uselist=False)
    financeiro = relationship("FinanceiroAnual", back_populates="indicador", uselist=False)
    
    # Índices para otimização
    __table_args__ = (
        Index('idx_municipio_ano', 'municipio_id', 'ano'),
        Index('idx_prestador_ano', 'prestador_id', 'ano'),
        Index('idx_ano', 'ano'),
        UniqueConstraint('ano', 'municipio_id', 'prestador_id', name='uq_ano_municipio_prestador')
    )

class RecursosHidricosAnual(Base):
    __tablename__ = "recursos_hidricos_anuais"
    
    id = Column(Integer, primary_key=True, index=True)
    indicador_id = Column(Integer, ForeignKey("indicadores_desempenho_anuais.id"), unique=True, nullable=False)
    
    # Volumes de água
    volume_agua_produzido = Column(Float)
    volume_agua_consumido = Column(Float)
    volume_agua_faturado = Column(Float)
    
    # Volumes de esgoto
    volume_esgoto_coletado = Column(Float)
    volume_esgoto_tratado = Column(Float)
    
    # Consumo energético
    consumo_eletrico_sistemas_agua = Column(Float)
    
    # Relacionamentos
    indicador = relationship("IndicadoresDesempenhoAnual", back_populates="recursos_hidricos")

class FinanceiroAnual(Base):
    __tablename__ = "financeiro_anuais"
    
    id = Column(Integer, primary_key=True, index=True)
    indicador_id = Column(Integer, ForeignKey("indicadores_desempenho_anuais.id"), unique=True, nullable=False)
    
    # Receitas
    receita_operacional_total = Column(Float)
    
    # Despesas
    despesa_exploracao = Column(Float)
    despesa_pessoal = Column(Float)
    despesa_energia = Column(Float)
    despesa_total_servicos = Column(Float)
    
    # Investimentos
    investimento_total_prestador = Column(Float)
    
    # Contas a receber
    credito_a_receber = Column(Float)
    
    # Relacionamentos
    indicador = relationship("IndicadoresDesempenhoAnual", back_populates="financeiro") 