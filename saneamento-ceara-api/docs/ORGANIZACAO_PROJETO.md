# Organização do Projeto - API de Saneamento do Ceará

## 📁 Estrutura Organizada

O projeto foi reorganizado para seguir as melhores práticas de desenvolvimento e facilitar a manutenção. Aqui está a estrutura final:

```
saneamento-ceara-api/
├── 📁 app/                          # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py                      # Configuração FastAPI
│   ├── database.py                  # Configuração do banco de dados
│   ├── models.py                    # Modelos SQLAlchemy
│   ├── schemas.py                   # Schemas Pydantic
│   ├── crud.py                      # Operações CRUD
│   └── 📁 routers/                  # Rotas da API
│       ├── __init__.py
│       ├── municipios.py            # Endpoints de municípios
│       └── analises.py              # Endpoints de análises
├── 📁 data/                         # Dados processados
│   └── dados_snis_ceara_limpos.csv  # Dados limpos e validados
├── 📁 scripts/                      # Scripts de processamento
│   ├── extract_data.py              # Extração e processamento
│   ├── load_data.py                 # Carregamento no banco
│   └── analise_limpeza_dados.py     # Análise e limpeza
├── 📁 docs/                         # Documentação
│   ├── DOCUMENTACAO_ANALISE_SNIS_CEARA.md
│   └── ORGANIZACAO_PROJETO.md       # Este arquivo
├── 📁 alembic/                      # Migrações do banco
├── 📄 requirements.txt              # Dependências Python
├── 📄 docker-compose.yml            # Configuração Docker
├── 📄 Dockerfile                    # Imagem Docker
├── 📄 .gitignore                    # Arquivos ignorados pelo Git
├── 📄 .env                          # Variáveis de ambiente
├── 📄 env.example                   # Exemplo de variáveis
└── 📄 README.md                     # Documentação principal
```

## 🔄 Mudanças Realizadas

### ✅ **Arquivos Organizados**

1. **Dados Limpos**: Movidos para `data/dados_snis_ceara_limpos.csv`
2. **Scripts**: Todos os scripts de processamento em `scripts/`
3. **Documentação**: Centralizada em `docs/`
4. **Configurações**: Arquivos de configuração na raiz

### ✅ **Arquivos Removidos**

1. **CSV Antigo**: `scripts/data/dados_snis_ceara.csv` (dados não limpos)
2. **Arquivos Temporários**: Scripts e documentação da raiz
3. **Ambiente Virtual**: `venv_analise/` (desnecessário)

### ✅ **Scripts Atualizados**

1. **`load_data.py`**: Atualizado para usar dados limpos
2. **`extract_data.py`**: Configurado para gerar dados limpos
3. **`.gitignore`**: Atualizado para ignorar arquivos desnecessários

## 📊 Fluxo de Dados

```
Dados Brutos (SNIS) 
    ↓
extract_data.py (Filtro + Processamento)
    ↓
dados_snis_ceara_limpos.csv
    ↓
analise_limpeza_dados.py (Análise + Validação)
    ↓
load_data.py (Carregamento no Banco)
    ↓
API FastAPI (Consulta e Análise)
```

## 🛠️ Scripts Disponíveis

### 1. **Extração de Dados** (`scripts/extract_data.py`)
- Filtra dados do Ceará
- Processa e limpa dados básicos
- Gera arquivo `dados_snis_ceara_limpos.csv`

### 2. **Análise e Limpeza** (`scripts/analise_limpeza_dados.py`)
- Análise detalhada de qualidade
- Identificação de outliers
- Limpeza avançada dos dados
- Geração de relatórios

### 3. **Carregamento** (`scripts/load_data.py`)
- Criação das tabelas
- Carregamento dos municípios
- Inserção dos dados limpos

## 📋 Padrões de Nomenclatura

### Arquivos
- **Dados**: `dados_snis_ceara_limpos.csv`
- **Scripts**: `snake_case.py`
- **Documentação**: `UPPERCASE.md`

### Diretórios
- **Código**: `app/`
- **Dados**: `data/`
- **Scripts**: `scripts/`
- **Documentação**: `docs/`

## 🔧 Configuração do Ambiente

### Variáveis de Ambiente (`.env`)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/saneamento_ceara
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=saneamento_ceara
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Dependências (`requirements.txt`)
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pandas
- Alembic

## 🚀 Comandos de Execução

### Desenvolvimento Local
```bash
# 1. Configurar ambiente
cd saneamento-ceara-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configurar banco
cp env.example .env
# Editar .env com suas configurações

# 3. Executar migrações
alembic upgrade head

# 4. Carregar dados
python scripts/load_data.py

# 5. Executar API
uvicorn app.main:app --reload
```

### Docker
```bash
# Executar com Docker Compose
docker-compose up --build
```

## 📈 Benefícios da Organização

### ✅ **Manutenibilidade**
- Código organizado e bem estruturado
- Separação clara de responsabilidades
- Documentação centralizada

### ✅ **Escalabilidade**
- Estrutura modular
- Fácil adição de novos endpoints
- Scripts reutilizáveis

### ✅ **Qualidade**
- Dados limpos e validados
- Processo documentado
- Padrões consistentes

### ✅ **Colaboração**
- Estrutura clara para novos desenvolvedores
- Documentação completa
- Controle de versão organizado

## 🔍 Próximos Passos

1. **Testes**: Implementar testes unitários e de integração
2. **Monitoramento**: Adicionar logs e métricas
3. **Cache**: Implementar cache para consultas frequentes
4. **Autenticação**: Adicionar sistema de autenticação
5. **Deploy**: Configurar pipeline de CI/CD

---

*Projeto organizado e pronto para desenvolvimento! 🚀* 