# API de Saneamento do Ceará

API REST para análise e consulta de dados do Sistema Nacional de Informações sobre Saneamento (SNIS) específicos do estado do Ceará.

## 📋 Descrição

Esta API fornece endpoints para consultar e analisar dados de saneamento básico dos 184 municípios do Ceará, incluindo informações sobre abastecimento de água, esgotamento sanitário, indicadores de qualidade e investimentos.

## 🏗️ Estrutura do Projeto

```
saneamento-ceara-api/
├── app/                    # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py            # Configuração FastAPI
│   ├── database.py        # Configuração do banco de dados
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Schemas Pydantic
│   ├── crud.py            # Operações CRUD
│   └── routers/           # Rotas da API
│       ├── __init__.py
│       ├── municipios.py  # Endpoints de municípios
│       └── analises.py    # Endpoints de análises
├── data/                  # Dados processados
│   └── dados_snis_ceara_limpos.csv
├── scripts/               # Scripts de processamento
│   ├── extract_data.py    # Extração e processamento de dados
│   ├── load_data.py       # Carregamento no banco de dados
│   └── analise_limpeza_dados.py
├── docs/                  # Documentação
│   └── DOCUMENTACAO_ANALISE_SNIS_CEARA.md
├── alembic/               # Migrações do banco de dados
├── requirements.txt       # Dependências Python
├── docker-compose.yml     # Configuração Docker
├── Dockerfile            # Imagem Docker
└── README.md             # Este arquivo
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- Docker (opcional)

### Instalação Local

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd saneamento-ceara-api
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Configure o banco de dados**
```bash
# Execute as migrações
alembic upgrade head

# Carregue os dados
python scripts/load_data.py
```

6. **Execute a aplicação**
```bash
uvicorn app.main:app --reload
```

### Instalação com Docker

```bash
# Construa e execute com Docker Compose
docker-compose up --build
```

## 📊 Dados

### Fonte dos Dados
- **SNIS**: Sistema Nacional de Informações sobre Saneamento
- **Período**: 2010-2022
- **Cobertura**: 184 municípios do Ceará
- **Variáveis**: 133 indicadores de saneamento

### Processamento dos Dados
Os dados passaram por um processo completo de limpeza e validação:

1. **Filtro por Estado**: Apenas dados do Ceará
2. **Limpeza**: Remoção de outliers e inconsistências
3. **Validação**: Verificação de integridade dos dados
4. **Documentação**: Relatório completo de qualidade

Veja a documentação detalhada em: `docs/DOCUMENTACAO_ANALISE_SNIS_CEARA.md`

## 🔌 Endpoints da API

### Municípios
- `GET /municipios/` - Lista todos os municípios
- `GET /municipios/{id}` - Dados de um município específico
- `GET /municipios/search?nome={nome}` - Busca por nome

### Análises
- `GET /analises/indicadores/{municipio_id}` - Indicadores de um município
- `GET /analises/comparacao/{municipio1}/{municipio2}` - Comparação entre municípios
- `GET /analises/ranking/{indicador}` - Ranking por indicador
- `GET /analises/evolucao/{municipio_id}` - Evolução temporal

### Estatísticas
- `GET /stats/geral` - Estatísticas gerais
- `GET /stats/municipios` - Estatísticas por município
- `GET /stats/indicadores` - Estatísticas por indicador

## 📈 Principais Indicadores

- **População Atendida**: Água e esgoto
- **Índices de Atendimento**: Percentual da população atendida
- **Qualidade**: Índices de perda, tratamento, etc.
- **Financeiro**: Receitas, despesas e investimentos
- **Infraestrutura**: Extensão de redes, ligações, etc.

## 🛠️ Desenvolvimento

### Scripts Disponíveis

- `scripts/extract_data.py`: Extrai e processa dados do SNIS
- `scripts/load_data.py`: Carrega dados no banco
- `scripts/analise_limpeza_dados.py`: Análise e limpeza de dados

### Estrutura do Banco de Dados

- **Municipio**: Informações dos municípios
- **DadosSaneamentoAnual**: Dados anuais de saneamento
- **PrestadorServico**: Prestadores de serviços

### Testes

```bash
# Execute os testes
pytest

# Com cobertura
pytest --cov=app
```

## 📚 Documentação da API

A documentação interativa está disponível em:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

- **Projeto**: API de Saneamento do Ceará
- **Dados**: SNIS (Sistema Nacional de Informações sobre Saneamento)
- **Cobertura**: Estado do Ceará (184 municípios)

## 🔄 Changelog

### v1.0.0
- ✅ API FastAPI funcional
- ✅ Dados do SNIS processados e limpos
- ✅ Endpoints para consultas e análises
- ✅ Documentação completa
- ✅ Docker configurado
- ✅ Estrutura organizada

---

*Desenvolvido com ❤️ para análise de dados de saneamento do Ceará* 