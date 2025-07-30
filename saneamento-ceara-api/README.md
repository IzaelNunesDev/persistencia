# API de Análise de Saneamento do Ceará

API RESTful para análise de dados de saneamento básico no Ceará baseada no SNIS (Sistema Nacional de Informações sobre Saneamento).

## 🚀 Status do Projeto

✅ **Refatoração Completa**: API totalmente refatorada e funcionando
- ✅ Separação da camada web (Dashboard) da API
- ✅ Schemas Pydantic melhorados com validações rigorosas
- ✅ Sistema de filtros avançados implementado
- ✅ Endpoints CRUD completos para todas as 5 entidades
- ✅ Sistema de logs detalhado implementado
- ✅ Migrações de banco de dados configuradas
- ✅ Script de gerenciamento criado

## 📊 Entidades da API

A API gerencia 5 entidades principais:

1. **Municípios** (`/api/v1/municipios/`)
   - Dados demográficos e informações básicas dos municípios do Ceará
   - Filtros: nome, população (min/max), ordenação customizada

2. **Prestadores de Serviço** (`/api/v1/prestadores/`)
   - Empresas e organizações que prestam serviços de saneamento
   - Filtros: nome, sigla, natureza jurídica

3. **Indicadores de Desempenho** (`/api/v1/indicadores/`)
   - Métricas anuais de desempenho do saneamento
   - Filtros: ano, município, prestador, ordenação

4. **Recursos Hídricos** (`/api/v1/recursos-hidricos/`)
   - Dados sobre produção e consumo de água
   - Filtros: volume, indicador relacionado

5. **Financeiro** (`/api/v1/financeiro/`)
   - Informações financeiras e de investimento
   - Filtros: receita, indicador relacionado

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Git

### Configuração Rápida

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd saneamento-ceara-api
   ```

2. **Configure o projeto** (automático):
   ```bash
   python scripts/manage.py setup
   ```

3. **Inicie a API**:
   ```bash
   python scripts/manage.py start
   ```

### Configuração Manual

1. **Crie o ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o banco de dados**:
   ```bash
   docker-compose up -d db
   ```

4. **Execute as migrações**:
   ```bash
   alembic upgrade head
   ```

5. **Inicie a API**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📋 Comandos de Gerenciamento

O projeto inclui um script de gerenciamento para facilitar operações comuns:

```bash
# Configuração completa do projeto
python scripts/manage.py setup

# Iniciar API
python scripts/manage.py start

# Parar banco de dados
python scripts/manage.py stop

# Executar migrações
python scripts/manage.py migrate

# Verificar saúde da API
python scripts/manage.py health

# Visualizar logs
python scripts/manage.py logs

# Gerenciar banco de dados
python scripts/manage.py db-start
python scripts/manage.py db-stop
```

## 🔗 Endpoints da API

### Endpoints Principais

- `GET /` - Informações da API
- `GET /health` - Verificação de saúde
- `GET /docs` - Documentação Swagger
- `GET /redoc` - Documentação ReDoc

### Endpoints de Entidades

#### Municípios
- `GET /api/v1/municipios/` - Listar municípios
- `GET /api/v1/municipios/{id}` - Obter município específico
- `POST /api/v1/municipios/` - Criar município
- `PUT /api/v1/municipios/{id}` - Atualizar município
- `DELETE /api/v1/municipios/{id}` - Excluir município
- `GET /api/v1/municipios/{id}/indicadores` - Indicadores do município

#### Prestadores
- `GET /api/v1/prestadores/` - Listar prestadores
- `GET /api/v1/prestadores/{id}` - Obter prestador específico
- `GET /api/v1/prestadores/sigla/{sigla}` - Buscar por sigla
- `POST /api/v1/prestadores/` - Criar prestador
- `PUT /api/v1/prestadores/{id}` - Atualizar prestador
- `DELETE /api/v1/prestadores/{id}` - Excluir prestador
- `GET /api/v1/prestadores/{id}/indicadores` - Indicadores do prestador

#### Indicadores
- `GET /api/v1/indicadores/` - Listar indicadores
- `GET /api/v1/indicadores/{id}` - Obter indicador específico
- `POST /api/v1/indicadores/` - Criar indicador
- `PUT /api/v1/indicadores/{id}` - Atualizar indicador
- `DELETE /api/v1/indicadores/{id}` - Excluir indicador
- `GET /api/v1/indicadores/{id}/recursos-hidricos` - Recursos hídricos relacionados
- `GET /api/v1/indicadores/{id}/financeiro` - Dados financeiros relacionados

#### Recursos Hídricos
- `GET /api/v1/recursos-hidricos/` - Listar recursos hídricos
- `GET /api/v1/recursos-hidricos/{id}` - Obter recurso específico
- `GET /api/v1/recursos-hidricos/indicador/{indicador_id}` - Por indicador
- `POST /api/v1/recursos-hidricos/` - Criar recurso
- `PUT /api/v1/recursos-hidricos/{id}` - Atualizar recurso
- `DELETE /api/v1/recursos-hidricos/{id}` - Excluir recurso
- `GET /api/v1/recursos-hidricos/estatisticas/volume-agua` - Estatísticas

#### Financeiro
- `GET /api/v1/financeiro/` - Listar dados financeiros
- `GET /api/v1/financeiro/{id}` - Obter dados específicos
- `GET /api/v1/financeiro/indicador/{indicador_id}` - Por indicador
- `POST /api/v1/financeiro/` - Criar dados financeiros
- `PUT /api/v1/financeiro/{id}` - Atualizar dados
- `DELETE /api/v1/financeiro/{id}` - Excluir dados
- `GET /api/v1/financeiro/estatisticas/receitas-despesas` - Estatísticas
- `GET /api/v1/financeiro/sustentabilidade/{ano}` - Análise de sustentabilidade

### Endpoints de Análise
- `GET /api/v1/analises/ranking/{indicador}` - Ranking de municípios
- `GET /api/v1/analises/evolucao/{municipio_id}` - Evolução temporal
- `GET /api/v1/analises/comparativo/{ano}` - Comparativo anual
- `GET /api/v1/analises/sustentabilidade/{ano}` - Análise de sustentabilidade
- `GET /api/v1/analises/recursos-hidricos/{ano}` - Análise de recursos hídricos

## 🔍 Filtros Disponíveis

### Municípios
- `nome` - Filtrar por nome (busca parcial)
- `populacao_min` - População mínima
- `populacao_max` - População máxima
- `order_by` - Campo para ordenação
- `order_direction` - Direção da ordenação (asc/desc)

### Indicadores
- `ano_inicio` - Ano inicial do período
- `ano_fim` - Ano final do período
- `municipio_id` - Filtrar por município
- `prestador_id` - Filtrar por prestador
- `order_by` - Campo para ordenação
- `order_direction` - Direção da ordenação

### Prestadores
- `nome` - Filtrar por nome
- `sigla` - Filtrar por sigla
- `natureza_juridica` - Filtrar por natureza jurídica
- `order_by` - Campo para ordenação
- `order_direction` - Direção da ordenação

## 📝 Logs

A aplicação gera logs detalhados em:

- `logs/api.log` - Logs gerais da aplicação
- `logs/errors.log` - Logs de erros

Os logs incluem:
- Requisições HTTP com duração
- Operações de banco de dados
- Informações de performance
- Erros e exceções

## 🗄️ Banco de Dados

- **Sistema**: PostgreSQL 14
- **Container**: Docker
- **Migrações**: Alembic
- **ORM**: SQLAlchemy

### Estrutura das Tabelas

1. **municipios** - Dados dos municípios
2. **prestadores_servico** - Prestadores de serviço
3. **indicadores_desempenho_anuais** - Indicadores de desempenho
4. **recursos_hidricos_anuais** - Dados de recursos hídricos
5. **financeiro_anuais** - Dados financeiros

## 🔧 Desenvolvimento

### Estrutura do Projeto

```
saneamento-ceara-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação principal
│   ├── database.py          # Configuração do banco
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Schemas Pydantic
│   ├── crud.py              # Operações CRUD
│   ├── logging_config.py    # Configuração de logs
│   └── routers/             # Endpoints da API
│       ├── municipios.py
│       ├── prestadores.py
│       ├── indicadores.py
│       ├── recursos_hidricos.py
│       ├── financeiro.py
│       └── analises.py
├── alembic/                 # Migrações
├── logs/                    # Arquivos de log
├── scripts/                 # Scripts de gerenciamento
├── docker-compose.yml       # Configuração Docker
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

### Validações Implementadas

- **Campos obrigatórios** com validação de tipo
- **Ranges numéricos** (ge, le, gt, lt)
- **Tamanhos de string** (min_length, max_length)
- **Padrões regex** para formatos específicos
- **Validações customizadas** (ex: sigla UF apenas CE)

## 🚀 Deploy

### Produção

Para deploy em produção:

1. Configure variáveis de ambiente
2. Use um servidor WSGI (Gunicorn)
3. Configure proxy reverso (Nginx)
4. Configure SSL/TLS
5. Configure backup do banco de dados

### Docker

```bash
# Build da imagem
docker build -t saneamento-ceara-api .

# Executar com Docker Compose
docker-compose up -d
```

## 📚 Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **README Refatorado**: [README_REFATORADO.md](README_REFATORADO.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique a documentação
2. Consulte os logs da aplicação
3. Abra uma issue no repositório

---

**Desenvolvido com ❤️ para análise de dados de saneamento no Ceará**