# API Analítica de Saneamento do Ceará com Dashboard Interativo

API RESTful completa para análise e consulta de dados do Sistema Nacional de Informações sobre Saneamento (SNIS) específicos do estado do Ceará, incluindo um dashboard interativo moderno.

## 📋 Descrição

Esta aplicação web completa fornece:
- **API RESTful** para consultar e analisar dados de saneamento básico dos 184 municípios do Ceará
- **Dashboard Interativo** com visualizações gráficas e análises em tempo real
- **Modelo de Dados Avançado** com 5 entidades bem estruturadas
- **Análises Complexas** de sustentabilidade, recursos hídricos e indicadores de desempenho

## 🏗️ Estrutura do Projeto

```
saneamento-ceara-api/
├── app/                    # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py            # Configuração FastAPI + Dashboard
│   ├── database.py        # Configuração do banco de dados
│   ├── models.py          # Modelos SQLAlchemy (5 entidades)
│   ├── schemas.py         # Schemas Pydantic
│   ├── crud.py            # Operações CRUD
│   ├── routers/           # Rotas da API
│   │   ├── __init__.py
│   │   ├── municipios.py  # Endpoints de municípios
│   │   ├── analises.py    # Endpoints de análises
│   │   └── dashboard.py   # Rotas do dashboard HTML
│   ├── templates/         # Templates HTML do dashboard
│   │   ├── base.html      # Template base
│   │   ├── index.html     # Página inicial
│   │   ├── analises.html  # Página de análises
│   │   └── municipio.html # Página de município
│   └── static/            # Arquivos estáticos
│       ├── css/
│       │   └── style.css  # Estilos customizados
│       └── js/
│           └── main.js    # JavaScript do dashboard
├── data/                  # Dados processados
│   └── dados_snis_ceara_limpos.csv
├── scripts/               # Scripts de processamento
│   ├── extract_data.py    # Extração e processamento de dados
│   ├── load_data.py       # Carregamento no banco de dados
│   └── analise_limpeza_dados.py # Análise e limpeza de dados
├── docs/                  # Documentação
│   ├── ANALISE_ABRANGENTE_SNIS_CEARA.md
│   └── RESUMO_EXECUTIVO_SNIS_CEARA.md
├── alembic/               # Migrações do banco de dados
├── requirements.txt       # Dependências Python
├── docker-compose.yml     # Configuração Docker
├── Dockerfile            # Imagem Docker
└── README.md             # Este arquivo
```

## 🗄️ Modelo de Dados (5 Entidades)

### 1. **Municipio** (Dimensão Geográfica)
- `id_municipio`, `nome`, `sigla_uf`, `populacao_urbana_estimada_2022`, `populacao_total_estimada_2022`, `quantidade_sedes_agua`, `quantidade_sedes_esgoto`, `nome_prestador_predominante`

### 2. **PrestadorServico** (Dimensão Organizacional)
- `id`, `sigla`, `nome`, `natureza_juridica`, `total_investido_historico`, `media_arrecadacao_anual`, `quantidade_municipios_atendidos`, `ano_primeiro_registro`

### 3. **IndicadoresDesempenhoAnual** (Tabela Fato Principal)
- `id`, `ano`, `municipio_id`, `prestador_id`, `populacao_atendida_agua`, `populacao_atendida_esgoto`, `indice_atendimento_agua`, `indice_coleta_esgoto`, `indice_tratamento_esgoto`, `indice_perda_faturamento`

### 4. **RecursosHidricosAnual** (Detalhes Operacionais)
- `id`, `indicador_id`, `volume_agua_produzido`, `volume_agua_consumido`, `volume_agua_faturado`, `volume_esgoto_coletado`, `volume_esgoto_tratado`, `consumo_eletrico_sistemas_agua`

### 5. **FinanceiroAnual** (Detalhes Financeiros)
- `id`, `indicador_id`, `receita_operacional_total`, `despesa_exploracao`, `despesa_pessoal`, `despesa_energia`, `despesa_total_servicos`, `investimento_total_prestador`, `credito_a_receber`

## 🚀 Como Rodar o Projeto

### ⚡ **Método Rápido (Recomendado) - Docker**

O projeto está configurado para rodar facilmente com Docker. Siga estes passos:

1. **Clone o repositório e entre na pasta**
```bash
git clone <url-do-repositorio>
cd saneamento-ceara-api
```

2. **Execute com Docker Compose**
```bash
# Subir os containers
docker-compose up --build -d

# Verificar se estão rodando
docker-compose ps
```

3. **Execute as migrações do banco de dados**
```bash
docker-compose exec api alembic upgrade head
```

4. **Carregue os dados**
```bash
docker-compose exec api python scripts/load_data.py
```

5. **Acesse o dashboard**
- **Dashboard Principal:** http://localhost:8000/dashboard
- **API Documentation:** http://localhost:8000/docs

### 🔧 **Método Local (Desenvolvimento)**

Se preferir rodar localmente:

1. **Pré-requisitos**
```bash
# Instale PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Crie o banco de dados
sudo -u postgres createdb saneamento_ceara
```

2. **Configure o ambiente Python**
```bash
# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
# DATABASE_URL=postgresql://usuario:senha@localhost/saneamento_ceara
```

4. **Execute as migrações**
```bash
alembic upgrade head
```

5. **Carregue os dados**
```bash
python scripts/load_data.py
```

6. **Execute a aplicação**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Como Acessar

### Dashboard Interativo
- **Página Inicial:** `http://localhost:8000/dashboard/`
- **Lista de Municípios:** `http://localhost:8000/dashboard/municipios`
- **Detalhes de Município:** `http://localhost:8000/dashboard/municipios/{id}`
- **Análises:** `http://localhost:8000/dashboard/analises`

### API RESTful
- **Informações da API:** `http://localhost:8000/api/v1`
- **Documentação Swagger:** `http://localhost:8000/docs`
- **Documentação ReDoc:** `http://localhost:8000/redoc`
- **Health Check:** `http://localhost:8000/health`

## 🔌 Endpoints da API

### Municípios
- `GET /api/v1/municipios/` - Lista todos os municípios
- `GET /api/v1/municipios/{id}` - Dados de um município específico
- `GET /api/v1/municipios/search?q={termo}` - Busca por nome
- `GET /api/v1/municipios/{id}/indicadores` - Indicadores de um município
- `GET /api/v1/municipios/{id}/evolucao` - Evolução temporal
- `GET /api/v1/municipios/{id}/recursos-hidricos` - Recursos hídricos
- `GET /api/v1/municipios/{id}/indicadores-financeiros` - Dados financeiros

### Análises
- `GET /api/v1/analises/ranking?indicador={tipo}&limit={n}` - Ranking por indicador
- `GET /api/v1/analises/evolucao?municipio_id={id}` - Evolução de município
- `GET /api/v1/analises/indicadores-principais` - Médias dos indicadores
- `GET /api/v1/analises/evolucao-temporal` - Evolução temporal geral
- `GET /api/v1/analises/comparativo` - Comparação entre municípios
- `GET /api/v1/analises/sustentabilidade-financeira` - Análise de sustentabilidade
- `GET /api/v1/analises/eficiencia-hidrica` - Eficiência hídrica

## 📊 Funcionalidades do Dashboard

### 📈 Visualizações Interativas
- **Gráficos de Linha** - Evolução temporal dos indicadores
- **Gráficos de Barras** - Comparação entre municípios
- **Gráficos de Pizza** - Distribuição de recursos financeiros
- **Cards de Indicadores** - Métricas principais em tempo real

### 🏆 Rankings e Comparações
- **Top 5 Municípios** - Melhores desempenhos por indicador
- **Posicionamento** - Ranking específico de cada município
- **Comparativo** - Análise lado a lado entre municípios

### 📊 Análises Avançadas
- **Sustentabilidade Financeira** - Receitas vs Despesas
- **Eficiência Hídrica** - Análise de perdas e eficiência
- **Evolução Temporal** - Tendências ao longo dos anos
- **Indicadores Principais** - Médias estaduais

## 🛠️ Comandos Úteis

### Docker
```bash
# Subir containers
docker-compose up -d

# Parar containers
docker-compose down

# Ver logs
docker-compose logs api

# Reconstruir
docker-compose up --build -d

# Executar comando no container
docker-compose exec api python scripts/load_data.py
```

### Banco de Dados
```bash
# Executar migrações
docker-compose exec api alembic upgrade head

# Carregar dados
docker-compose exec api python scripts/load_data.py

# Verificar dados carregados
docker-compose exec api python -c "from app.database import engine; from app.models import IndicadoresDesempenhoAnual; from sqlalchemy.orm import sessionmaker; Session = sessionmaker(bind=engine); session = Session(); print(f'Total de registros: {session.query(IndicadoresDesempenhoAnual).count()}')"
```

### Desenvolvimento
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar testes
pytest

# Formatar código
black app/

# Verificar tipos
mypy app/
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Alembic** - Migrações de banco de dados
- **Pydantic** - Validação de dados
- **Jinja2** - Templates HTML

### Frontend
- **Pico.css** - Framework CSS minimalista
- **Chart.js** - Gráficos interativos
- **JavaScript Vanilla** - Funcionalidades dinâmicas

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Uvicorn** - Servidor ASGI

## 📈 Principais Indicadores Analisados

- **Atendimento de Água** - Percentual da população atendida
- **Coleta de Esgoto** - Percentual da população com coleta
- **Tratamento de Esgoto** - Percentual do esgoto tratado
- **Perda de Faturamento** - Índice de perdas na distribuição
- **Recursos Hídricos** - Volumes produzidos, consumidos e faturados
- **Indicadores Financeiros** - Receitas, despesas e investimentos

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco de dados**
```bash
# Verificar se PostgreSQL está rodando
docker-compose logs db

# Recriar containers
docker-compose down -v
docker-compose up --build -d
```

2. **Dados não carregados**
```bash
# Verificar se o arquivo CSV existe
ls -la data/

# Executar carregamento novamente
docker-compose exec api python scripts/load_data.py
```

3. **Erro de migração**
```bash
# Resetar migrações
docker-compose exec api alembic downgrade base
docker-compose exec api alembic upgrade head
```

4. **Dashboard não carrega**
```bash
# Verificar logs da API
docker-compose logs api

# Verificar se Jinja2 está instalado
docker-compose exec api pip list | grep jinja
```

## 📚 Documentação

- **API Documentation:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Documentação Completa:** `docs/`

## 🎯 Status do Projeto

### ✅ **Funcionalidades Implementadas**
- ✅ API RESTful completa
- ✅ Dashboard interativo funcionando
- ✅ Banco de dados populado (2.257 registros)
- ✅ Rankings e análises funcionando
- ✅ Gráficos interativos
- ✅ Templates responsivos
- ✅ Docker configurado

### 📊 **Dados Disponíveis**
- **184 municípios** do Ceará
- **Dados de 2022** (ano mais recente)
- **5 indicadores principais** de saneamento
- **Análises comparativas** entre municípios

## 📝 Changelog

### v2.1.0 - Correções e Melhorias
- ✅ Corrigido parsing de JSON no frontend
- ✅ Corrigida estrutura de resposta da API
- ✅ Melhorado tratamento de valores NaN/None
- ✅ Corrigido carregamento de dados
- ✅ Adicionado Jinja2 para templates
- ✅ Dashboard 100% funcional

### v2.0.0 - Dashboard Interativo
- ✅ Dashboard HTML completo com Pico.css
- ✅ Gráficos interativos com Chart.js
- ✅ Modelo de dados atualizado (5 entidades)
- ✅ Análises avançadas de sustentabilidade
- ✅ Eficiência hídrica e recursos financeiros
- ✅ Templates responsivos e modernos
- ✅ JavaScript para funcionalidades dinâmicas

### v1.0.0 - API Base
- ✅ API FastAPI funcional
- ✅ Dados do SNIS processados e limpos
- ✅ Endpoints para consultas e análises
- ✅ Documentação completa
- ✅ Docker configurado

---

**🎉 O projeto está 100% funcional e pronto para uso!**