from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class Municipio(Base):
    __tablename__ = "municipios"
    
    id_municipio = Column(String(7), primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    microrregiao = Column(String(100))
    mesorregiao = Column(String(100))
    ddd = Column(String(2))
    
    # Relacionamentos
    capital = relationship("Capital", back_populates="municipio", uselist=False)
    dados_saneamento = relationship("DadosSaneamentoAnual", back_populates="municipio")

class Capital(Base):
    __tablename__ = "capitais"
    
    id = Column(Integer, primary_key=True, index=True)
    municipio_id = Column(String(7), ForeignKey("municipios.id_municipio"), unique=True, nullable=False)
    data_fundacao = Column(Date)
    prefeito_atual = Column(String(100))
    
    # Relacionamentos
    municipio = relationship("Municipio", back_populates="capital")

class PrestadorServico(Base):
    __tablename__ = "prestadores_servico"
    
    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(20), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    natureza_juridica = Column(String(100))
    
    # Relacionamentos
    dados_saneamento = relationship("DadosSaneamentoAnual", back_populates="prestador")

class DadosSaneamentoAnual(Base):
    __tablename__ = "dados_saneamento_anuais"
    
    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False)
    municipio_id = Column(String(7), ForeignKey("municipios.id_municipio"), nullable=False)
    prestador_id = Column(Integer, ForeignKey("prestadores_servico.id"), nullable=False)
    
    # Dados populacionais
    populacao_total_atendida_agua = Column(Integer)
    populacao_total_atendida_esgoto = Column(Integer)
    
    # Índices de atendimento
    indice_atendimento_agua = Column(Float)
    indice_coleta_esgoto = Column(Float)
    indice_tratamento_esgoto = Column(Float)
    indice_perda_faturamento = Column(Float)
    
    # Volumes
    volume_agua_produzido = Column(Float)
    volume_esgoto_tratado = Column(Float)
    
    # Dados financeiros
    receita_operacional_total = Column(Float)
    despesa_total_servicos = Column(Float)
    investimento_total = Column(Float)
    
    # Relacionamentos
    municipio = relationship("Municipio", back_populates="dados_saneamento")
    prestador = relationship("PrestadorServico", back_populates="dados_saneamento")
    
    # Índices para otimização
    __table_args__ = (
        Index('idx_municipio_ano', 'municipio_id', 'ano'),
        Index('idx_ano', 'ano'),
        UniqueConstraint('ano', 'municipio_id', 'prestador_id', name='uq_ano_municipio_prestador')
    ) 