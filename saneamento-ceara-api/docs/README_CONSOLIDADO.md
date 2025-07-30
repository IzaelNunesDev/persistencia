# 📊 Projeto Saneamento Ceará - Documentação Consolidada

## 🎯 Visão Geral

Este projeto realiza uma análise abrangente dos dados do Sistema Nacional de Informações sobre Saneamento (SNIS) específicos do estado do Ceará, fornecendo uma API RESTful completa e um dashboard interativo para análise de dados de saneamento básico.

## 📈 Principais Descobertas da Análise

### 🔍 **Gap Crítico de Cobertura**
- **Problema**: Diferença de 38.5 pontos percentuais entre água (77.7%) e esgoto (39.3%)
- **Impacto**: Risco sanitário e ambiental significativo
- **Urgência**: Necessidade de investimentos prioritários em esgotamento sanitário

### ⚖️ **Alta Desigualdade Regional**
- **Coeficiente de variação**: 181.6% (água) e 381.0% (esgoto)
- **Implicação**: Grandes disparidades entre municípios
- **Municípios críticos**: 25+ municípios com cobertura abaixo de 50%

### 📊 **Crescimento Positivo mas Insuficiente**
- **Água**: 15.3% de crescimento (2010-2022)
- **Esgoto**: 12.83% de crescimento no mesmo período
- **Análise**: Taxas insuficientes para universalização até 2030

### 💧 **Desafios Operacionais**
- **Perdas de água**: 5 municípios com perdas superiores a 50%
- **Eficiência**: Oportunidades de melhoria na gestão operacional
- **Impacto financeiro**: Perdas significativas de recursos

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
│   ├── RESUMO_EXECUTIVO_SNIS_CEARA.md
│   └── README_CONSOLIDADO.md
├── alembic/               # Migrações do banco de dados
├── requirements.txt       # Dependências Python
├── docker-compose.yml     # Configuração Docker
├── Dockerfile            # Imagem Docker
└── README.md             # Documentação principal
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

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.10+
- PostgreSQL 14+
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
pip install jinja2  # Para templates HTML
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

# Carregue os dados (se disponível)
python scripts/load_data.py
```

6. **Execute a aplicação**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Instalação com Docker

```bash
# Construa e execute com Docker Compose
docker-compose up --build
```

## 🌐 Como Acessar

### Dashboard Interativo
- **Página Inicial:** `http://localhost:8000/dashboard/`
- **Lista de Municípios:** `http://localhost:8000/dashboard/municipios`
- **Detalhes de Município:** `http://localhost:8000/dashboard/municipios/{id}`
- **Análises:** `http://localhost:8000/dashboard/analises`
- **Comparativo:** `http://localhost:8000/dashboard/comparativo`
- **Sustentabilidade:** `http://localhost:8000/dashboard/sustentabilidade`
- **Recursos Hídricos:** `http://localhost:8000/dashboard/recursos-hidricos`

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

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Alembic** - Migrações de banco de dados
- **Pydantic** - Validação de dados

### Frontend
- **Jinja2** - Templates HTML
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

## 🛠️ Desenvolvimento

### Scripts Disponíveis

- `scripts/extract_data.py`: Extrai e processa dados do SNIS
- `scripts/load_data.py`: Carrega dados no banco
- `scripts/analise_limpeza_dados.py`: Análise e limpeza de dados

### Estrutura do Banco de Dados

- **Municipio**: Informações dos municípios
- **PrestadorServico**: Prestadores de serviços
- **IndicadoresDesempenhoAnual**: Dados anuais de desempenho
- **RecursosHidricosAnual**: Dados de recursos hídricos
- **FinanceiroAnual**: Dados financeiros

### Migrações

```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

## 📚 Documentação

- **API Documentation:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Documentação Completa:** `docs/`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🔄 Changelog

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

*Desenvolvido com ❤️ para análise de dados de saneamento do Ceará* 